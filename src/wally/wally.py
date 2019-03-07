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

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from esearch import esearcher
from esearch import esearch_analyzer
from elink import elinker
from elink import elink_analyzer
from epost import eposter
from epost import epost_analyzer
from efetch import efetcher
from esummary import esummarizer
from esummary import esummary_analyzer

from . import wally_query

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class Wally:

  analyzers = {}
  queries = {}

  class Pipeline:

    def __init__(self, query_map):
      self.query_map = query_map
      self.queries = queue.Queue()

    def add_search(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('esearch', parameter, dependency, analyzer))

    def add_link(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('elink', parameter, dependency, analyzer))

    def add_fetch(self, parameter=None, dependency=None, analyzer=None):
      if analyzer == None:
        sys.exit("Callimachus error: fetch requests require an analyzer but none given. Abort.")
      return self.add_query(wally_query.WallyQuery('efetch', parameter, dependency, analyzer))

    def add_post(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('epost', parameter, dependency, analyzer))

    def add_summary(self, parameter=None, dependency=None, analyzer=None):
      return self.add_query(wally_query.WallyQuery('esummary', parameter, dependency, analyzer))

    def add_query(self, query):
      self.queries.put(query.id)
      self.query_map[query.id] = query
      return query.id

  def __init__(self, email, apikey=None, threads=None):
    self.tool = 'wally'
    self.email = email
    self.apikey = apikey
    self.threads = threads

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

  def check_query(self, query):
    if not Wally.analyzers[query.id]:
      sys.exit("Request errors in query {}".format(query.id))
    if not Wally.analyzers[query.id].isSuccess():
      logger.info(json.dumps({"Callimachus-Info":{"msg": "Error in response",
                                                  "query": {"id":query.id},
                                                  "action":"abort"}}))
      sys.exit()

  def get_result(self, query_id):
    return self.analyzers[query_id].result

  def new_pipeline(self):
    return self.Pipeline(Wally.queries)

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
