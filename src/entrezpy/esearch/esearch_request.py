#-------------------------------------------------------------------------------
#  \file esearch_request.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \description The Esearch request class which inherits edrequest.EdRequest. It
#               assembles Esearch requests and stores the results.
#  \copyright 2017,2018 The University of Sydney
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import entrezpy_base.request

class EsearchRequest(entrezpy_base.request.EutilsRequest):

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
    self.rettype = parameter.rettype
    self.sort = parameter.sort
    self.field = parameter.field
    self.datetype = parameter.datetype
    self.reldate = parameter.reldate
    self.mindate = parameter.mindate
    self.maxdate = parameter.maxdate
    logger.debug(json.dumps({'NewRequest':{'id':self.id,
                                           'query-id':self.query_id,
                                           'retstart':self.retstart,
                                           'retmax':self.retmax}}))

  def prepare_qry(self):
    qry = self.prepare_base_qry(extend={'term' : self.term,
                                        'retmax' : self.retmax,
                                        'retstart' : self.retstart,
                                        'retmode' : self.retmode,
                                        'rettype' : self.rettype})
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
