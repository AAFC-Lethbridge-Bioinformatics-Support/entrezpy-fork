#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2018 The University of Sydney
# \description Demonstrate Entrezpy's esearch functionality and setup.
#   Esearch() searched Entrez databases and returns corresponding UIDs
# or WebEnv/Querykey references [0].

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
#    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.Esearch
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
updating sys.payth. The example assumes you cloned the git repository.
$reporoot
|-- examples
|   `-- entrezpy.epost-examples.py  <-You are here
`-- src
    `-- entrezpy
        `-- esearch
            |-- esearch_analyzer.py
            `-- esearcher.py
"""

import os
import sys
import time
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.esearch.esearcher
import entrezpy.esearch.esearch_analyzer

def main():
  ap = argparse.ArgumentParser(description="ncbipy-eutils esearch examples from \
                  https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch")
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
    {'db':'nucleotide','term':'viruses[orgn]', 'rettype':'count'},
    #{'db':'nucleotide','term':'viruses[orgn]'},
    #{'db':'nucleotide','term':'viruses[orgn]', 'limit': 100, 'retmax' : 98},
    #{'db':'pubmed','term':'cancer','reldate':60,'datetype':'edat','retmax':100,'usehistory':True},
    #{'db':'pubmed','term':'PNAS[ta] AND 97[vi]', 'retstart':6, 'retmax': 6},
    #{'db':'nlmcatalog','term':'obstetrics AND ncbijournals[filter]', 'retmax':20},
    #{'db':'pmc','term':'stem cells AND free fulltext[filter]'},
    #{'db':'nucleotide','term':'biomol trna', 'field':'prop'},
    #{'db':'protein','term':'70000:90000[molecular weight]', 'retmax':20}
    ]

  for i in range(len(examples)):
    start = time.time()
    print("## Query {}\nParameter:{}".format(i, examples[i]))
    a = entrezpy.esearch.esearch_analyzer.EsearchAnalyzer()
    es = entrezpy.esearch.esearcher.Esearcher('esearcher', args.email, args.apikey)
    es.inquire(examples[i], analyzer=a)
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
          dupl = 0
          for k in uniq:
            if uniq[k] > 0:
              dupl += 1
              print(k)
          print(dupl)
    print("Duration: {} sec\n--------------------------".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
