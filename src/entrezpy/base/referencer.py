#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

class EutilReferencer:

  class Reference:

    def __init__(self, webenv, querykeys):
      self.webenv = webenv
      self.querykeys = querykeys

  def __init__(self, webenv, querykey):
    self.references = {}
    if webenv:
      self.add_reference(webenv, querykey)

  def add_reference(self, webenv, querykey):
    if webenv not in self.references:
      self.references[webenv] = [int(querykey)]
    if self.references[webenv][-1] != int(querykey):
      self.references[webenv].append(int(querykey))

  def get_reference(self, webenv):
    if webenv not in self.references:
      return None
    return self.Reference(webenv, self.references[webenv])

  def dump(self):
    return self.references

  def size(self):
    return len(self.references)
