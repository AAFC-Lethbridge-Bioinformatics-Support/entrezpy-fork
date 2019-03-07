#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import time
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import elink.elinker
import elink.elink_analyzer


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
              {'dbfrom':'protein', 'db' : 'gene','id' : [15718680,157427902]},
              {'dbfrom':'pubmed', 'db' : 'pubmed','id' : [15718680, 20210808], 'cmd':'neighbor_score'},
              {'dbfrom':'protein', 'db' : 'gene','id' : [15718680, 157427902], 'cmd':'neighbor_history'},
              {'dbfrom':'protein', 'id' : [15718680, 157427902], 'cmd':'acheck'},
              {'dbfrom':'protein', 'db' : 'pubmed', 'id' : [15718680, 157427902], 'cmd':'acheck'},
              {'dbfrom':'nuccore', 'id' : [21614549,219152114], 'cmd':'ncheck'},
              {'dbfrom':'protein', 'id' : [15718680,157427902], 'cmd':'lcheck'},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'llinks'},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'llinkslib'},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'prlinks',},
              {'dbfrom':'pubmed', 'id' : [19880848,19822630], 'cmd':'prlinks', 'retmode':'ref'},
             ]

  for i in range(len(examples)):
    start = time.time()
    print("## Query {}\nParameter:{}".format(i, examples[i]))
    a = elink.elink_analyzer.ElinkAnalyzer()
    ef = elink.elinker.Elinker('elinker', args.email, args.apikey)
    ef.inquire(examples[i], analyzer=a)
    if not a.isSuccess():
      print("Status:\tFailed:\n\tError: {}\n".format(a.error))
    else:
      print("Status:\tSuccess")
      print("######### Start fetched result #########")
      print(a.result.dump())
      print("######### End fetched result #########")
    print("Duration: {} sec\n--------------------------".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()

#cmd=llinkslib

#https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848,19822630&cmd=prlinks

#Example: Link directly to the full text for a PubMed abstract at the provider's web site.

#https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id=19880848&cmd=prlinks&retmode=ref
