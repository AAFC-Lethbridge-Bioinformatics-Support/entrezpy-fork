#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2018 The University of Sydney
# \description Demonstrate Entrezpy's esearch functionality and setup.
#   Elink() links UIDs between Entrez databases or reports outside links for
# UIDs, e.g. publications linked to this UID[0].

# The examples are stored as parameters in the list `examples` (taken from [0]).
#   Outline:
#     0. Import entrezpy
#     1. Create an instance of Esearcher() with the required parameters:
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
#    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.Elink
#    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
#    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
#-------------------------------------------------------------------------------

import os
import sys
import json
import time
import argparse

""" Setup Entrezpy
Set the proper import path to the required classes relative to this file by
updating sys.payth. The example assumes you cloned the git repository.
$reporoot
|-- examples
|   `-- entrezpy.epost-examples.py  <-You are here
`-- src
    `-- entrezpy
        `-- elink
            |-- elink_analyzer.py
            `-- elinker.py
"""

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.elink.elinker
import entrezpy.elink.elink_analyzer


def main():
  ap = argparse.ArgumentParser(description="ncbipy-epost examples from \
                https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch")
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI'),
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')

  args = ap.parse_args()
  examples = [
              {'dbfrom' : 'protein', 'db' : 'gene', 'id' : [15718680,157427902]},
              {'dbfrom':'pubmed', 'db' : 'pubmed','id' : [15718680, 20210808], 'cmd':'neighbor_score'},
              {'dbfrom':'protein', 'db' : 'gene','id' : [15718680, 157427902], 'cmd':'neighbor_history', 'link':False},
              {'dbfrom':'protein', 'db' : 'gene','id' : [15718680, 157427902], 'cmd':'neighbor_history'},
              {'dbfrom':'protein', 'id' : [15718680, 157427902], 'cmd':'acheck'},
              {'dbfrom':'protein', 'db' : 'pubmed', 'id' : [15718680, 157427902], 'cmd':'acheck'},
              {'dbfrom':'nuccore', 'id' : [21614549,219152114], 'cmd':'ncheck'},
              {'dbfrom':'protein', 'id' : [15718680,157427902], 'cmd':'lcheck'},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'llinks'},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'llinkslib', 'link' : False},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'prlinks',},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'prlinks', 'retmode':'ref'},
             ]

  start = time.time()
  for i in range(len(examples)):
    qrystart = time.time()
    ef = entrezpy.elink.elinker.Elinker('elinker', args.email, args.apikey)
    a = ef.inquire(examples[i], entrezpy.elink.elink_analyzer.ElinkAnalyzer())
    print("+Query {}\n+++\tParameters: {}\n+++\tStatus:".format(i, examples[i]), end='')
    if not a.isSuccess():
      print("\tFailed: Response errors")
      return 0
    print("\tResponse OK")
    if a.isEmpty():
      print("+No results for example {}".format(i))
    else:
      print("+++\tStart dumping results\n+++%%%\t{}".format(json.dumps(a.get_result().dump())))
      print("+++\tEnd  Results")
      print("+++\tFollow-up parameters:")
      if not a.follow_up():
        print("+++\t\tNo follow-up parameters")
      else:
        print("+++\t\t{}".format(a.follow_up()))
    print("+++\tTime query: {} sec".format(time.time()-qrystart))
  print("+Time total: {} sec".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
