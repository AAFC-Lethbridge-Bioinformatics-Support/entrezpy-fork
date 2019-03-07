#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description The Wally class facilitates the assembly of Edirect
#                queries.
#-------------------------------------------------------------------------------

import os
import sys
import json
import time
import logging
import queue

#sys.path.insert(1, os.path.join(sys.path[0], '../'))
from ..esearch import esearcher
from ..esearch import esearch_analyzer
from ..elink import elinker
from ..elink import elink_analyzer
from ..epost import eposter
from ..epost import epost_analyzer
from ..efetch import efetcher
from ..esummary import esummarizer
from ..esummary import esummary_analyzer

from . import wally_query

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

## Wally simplifies to create pipelines and queries for entrzpy.
# Wally stores the results from previous requests, allowing to retrieve them
# later if required, reducing the need to redownload data within a pipeline.
class Wally:

  ## Static dictionaries to store results in analyzers and individual queries
  # for pipelines in queries.
  analyzers = {}
  queries = {}

  ## Nested class handling requets piplines. Wally will return an instance
  # of Pipeline which can be than populated with requests. Individual requests
  # can reuse parameters from earlier requests. If earlier requets are given as
  # dependencies as well as new parameters, the new parameters will overwrite
  # those from the dependency.
  class Pipeline:

    ## Ctor for Pipeline
    # store reference to global query storage in query_map and initialize queue
    # to store query for current pipeline

    def __init__(self, query_map):
      self.query_map = query_map
      self.queries = queue.Queue()

    ## add search, link, post and sumary queries to pipeline
    # @param[in] parameter dictionary with entrez parameters for search
    # @param[in] dependency uuid.uuid4()  id for earlier search
    # @param[in] analyzer analyzer instance to use for this search
    # @param[out] WallyQuery() instance
    def add_search(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('esearch', parameter, dependency, analyzer))

    ## add link query. Same options as add_search()
    def add_link(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('elink', parameter, dependency, analyzer))

    ## add post query. Same options as add_search()
    def add_post(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('epost', parameter, dependency, analyzer))

    ## add summary query. Same options as add_search()
    def add_summary(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('esummary', parameter, dependency, analyzer))

    ## add fetch query to pipeline. Same options as add_search(), but
    # requires an analyzer
    def add_fetch(self, parameter=None, dependency=None, analyzer=None):
      if analyzer == None:
        sys.exit("Wally.Pipline error: fetch requests require an analyzer but none given. Abort.")
      return self.add_query(wally_query.WallyQuery('efetch', parameter, dependency, analyzer))

    ## add query to global and local storage
    # @param[in] query WallyQuery()
    # @param[out] uuid.uuid4() query id for added query
    def add_query(self, query):
      self.queries.put(query.id)
      self.query_map[query.id] = query
      return query.id

  ## Ctor for Wally
  # Wally can use multiple threads to speed up data download, but some external
  # libraries used within analyzers can break, e.g. SQLite3
  # @param[in] email email address as requirs by NCBI Eutils
  # @param[in] apikey NCBI Apikey
  # @param[in] threads int  Number of threads to use for data download.
  def __init__(self, email, apikey=None, threads=None):
    self.tool = 'wally'
    self.email = email
    self.apikey = apikey
    self.threads = threads

  ## run the queries within the local pipeline.
  # Individual queries are recognized and a corrsponding entrezpy method
  # invoked. If errors are encountered, it aborts.
  # param[in] Wally.Pipeline() Wally pipeline instance with queries in queue.
  def run(self, qry):
    while not qry.queries.empty():
      q = Wally.queries[qry.queries.get()]
      q.resolve_dependency(Wally.analyzers)
      logger.info(json.dumps({"Inquire" : {"id" : q.id, "category": q.category}}))
      if q.category == 'esearch':
        Wally.analyzers[q.id] = self.search(q)
      if q.category == 'elink':
        Wally.analyzers[q.id] = self.link(q)
      if q.category == 'efetch':
        Wally.analyzers[q.id] = self.fetch(q)
      if q.category == 'epost':
        Wally.analyzers[q.id] = self.post(q)
      if q.category == 'esummary':
        Wally.analyzers[q.id] = self.summarize(q)
      self.check_query(q)
    return Wally.analyzers[q.id]

  ## Check if an individual query in a pipeline has been succesful.
  # Aborts if errors are encountered
  # @param[in] WallyQuery()
  def check_query(self, query):
    if not Wally.analyzers[query.id]:
      sys.exit("Request errors in query {}".format(query.id))
    if not Wally.analyzers[query.id].isSuccess():
      logger.info(json.dumps({"Wally-Info":{"msg": "Error in response",
                                                  "query": {"id":query.id},
                                                  "action":"abort"}}))
      sys.exit()

  ## return a stored result from a previous run.
  # @param[in] query_id, uuid.uuid4() query id
  # @param[out] result, result instance or None if not found
  def get_result(self, query_id):
    r = self.analyzers.get(query_id)
    if not r:
      return None
    return r.result

  ## get new instance of Wally.Pipeline()
  def new_pipeline(self):
    return self.Pipeline(Wally.queries)

  ## Configure and run a entrepy queries
  # Analyzers are passed as class and instantiated later. Ensures new instances
  # for every query
  # @param[in] query WallyQuery()
  # @param[in] analzyer analyzer class
  def search(self, query, analyzer=esearch_analyzer.EsearchAnalyzer):
    analyzer=analyzer()
    if query.analyzer:
      analyzer = query.analyzer
    esearch = esearcher.Esearcher(self.tool, self.email, self.apikey, threads=self.threads, id=query.id)
    return esearch.inquire(parameter=query.parameter, analyzer=analyzer)

  def summarize(self, query, analyzer=esummary_analyzer.EsummaryAnalzyer):
    analyzer=analyzer()
    if query.analyzer:
      analyzer = query.analyzer
    esummary = esummarizer.Esummarizer(self.tool, self.email, self.apikey, threads=self.threads, id=query.id)
    return esummary.inquire(parameter=query.parameter, analyzer=analyzer)

  def link(self, query, analyzer=elink_analyzer.ElinkAnalyzer):
    analyzer=analyzer()
    if query.analyzer:
      analyzer = query.analyzer
    linker = elinker.Elinker(self.tool, self.email, self.apikey, threads=self.threads, id=query.id)
    return linker.inquire(parameter=query.parameter, analyzer=analyzer)

  def post(self, query, analyzer=epost_analyzer.EpostAnalyzer):
    analyzer=analyzer()
    if query.analyzer:
      analyzer = query.analyzer
    poster = eposter.Eposter(self.tool, self.email, self.apikey, threads=self.threads, id=query.id)
    return poster.inquire(parameter=query.parameter, analyzer=analyzer)

  def fetch(self, query):
    fetcher = efetcher.Efetcher(self.tool, self.email, self.apikey, threads=self.threads, id=query.id)
    return fetcher.inquire(parameter=query.parameter, analyzer=query.analyzer)
