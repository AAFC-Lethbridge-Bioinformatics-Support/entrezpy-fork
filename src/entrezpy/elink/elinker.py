#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright  GNU Lesser General Public License
#  \description Elinker class to link EDirect search results.
#-------------------------------------------------------------------------------

import os
import sys
import time
import json
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import query
from . import elink_parameter
from . import elink_request
from . import elink_analyzer

logger = logging.getLogger(__name__)

## Elinker implements elink queries to E-Utilities [0]
# Elinker inherits query.EutilsQuery and implements the inquire() method
# to link data sets on NCBI Entrez servers. All parameters described in [0] are
# acccepted. Elink queries consist of one request linking uids or an earlier
# requests on the history server within the same or different Enrez database.
# [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink

class Elinker(query.EutilsQuery):

  def __init__(self, tool, email, apikey=None, threads=0, id=None):
    super().__init__('elink.fcgi', tool, email, apikey, threads, id=id)

  ## Implemented inquire() from query.EutilsQuery
  # Elink consists of one query.
  # @params[in] parameter dictionary with aguments as described in [0]
  # @params[in] analyzer  analyzer instance
  # @return the analyzer instance if no request errors have been encountered
  # @return None if request errors have been encountered
  def inquire(self, parameter, analyzer=elink_analyzer.ElinkAnalyzer()):
    logger.debug(logger.debug({'tool':self.tool, 'url':self.url, 'threads': self.num_threads, 'email':self.contact}))
    p = elink_parameter.ElinkParameter(parameter)
    self.monitor_start(p)
    self.add_request(elink_request.ElinkRequest(p), analyzer)
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
