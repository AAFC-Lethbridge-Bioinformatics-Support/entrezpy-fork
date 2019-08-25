#!/usr/bin/env python3
"""
.. module:: pubmed-fetcher.py
  :synopsis:
    Frontend for tutorial to extend entrezpy by develpoing a PubMed record fetcher

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate extending entrezpy by implementing a Pubmed fetcher for conduit.

  Setup
  -----
  Set the proper import path to the required classes relative to this file by
  updating ``sys.payth``. The example assumes you cloned the git repository from
  https://gitlab.com/ncbipy/entrezpy.git.
  The tutorial can be found at $reporoot/docs/entrezpy-doc/source/

::
  $reporoot
  |-- examples
  |   `-- tutorials
  |       `-- pubmed
  |           `-- pubmed-fetcher.py  <-You are here
  `-- src
      `-- entrezpy
          |-- conduit.py
          `-- base
              |-- analzyer.py
              `-- result.py

"""

import os
import sys
import xml.etree.ElementTree


# If entrezpy is installed using PyPi uncomment th line 'import entrezpy'
# and comment the 'sys.path.insert(...)'
# import entrezpy
sys.path.insert(1, os.path.join(sys.path[0], '../../../src'))
# Import required entrepy modules
import entrezpy.conduit
import entrezpy.base.result
import entrezpy.base.analyzer


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
    # Store individual pubmed record in dict to avoid duplicates
    self.pubmed_records = {}

  def size(self):
    return len(self.pubmed_records)

  def isEmpty(self):
    if not self.pubmed_records:
      return True
    return False

  def get_link_parameter(self, reqnum=0):
    pass

  def add_pubmed_record(self, pubmed_record):
    self.pubmed_records[pubmed_record.pmid] = pubmed_record

class PubmedAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):

  def __init__(self):
    super().__init__()

  def init_result(self, response, request):
    if self.result is None:
      self.result = PubmedResult(response, request)

  def analyze_error(self, response, request):
    print(json.dumps({__name__:{'Response': {'dump' : request.dump(),
                                             'error' : response.getvalue()}}}))

  def analyze_result(self, response, request):
    """
    Parse PubMed  XML line by line to extract authors and citations.
    xml.etree.ElementTree.iterparse reads the XML file incrementaly and each
    <PubmedArticle> is cleared after processing.
    """
    self.init_result(response, request)
    isAuthorList = False
    isAuthor = False
    isRefList = False
    isRef = False
    medrec = None
    for event, elem in xml.etree.ElementTree.iterparse(response, events=["start", "end"]):
      if event == 'start':
        if elem.tag == 'PubmedArticle':
          medrec = PubmedRecord()
        if elem.tag == 'AuthorList':
          isAuthorList = True
        if isAuthorList and elem.tag == 'Author':
          isAuthor = True
          medrec.authors.append({'fname': None, 'lname': None})
        if elem.tag == 'ReferenceList':
          isRefList = True
        if isRefList and elem.tag == 'Reference':
          isRef = True
      else:
        if elem.tag == 'PubmedArticle':
          self.result.add_pubmed_record(medrec)
          elem.clear()
        if elem.tag == 'AuthorList':
          isAuthorList = False
        if isAuthorList and elem.tag == 'Author':
          isAuthor = False
        if elem.tag == 'ReferenceList':
          isRefList = False
        if elem.tag == 'Reference':
          isRef = False
        if elem.tag == 'PMID':
          medrec.pmid = elem.text
        if isAuthor and elem.tag == 'LastName':
          medrec.authors[-1]['lname'] = elem.text
        if isAuthor and elem.tag == 'ForeName':
          medrec.authors[-1]['fname'] = elem.text
        if isRef and elem.tag == 'Citation':
          medrec.citations.append(elem.text)

def main():
  c = entrezpy.conduit.Conduit(sys.argv[1])
  fetch_pubmed = c.new_pipeline()
  fetch_pubmed.add_fetch({'db':'pubmed', 'id':[sys.argv[2].split(',')],
                          'retmode':'xml'}, analyzer=PubmedAnalyzer())
  a = c.run(fetch_pubmed)
  print(a)
  res = a.get_result()
  for i in res.pubmed_records:
    print(i, res.pubmed_records[i].authors, res.pubmed_records[i].citations)
  return 0

if __name__ == '__main__':
  main()
