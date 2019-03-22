#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys
import time
import json
import subprocess
import argparse
import xml.etree.ElementTree

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import entrezpy.esearch.esearcher
import entrezpy.esearch.esearch_analyzer

class Test:

  edirect_param_map = {'term' : '-query',
                       'db' : '-db',
                       'sort' : '-sort',
                       'field' : '-field',
                       'reldate' : '-days',
                       'datetype' : '-datetype',
                       'mindate' : '-mindate',
                       'maxdate' : '-maxdate',
                       'retstart' :'-start',
                       'retmax' : '-stop'}

  def __init__(self, edirect_cmd, entrepy_func, email, apikey=None, apikey_var=None, threads=None):
    self.edirect_cmd = edirect_cmd
    self.tool = 'entrezpyTester' + entrepy_func
    self.email = email
    self.apikey = apikey
    self.apikey_var = apikey_var
    self.threads = threads

  def run_edirect(self, params):
    cmd = [self.edirect_cmd]
    for i in params:
      if i in Test.edirect_param_map:
        cmd.append(Test.edirect_param_map[i])
        cmd.append(str(params[i]))
    print(cmd)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    if proc.returncode != 0:
      print("Edirect run failed")
      return None
    return proc.stdout

  def run_entrezpy(self, params):
    # run entrespy
    # return result
    pass

  def parse_edirect_result(self, edresult):
    # return struct with expected attributes
    pass

  def compare_results(self, edresult, result):
    # actual test in comparing edirect to entrezpy
    # set self.isSuccess
    pass

  def show_comparison_result(self, edresult, result):
    # print stuff to stdout
    pass

  def test(self, params):
    edresult = self.run_edirect(params)
    result = self.run_entrezpy(params)
    if not edresult:
      return False
    if not result:
      return False
    return self.compare_results(self.parse_edirect_result(edresult), result)

class EsearchTest(Test):

  class EntrezpyResult:

    def __init__(self, uids, count, dump):
      self.uids = uids
      if uids:
        self.uids = sorted(uids)
      self.count = count
      self.result = dump

  class EdirectResult:

    def __init__(self, uids, count, result):
      if uids:
        self.uids = sorted(uids)
      self.uids = uids
      self.count = count
      self.result = result

  def __init__(self, esearch_bin, email, apikey=None, apikey_var=None, threads=None):
    super().__init__(esearch_bin, 'esearch', email, apikey=None, apikey_var=None, threads=None)


  def run_entrezpy(self, param):
    es = entrezpy.esearch.esearcher.Esearcher(self.tool, self.email, self.apikey,
                                              self.apikey_var, self.threads)
    a = es.inquire(param, entrezpy.esearch.esearch_analyzer.EsearchAnalyzer())
    if a:
      return EsearchTest.EntrezpyResult(a.get_result().uids, a.get_result().count, a.get_result().dump())
    return None

  def parse_edirect_result(self, edresult):
    res = io.StringIO(edresult)
    count = None
    uids = []
    isId = False
    for event, elem in xml.etree.ElementTree.iterparse(res, events=['start', 'end']):
      if event == 'end':
        if elem.tag == 'Count':
          count = int(elem.text)
        if elem.tag == 'Idlist':
          isId = False

      if event == 'start' and elem.tag == 'Idlist':
        isId = True
      if isId and event == 'end' and elem.tag == 'Id':
        uids.append(elem.text)

    return EsearchTest.EdirectResult(uids, count, res)

  def show_comparison_result(self, edresult, result):
    print("Test {}".format(self.tool))
    print("Count:\nEdirect:\t{}\nEntrezpy:\t{}".format(edresult.count, result.count))
    print("UIDs:\nEdirect:\t{}\nEntrezpy:\t{}".format(edresult.uids, result.uids))
    print(edresult.result.getvalue())
    print(result.result)

  def compare_results(self, edresult, result):
    if edresult.count != result.count:
      print("Bad result. Different count")
      self.show_comparison_result(edresult, result)
      return False
    if edresult.uids and result.uids:
      for i in range(len(edresult.uids)):
        if edresult.uids[i] != result.uids[i]:
          print("Bad result. Different UIDs")
          self.show_comparison_result(edresult, result)
          return False
    self.show_comparison_result(edresult, result)
    return True

def main():
  ap = argparse.ArgumentParser(description="Esearch test")
  ap.add_argument('--email',
                  type=str,
                  required=True,
                  help='email required by NCBI')
  ap.add_argument('--apikey',
                  type=str,
                  default=None,
                  help='NCBI apikey (optional)')

  args = ap.parse_args()
  examples = [
    #{'db':'nucleotide','term':'viruses[orgn]', 'rettype':'count'},
    #{'db':'nucleotide','term':'viruses[orgn]', 'retmax': 1, 'rettype':'uilist'},
    {'db':'nucleotide','term':'viruses[orgn]', 'retmax': 110000,},
    #{'db':'nucleotide','term':'viruses[orgn]', 'limit': 100, 'retmax' : 99, 'idtype' : 'acc'},
    #{'db':'pubmed','term':'cancer','reldate':60,'datetype':'edat','retmax':89, 'limit': 120, 'usehistory':True},
    #{'db':'pubmed','term':'PNAS[ta] AND 97[vi]', 'retstart':6, 'retmax': 6},
    #{'db':'nlmcatalog','term':'obstetrics AND ncbijournals[filter]', 'retmax':20},
    #{'db':'pmc','term':'stem cells AND free fulltext[filter]'},
    #{'db':'nucleotide','term':'biomol trna', 'field':'prop', 'mindate': 1982, 'maxdate':2017}, # Empty result
    #{'db':'nucleotide','term':'biomol trna', 'field':'prop', 'sort' : 'Date Released', 'mindate': 2018, 'maxdate':2019, 'datetype' : 'pdat'},
    #{'db':'protein','term':'70000:90000[molecular weight]', 'retmax':20}
    ]

  et = EsearchTest('esearch', args.email)
  res = et.test(examples[0])
  #def check_uid_uniqeness(result):
    #uniq = {}
    #dupl_count = {}
    #for i in result.uids:
      #if i not in uniq:
        #uniq[i] = 0
      #uniq[i] += 1
      #if uniq[i] > 1:
        #dupl_count[i] = uniq[i]
    #if len(uniq) !=  result.size():
      #print("!: ERROR: Found  {} duplicate uids. Not expected. Duplicated UIDs:".format(len(dupl_count)))
      #for i in dupl_count:
        #print("{}\t{}".format(i, dupl_count[i]))
      #return False
    #return True

  #start = time.time()
  #for i in range(len(examples)):
    #qrystart = time.time()
    #es = entrezpy.esearch.esearcher.Esearcher('esearcher', args.email, args.apikey)
    #a = es.inquire(examples[i], entrezpy.esearch.esearch_analyzer.EsearchAnalyzer())
    #print("+Query {}\n+++\tParameters: {}\n+++\tStatus:".format(i, examples[i]), end='')
    #if not a.isSuccess():
      #print("\tFailed: Response errors")
      #return 0
    #print("\tResponse OK")
    #if a.isEmpty():
      #print("+++\tWARNING: No results for example {}".format(i))
    #print("+++\tStart dumping results\n+++%%%\t{}".format(json.dumps(a.get_result().dump())))
    #if check_uid_uniqeness(a.get_result()):
      #print("+++\tFetched all request UIDs ({}):\n\t{}".format(len(a.get_result().uids),
                                                          #','.join(str(x) for x in a.get_result().uids)))
      #print("+++\tFollow-up parameters:\n+++\t\t{}".format(a.follow_up()))
    #print("+++\tEnd  Results")
    #print("+++\tQuery time: {} sec".format(time.time()-qrystart))
  #print("+Total time: {} sec".format(time.time()-start))
  #return 0

if __name__ == '__main__':
  main()
