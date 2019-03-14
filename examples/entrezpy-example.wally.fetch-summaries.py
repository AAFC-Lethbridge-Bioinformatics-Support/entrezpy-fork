#!/usr/bin/env python3
"""
.. module:: entrezpy-example.wally.fetch-summaries
  :synopsis:
    Example of using entrezpy's Wally to run a summary pipeline

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate Entrezpy's Wally class and setup. Wally facilitates the
  creation of E-Utility query pipelines [0].

  The examples are stored as parameters in the list `examples` (taken from [0]).
  Outline
  -------
  0. Import entrezpy
  1. Create a Wally instance  with the required parameters:
      - instance name
      - user email.
      These are required by NCBI [1]. The instance name corresponds to the
      Eutils `tool` parameter [1].
  2. Get a new Wally pipeline
  3. Add queries to the pipline
  4. Run the pipeline
  3. Print specific attributes form the summaries to STDOUT

  Setup
  -----
  Set the proper import path to the required classes relative to this file by
  updating ``sys.payth``. The example assumes you cloned the git repository from
  https://gitlab.com/ncbipy/entrezpy.git.

::
  $reporoot
  |-- examples
  |   `-- entrezpy-examples.wally.fetch-summaries.py  <-You are here
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
import json
import time
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.wally

def main():
  ap = argparse.ArgumentParser(description='Simple ncbipy-esearch-example')
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI'),
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')
  ap.add_argument('--apikey_envar',
                  type=str,
                  default=None,
                  help='Environment varriable storing NCBI apikey (optional)')
  ap.add_argument('--threads',
                  type=int,
                  default=0,
                  help='number of threads to use (default=no threads)')
  ap.add_argument('--use_history',
                  default=False,
                  action='store_true',
                  help='Run example using NCBI history server for linking')

  args = ap.parse_args()

  start = time.time()
  w = entrezpy.wally.Wally(args.email, args.apikey, args.apikey_envar, threads=args.threads)
  px = w.new_pipeline()
  pid = px.add_search({'db' : 'gene',
                       'term' : 'tp53[preferred symbol] AND human[organism]',
                       'rettype' : 'count'})
  if args.use_history:
    pid = px.add_link({'db' : 'protein', 'cmd':'neighbor_history'}, dependency=pid)
    pid = px.add_search(dependency=pid)
  else:
    pid = px.add_link({'db' : 'protein'}, dependency=pid)
  pid = px.add_summary(dependency=pid)
  analyzer = w.run(px)
  for i in analyzer.result.summaries:
    print("{}\t{}".format(analyzer.result.summaries[i].get('caption'),
                          analyzer.result.summaries[i].get('sourcedb')))
  print("Threads: {}\tSummaries: {}\nDurations: {} [s]".format(w.threads,
                                                len(analyzer.result.summaries),
                                                 time.time()-start))
  return 0

if __name__ == '__main__':
  main()
