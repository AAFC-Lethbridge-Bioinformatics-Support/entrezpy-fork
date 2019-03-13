#!/usr/bin/env python3
"""
.. module:: entrezpy-examples.esearch
  :synopsis:
    Example of using entrezpy's esearch function.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate Entrezpy's efetch functionality and setup. Efetcher() fetches
  given UIDs or accessions in the requested format and  style from the given
  NCBI Entrez database [0].

  The examples are stored as parameters in the list `examples` (taken from [0]).
  Outline
  -------
  0. Import entrezpy
  1. Create an Efetcher() instance with the required parameters:
      - instance name
      - user email.
      These are required by NCBI [1]. The instance name corresponds to the
      Eutils `tool` parameter [1].
  2. Loop over the examples and fetch the results as XML and text by
     updating the `retmode` parameter[1] on-the-fly.
  3. Print results to STDOUT

  Setup
  -----
  Set the proper import path to the required classes relative to this file by
  updating `sys.payth`. The example assumes you cloned the git repository from
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
import argparse


sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.efetch.efetcher
import entrezpy.efetch.efetch_analyzer
import entrezpy.esearch.esearcher


def main():
  # Python argument parser (see [2] for more details)
  demo_src = 'https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch'
  ap = argparse.ArgumentParser(description="Entrezpy Efetcher() examples ({})".format(demo_src))
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
  # by Efetcher.
  examples = [
              #{'db' : 'pubmed','id' : [17284678,9997], 'retmode':'text', 'rettype': 'abstract'},
              #{'db': 'pubmed', 'id': [11748933,11700088], 'retmode':'xml'},
              #{'db': 'nuccore', 'id': [21614549], 'strand':1, 'seq_start' : 1, 'seq_stop' : 100, 'rettype':'fasta'},
              #{'db': 'nuccore', 'id': [21614549], 'strand':2, 'seq_start' : 1, 'seq_stop' : 100, 'rettype':'fasta'},
              #{'db': 'nuccore', 'id': [21614549], 'complexity' : 3},
              #{'db': 'nucleotide', 'id': [5]},
              #{'db': 'nucleotide', 'id': [5], 'rettype':'fasta'},
              #{'db': 'nucleotide', 'id': [5], 'rettype':'gb'},
              #{'db': 'popset', 'id': [12829836], 'rettype':'gp'},
              #{'db': 'protein', 'id': [8], 'rettype':'gp', 'retmode':'xml'},
              #{'db': 'sequences', 'id': [312836839,34577063], 'rettype':'fasta', 'retmode':'xml'},
              #{'db': 'gene', 'id': [2], 'retmode':'xml'},
              {'db': 'pmc', 'id': [212403], 'retmode':'json'}
             ]
  #es = entrezpy.esearch.esearcher.Esearcher('esearcher', args.email, args.apikey)
  #sa = es.inquire({'db':'nucleotide','term':'viruses[orgn]', 'retmax': 0})

  #ef = entrezpy.efetch.efetcher.Efetcher('efetch', args.email, args.apikey)
  #p = sa.get_result().get_link_parameter()
  #p.update({'retstart' : 10, 'retmax':30})
  #a = ef.inquire(p)

  ## Loop over examples
  start = time.time()
  for i in range(len(examples)):
    for j in ['xml', 'text']:
      qrystart = time.time()
      ef = entrezpy.efetch.efetcher.Efetcher('efetcher', args.email, args.apikey)
      examples[i].update({'retmode':j})
      a = ef.inquire(examples[i], entrezpy.efetch.efetch_analyzer.EfetchAnalyzer())
      print("+Query {}\n+++\tParameters: {}\n+++\tStatus:".format(i, examples[i]), end='')
      if not a:
        print("\tFailed: Response errors")
        return 0
      print("\tResponse OK")
      print("+++\tQuery time: {} sec".format(time.time()-qrystart))
  print("+Total time: {} sec".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
