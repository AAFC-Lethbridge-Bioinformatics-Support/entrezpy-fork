#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description Demonstrate Entrezpy's efetch functionality and use as library.
#   The examples are stored as parameters in the list `examples` (see [0]).
#               Outline to use efetch as library:
                  0. Create an instance of an Efetch analyzer. See below for
                     more detail.
                  1. Create an instance of Efetcher() with the minimum required
                     parameters: The name of the instance and user email. The
                     former corresponds to the Eutils tool parameter [1].
  References:
    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requiremen
    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
#-------------------------------------------------------------------------------

#def __init__(self, tool, email, apikey=None, threads=0, id=None):
# Standard Python libraries
import os
import sys
import time
import argparse

""" Setup Entrezpy
Set the proper import path to the required classes relative to this file by
updating sys.payth.
$reporoot
|-- examples
|   |-- entrezpy.efetch-examples.py
`-- src
    `-- entrezpy
"""
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.efetch.efetcher
import entrezpy.efetch.efetch_analyzer

def main():
  # Python argument parser. See [2]
  ap = argparse.ArgumentParser(description="ncbipy-epost examples from \
                https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch")
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI')
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')

  args = ap.parse_args()

  # Prepare list of examples. Each example is a parameter dictionary as expected
  # by efetch
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
      # Instantiate an Efetch analyzer to pass into the fetch request to analyse
      # the results.
      a = entrezpy.efetch.efetch_analyzer.EfetchAnalyzer()
      ef = entrezpy.efetch.efetcher.Efetcher('efetcher', args.email, args.apikey)
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
