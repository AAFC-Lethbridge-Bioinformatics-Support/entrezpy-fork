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

.. module:: entrezpy.esearch.esearch_parameter
  :synopsis:
    Export EsearchParameter for NCBI E-Utils Esearch  queries

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


MAX_REQUEST_SIZE = 100000
"""Maximum number of UIDs for one request"""

class EsearchParameter(entrezpy.base.parameter.EutilsParameter):
  """EsearchParameter checks query specific parameters and configures an Esearch
  query. If more than one request is required to fetch all search results,
  the instance is reconfigured by
  :func:`entrezpy.esearch.esearcher.configure_follow_up`.

  .. note :: EsearchParameter works best when using the NCBI Entrez history
    server. If usehistory is not used, linking requests cannot be guaranteed.
  """

  def __init__(self, parameter):
    super().__init__(parameter)
    self.query_size = None
    self.retmode = 'json'
    self.uilist = self.set_uilist(parameter.get('rettype'))
    self.limit = parameter.get('limit', None)
    self.retmax = self.adjust_retmax(int(parameter.get('retmax', MAX_REQUEST_SIZE)))
    self.retstart = int(parameter.get('retstart', 0))
    self.usehistory = parameter.get('usehistory', True)
    self.term = parameter.get('term')
    self.sort = parameter.get('sort')
    self.field = parameter.get('field')
    self.datetype = parameter.get('datetype')
    self.reldate = parameter.get('reldate')
    self.mindate = parameter.get('mindate')
    self.maxdate = parameter.get('maxdate')
    self.idtype = parameter.get('idtype')
    self.check()

  def goodDateparam(self):
    """Check for good paraeters wehn using date

    :rtype: bool
    """
    useDate = False
    if self.useMinMaxDate():
      if self.reldate:
        logger.error(json.dumps({__name__: {'Error' : 'Cannot use reldate and Min/Max dates'}}))
        return False
      useDate = True
    if self.reldate:
      useDate = True
    if useDate and (not self.datetype):
      logger.error(json.dumps({__name__: {'Error' : 'Require datetype with dates'}}))
      return False
    return True

  def useMinMaxDate(self):
    """Maxdate and mindate are required together

    :rtype: bool
    """
    if self.mindate or self.maxdate: # Intend to use max/min dates
      if self.mindate and self.maxdate: # Require both
        return True
      logger.error(json.dumps({__name__: {'Error' : 'Require mindate and maxdate'}}))
    return False

  def set_uilist(self, rettype):
    """Set rettype parameter to mimic rettype options for XML

    :rtype: bool
    """
    if not rettype or (rettype == 'uilist'):
      return True
    return False

  def adjust_retmax(self, retmax):
    """Adjusts retmax parameter

    :param int retmax: retmax value
    :return: adjusted retmax
    :rtype: int
    """
    if not self.uilist:
      return 0
    if retmax > MAX_REQUEST_SIZE:
      return MAX_REQUEST_SIZE
    if self.limit and (self.limit <= retmax):
      return self.limit
    return retmax

  def calculate_expected_requests(self, qsize=None, reqsize=None):
    """Calculate anf set the expected number of requests. Uses internal
    parameters if non are provided.

    :param int or None qsize: query size, i.e. expected number of data sets
    :param int reqsize: number of data sets  to fetch in one request
    """
    if not qsize:
      qsize = self.query_size
    if not reqsize:
      reqsize = self.retmax
    self.expected_requests = math.ceil(qsize / reqsize)

  def check(self):
    """Implements :class:`entrezpy.base.parameter.EutilsParameter.check` to
    check for the minumum required parameters. Aborts if any check fails.
    """
    if not self.haveDb():
      sys.exit(logger.error(json.dumps({__name__: {'Error' : {'Missing parameter': 'db'},
                                                   'action' : 'abort'}})))

    if not self.haveExpectedRequets():
      sys.exit(logger.error(json.dumps({__name__ : {'Error' :
                                                    {'expected requests' : self.expected_requests},
                                                    'action' : 'abort'}})))

    if not self.goodDateparam():
      sys.exit(logger.error(json.dumps({__name__ : {'Error' : 'Bad date parameters',
                                                    'action' : 'abort'}})))

    if not self.term and not self.webenv:
      sys.exit(logger.error(json.dumps({__name__:{'Error': {'Missing  parameters' : 'term, WebEnv'},
                                                  'action' : 'abort'}})))

  def dump(self):
    return {'db' : self.db, 'webenv' : self.webenv, 'querykey' : self.querykey,
            'usehistory' : self.usehistory, 'term':self.term, 'retmode':self.retmode,
            'uilist': self.uilist, 'retmax': self.retmax, 'retstart': self.retstart,
            'sort' : self.sort, 'field' : self.field, 'datetype' : self.datetype,
            'reldate' : self.reldate, 'mindate' : self.mindate, 'maxdate' : self.maxdate,
            'expected_requsts' : self.expected_requests, 'query_size' : self.query_size,
            'max_request_size' : MAX_REQUEST_SIZE}
