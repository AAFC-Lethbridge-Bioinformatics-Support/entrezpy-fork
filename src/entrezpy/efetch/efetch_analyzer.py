#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

from ..entrezpy_base import analyzer

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
    logger.info(json.dumps({__name__:{'Response-Error': {
                                      'request-dump' : request.dump_internals(),
                                       'error' : response}}}))

    logger.debug(json.dumps({__name__:{'Response-Error': {
                                       'request-dump' : request.dump_internals(),
                                       'error' : response}}}))
