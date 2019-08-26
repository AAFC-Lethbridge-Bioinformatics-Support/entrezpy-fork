#!/usr/bin/env python3


import os
import sys


"""
If entrezpy is installed using PyPi uncomment th line 'import entrezpy'  and
comment the 'sys.path.insert(...)'
"""
# import entrezpy
sys.path.insert(1, os.path.join(sys.path[0], '../../../src'))
# Import required entrepy modules
import entrezpy.conduit


class PubmedRecord:
  """
  Simple data class to store individual Pubmed records. Individual authors will
  be stored as dict('lname':last_name, 'fname': first_name) in authors.
  Citations as string elements in the list citations.
  """
  def __init__(self):
    self.pmid = None
    self.title = None
    self.authors = []
    self.citations = []


class PubmedAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """
  Derived class of :class:`entrezpy.base.analyzer.EutilsAnalyzer` to analyze and
  parse PubMed responses and requests.
  """

  def __init__(self):
    super().__init__()

  def init_result(self, response, request):
    """Implemented virtual method :meth:`entrezpy.base.analyzer.init_result`.
    This method initiate a result instance when analyzing the first response"""
    pass

  def analyze_error(self, response, request):
    """Implement virtual method :meth:`entrezpy.base.analyzer.analyze_error` to
    handle Entrez errors."""
    pass

  def analyze_result(self, response, request):
    """Implement virtual method :meth:`entrezpy.base.analyzer.analyze_result`.
    Parse PubMed  XML to extract authors and citations"""
    pass

def main():
  c = entrezpy.conduit.Conduit(sys.argv[1])
  fetch_pubmed = c.new_pipeline()
  fetch_pubmed.add_fetch({'db':'pubmed', 'id':[sys.argv[2]], 'retmode':'xml'})
  c.run(fetch_pubmed)
  return 0

if __name__ == '__main__':
  main()
