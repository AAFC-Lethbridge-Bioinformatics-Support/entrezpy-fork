#-------------------------------------------------------------------------------
#  \author Jan Piotr Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 USYD
#  \description
#-------------------------------------------------------------------------------

import os
import sys
import json
import logging
import xml.etree.ElementTree

sys.path.insert(1, os.path.join(sys.path[0], '../'))
from entrezpy_base import analyzer
from . import elink_result
from . import linkset

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class ElinkAnalyzer(analyzer.EutilsAnalyzer):

  check_cmds = {'acheck', 'ncheck', 'lcheck', 'llinks', 'prlinks'}

  def __init__(self):
    super().__init__()
    self.result = elink_result.ElinkResult()
    self.dbmap = {}
    self.linkname_map = {}

  def analyze_error(self, response, request):
    print(response)

  def analyze_result(self, response, request):
    logger.debug("{}-response: {}".format(__name__, response))
    self.result.cmd = request.cmd
    if request.cmd == 'neighbor': # uids
      self.analyze_cmd_neighbor(response['linksets'])
    if request.cmd == 'neighbor_history': #history server
      self.analyze_cmd_neighbor_history(response['linksets'])
    if request.cmd == 'neighbor_score': #history server
      self.analyze_cmd_neighbor_score(response['linksets'])
    if request.cmd in ElinkAnalyzer.check_cmds:
      self.analyze_linkinfo(response['linksets'])
    if request.cmd == 'llinkslib':
      self.parse_llinkslib(response)

  def analyze_linkinfo(self, linksets):
    for i in linksets:
      if self.result.cmd == 'acheck':
        for j in i['idchecklist']:
          for k in i['idchecklist']['idlinksets']:
            self.result.linksets.append(linkset.LinkInfo(k['id'], i['dbfrom'], k['linkinfos']))
      if self.result.cmd == 'ncheck' or self.result.cmd == 'lcheck':
        if i['dbfrom'] not in self.dbmap:
          self.result.linksets.append(linkset.DbLinkCheck(i['dbfrom'], self.result.cmd))
          self.dbmap[i['dbfrom']] = len(self.result.linksets) - 1
        self.result.linksets[self.dbmap[i['dbfrom']]].add_ids(i['idchecklist']['ids'])
      if self.result.cmd == 'llinks' or self.result.cmd == 'prlinks':
        if i['dbfrom'] not in self.dbmap:
          self.result.linksets.append(linkset.LinkOutProvider(i['dbfrom']))
          self.dbmap[i['dbfrom']] = self.dbmap[i['dbfrom']] = len(self.result.linksets) - 1
        self.result.linksets[self.dbmap[i['dbfrom']]].add_urllist(i['idurllist'])

  def analyze_cmd_neighbor_score(self, linksets):
    for i in linksets:
      for j in i['linksetdbs']:
        self.result.linksets.append(linkset.NeighborScore(i['dbfrom'], j['dbto'], i['ids'], j['links'],j['linkname']))

  def analyze_cmd_neighbor(self, linksets):
    for i in linksets:
      if i['dbfrom'] not in self.dbmap:
        self.dbmap[i['dbfrom']] = {}
      for j in i['linksetdbs']:
        if j['dbto'] not in self.dbmap[i['dbfrom']]:
          if len(i['ids']) == 1: # 1-to-1 link
            self.result.linksets.append(linkset.LinkedLinkset(i['dbfrom'], j['dbto'], i['ids'], j['links'], j['linkname']))
          if len(i['ids']) > 1: # all vs. all
            self.result.linksets.append(linkset.LooseLinkset(i.get('dbfrom'), j.get('dbto'), i['ids'], j['links'], j['linkname']))
          self.dbmap[i['dbfrom']][j['dbto']] = len(self.result.linksets) - 1
        else:
          self.result.linksets[self.dbmap[i['dbfrom']][j['dbto']]].add_links(i['ids'], j['links'], j['linkname'])

  def analyze_cmd_neighbor_history(self, linksets):
    for i in linksets:
      if i['dbfrom'] not in self.dbmap:
        self.dbmap[i['dbfrom']] = {}
        for j in i['linksetdbhistories']:
          if j['dbto'] not in self.dbmap[i['dbfrom']]:
            self.result.linksets.append(linkset.LinksetHistory(i.get('dbfrom'), i.get('webenv')))
            self.dbmap[i['dbfrom']][j['dbto']] = len(self.result.linksets) - 1
          self.result.linksets[self.dbmap[i['dbfrom']][j['dbto']]].add_history_link(j['dbto'], j['linkname'], j['querykey'])

  def parse_llinkslib(self, linksets):
    current_dbfrom = None
    current_id = None
    objurl = {'attributes' : []}
    collect_url = False
    objurllist = []
    collect_id = False
    provider = {}
    for event, elem in xml.etree.ElementTree.iterparse(linksets, events=['start','end']):
      if elem.tag == 'DbFrom':
        current_dbfrom = elem.text
        if current_dbfrom not in self.dbmap:
          self.result.linksets.append(linkset.LinkOutProvider(elem.text))
          self.dbmap[current_dbfrom] = len(self.result.linksets) - 1
      if elem.tag == 'IdUrlSet':
        if event == 'start':
          collect_id = True
        if event == 'end':
          self.result.linksets[self.dbmap[current_dbfrom]].urls[current_id] = objurllist
          collect_id = False
          objurllist = []
      if collect_id and elem.tag == 'Id':
        current_id = int(elem.text)
        collect_id = False
      if elem.tag == 'ObjUrl':
        if event == 'start':
          collect_url = True
          collect_provider = False
        if event == 'end':
          collect_url = False
          objurl['provider'] = {**provider}
          objurllist.append(objurl)
          objurl = {'attributes' : []}
      if collect_url:
        if elem.tag == 'Provider':
            if event == 'start':
              collect_provider = True
            if event == 'end':
              collect_provider = False
        if event == 'end':
          if elem.tag == 'Attribute':
            objurl['attributes'].append(elem.text)
          elif collect_provider:
            provider[elem.tag.lower()] = elem.text
          else:
            objurl[elem.tag.lower()] = elem.text
