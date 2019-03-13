"""
..
  Copyright 2018 The University of Sydney
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

.. module:: entrezpy.esummary.esummary_result
  :synopsis: Exports class EsummaryResult implementing entrezpy results from
    NCBI Esummary E-Utility requests

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import entrezpy.base.result


class EsummaryResult(entrezpy.base.result.EutilsResult):

  def __init__(self, response, request):
    super().__init__('esummary', request.query_id, request.db, response.get('webenv'))
    self.summaries = {}

  def add_summary(self, uid, summaries):
    if int(uid) not in self.summaries:
      self.summaries[int(uid)] = summaries.pop(uid)

  def dump(self):
    """:rtype: dict"""
    return {'db':self.db, 'size' : self.size(), 'function' : self.function,
            'summaries': [self.summaries[x] for x in self.summaries]}

  def get_link_parameter(self, reqnum=0):
    """Esummary has no link automated link ability"""
    pass

  def size(self):
    return len(self.summaries)

  def isEmpty(self):
    if self.size() == 0:
      return True
    return False
