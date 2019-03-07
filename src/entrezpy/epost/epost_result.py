#-------------------------------------------------------------------------------
#  \file epost_result.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json

sys.path.insert(1, os.path.join(sys.path[0], '../'))

from entrezpy_base import result

class EpostResult(result.EutilsResult):

  def __init__(self, db=None, webenv=None, querykey=0, size=1):
    super().__init__('epost', db=db, webenv=webenv, querykey=querykey)
    self.size = size

  def dump(self):
    return json.dumps({'db':self.db,'webenv':self.webenv,'size':self.size,
                       'querykey':self.querykey, 'len_uids': len(self.uids),
                       'uids' : self.uids, "typ":self.typ})

  def get_link_parameter(self):
    return {'WebEnv' : self.webenv,
            'QueryKey' : self.querykey,
            'db' : self.db,
            'size' : self.size}
