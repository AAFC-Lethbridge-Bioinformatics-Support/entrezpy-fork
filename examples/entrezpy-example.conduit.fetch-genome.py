#!/usr/bin/env python3
"""
.. module:: entrezpy-example.conduit.fetch-genomes
  :synopsis:
    Example of using entrezpy's Conduit to fetch genomes

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>

..
  Copyright 2018 The University of Sydney

  Demonstrate Entrezpy's Conduit class and setup. Conduit facilitates the
  creation of E-Utility query pipelines [0].

  The examples are stored as parameters in the list `examples` (taken from [0]).
  Outline
  -------
  0. Import entrezpy
  1. Create a Conduit instance  with the required parameters:
      - instance name
      - user email.
      These are required by NCBI [1]. The instance name corresponds to the
      Eutils `tool` parameter [1].
  2. Get a new Conduit pipeline to fetch genome information
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
  |   `-- entrezpy-examples.conduit.fetch-summaries.py  <-You are here
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
# Import efetch_analyzer module to inherit default EfetchAnalyzer
import entrezpy.efetch.efetch_analyzer
# Import conduit module
import entrezpy.conduit

class GenomeAssembler(entrezpy.efetch.efetch_analyzer.EfetchAnalyzer):
  """Derive a simple but specialized analyzer from the  default EfetchAnalyzer.
  This allows us reuse the error handling but implement specific handling of
  the incoming data. To implement specific error handling, the analyzer should
  be derived from entrezpy.base.analyzer.EutilsAnalyzer. This example shows
  only a quick and dirty approach."""

  def __init__(self, metadata=None):
    """Init a GenomeAssenbler with NCBI summary data. In case we need to fetch
    multiple requests, e.g. WGS shotgun sequences, set a file handler as
    attribute."""
    super().__init__()
    self.species = metadata['speciesname'].replace(' ', '_')
    self.assembly = metadata['assemblyaccession']
    self.taxid = metadata['taxid']
    self.fh = None
    self.fname = None

  def analyze_result(self, response, request):
    """Set file handler and filename if it's the first query request. Otherwise
    append. """
    if not self.fh:
      self.fname = "{}-{}-{}.{}".format(self.species, self.taxid, self.assembly, request.rettype)
      self.fh = open(self.fname, 'w')
    else:
      self.fh = open(self.fname, 'a')
    self.fh.write(response.getvalue())
    self.fh.close()

  def isEmpty(self):
    """Since the analyzer is not using a entrezpy.base.result.EutilsResult to
    store results, we have to overwrite the method to report empty results."""
    if self.fh:
      return False
    return True

def main():
  ap = argparse.ArgumentParser(description='Conduit example to fetch and store genomes \
        from https://github.com/NCBI-Hackathons/EDirectCookbook#genomic-sequence-fastas-from-refseq-assembly-for-specified-taxonomic-designation')
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

  # Init a Conduit instance
  w = entrezpy.conduit.Conduit(args.email, args.apikey, args.apikey_envar, threads=args.threads)
  # Create new Conduit pipeline
  find_genomes = w.new_pipeline()
  # Add a search query to the pipeline
  search_pid = find_genomes.add_search({'db' : 'assembly', 'term' : 'Leptospira alstonii[ORGN] AND latest[SB]'})
  # Add a summary query to the pipeline based on the search results
  summary_pid = find_genomes.add_summary(dependency=search_pid)
  # Add a link query to the pipeline based on the search results. Force UIDs
  # by unsetting Webenv
  link_id = find_genomes.add_link({'db':'nuccore','linkname': 'assembly_nuccore_refseq', 'WebEnv':None}, dependency=search_pid)
  # Run find_genomes pipeline
  link_analyzer = w.run(find_genomes)
  # Set fetch parameter for the sequences to fetch
  fetch_params = {'retmode':'text', 'rettype':'fasta'}
  # Loop through the source UIDs of the link results
  for i in link_analyzer.get_result().linksets:
    print("Fetching sequences")
    # Get the database and UIDs for the genome sequences from the linked UIDs.
    # Summaries are stored as dictionaries {UID : Summary}, so we need to
    # flatten the structure
    for db, uids in i.get_link_uids().items():
      fetch_params.update({'db' : db, 'id' :uids})
    # Create new pipeline to fetch genomes
    cat_genomes = w.new_pipeline()
    # Init adjusted analyzer with the summaries from the previous pipeline as
    # metadata
    a = GenomeAssembler(metadata=w.get_result(summary_pid).summaries[i.uid])
    # Add fetch step to new pipeline
    cat_genomes.add_fetch(fetch_params, analyzer=a)
    # Run new pipeline
    w.run(cat_genomes)
  return 0

if __name__ == '__main__':
  main()
