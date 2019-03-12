#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2018 The University of Sydney
# \description Demonstrate Entrezpy's epost functionality and setup.
#   Eposter() posts a UIDs to the Entrez history server and returns the
#   corresponding WebEnv and Querykey for subsequent use [0].
#   For
# The examples are stored as parameters in the list `examples` (taken from [0]).
#   Outline:
#     0. Import entrezpy
#     1. Create an instance of Eposter() with the required parameters:
#         - instance name
#         - user email.
#         These are required by NCBI [1]. The instance name corresponds to the
#         Eutils `tool` parameter [1].
#     3. Loop over the examples, post the UIDs and return the corresponding
#        WebEnv and QueryKey for them to later use.
#
# N.B.
#   NCBI api key[1]: If an apikey is passed to Efetcher(), it will be used to
#                    allow more requests [1]. Without apikey, Entrezpy checks if
#                    the environmental variable $NCBI_API_KEY is set. If not,
#                    less queries per second are performed.
#
#  References:
#    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost
#    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
#    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
#-------------------------------------------------------------------------------

import os
import sys
import time
import json
import argparse

""" Setup Entrezpy
Set the proper import path to the required classes relative to this file by
updating sys.payth. The example assumes you cloned the repository.
$reporoot
|-- examples
|   `-- entrezpy.epost-examples.py  <-You are here
`-- src
    `-- entrezpy
        `-- epost
            |-- epost_analyzer.py
            `-- eposter.py
"""
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.epost.eposter
import entrezpy.epost.epost_analyzer

def main():
  demo_src = 'https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost'
  ap = argparse.ArgumentParser(description="Entrezpy Eposter examples ({})".format(demo_src))
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI'),
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')

  args = ap.parse_args()
  examples = [{'db' : 'pubmed','id' : [11237011,12466850]},
              {'db' : 'pubmed','id' : [11237011]},
              {'db' : 'pubmed','id' : [12466850]}]
  hist_ex = {'db' : 'pubmed','id' : [11237011]}

  start = time.time()
  for i in range(len(examples)):
    substart = time.time()
    ep = entrezpy.epost.eposter.Eposter('eposter', args.email, args.apikey)
    a = ep.inquire(examples[i])
    print("+Query {}\n\tParameters: {}\n\tStatus:".format(i, examples[i]), end='')
    if not a.isSuccess():
      print("\tFailed:\n\t\tError: {}".format(a.error))
      return 0
    print("\tSuccess")
    if a.result.isEmpty():
      print("+No results for example {}".format(i))
    else:
      print("\t+++Start dumping results+++\n%%%\t{}".format(json.dumps(a.result.dump())))
      print("\t+++End  Results+++\n\tFollow-up parameters:")
      if not a.result.get_link_parameter():
        print("\t\tNo follow-up parameters")
      else:
        print("\t\t{}".format(a.result.get_link_parameter()))
    print("+Time query: {} sec".format(time.time()-substart))

  print("+Update WebEnv of query #2 with query #3")
  ep = entrezpy.epost.eposter.Eposter('eposter', args.email, args.apikey)
  new_a = ep.inquire(dict({'WebEnv':a.result.webenv}, **examples[1]))
  #return dict(extend, **reqdump)
  print(a.result.dump(), '\n', new_a.result.dump())
  print("+Time total: {} sec".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
