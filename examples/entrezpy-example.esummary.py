#!/usr/bin/env python3
"""
.. module:: entrezpy-examples.esummary
  :synopsis:
    Example of using entrezpy's esummary function.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate Entrezpy's esummary functionality and setup. Esummary() fetches
  summaries for given UIDs in JSON from the given NCBI Entrez database [0].

  The examples are stored as parameters in the list `examples` (taken from [0]).
  Outline
  -------
  0. Import entrezpy
  1. Create an Esummary() instance with the required parameters:
      - instance name
      - user email.
      These are required by NCBI [1]. The instance name corresponds to the
      Eutils `tool` parameter [1].
  2. Loop over the examples and fetch the summaries.
  3. Print results to STDOUT

  Setup
  -----
  Set the proper import path to the required classes relative to this file by
  updating ``sys.payth``. The example assumes you cloned the git repository from
  https://gitlab.com/ncbipy/entrezpy.git.

::
  $reporoot
  |-- examples
  |   `-- entrezpy-examples.efetch.py  <-You are here
  `-- src
      `-- entrezpy
          `-- efetch
              |-- efetch_analyzer.py
              `-- efetch.py

  N.B.
    NCBI api key[1]: If an apikey is passed to Efetcher(), it will be used to
                    allow more requests [1]. Without apikey, Entrezpy checks if
                    the environmental variable $NCBI_API_KEY is set. If not,
                    less queries per second are performed.

    Efetch analyzer:  Efecth is unique in respect to all other functions as its
                      function `inquire` requires an analyzer as parameter. This
                      example uses the default analyzer which prints either the
                      errors or stores the result as string to
                      `analyzer.result`. It can be easly adapted for more
                      complex tasks (see documentation).
  References:
    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
"""


import os
import sys
import time
import json
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))

import entrezpy.esummary.esummarizer
import entrezpy.esummary.esummary_analyzer


def main():
  # Python argument parser (see [2] for more details)
  demo_src = 'https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESummary'
  ap = argparse.ArgumentParser(description="Entrezpy Esummarizer examples ({})".format(demo_src))
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI')
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')

  args = ap.parse_args()

  # Prepare list of examples. Each example is a parameter dictionary as expected
  # by Esummarizer.
  examples = [
              {'db' : 'pubmed', 'id' : [11850928, 11482001]},
              {'db' : 'protein', 'id' : [28800982, 28628843]},
              {'db' : 'nucleotide', 'id' : [28864546, 28800981]},
              {'db' : 'structure', 'id' : [19923, 12120]},
              {'db' : 'taxonomy', 'id' : [9913, 30521]}
             ]

  # Loop over examples
  start = time.time()
  for i in range(len(examples)):
    qrystart = time.time()
    es = entrezpy.esummary.esummarizer.Esummarizer('esummary', args.email, args.apikey)
    a = es.inquire(examples[i], entrezpy.esummary.esummary_analyzer.EsummaryAnalzyer())
    print("+Query {}\n+++\tParameters: {}\n+++\tStatus:".format(i, examples[i]), end='')
    if not a.isSuccess():
      print("\tFailed: Response errors")
      return 0
    print("\tResponse OK")
    if a.isEmpty():
      print("+++\tWARNING: No results for example {}".format(i))
    print("+++\tStart dumping results\n+++%%%\t{}".format(json.dumps(a.get_result().dump())))
    print("+++\tFetched summaries ({}):\n\t{}".format(a.result.size(), a.get_result().summaries))
    print("+++\tEnd  Results\n+++\tQuery time: {} sec".format(time.time()-qrystart))
  print("+Total time: {} sec".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
