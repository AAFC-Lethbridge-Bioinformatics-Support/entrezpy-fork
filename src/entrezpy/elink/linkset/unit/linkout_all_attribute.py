#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import entrezpy.elink.linkset.unit.linksetunit

class LinkOutAllAttribute(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):

  @classmethod
  def new(cls, unit):
    return cls(unit)

  class Provider:

    def __init__(self, provider_obj):
      self.id = provider_obj.pop('id', None)
      self.name = provider_obj.pop('name', None)
      self.nameabbr = provider_obj.pop('nameabbr', None)
      self.url = provider_obj.pop('url', None)
      self.iconurl = provider_obj.pop('iconurl', None)

    def dump(self):
      return {'id' : self.id, 'name' : self.name, 'nameabbr' : self.nameabbr,
              'url' : self.url, 'iconurl' : self.iconurl}

  def __init__(self, unit):
    super().__init__(None, unit.pop('linkname', None))
    self.iconurl = unit.pop('iconurl', None)
    self.subjecttype = unit.pop('subjecttype', None)
    self.category = unit.pop('category', None)
    self.attributes = unit.pop('attributes', [])
    self.provider  = self.Provider(unit.pop('provider', {}))

  def dump(self):
    return dict({ 'iconurl' : self.iconurl, 'linkname' : self.linkname,
                  'subjecttype':self.subjecttype, 'category' : self.category,
                  'attributes' : self.attributes, 'provider' : self.provider.dump()},
                   **self.basic_dump())
