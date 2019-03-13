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

.. module:: entrezpy.efetch.efetcher
  :synopsis: Exports class Efetcher implementing Efetch queries to NCBI EUtils.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
import logging

import entrezpy.base.query
import entrezpy.efetch.efetch_parameter
import entrezpy.efetch.efetch_request
import entrezpy.efetch.efetch_analyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class Efetcher(entrezpy.base.query.EutilsQuery):
  """Efetcher implements Efetch E-Utilities queries [0]. It implements
  :meth:`entrezpy.base.query.EutilsQuery.inquire` to fetch data from NCBI
  Entrez servers.
  [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
  [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/table/
  chapter2.T._entrez_unique_identifiers_ui/?report=objectonly
  """

  def __init__(self, tool, email, apikey=None, apikey_var=None, threads=None, qid=None):
    """:ivar result: :class:`entrezpy.base.result.EutilsResult`"""
    super().__init__('efetch.fcgi', tool, email, apikey, threads, qid=qid)

  def inquire(self, parameter, analyzer=entrezpy.efetch.efetch_analyzer.EfetchAnalyzer()):
    """Implements :meth:`entrezpy.base.query.EutilsQuery.inquire` and configures
    follow-up requests if required.

    :param dict parameter: EFetch parameter
    :param analyzer: analyzer for Efetch results
    :type analyzer: :class:`entrezpy.base.analyzer.EutilsAnalyzer`
    :return: analyzer instance or None if request errors have been encountered
    :rtype: :class:`entrezpy.base.analyzer.EutilsAnalyzer` or None
    """
    logger.debug(json.dumps({__name__ : {'Parameter' : p.dump()}}))
    p = entrezpy.efetch.efetch_parameter.EfetchParameter(parameter)
    req_size = p.request_size
    self.monitor_start(p)
    for i in range(p.expected_requests):
      if i * req_size + req_size > p.retmax:
        req_size = p.retmax % p.request_size
      self.add_request(entrezpy.efetch.efetch_request.EfetchRequest(p,
                                                                    (i*p.request_size),
                                                                    req_size),
                       analyzer)
    self.request_pool.drain()
    self.monitor_stop()
    if self.check_requests() == 0:
      return analyzer
    return None

  def check_requests(self):
    """Test for request errors

      :return: 1 if request errors else 0
      :rtype: int
    """
    if not self.hasFailedRequests():
      logger.info(json.dumps({__name__ : {'Query status' : {self.id : 'OK'}}}))
      return 0
    logger.info(json.dumps({__name__ : {'Query status' : {self.id : 'failed'}}}))
    logger.debug(json.dumps({__name__ : {'Query status' :
                                         {self.id : 'failed',
                                          'request-dumps' : [x.dump_internals()
                                                             for x in self.failed_requests]}}}))
    return 1