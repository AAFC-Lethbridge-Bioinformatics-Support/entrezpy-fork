#!/usr/bin/env python3

import os
import sys
import xml.etree.ElementTree


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

class PubmedResult(entrezpy.base.result.EutilsResult):
  """
  Derived class to store a Pubmed query. Individual Pubmed records
  (PubmecRecord) are stored in pubmed_records.

  :param response: inspected response from PubmedAnalyzer
  :param request: request linked to the current response
  :ivar dict pubmed_records: storing PubmedRecord instances
  """

  def __init__(self, response, request):
    super().__init__(request.eutil, request.query_id, request.db)
    self.pubmed_records = {}

  def size(self):
    pass

  def isEmpty(self):
    pass

  def get_link_parameter(self, reqnum=0):
    pass

  def add_pubmed_record(self, pubmed_record):
    pass

class PubmedAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """
  Derived class to analyze and parse Pubmed responses and requests.
  """

  def __init__(self):
    super().__init__()

  def init_result(self, response, request):
    pass

  def analyze_error(self, response, request):
    pass

  def analyze_result(self, response, request):
    pass

def main():
  c = entrezpy.conduit.Conduit(sys.argv[1])
  fetch_pubmed = c.new_pipeline()
  fetch_pubmed.add_fetch({'db':'pubmed', 'id':[sys.argv[2]], 'retmode':'xml'})
  c.run(fetch_pubmed)
  return 0

if __name__ == '__main__':
  main()
