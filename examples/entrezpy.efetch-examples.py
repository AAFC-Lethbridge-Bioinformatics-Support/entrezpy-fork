#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
#-------------------------------------------------------------------------------

import os
import sys
import time
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import efetch.efetcher
import efetch.efetch_analyzer

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
              {'db' : 'pubmed','id' : [17284678,9997], 'retmode':'text', 'rettype': 'abstract'},
              {'db': 'pubmed', 'id': [11748933,11700088], 'retmode':'xml'},
              {'db': 'pmc', 'id': [212403], 'retmode':'json'},
              {'db': 'nuccore', 'id': [21614549], 'strand':1, 'seq_start' : 1, 'seq_stop' : 100, 'rettype':'fasta'},
              {'db': 'nuccore', 'id': [21614549], 'strand':2, 'seq_start' : 1, 'seq_stop' : 100, 'rettype':'fasta'},
              {'db': 'nuccore', 'id': [21614549], 'complexity' : 3},
              {'db': 'nucleotide', 'id': [5]},
              {'db': 'nucleotide', 'id': [5], 'rettype':'fasta'},
              {'db': 'nucleotide', 'id': [5], 'rettype':'gb'},
              {'db': 'popset', 'id': [12829836], 'rettype':'gp'},
              {'db': 'protein', 'id': [8], 'rettype':'gp', 'retmode':'xml'},
              {'db': 'sequences', 'id': [312836839,34577063], 'rettype':'fasta', 'retmode':'xml'},
              {'db': 'gene', 'id': [2], 'retmode':'xml'}
             ]
  for i in range(len(examples)):
    start = time.time()
    for j in ['xml', 'text']:
      examples[i].update({'retmode':j})
      print("## Query {} in {}\nParameter:{}".format(i, j, examples[i]))
      a = efetch.efetch_analyzer.EfetchAnalyzer()
      ef = efetch.efetcher.Efetcher('efetcher', args.email, args.apikey)
      ef.inquire(examples[i], analyzer=a)
      if not a.isSuccess():
        print("Status:\tFailed:\n\tError: {}\n".format(a.error))
      else:
        print("Status:\tSuccess")
        print("######### Start fetched result #########")
        print(a.result)
        print("######### End fetched result #########")
      print("Duration: {} sec\n--------------------------".format(time.time()-start))
  return 0

if __name__ == '__main__':
  main()
