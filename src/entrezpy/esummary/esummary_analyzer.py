#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import analyzer
from . import esummary_result

class EsummaryAnalzyer(analyzer.EutilsAnalyzer):

  def __init__(self):
    super().__init__()
    self.result = None

  def analyze_result(self, response, request):
    if not self.result:
      self.result = esummary_result.EsummaryResult(db=request.db,
                                                   querykey=request.querykey,
                                                   webenv=request.webenv)
    self.result.uids += response['result']['uids']
    for i in response['result']['uids']:
      self.result.add_summary(i, response['result'])
    response.pop('result')

  def analyze_error(self, response, request):
    if 'error' in response:
      self.error = response['error']
    if 'esummaryresult' in response:
      self.error = response['esummaryresult']
    logger.info(json.dumps({__name__:{"Response-Error":
                                        {
                                          "tool": request.tool,
                                          "request-id": request.id,
                                          "query-id":request.query_id,
                                          "error": self.error
                                        }}}))
    logger.debug(json.dumps({__name__:{"Response-Error":
                                        {
                                          "tool": request.tool,
                                          "request-id": request.id,
                                          "query-id":request.query_id,
                                          "error": self.error,
                                          "request-dump":request.dump_internals()
                                        }}}))
