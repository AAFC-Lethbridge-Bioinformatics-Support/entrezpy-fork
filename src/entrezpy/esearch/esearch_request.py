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

.. module:: entrezpy.elinker.elink_request
  :synopsis:
    Exports ElinkRequest implementing requests from ElinkAnalyzer

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import logging

import entrezpy.base.request


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class EsearchRequest(entrezpy.base.request.EutilsRequest):

  def __init__(self, parameter, start, size):
    super().__init__('esearch', parameter.db)
    self.id = None
    self.term = parameter.term
    self.retstart = start
    self.retmax = size
    self.retmode = parameter.retmode
    self.usehistory = parameter.usehistory
    self.webenv = parameter.webenv
    self.querykey = parameter.querykey
    self.sort = parameter.sort
    self.field = parameter.field
    self.idtype = parameter.idtype
    self.datetype = parameter.datetype
    self.reldate = parameter.reldate
    self.mindate = parameter.mindate
    self.maxdate = parameter.maxdate
    logger.debug(json.dumps({'NewRequest':{'id':self.id,
                                           'query-id':self.query_id,
                                           'retstart':self.retstart,
                                           'retmax':self.retmax}}))

  def get_post_parameter(self):
    qry = self.prepare_base_qry(extend={'term' : self.term,
                                        'retmax' : self.retmax,
                                        'retstart' : self.retstart,
                                        'retmode' : self.retmode})
    if self.usehistory:
      qry.update({'usehistory' : 'y'})
    if self.webenv:
      qry.update({'WebEnv' : self.webenv})
    if self.querykey:
      qry.update({'query_key' : self.querykey})
    if self.sort:
      qry.update({'sort' : self.sort})
    if self.field:
      qry.update({'field' : self.field})
    if self.datetype:
      qry.update({'datetype' : self.datetype})
    if self.reldate:
      qry.update({'reldate' : self.reldate})
    if self.mindate:
      qry.update({'mindate' : self.mindate})
    if self.maxdate:
      qry.update({'maxdate' : self.maxdate})
    if self.idtype:
      qry.update({'idtype' : self.idtype})
    logger.debug(json.dumps({'PreppedRequest':{'id':self.id, 'query-id':self.query_id,
                                              'retstart':self.retstart,'retmax':self.retmax,
                                              'dump':self.dump()}}))
    return qry

  def dump(self):
    return self.dump_internals({'retmax' : self.retmax,
                                'retstart' : self.retstart,
                                'retmode' : self.retmode,
                                'usehistory' : self.usehistory,
                                'WebEnv' : self.webenv,
                                'query_key' : self.querykey,
                                'sort' : self.sort,
                                'field' : self.field,
                                'datetype' : self.datetype,
                                'reldate' : self.reldate,
                                'mindate' : self.mindate,
                                'maxdate' : self.maxdate})
