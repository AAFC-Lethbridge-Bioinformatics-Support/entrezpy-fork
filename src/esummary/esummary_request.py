#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import request

class EsummaryRequest(request.EutilsRequest):

  def __init__(self, parameter, start, size):
    super().__init__('esummary', parameter.db)
    self.retstart = start
    self.retmax = size
    self.retmode = parameter.retmode
    self.esummary_version = parameter.esummary_version
    self.uids =  parameter.uids[start:start+size]
    self.webenv = parameter.webenv
    self.querykey = parameter.querykey

  def prepare_qry(self):
    qry = self.prepare_base_qry(extend={'retmode':self.retmode})
    if self.retmode == 'xml':
      qry.update({'version' : self.esummary_version})

    if self.webenv and self.querykey:
      qry.update({'WebEnv' : self.webenv, 'query_key':self.querykey,
                  'retstart' : self.retstart,'retmax' : self.retmax})
    else:
      qry.update({'id' : ','.join(str(x) for x in self.uids)})
    return qry
