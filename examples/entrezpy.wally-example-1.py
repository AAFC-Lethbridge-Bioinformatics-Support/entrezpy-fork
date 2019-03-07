#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description https://github.com/NCBI-Hackathons/EDirectCookbook#genomic-sequence-fastas-from-refseq-assembly-for-specified-taxonomic-designation
#-------------------------------------------------------------------------------

import os
import sys
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import efetch.efetch_analyzer
import wally.wally

class GenomeAssembler(efetch.efetch_analyzer.EfetchAnalyzer):

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
  args = ap.parse_args()

  search_p = {'db' : 'assembly', 'term' : 'Leptospira alstonii[ORGN] AND latest[SB]'}
  link_p = {'db':'nuccore', 'linkname': 'assembly_nuccore_refseq', 'query_key':None}
  w = wally.wally.Wally(args.email, args.apikey)
  px =w.new_pipeline()
  search_pid = px.add_search(search_p)
  summary_pid = px.add_summary(dependency=search_pid)
  link_pid = px.add_link(link_p, dependency=search_pid)
  w.run(px)
  for i in w.get_result(link_pid).linksets:
    for j in i.links:
      pxn = w.new_pipeline()
      a = GenomeAssembler(metadata=w.get_result(summary_pid).summaries[j])
      pxn.add_fetch({'db':i.dbto, 'retmode':'text', 'rettype':'fasta', 'id':i.links[j]}, analyzer=a)
      w.run(pxn)
  return 0

if __name__ == '__main__':
  main()
