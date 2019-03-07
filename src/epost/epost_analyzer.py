#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging
import xml.etree.ElementTree

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import analyzer
from . import epost_result

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class EpostAnalyzer(analyzer.EutilsAnalyzer):

  def __init__(self):
    super().__init__()
    self.result = None

  def analyze_result(self, response, request):
    self.result = epost_result.EpostResult(db=request.db, size=request.size)
    for event, elem in xml.etree.ElementTree.iterparse(response, events=["end"]):
      if event == 'end' and elem.tag == 'QueryKey':
        self.result.querykey = elem.text
      if event == 'end' and elem.tag == 'WebEnv':
        self.result.webenv = elem.text
      elem.clear()

  def analyze_error(self, response, request):
    for event, elem in xml.etree.ElementTree.iterparse(response, events=["end"]):
      if elem.tag == 'ERROR':
        self.error = elem.text
        break
      elem.clear()

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

  def get_result(self):
    return self.result
