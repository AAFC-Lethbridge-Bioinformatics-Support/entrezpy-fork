#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
# \copyright 2018 The University of Sydney
# \description Demonstrate Entrezpy's efetch functionality and setup.
#   Efetcher() fetches the given UIDs or accessions in the requested format and
#   style from the given NCBI Entrez database [0].
#
# The examples are stored as parameters in the list `examples` (taken from [0]).
#   Outline:
#     0. Import entrezpy
#     1. Create an instance of an EfetchAnalyzer.
#     2. Create an instance of Efetcher() with the required parameters:
#         - instance name
#         - user email.
#         These are required by NCBI [1]. The instance name corresponds to the
#         Eutils `tool` parameter [1].
#     3. Loop over the examples and request the results as XML and text by
#        updating the `retmode` parameter[1] on-the-fly.
#     4. Print results as XML and text to STDOUT
#
# N.B.
#   NCBI api key[1]: If an apikey is passed to Efetcher(), it will be used to
#                    allow more requests [1]. Without apikey, Entrezpy checks if
#                    the environmental variable $NCBI_API_KEY is set. If not,
#                    less queries per second are performed.
#
#   Efetch analyzer:  Efecth is unique in respect to all other functions as its
#                     function `inquire` requires an analyzer as parameter. This
#                     example uses the default analyzer which prints either the
#                     errors or stores the result as string to
#                     `analyzer.result`. It can be easly adapted for more
#                     complex tasks (see documentation).
#  References:
#    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
#    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
#    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
#-------------------------------------------------------------------------------

# Standard Python libraries
import os
import sys
import time
import argparse

""" Setup Entrezpy
Set the proper import path to the required classes relative to this file by
updating sys.payth. The example assumes you cloned the repository.
$reporoot
|-- examples
|   `-- entrezpy.efetch-examples.py   <-You are here
`-- src
    `-- entrezpy
        `-- efetch
            |-- efetch_analyzer.py
            `-- efetcher.py
"""
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.efetch.efetcher
import entrezpy.efetch.efetch_analyzer

def main():
  # Python argument parser (see [2] for more details)
  demo_src = 'https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch'
  ap = argparse.ArgumentParser(description="Entrezpy Efetcher() examples ({})".format(demo_src))
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
  # by Efetcher.
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
  # Loop over examples
  for i in range(len(examples)):
    start = time.time()
    # Each example is requested as XML and text.
    for j in ['xml', 'text']:
      print("## Query {} in {}\nParameter:{}".format(i, j, examples[i]))
      # Instantiate the dfeault Efetch analyzer to pass into the request to
      # analyze results. This simple analyzer just prints results to STDOUT
      a = entrezpy.efetch.efetch_analyzer.EfetchAnalyzer()

      # Instantiate an Efetcher with the the required arguments for name and
      # user email and the optional argument apikey (see above).
      ef = entrezpy.efetch.efetcher.Efetcher('efetcher', args.email, args.apikey)

      # Run query using inquire(). Set the retmode parameter for each example
      # on the fly.
      examples[i].update({'retmode':j})
      ef.inquire(examples[i], analyzer=a)

      # Check for successful query. Print duration, error or result to STDOUT.
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
