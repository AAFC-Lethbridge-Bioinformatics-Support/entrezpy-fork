#-------------------------------------------------------------------------------
#  \file efetcher.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \description Implements efetch requests to NCBI. Inherits from EdFunction.
#  \copyright 2018 The University of Sydney
#  \version 1.0.2
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import query
from . import efetch_parameter
from . import efetch_request
from . import efetch_analyzer

logger = logging.getLogger(__name__)

## Efetcher implements efetch queries to E-Utilities [0]
# It inherits the query.EutilsQuery class and implements the inquire() method
# to fetch data from NCBI Entrez servers. All parameters described in [0] are
# acccepted.
#
# Parameters and valid arguments
#   db : database to query. A list of valid databases is given in [1]
#
# [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
# [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly

class Efetcher(query.EutilsQuery):

  def __init__(self, tool, email, apikey=None, threads=0, id=None):
    super().__init__('efetch.fcgi', tool, email, apikey, threads, id=id)

  ## Implemented inquire() from query.EutilsQuery
  # Efetch can consist of several queries, depending on the format requested.
  # Subsequent fetch request are created by increasing the start of the request
  # and keeping the size constant. The request size is adjusted if it's smaller
  # than the default request size.
  # @params[in] parameter dictionary with aguments as described in [0]
  # @params[in] analyzer  analyzer instance
  # @return the analyzer instance if no request errors have been encountered
  # @return None if request errors have been encountered
  def inquire(self, parameter, analyzer=efetch_analyzer.EfetchAnalyzer()):
    p = efetch_parameter.EfetchParameter(parameter)
    req_size = p.request_size
    self.monitor_start(p)
    for i in range(p.expected_requests):
      if i * req_size + req_size > p.query_size:
        req_size = p.query_size % p.request_size
      self.add_request(efetch_request.EfetchRequest(p, (i*p.request_size),req_size), analyzer)
    self.request_pool.drain()
    self.monitor_stop()
    if self.check_requests() == 0:
      return analyzer
    return None

  ## Function to test if request errors were encountered
  # It checks if the failed request list populated by
  # EutilsQuery.RequestPool
  # @return 0 if no request error
  # @return 1 if error requets
  def check_requests(self):
    if not self.hasFailedRequests():
      logger.info(json.dumps({__name__+"-"+self.id: "Query requests OK"}))
      return 0
    else:
      logger.info(json.dumps({__name__+"-"+self.id:{"Failed requests" : [x.dump_internals() for x in self.failed_requests]}}))
      return 1
