#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class LinkIn(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, dbto, hasneighbor):
    return cls(dbto, hasneighbor)

  def __init__(self, dbto, hasneighbor):
    super().__init__(dbto, None)
    self.hasneighbor = True if hasneighbor == 'Y' else False

  def dump(self):
    return dict({'hasneighbor' : self.hasneighbor}, **self.basic_dump())
