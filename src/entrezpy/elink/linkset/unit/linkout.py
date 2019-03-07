#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class LinkOut(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, dbto, haslinkout):
    return cls(dbto, haslinkout)

  def __init__(self, dbto, haslinkout):
    super().__init__(dbto, None)
    self.haslinkout = True if haslinkout == 'Y' else False

  def dump(self):
    return dict({'haslinkout' : self.haslinkout}, **self.basic_dump())
