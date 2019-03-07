#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class LinkOutNonlibAttributes(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, objurl):
    return cls(objurl)

  def __init__(self, objurl):
    super().__init__(None, None)
    self.objurl = objurl

  def dump(self):
    return dict({'objurl' : self.objurl}, **self.basic_dump())
