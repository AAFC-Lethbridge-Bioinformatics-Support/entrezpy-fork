#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import math
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import entrezpy_base.parameter

logger = logging.getLogger(__name__)

## EfetchParameter implements checks and configures an EftechQuery().
# EfetchParameter inherits entrezpy_base.parameter.EutilsParameter.
# A fetch query knows its size due to the id parameter or earlier result
# stored on the Entrez history server using WebEnv and query_key
# The default retmode (fetch format) is set to XML because all E-Utilities
# can retun XML data but not JSON data, unfortunately.

# nuccore complexity=> ASN.1 as text
class EfetchParameter(entrezpy_base.parameter.EutilsParameter):

  ## Max size of UIDs to fetch per request
  max_request_size = {'xml' : 10000, 'json' : 500, 'text' : 10000}

  ## Enforced request uid sizes by NCBI for fetch requests by format
  valid_retmodes = {'pmc' : {'xml'},
                    'pubmed' : {'xml', 'text'},
                    'nuccore': {'text','xml'},
                    'poset': {'text','xml'},
                    'protein': {'text','xml'},
                    'sequences': {'text','xml'},
                    'gene': {'text','xml'}}


  def __init__(self, parameter):
    super().__init__(parameter)
    self.uids = parameter.get('id', [])
    self.rettype = parameter.get('rettype')
    self.retmode = parameter.get('retmode', 'xml')
    self.retstart = int(parameter.get('retstart', 0))
    self.retmax = int(parameter.get('retmax', EfetchParameter.max_request_size.get(self.retmode, 'xml')))
    self.strand = parameter.get('strand')
    self.seqstart = parameter.get('seq_start')
    self.seqstop = parameter.get('seq_stop')
    self.complexity = parameter.get('complexity')
    self.query_size = self.set_query_size()
    self.request_size = self.set_request_size()
    self.expected_requests = self.calculate_expected_requests(self.query_size,
                                                              self.request_size)

  ## Function to set the query size
  # When linking results with uids, the size has to be adjusted
  # @return query size
  def set_query_size(self, qsize=None):
    if qsize:
      return qsize
    if self.uids:
      return len(self.uids)
    return self.retmax

  ## Function to adjust the request size if the query size is smaller
  # defaults to self.retmax
  # @param[in] qsize int enforce query size
  # @return request size
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

  ## Implemented check() function
  # Testing for required parameters and aborting if they are missing/wrong
  # When using the history server, efetch queries require WebEnv and query_key
  def check(self):
    if not self.haveDb():
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing parameter", "parameter":
                                                              {"term":self.db,"action":"abort"}}}))
      sys.exit()
    if not self.haveExpectedRequets():
      logger.error(json.dumps({"Parameter-error":{"msg": "Calculating expected requests failed",
                                                                "parameter": {"term":self.expected_requests, "action":"abort"}}}))
      sys.exit()
    if not self.uids and not self.haveQuerykey() and not self.haveWebenv():
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing required parameters",
                                                         "parameters": {"ids":self.uids,
                                                                        "QueryKey":self.querykey,
                                                                        "WebEnv":self.webenv},
                                                         "action":"abort"}}))
      sys.exit()
