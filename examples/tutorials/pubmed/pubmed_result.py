#!/usr/bin/env python3
"""
.. module:: entrezpy-example.conduit.fetch-genomes
  :synopsis:
    Tutorial to extend entrezpy by develpoing a PubMed record fetcher

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate extending entrezpy by implementing a Pubmed result class by
  inheriting the class entrezpy.base.result.EutilsResult.


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
  |           `-- pubmed_result.py  <-You are here
  `-- src
      `-- entrezpy
          `-- base
              `-- result.py
"""

import io
import os
import sys

# If enrezpy is installed using PyPi uncomment line 40 and comment line 41
# import entrezpy
sys.path.insert(1, os.path.join(sys.path[0], '../../../src'))
# Import base result module to inherit entrezpy.base.result.EutilsResult
import entrezpy.base.result

class PubmedResult(entrezpy.base.result.EutilsResult):

  def __init__(response, request):
    super().__init__('pubmed', request.query_id, request.db, response.get('webenv'),
                     response.pop('querykey', None))
    # Store individual pubmed record in dict to avoid duplicates
    self.pubmed_records = {}
