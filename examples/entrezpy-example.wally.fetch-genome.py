#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description https://github.com/NCBI-Hackathons/EDirectCookbook#genomic-sequence-fastas-from-refseq-assembly-for-specified-taxonomic-designation
#-------------------------------------------------------------------------------

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

def assembly_status_screener(summary_result):
  filtr = {'assemblystatus':'Complete Genome'}
  complete_genome_uids = []
  for i in summary_result.summaries:
    keep = True
    for j in filtr:
      if summary_result.summaries[i][j] != filtr[j]:
        keep = False
    if keep:
      print(summary_result.summaries[i]['uid'])
      complete_genome_uids.append(i)
  return complete_genome_uids

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
  link_id = find_genomes.add_link({'db':'nuccore','linkname': 'assembly_nuccore_refseq'}, dependency=search_pid)
  link_analyzer = w.run(find_genomes)
  for i in link_analyzer.get_result().linksets:
    print("Fetching sequences")
    for j in i.linkunits:
      print("\t", j.uid)
      #pxn = w.new_pipeline()
      #a = GenomeAssembler(metadata=w.get_result(summary_pid).summaries[j])
      #pxn.add_fetch({'db':i.dbto, 'retmode':'text', 'rettype':'fasta', 'id':i.links[j]}, analyzer=a)
      #w.run(pxn)
  return 0

if __name__ == '__main__':
  main()
