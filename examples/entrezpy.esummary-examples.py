#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost
# parameters to force error messages:
#   {'db' : 'pubmed','id' : ['PRJNA356464']}
#   {'db' : 'unists','id' : [254085]}
#-------------------------------------------------------------------------------

import os
import sys
import time
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import esummary.esummarizer
import esummary.esummary_analyzer

def main():
  ap = argparse.ArgumentParser(description="ncbipy-epost examples from \
                https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESummary")
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
              {'db' : 'pubmed','id' : [11850928,11482001]},
              {'db' : 'protein','id' : [28800982,28628843]},
              {'db' : 'nucleotide','id' : [28864546,28800981]},
              {'db' : 'structure','id' : [19923,12120]},
              {'db' : 'taxonomy','id' : [9913,30521]}
             ]

  for i in range(len(examples)):
    start = time.time()
    print("## Query {}\nParameter:{}".format(i, examples[i]))
    a = esummary.esummary_analyzer.EsummaryAnalzyer()
    esum = esummary.esummarizer.Esummarizer('eposter', args.email, args.apikey)
    esum.inquire(examples[i], analyzer=a)
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
