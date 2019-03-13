#!/usr/bin/env python3
"""
.. module:: entrezpy-examples.esearch
  :synopsis:
    Example of using entrezpy's esearch function.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  entrezpy-examples.esearch.py is free software: you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public License as
  published by the Free Software Foundation, either version 3 of the License,
  or (at your option) any later version.

  entrezpy-examples.esearch.py is distributed in the hope that it will be
  useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
  Public License for more details.

  You should have received a copy of the GNU General Public License along with
  entrezpy.esearch-exmaples.py. If not, see <https://www.gnu.org/licenses/>.

  The examples are stored as parameters in the list `examples` (modified  from
  [0]).

  Outline
  -------
  0. Import entrezpy

  1. Create an instance of Esearcher() with the required parameters:
      - instance name
      - user email.
      These are required by NCBI [1]. The instance name corresponds to the
      Eutils `tool` parameter [1].

  3. Loop over the examples and return the UIDs or corresponding WebEnv and
     QueryKey.

  N.B.
  NCBI api key[1]: If an apikey is passed as parameter it will be used to
  allow more requests [1]. Without apikey, Entrezpy checks if the environmental
  variable $NCBI_API_KEY is set. If not, less queries per second are performed.

  Setup
  -----
  Set the proper import path to the required classes relative to this file by
  updating `sys.payth`. The example assumes you cloned the git repository from
  https://gitlab.com/ncbipy/entrezpy.git.

  $reporoot
  |-- examples
  |   `-- entrezpy-examples.esearch.py  <-You are here
  `-- src
      `-- entrezpy
          `-- esearch
              |-- esearch_analyzer.py
              `-- esearcher.py

  References:
    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.Esearch
    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
"""


import os
import sys
import time
import json
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
    {'db':'nucleotide','term':'viruses[orgn]'},
    {'db':'nucleotide','term':'viruses[orgn]', 'retmax': 110000},
    {'db':'nucleotide','term':'viruses[orgn]', 'retmax': 0},
    {'db':'nucleotide','term':'viruses[orgn]', 'reqsize': 100, 'retmax' : 99, 'idtype' : 'acc'},
    {'db':'pubmed','term':'cancer','reldate':60,'datetype':'edat','retmax':89, 'usehistory':True},
    {'db':'pubmed','term':'PNAS[ta] AND 97[vi]', 'retstart':6, 'retmax': 6},
    {'db':'nlmcatalog','term':'obstetrics AND ncbijournals[filter]', 'retmax':20},
    {'db':'pmc','term':'stem cells AND free fulltext[filter]'},
    {'db':'nucleotide','term':'biomol trna', 'field':'prop', 'mindate': 1982, 'maxdate':2017}, # Parameter Fail
    {'db':'nucleotide','term':'biomol trna', 'field':'prop', 'sort' : 'Date Released', 'mindate': 2018, 'maxdate':2019, 'datetype' : 'pdat'},
    {'db':'protein','term':'70000:90000[molecular weight]', 'retmax':20}
    ]

  def check_uid_uniqeness(result):
    uniq = {}
    dupl_count = {}
    for i in result.uids:
      if i not in uniq:
        uniq[i] = 0
      uniq[i] += 1
      if uniq[i] > 1:
        dupl_count[i] = uniq[i]
    if len(uniq) !=  result.size():
      print("!: ERROR: Found  {} duplicate uids. Not expected. Duplicated UIDs:".format(len(dupl_count)))
      for i in dupl_count:
        print("{}\t{}".format(i, dupl_count[i]))
      return False
    return True

  start = time.time()
  for i in range(len(examples)):
    qrystart = time.time()
    es = entrezpy.esearch.esearcher.Esearcher('esearcher', args.email, args.apikey)
    a = es.inquire(examples[i], entrezpy.esearch.esearch_analyzer.EsearchAnalyzer())
    print("+Query {}\n+++\tParameters: {}\n+++\tStatus:".format(i, examples[i]), end='')
    if not a.isSuccess():
      print("\tFailed: Response errors")
      return 0
    print("\tResponse OK")
    if a.isEmpty():
      print("+++\tWARNING: No results for example {}".format(i))
    print("+++\tStart dumping results\n+++%%%\t{}".format(json.dumps(a.get_result().dump())))
    if check_uid_uniqeness(a.get_result()):
      if a.get_result().retmax == a.result.size():
        print("+++\tRequest OK")
      else:
        print("+++\tRequest failed")
      print("+++\tFetched UIDs ({}):\n\t{}".format(a.result.size(), ','.join(str(x) for x in a.get_result().uids)))
      print("+++\tFollow-up parameters:\n+++\t\t{}".format(a.follow_up()))
    print("+++\tEnd  Results\n+++\tQuery time: {} sec".format(time.time()-qrystart))
  print("+Total time: {} sec".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
