#-------------------------------------------------------------------------------
#  \file epost_request.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import request

class EpostRequest(request.EutilsRequest):

  def __init__(self, parameter):
    super().__init__('epost', parameter.db)
    self.uids =  parameter.uids
    self.size = len(parameter.uids)
    self.webenv = parameter.webenv
    self.retmode = parameter.retmode

  def prepare_qry(self):
    print("asasas", self.db)
    return self.prepare_base_qry(extend={'id' : ','.join(str(x) for x in self.uids),
                                         'WebEnv' : self.webenv})
  def dump(self):
    return self.dump_internals({'retmode':self.retmode, 'WebEnv':self.webenv})
