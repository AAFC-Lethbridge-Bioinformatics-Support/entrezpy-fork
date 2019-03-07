# Copyright 2018, 2019 The University of Sydney
# This file is part of entrezpy.
#
#  Entrezpy is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Entrezpy is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with entrezpy.  If not, see <https://www.gnu.org/licenses/>.
"""
.. module:: esearch_result
   :synopsis: This module is part of entrezpy. It exports the EsearchResult
      class for SearchAnalyzer. It inherits entrezpy.base.result.EutilsResult

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import entrezpy.base.result


class EsearchResult(entrezpy.base.result.EutilsResult):
  """ EsearchResult sstores fetched UIDs and/or WebEnv-QueryKeys and
  creates follow-up parameters.

  :param dict response: Esearch response
  :param request: Esearch request instance for this query
  :type request: :class:`entrezpy.esearch.esearch_request.EsearchRequest`
  """

  def __init__(self, response, request):
    super().__init__('esearch', request.query_id, request.db, response.get('webenv'),
                     response.pop('querykey', None))
    self.count = int(response.get('count'))
    self.retmax = int(response.pop('retmax'))
    self.retstart = int(response.pop('retstart'))
    self.uids = response.pop('idlist', [])
    print(self.dump())
    print(self.uids)

  def dump(self):
    """Dumps instance attributes

    :rtype: dict
    """
    return {'db':self.db, 'count' : self.count, 'uid' : self.uids,
            'retmax' : self.retmax,
            'retstart' : self.retstart, 'references' : self.references.dump(),
            'len_uids' : len(self.uids), 'function':self.function}

  def get_link_parameter(self):
    """Assemble follow-up parameters for linking.

    :rtype: dict
    """
    return {'db' : self.db, 'size' : self.size(), 'id' : self.uids,
            'WebEnv' : self.webenv,
            'query_key' : self.references.get_querykeys(self.webenv)[-1]}


  def isEmpty(self):
    """Empty search result has no webenv/querykey and/or no fetched UIDs"""
    if self.references.size() > 0:
      return False
    if self.uids:
      return False
    return True

  def size(self):
    return len(self.uids)

  def query_size(self):
    return self.count

  def add_response(self, response):
    self.references.add_reference(response.pop('webenv', None), response.pop('querykey', None))
    self.uids += response.pop('idlist', [])
    print(self.dump())
