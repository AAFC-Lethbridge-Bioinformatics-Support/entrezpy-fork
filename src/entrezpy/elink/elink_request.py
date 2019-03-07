#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Elink request for NCBI's EDirect
#-------------------------------------------------------------------------------

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import request

class ElinkRequest(request.EutilsRequest):

  cmd_wo_1to1 = {'neighbor_score' : 0}

  def __init__(self, parameter):
    super().__init__('elink', parameter.db)
    self.dbfrom = parameter.dbfrom
    self.cmd = parameter.cmd
    self.querykey = parameter.querykey
    self.webenv = parameter.webenv
    self.uids = parameter.uids
    self.retmode = parameter.retmode
    self.linkname = parameter.linkname
    self.term = parameter.term
    self.holding = parameter.holding
    self.datetype = parameter.datetype
    self.reldate = parameter.reldate
    self.mindate = parameter.mindate
    self.maxdate = parameter.maxdate

  def prepare_qry(self):
    qry = self.prepare_base_qry(extend={'db':self.db, 'retmode':self.retmode,
                                        'cmd':self.cmd, 'dbfrom':self.dbfrom})
    if self.webenv and self.querykey:
      qry.update({'WebEnv' : self.webenv, 'query_key' : self.querykey})
    else:
      if self.cmd == 'neighbor':
        qry.update({'id' : self.uids})
      else:
        qry.update({'id' : ','.join(str(x) for x in self.uids)})
    if self.linkname and (self.cmd == 'neighbor' or self.cmd == 'neighbor_history'):
      qry.update({'linkname' : self.linkname})
    if self.term:
      qry.update({'term' : self.term})
    if self.holding:
      qry.update({'holding' : self.holding})
    if self.datetype:
      qry.update({'datetype' : self.datetype})
    if self.reldate:
      qry.update({'reldate' : self.reldate})
    if self.mindate:
      qry.update({'mindate' : self.mindate})
    if self.maxdate:
      qry.update({'maxdate' : self.maxdate})
    if  not self.db:
      qry.pop('db')
    return qry

  def dump(self):
    return self.dump_internals({'retmode' : self.retmode,
                                'WebEnv' : self.webenv,
                                'cmd' : self.cmd,
                                'holding' : self.holding,
                                'term' : self.term,
                                'query_key' : self.querykey,
                                'dbfrom' : self.dbfrom,
                                'datetype' : self.datetype,
                                'reldate' : self.reldate,
                                'mindate' : self.mindate,
                                'maxdate' : self.maxdate})
