"""
..
  Copyright 2018, 2019 The University of Sydney
  This file is part of entrezpy.

  Entrezpy is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option) any
  later version.

  Entrezpy is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with entrezpy.  If not, see <https://www.gnu.org/licenses/>.

.. module:: entrezpy.efetch.efetch_parameter
  :synopsis: Export EfetchParameter for NCBI E-Utils Efetch queries

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import math
import json
import logging

import entrezpy.base.parameter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# nuccore complexity=> ASN.1 as text
DEF_RETMODE = 'xml'
"""Default retmode for fetch requests"""

class EfetchParameter(entrezpy.base.parameter.EutilsParameter):
  """EfetchParameter implements checks and configures an EftechQuery. A fetch
  query knows its size due to the id parameter or earlier result stored on the
  Entrez history server using WebEnv and query_key. The default retmode
  (fetch format) is set to XML because all E-Utilities can retun XML but not
  JSON, unfortunately.
  """

  req_limits = {'xml' : 10000, 'json' : 500, 'text' : 10000}
  """Max number of UIDs to fetch per request mode"""

  valid_retmodes = {'pmc' :       {'xml'},
                    'gene' :      {'text', 'xml'},
                    'poset' :     {'text', 'xml'},
                    'pubmed' :    {'text', 'xml'},
                    'nuccore' :   {'text', 'xml'},
                    'protein' :   {'text', 'xml'},
                    'sequences' : {'text', 'xml'}}
  """Enforced request uid sizes by NCBI for fetch requests by format"""

  def __init__(self, param):
    super().__init__(param)
    self.uids = param.get('id', [])
    self.rettype = param.get('rettype')
    self.retmode = self.check_retmode(param.get('retmode', DEF_RETMODE))
    self.retmax =  self.adjust_retmax(param.get('retmax'))
    self.reqsize = self.adjust_reqsize(param.get('reqsize'))
    self.retstart = int(param.get('retstart', 0))
    self.strand = param.get('strand')
    self.seqstart = param.get('seq_start')
    self.seqstop = param.get('seq_stop')
    self.complexity = param.get('complexity')
    self.query_size = self.set_query_size()
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

  def adjust_retmax(self, retmax):
    """Adjusts retmax parameter. Order of check is crucial.

    :param int retmax: retmax value
    :return: adjusted retmax or None if all UIDs are fetched
    :rtype: int or None
    """
    ## Fix retmx and query size
    if retmax is None:
      return None
    return int(retmax)

  def check_retmode(self, retmode):
    if retmode not in EfetchParameter.req_limits:
      sys.exit(logger.error(json.dumps({__name__ : {'Unknown retmode': retmode,
                                                    'action' : 'abort'}})))

    if self.db in EfetchParameter.valid_retmodes and \
       retmode not in EfetchParameter.valid_retmodes[self.db]:
      sys.exit(logger.error(json.dumps({__name__ : {'Bad retmode for database': {
                                                     'db' : self.db,
                                                     'retmnode' : self.retmode},
                                           'action' : 'abort'}})))
    return retmode

  def adjust_reqsize(self, reqsize):
    if reqsize is None:
      return EfetchParameter.req_limits.get(self.retmode)
    if int(reqsize) > EfetchParameter.req_limits.get(self.retmode):
      return EfetchParameter.req_limits.get(self.retmode)
    if self.retmax and (int(reqsize) < self.retmax):
      return self.retmax
    return int(reqsize)

  def calculate_expected_requests(self, qsize=None, reqsize=None):
    """Calculate anf set the expected number of requests. Uses internal
    parameters if non are provided.

    :param int or None qsize: query size, i.e. expected number of data sets
    :param int reqsize: number of data sets  to fetch in one request
    """
    if not qsize:
      qsize = self.retmax
    if self.retmax == 0:
      return 1
    if not reqsize:
      reqsize = EfetchParameter.req_limits.get(self.retmode)
    self.expected_requests = math.ceil(qsize / reqsize)

  ## Implemented check() function
  # Testing for required parameters and aborting if they are missing/wrong
  # When using the history server, efetch queries require WebEnv and query_key
  def check(self):
    if not self.haveDb():
      logger.error(json.dumps({__name__ : {'Missing parameter': {'db' : self.db},
                                           'action' : 'abort'}}))
      sys.exit()
    if not self.haveExpectedRequets():
      logger.error(json.dumps({__name__ : {'Bad expected requests' : self.expected_requests,
                                           'action' : 'abort'}}))
      sys.exit()
    if not self.uids and not self.haveQuerykey() and not self.haveWebenv():
      logger.error(json.dumps({__name__ : {'Missing parameters': {'id': self.uids,
                                                                  'QueryKey': self.querykey,
                                                                  'WebEnv' : self.webenv},
                                           'action' : 'abort'}}))
      sys.exit()

  def dump(self):
    return {'db' : self.db,
            'WebEnv':self.webenv,
            'query_key' : self.querykey,
            'uids' : self.uids,
            'retmode' : self.retmode,
            'rettype' : self.rettype,
            'retstart' : self.retstart,
            'retmax' : self.retmax,
            'strand' : self.strand,
            'seqstart' : self.seqstart,
            'seqstop' : self.seqstop,
            'complexist' : self.complexity,
            'query_size' : self.query_size,
            'request_size' : self.request_size,
            'expected_requets' : self.expected_requests}
