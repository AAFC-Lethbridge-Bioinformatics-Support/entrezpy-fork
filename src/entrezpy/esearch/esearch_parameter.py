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

## EsearchParameter implements checks and configures an Esearcher() query.
# EsearchParameter inherits entrezpy_base.parameter.EutilsParameter.
# Esearcher() uses EsearchParameter() to obtain the first request to figure out
# the number of found data sets (Count number from E-Utiltites).
# If more than one request is required, the function prepare_follow_up()
# configures EsearchParameter() for multiple requests using the first result.
#
# EsearchParameter works best when using the NCBI Entrez history server. If
# usehistory is not used, linking requests cannot be guaranteed.
#
# JSON formated results are currently enforced due to its simplicity.

class EsearchParameter(entrezpy_base.parameter.EutilsParameter):

  ## maximum number of data sets per request
  max_request_size = 100000

  def __init__(self, parameter):
    super().__init__(parameter)
    self.term = parameter.get('term')
    #self.retmode = parameter.get('retmode', 'json')
    self.usehistory = parameter.get('usehistory', True)
    self.retmode = 'json'
    self.rettype = parameter.get('rettype', 'uilist')
    self.retmax = int(parameter.get('retmax', -1))
    self.retstart = int(parameter.get('retstart', 0))
    self.sort = parameter.get('sort')
    self.field = parameter.get('field')
    self.datetype = parameter.get('datetype')
    self.reldate = parameter.get('reldate')
    self.mindate = parameter.get('mindate')
    self.maxdate = parameter.get('maxdate')
    self.query_size = self.set_query_size()
    self.request_size = self.set_request_size()
    self.expected_requests = self.calculate_expected_requests(self.query_size, self.request_size)
    self.check()

  def set_query_size(self):
    if self.retmax == -1:
      self.retmax = EsearchParameter.max_request_size
      return -1
    return self.retmax

  ## Function to adjust the request size if the query size is smaller
  #@return request size
  def set_request_size(self):
    if self.query_size == -1:
      return EsearchParameter.max_request_size
    if self.query_size < EsearchParameter.max_request_size:
      return self.query_size
    return EsearchParameter.max_request_size

  ## Function to calculate the expected number of requests
  # If the retmax parameter is 0, no uids are returned, analogous to
  # rettype=uilist. However, this is still 1 request
  # @param[in] query_size   int query size
  # @param[in] request_size int request size
  # @return 1 if retmax is set to 0
  # @return number of expected requests
  def calculate_expected_requests(self, query_size, request_size):
    if self.query_size == -1:
      return 1
    if self.retmax == 0:
      return 1
    return math.ceil(query_size / request_size)

  ## Implemented check() function
  # Testing for required parameters and aborting if they are missing/wrong
  def check(self):
    if not self.haveDb():
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing parameter", "parameter":
                                                              {"term":self.db,"action":"abort"}}}))
      sys.exit()

    if not self.haveExpectedRequets():
      logger.error(json.dumps({"Parameter-error":{"msg": "Calculating expected requests failed",
                                                                "parameter": {"term":self.expected_requests, "action":"abort"}}}))
      sys.exit()

    if not self.term:
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing parameter",
                                                               "parameter": {"term":self.term, "action":"abort"}}}))
      sys.exit()

  ## Function adjusting EsearchParameter() to fetch remaining results
  # It adjusts the required requests based on the initial result and prepares
  # EsearchParameter() to fetch the remaining results using the history server
  # Only called if the initial result is not using uids and reports a count
  # larger than the max query size. Already fetched uids are kept and retstart
  # adjusted to avoid redownload of redundant data.
  # @param[in] result first inquiry result.
  def prepare_follow_up(self, result):
    self.webenv = result.webenv
    self.querykey = result.querykey
    #self.retstart = len(result.uids)
    #self.query_size -= self.retmax
    self.expected_requests = self.calculate_expected_requests(self.query_size, EsearchParameter.max_request_size)

  ## Dump all attributes for debugging
  # @return dictionary with all attributes
  def dump(self):
    return {'db' : self.db, 'webenv' : self.webenv, 'querykey' : self.querykey,
            'usehistory' : self.usehistory, 'term':self.term, 'retmode':self.retmode,
            'rettype': self.rettype, 'retmax': self.retmax, 'retstart': self.retstart,
            'sort' : self.sort, 'field' : self.field, 'datetype' : self.datetype,
            'reldate' : self.reldate, 'mindate' : self.mindate, 'maxdate' : self.maxdate,
            'expected_requets' : self.expected_requests, 'query_size' : self.query_size,
            'request_size' : self.request_size, 'max_request_size' : EsearchParameter.max_request_size}
