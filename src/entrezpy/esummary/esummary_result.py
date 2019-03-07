#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description:
#-------------------------------------------------------------------------------

import os
import sys
import json

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import result

class EsummaryResult(result.EutilsResult):

  def __init__(self, db=None, webenv=None, uids=[], querykey=None):
    super().__init__('esummary', db=db, webenv=webenv, uids=uids, querykey=querykey)
    self.summaries = {}

  def add_summary(self, uid, summaries):
    if int(uid) not in self.summaries:
      self.summaries[int(uid)] = summaries.pop(uid)

  def dump(self):
    return json.dumps({"typ":self.typ, "db":self.db, "webenv":self.webenv,
                       "uids" : self.uids, "querykey" : self.querykey,
                       "summaries": [self.summaries[x] for x in self.summaries]})

  def get_link_parameters(self):
    return {'db' : self.db, 'size' : self.count, 'id' : self.uids,
            'WebEnv' : self.webenv, 'QueryKey' : self.querykey}
