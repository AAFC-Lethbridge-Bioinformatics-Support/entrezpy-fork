#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description https://github.com/NCBI-Hackathons/EDirectCookbook#get-all-sra-runs-for-a-given-bioproject
#-------------------------------------------------------------------------------

import os
import sys
import json
import time
import argparse

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import wally.wally

def main():
  ap = argparse.ArgumentParser(description='Simple ncbipy-esearch-example')
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI'),
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')
  ap.add_argument('--threads',
                  type=int,
                  default=0,
                  help='number of threads to use (default=1)')
  ap.add_argument('--use_history',
                  default=False,
                  action='store_true',
                  help='Run example using NCBI history server for linking')

  args = ap.parse_args()

  start = time.time()
  w = wally.wally.Wally(args.email, args.apikey, threads=args.threads)
  px = w.new_pipeline()
  pid = px.add_search({'db' : 'gene', 'term' : 'tp53[preferred symbol] AND human[organism]', 'retmode':'count'})
  if args.use_history:
    pid = px.add_link({'db' : 'protein', 'cmd':'neighbor_history'}, dependency=pid)
    pid = px.add_search(dependency=pid)
  else:
    pid = px.add_link({'db' : 'protein'}, dependency=pid)
  pid = px.add_summary(dependency=pid)
  analyzer = w.run(px)
  for i in analyzer.result.summaries:
    print("{}\t{}".format(analyzer.result.summaries[i].get('caption'),
                          analyzer.result.summaries[i].get('sourcedb')))
  print("Threads: {}\tSummaries: {}\nDurations: {} [s]".format(w.threads,
                                                len(analyzer.result.summaries),
                                                 time.time()-start))
  return 0

if __name__ == '__main__':
  main()
