#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class NeighborLinksetUnit(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, uid, dbto, linkname):
    return cls(uid, dbto, linkname)

  def __init__(self, uid, dbto, linkname):
    super().__init__(dbto, linkname)
    self.uid = int(uid)

  def dump(self):
    return dict({'uid' : self.uid}, **self.basic_dump())
