#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys
import math
import json
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import entrezpy_base.parameter

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

## EsummaryParameter implements checks and configures an Esummary() query.
# EsummaryParameter inherits entrezpy_base.parameter.EutilsParameter.
# A summary query knows its size due to the id parameter or earlier result
# stored on the Entrez history server using WebEnv and query_key.
# The default retmode (fetch format) is set to JSON but if XML is returned
# it defautls to the new 2.0 version.

class EsummaryParameter(entrezpy_base.parameter.EutilsParameter):

  ## maximum number of data sets per request
  max_request_size = {'xml' : 10000, 'json' : 500}

  def __init__(self, parameter):
    super().__init__(parameter)
    self.uids = parameter.get('id', [])
    self.retmode = parameter.get('retmode', 'json')
    self.retmax = int(parameter.get('retmax', EsummaryParameter.max_request_size.get(self.retmode, 'json')))
    self.retstart = int(parameter.get('retstart', 0))
    self.esummary_version = parameter.get('version', '2.0')
    self.query_size = self.set_query_size()
    self.request_size = self.set_request_size()
    self.expected_requests = self.calculate_expected_requests(self.query_size, self.request_size)
    self.check()

  ## Function to adjust the request size if the query size is smaller
  # defaults to self.retmax
  # @param[in] qsize int enforce query size
  # @return request size
  def set_query_size(self, qsize=None):
    if qsize != None:
      return qsize
    if self.uids:
      return len(self.uids)
    return self.retmax

  ## Function to set the query size
  # When linking results with uids, the size has to be adjusted
  # @return query size
  def set_request_size(self):
    if self.query_size < self.retmax:
      return self.query_size
    return self.retmax

  ## Function to calculate the expected number of requests
  # If the retmax parameter is 0, no uids are returned.
  # However, this is still 1 request
  # @param[in] query_size   int query size
  # @param[in] request_size int request size
  # @return 1 if retmax is set to 0
  # @return number of expected requests
  def calculate_expected_requests(self, query_size, request_size):
    if self.retmax == 0:
      return 1
    return math.ceil(query_size / request_size)

  def check(self):
    if not self.haveDb():
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing parameter", "parameter":
                                                              {"db":self.db,"action":"abort"}}}))
      sys.exit()
    if not self.haveExpectedRequets():
      logger.error(json.dumps({"Parameter-error":{"msg": "Calculating expected requests failed",
                                                                "parameter": {"expected requests":self.expected_requests, "action":"abort"}}}))
      sys.exit()
    if not self.uids and not self.haveQuerykey() and not self.haveWebenv():
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing required parameters",
                                                         "parameters": {"ids":self.uids,
                                                                        "QueryKey":self.querykey,
                                                                        "WebEnv":self.webenv},
                                                         "action":"abort"}}))
      sys.exit()
