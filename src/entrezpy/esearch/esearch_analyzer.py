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
from . import esearch_result

##  EsearchAnalyzer implements the analyzer for efetch data
# JSON formatted data is currnetly enforced since it's easier to handle than
# XML. If no errors have been encountered, the result is stored in the
# esearch_result.EsearchResult class.
class EsearchAnalyzer(analyzer.EutilsAnalyzer):

  ## Ctor
  def __init__(self):
    super().__init__()
    self.result = None
    self.error = None

  def analyze_result(self, response, request):
    if not self.result:
      self.result = esearch_result.EsearchResult(request.db,
                                      response['esearchresult'].pop('count'),
                                      response['esearchresult'].pop('webenv', None),
                                      response['esearchresult'].pop('querykey', None),
                                      response['esearchresult'].get('idlist', []),
                                      response['esearchresult'].pop('retmax'),
                                      response['esearchresult'].pop('retstart'))
    else:
      self.result.uids += response['esearchresult'].get('idlist', [])

  def analyze_error(self, response, request):
    self.error = response['esearchresult']
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
