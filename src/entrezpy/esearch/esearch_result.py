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

class EsearchResult(result.EutilsResult):

  def __init__(self, db=None, count=None, webenv=None, querykey=None, uids=[], retmax=0, retstart=0):
    super().__init__('esearch', db=db, uids=uids, webenv=webenv, querykey=int(querykey))
    self.count = int(count)
    self.retmax = int(retmax)
    self.retstart = int(retstart)

  def dump(self):
    return json.dumps({"db":self.db, "count" : self.count, "uids" : self.uids,
                       "querykey" : self.querykey, "retmax" : self.retmax,
                       "retstart" : self.retstart, "webenv" : self.webenv,
                       "len_uids" : len(self.uids), "typ":self.typ})

  def get_link_parameter(self):
    return {'db' : self.db, 'size' : self.count, 'id' : self.uids,
            'WebEnv' : self.webenv, 'query_key' : self.querykey}
