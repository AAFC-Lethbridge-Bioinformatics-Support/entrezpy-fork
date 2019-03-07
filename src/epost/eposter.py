#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import query
from . import epost_request
from . import epost_analyzer
from . import epost_parameter

logger = logging.getLogger(__name__)

## Eposter implements epost queries to E-Utilities [0]
# It inherits the query.EutilsQuery class and implements the inquire() method
# to search NCBI. All parameters described in [0] are acccepted.
# An EPost query posts uids to the history server. If no WebEnv is given,
# a new WebEnv with query key is created and returned. If a WebEvn is is given,
# the passed uids will be added to this webenv and an associated query key
# returned.
#
# [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost
class Eposter(query.EutilsQuery):

  def __init__(self, tool, email, apikey=None, threads=0, id=None):
    super().__init__('epost.fcgi', tool, email, apikey, threads, id=id)

  ## Implemented inquire() from query.EutilsQuery
  # Epost is only one request
  #@params[in] parameter dictionary with aguments as described in [0]
  #@params[in] analyzer  analyzer instance
  #@return the analyzer instance if no request errors have been encountered
  #@return None if request errors have been encountered
  def inquire(self, parameter, analyzer=epost_analyzer.EpostAnalyzer()):
    p = epost_parameter.EpostParameter(parameter)
    self.monitor_start(p)
    self.add_request(epost_request.EpostRequest(p), analyzer)
    self.request_pool.drain()
    self.monitor_stop()
    if self.check_requests() != 0:
      return None
    return analyzer


  ## Function to test if request errors were encountered
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
