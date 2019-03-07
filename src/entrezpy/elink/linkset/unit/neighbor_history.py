#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class NeighborHistoryLinkset(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, dbto, linkname, querykey, webenv):
    return cls(dbto, linkname, querykey, webenv)

  def __init__(self, dbto, linkname, querykey, webenv):
    super().__init__(dbto, linkname)
    self.querykey = querykey
    self.webenv = webenv

  def dump(self):
    return dict({'webenv' : self.webenv, 'querykey' : self.querykey}, **self.basic_dump())
