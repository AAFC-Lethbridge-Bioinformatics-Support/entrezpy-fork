#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \description  Class handling search requests to NCBI.
#                https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
#  \copyright 2017,2018 The University of Sydney
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import query
from . import esearch_request
from . import esearch_analyzer
from . import esearch_parameter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

## Esearcher implements esearch queries to E-Utilities [0]
# It inherits the query.EutilsQuery class and implements the inquire() method
# to search NCBI. All parameters described in [0] are acccepted.
# Esearcher() uses the first request to configure itself to fetch all
# requested data if required.
#
# [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

class Esearcher(query.EutilsQuery):

  def __init__(self, tool, email, apikey=None, threads=0, id=None):
    super().__init__('esearch.fcgi', tool, email, apikey, threads, id=id)

  ## Implemented inquire() from query.EutilsQuery
  # Runs initial_search() to figure out the query size. If a follow up is
  # required, the EsearchParameter() is adjusted.
  # Adjusts the size of the request if less than the allowed query size has
  # to be fetched
  #@params[in] parameter dictionary with aguments as described in [0]
  #@params[in] analyzer  analyzer instance
  #@return the analyzer instance if no request errors have been encountered
  #@return None if request errors have been encountered
  def inquire(self, parameter, analyzer=esearch_analyzer.EsearchAnalyzer()):
    p = esearch_parameter.EsearchParameter(parameter)
    logger.debug(json.dumps({__name__+"-"+self.id: {"parameter":p.dump()}}))
    self.monitor_start(p)
    follow_up = self.initial_search(p, analyzer)
    if not follow_up:
      self.monitor_stop()
      if not analyzer.isSuccess():
        return None
      return analyzer
    self.monitor_update(follow_up)
    req_size = follow_up.request_size
    for i in range(1, follow_up.expected_requests):
      if (i * req_size + req_size) > follow_up.query_size:
        logger.debug(json.dumps({__name__:{"adjust-reqsize":{"request":i,
                                                              "start":(i*follow_up.request_size),
                                                              "end": i*req_size+req_size,
                                                              "query_size": follow_up.query_size,
                                                              "adjusted-reqsize": follow_up.query_size%follow_up.request_size}}}))
        req_size = follow_up.query_size % follow_up.request_size
      logger.debug(json.dumps({__name__:{"request":i,
                                         "expected":follow_up.expected_requests,
                                         "start":(i*follow_up.request_size),
                                         "end":(i*follow_up.request_size)+req_size,
                                         "reqsize":req_size}}))
      self.add_request(esearch_request.EsearchRequest(follow_up, (i*follow_up.request_size), req_size), analyzer)
    self.request_pool.drain()
    self.monitor_stop()
    if self.check_requests() != 0:
      logger.debug(json.dumps({__name__:{"Requeste-Error": "follow-up"}}))
      return None
    return analyzer



  ## Function to establish the size of the query/number of requsts
  # A follow up is triggered only if parameter.rettype = uilist and
  # more data than the maximum query size is expected.
  #@param[in] parameter EsearchParameter() instance
  #@param[in] analyzer analyzer instance
  #@return None if no follow up is required
  #@return modified parameter for follow-up
  def initial_search(self, parameter, analyzer):
    self.add_request(esearch_request.EsearchRequest(parameter, parameter.retstart, parameter.retmax), analyzer)
    self.request_pool.drain()
    if self.check_requests() != 0:
      logger.debug(json.dumps({__name__:{"Request-Error": "inital search"}}))
      return None
    if not analyzer.isSuccess():
      logger.debug(json.dumps({__name__:{"Response-Error": "inital search"}}))
      return None
    if parameter.rettype == 'uilist':
      if parameter.query_size == -1:
        parameter.query_size = analyzer.result.count
      if parameter.query_size > len(analyzer.result.uids):
        logger.debug(json.dumps({__name__:{"Followup":{ "fetch": parameter.query_size}}}))
        parameter.prepare_follow_up(analyzer.result)
        parameter.check()
        return parameter
    return None

  ## Function to tets if request errors were encountered
  # It checks if the failed request list populated by
  # EutilsQuery.RequestPool
  #@return 0 if no request error
  #@return 1 if error requets
  def check_requests(self):
    if not self.hasFailedRequests():
      logger.info(json.dumps({__name__+"-"+self.id: "Query requests OK"}))
      return 0
    else:
      logger.info(json.dumps({__name__+"-"+self.id:{"Failed requests" : [x.dump_internals() for x in self.failed_requests]}}))
      return 1
