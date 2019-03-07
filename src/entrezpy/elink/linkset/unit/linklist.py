#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class LinkList(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, dbto, linkname, menutag, htmltag, priority):
    return cls(dbto, linkname, menutag, htmltag, priority)

  def __init__(self, dbto, linkname, menutag, htmltag, priority):
    super().__init__(dbto, linkname)
    self.menutag = menutag
    self.htmltag = htmltag
    self.priority = priority

  def dump(self):
    return dict({'htmltag' : self.htmltag, 'priority' : self.priority}, **self.basic_dump())
