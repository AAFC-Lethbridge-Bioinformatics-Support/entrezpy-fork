#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Demonstrate Entrezpy's esummary functionality and setup.
# Esummarizer() fetches summaries for given UIDs in the given style and
# format [0].
#
# The examples are stored as parameters in the list `examples` (taken from [0]).
#   Outline:
#     0. Import entrezpy
#     1. Create an instance of Esummarizer() with the required parameters:
#         - instance name
#         - user email.
#         These are required by NCBI [1]. The instance name corresponds to the
#         Eutils `tool` parameter [1].
#     3. Loop over the examples and fetch the summaries in JSON (default)
#     4. Esumarizer.inquire() returns the default esummary analyzer and prints
#        summaries to STDOUT.
#
#  NCBI api key [1]:  If an apikey is passed to Efetcher(), it will be used to
#                     allow more requests [1]. Without apikey, Entrezpy checks
#                     if  the environmental variable $NCBI_API_KEY is set. If
#                     not, less queries per second are performed.
#  References:
#    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost
#    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
#    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
#   Parameters to force error messages:
#   {'db' : 'pubmed','id' : ['PRJNA356464']}
#   {'db' : 'unists','id' : [254085]}
#-------------------------------------------------------------------------------

import os
import sys
import time
import argparse

""" Setup Entrezpy
Set the proper import path to the required classes relative to this file by
updating sys.path. The example assumes you cloned the repository.
$reporoot
|-- examples
|   `-- entrezpy.esummary-examples.py   <-You are here
`-- src
    `-- entrezpy
        `-- esummary
            |-- esummary_analyzer.py
            `-- esummarizer.py
"""
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.esummary.esummarizer
import entrezpy.esummary.esummary_analyzer

def main():
  # Python argument parser (see [2] for more details)
  demo_src = 'https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESummary'
  ap = argparse.ArgumentParser(description="Entrezpy Esummarizer examples ({})".format{demo_src})
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI'),
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')

  args = ap.parse_args()

  # Prepare list of examples. Each example is a parameter dictionary as expected
  # by Esummarizer.
  examples = [
              {'db' : 'pubmed','id' : [11850928,11482001]},
              {'db' : 'protein','id' : [28800982,28628843]},
              {'db' : 'nucleotide','id' : [28864546,28800981]},
              {'db' : 'structure','id' : [19923,12120]},
              {'db' : 'taxonomy','id' : [9913,30521]}
             ]

  # Loop over examples
  for i in range(len(examples)):
    start = time.time()
    print("## Query {}\nParameter:{}".format(i, examples[i]))

    # Instantiate an Esummarizer. Esummarizer.inquire() returns the default
    # Esummary analzyer which stores results as a dictionary in
    # analyzer.result.uids. In this example,print the summaries to STDOUT.
    es = entrezpy.esummary.esummarizer.Esummarizer('esummarizer', args.email, args.apikey)
    a = es.inquire(examples[i])
    # Check for successful query. Print duration, error or result to STDOUT.
    if not a.isSuccess():
      print("Status:\tFailed:\n\tError: {}\n".format(a.error))
    else:
      print("Status:\tSuccess\n\tResult:{}".format(a.result.dump()))
      if a.result.uids:
        uniq = {}
        for j in a.result.uids:
          if j not in uniq:
            uniq[j] = 0
          uniq[j] += 1
        if len(uniq) == len(a.result.uids):
          print("All requested uids fetched ({}):\n\t{}".format(len(a.result.uids),
                                                             ','.join(str(x) for x in a.result.uids)))
        else:
          print("Found duplicate uids")
          for k in uniq:
            if uniq[k] > 0:
              print(k)
    print("Duration: {} sec\n--------------------------".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
