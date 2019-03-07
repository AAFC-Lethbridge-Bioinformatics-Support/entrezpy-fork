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

class EfetchAnalyzer(analyzer.EutilsAnalyzer):

  def __init__(self):
    super().__init__()
    self.result = ''

  def analyze_result(self, response, request):
    if request.rettype == 'json':
      self.result += response
    else:
      self.result += response.getvalue()

  def analyze_error(self, response, request):
    self.error = response
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

def main():

  return 0

if __name__ == '__main__':
  main()
