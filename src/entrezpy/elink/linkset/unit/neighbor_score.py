#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class NeighborScoreLinkset(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, link, dbto, linkname):
    return cls(link, dbto, linkname)

  def __init__(self, link, dbto, linkname):
    super().__init__(dbto, linkname)
    self.uid = int(link['id'])
    self.score = int(link['score'])

  def dump(self):
    return dict({'uid' : self.uid, 'score' : self.score}, **self.basic_dump())
