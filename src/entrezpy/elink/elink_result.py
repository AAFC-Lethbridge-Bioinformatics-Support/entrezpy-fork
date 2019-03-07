#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import result

class ElinkResult(result.EutilsResult):

  def __init__(self):
    super().__init__('elink')
    self.linksets = []
    self.cmd = None

  def dump(self):
    dump = {"typ" : self.typ, 'linksets' : []}
    for i in self.linksets:
      dump['linksets'].append(i.dump())
    return dump

  def get_link_parameter(self):
    if self.cmd == 'neighbor_history':
      return self.collapse_history_linksets()

    if self.cmd == 'neighbor':
      return self.collapse_uid_linksets()

  def collapse_history_linksets(self):
    parameters = []
    for i in self.linksets:
      for j in i.links:
        parameters.append({'WebEnv':i.webenv, 'db':j, 'term': ' OR '.join(str("#{0}".format(x.querykey)) for x in  i.links[j])})
    if len(parameters) > 1:
      sys.exit("Dev: more than one link linking parameter. Check.")
    return parameters[0]

  def collapse_uid_linksets(self):
    dbs = {}
    for i in self.linksets:
      if i.dbto not in dbs:
        dbs[i.dbto] = []
      for j in i.links:
        dbs[i.dbto]  += i.links[j]
      if len(dbs) > 1:
        sys.exit("Dev: more than one dbto linking parameter. Check.")
      for i in dbs:
        return {'db' : i, 'id' : dbs[i]}
