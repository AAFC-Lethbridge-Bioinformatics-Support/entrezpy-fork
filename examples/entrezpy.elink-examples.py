#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json
import time
import argparse

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
    substart = time.time()
    ef = entrezpy.elink.elinker.Elinker('elinker', args.email, args.apikey)
    a = ef.inquire(examples[i], entrezpy.elink.elink_analyzer.ElinkAnalyzer())
    print("+Query {}\n\tParameters: {}\n\tStatus:".format(i, examples[i]), end='')
    if not a.isSuccess():
      print("\tFailed:\n\t\tError: {}".format(a.error))
      return 0
    print("\tSuccess")
    if a.result.isEmpty():
      print("+No results for example {}".format(i))
    else:
      print("\t+++Start dumping results+++\n%%%\t{}".format(json.dumps(a.result.dump())))
      print("\t+++End  Results+++")
      print("\tFollow-up parameters:")
      if not a.result.get_link_parameter():
        print("\t\tNo follow-up parameters")
      else:
        print("\t\t{}".format(a.result.get_link_parameter()))
    print("+Time query: {} sec".format(time.time()-substart))
  print("+Time total: {} sec".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
