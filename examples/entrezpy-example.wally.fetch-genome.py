#!/usr/bin/env python3
"""
.. module:: entrezpy-example.wally.fetch-genomes
  :synopsis:
    Example of using entrezpy's Wally to fetch genomes

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate Entrezpy's Wally class and setup. Wally facilitates the
  creation of E-Utility query pipelines [0].

  The examples are stored as parameters in the list `examples` (taken from [0]).
  Outline
  -------
  0. Import entrezpy
  1. Create a Wally instance  with the required parameters:
      - instance name
      - user email.
      These are required by NCBI [1]. The instance name corresponds to the
      Eutils `tool` parameter [1].
  2. Get a new Wally pipeline to fetch genome information
  3. Add queries to the pipline
  4. Run the pipeline
  5. Adjust the Efetch analyzer to write genome FASTA files with metadata
  6. Create a new pipeline to fetch genome sequences using the adjusted Efetch
     analyzer.

  Setup
  -----
  Set the proper import path to the required classes relative to this file by
  updating ``sys.payth``. The example assumes you cloned the git repository from
  https://gitlab.com/ncbipy/entrezpy.git.

::
  $reporoot
  |-- examples
  |   `-- entrezpy-examples.wally.fetch-summaries.py  <-You are here
  `-- src
      `-- entrezpy
          `-- efetch
              |-- efetch_analyzer.py
              `-- efetch.py

  N.B.
    NCBI api key[1]: If an apikey is passed to Efetcher(), it will be used to
                    allow more requests [1]. Without apikey, Entrezpy checks if
                    the environmental variable $NCBI_API_KEY is set. If not,
                    less queries per second are performed.

    Efetch analyzer:  Efecth is unique in respect to all other functions as its
                      function `inquire` requires an analyzer as parameter. This
                      example uses the default analyzer which prints either the
                      errors or stores the result as string to
                      `analyzer.result`. It can be easly adapted for more
                      complex tasks (see documentation).
  References:
    [0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch
    [1]: https://www.ncbi.nlm.nih.gov/books/NBK25497/#chapter2.Usage_Guidelines_and_Requirement
    [2]: https://docs.python.org/3/library/argparse.html#module-argparse
"""

import os
import sys
import json
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.efetch.efetch_analyzer
import entrezpy.wally

class GenomeAssembler(entrezpy.efetch.efetch_analyzer.EfetchAnalyzer):

  def __init__(self, metadata=None):
    super().__init__()
    self.species = metadata['speciesname'].replace(' ', '_')
    self.assembly = metadata['assemblyaccession']
    self.taxid = metadata['taxid']

  def analyze_result(self, response, request):
    fh = open("{}-{}-{}.{}".format(self.species, self.taxid, self.assembly, request.rettype), 'w')
    fh.write(response.getvalue())
    fh.close()

def main():
  ap = argparse.ArgumentParser(description='Callimachus extended example for EDirect \
        example https://github.com/NCBI-Hackathons/EDirectCookbook#genomic-sequence-fastas-from-refseq-assembly-for-specified-taxonomic-designation')
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI'),
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')
  ap.add_argument('--apikey_envar',
                  type=str,
                  default=None,
                  help='Environment varriable storing NCBI apikey (optional)')
  ap.add_argument('--threads',
                  type=int,
                  default=0,
                  help='number of threads to use (default=no threads)')
  ap.add_argument('--use_history',
                  default=False,
                  action='store_true',
                  help='Run example using NCBI history server for linking')

  args = ap.parse_args()

  w = entrezpy.wally.Wally(args.email, args.apikey, args.apikey_envar, threads=args.threads)
  find_genomes = w.new_pipeline()
  search_pid = find_genomes.add_search({'db' : 'assembly', 'term' : 'Leptospira alstonii[ORGN] AND latest[SB]'})
  summary_pid = find_genomes.add_summary(dependency=search_pid)
  link_id = find_genomes.add_link({'db':'nuccore','linkname': 'assembly_nuccore_refseq', 'WebEnv':None}, dependency=search_pid)
  link_analyzer = w.run(find_genomes)
  fetch_params = {'retmode':'text', 'rettype':'fasta'}
  for i in link_analyzer.get_result().linksets:
    print("Fetching sequences")
    print(i.get_link_uids())
    for db, uids in i.get_link_uids().items():
      print("asasasassas", db, uids)
      fetch_params.update({'db' : db, 'id' :uids})
    print(fetch_params)
    cat_genomes = w.new_pipeline()
    a = GenomeAssembler(metadata=w.get_result(summary_pid).summaries[i.uid])
    cat_genomes.add_fetch(fetch_params, analyzer=a)
    w.run(cat_genomes)
  return 0

if __name__ == '__main__':
  main()
