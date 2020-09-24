"""
..
  Copyright 2018, 2019 The University of Sydney
  This file is part of entrezpy.

  Entrezpy is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option) any
  later version.

  Entrezpy is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with entrezpy.  If not, see <https://www.gnu.org/licenses/>.

.. module:: entrezpy.elinker.elink_analyzer
   :synopsis: Exports the ElinkeAnalzyer class to analyze Elink query results.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import json
import xml.etree.ElementTree


import entrezpy.base.analyzer
import entrezpy.elink.elink_result
import entrezpy.elink.linkset.base
import entrezpy.elink.linkset.linked
import entrezpy.elink.linkset.relaxed
import entrezpy.elink.linkset.unit.linkin
import entrezpy.elink.linkset.unit.linklist
import entrezpy.elink.linkset.unit.linkout
import entrezpy.elink.linkset.unit.linkoutallattribute
import entrezpy.elink.linkset.unit.linkoutnonlibattribute
import entrezpy.elink.linkset.unit.linkoutprovider
import entrezpy.elink.linkset.unit.neighbor
import entrezpy.elink.linkset.unit.neighborhistory
import entrezpy.elink.linkset.unit.neighborscore
import entrezpy.log.logger


class ElinkAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """
  ElinkAnalyzer implements parsing and superficial analysis of responses from
  ELink queries. ElinkAnalyzer implements the virtual methods
  :meth:`.analyze_result` and :meth:`.analyze_error`. The variety in possible
  Elink response formats results in several specialized parser. Default is to
  obtain results in JSON.

  ElinkAnalyzer instances create :class:`linked.Linkset` or
  :class:`relaxed.Linkset` instances, depending on the request Elink result.
  :func:`entrezpy.elink.linkset.bare.Linkset.new_unit` is called to set the
  type of LinkSet unit based ont he used Elink command.

  .. warning:: Expect for 'llinkslib', all responses are expected in JSON.
                 ElinkAnalyzer will abort if a response from another command is
                 not in JSON.
  """

  def __init__(self):
    """:ivar result: :class:`entrezpy.elink.elink_result.ElinkResult`"""
    super().__init__()
    self.logger = entrezpy.log.logger.get_class_logger(ElinkAnalyzer)
    self.isLinkList = False

  def init_result(self, response, request):
    """Inits :class:`entrezpy.elink.elink_result.ElinkResult`"""
    if not self.result:
      self.result = entrezpy.elink.elink_result.ElinkResult(request.query_id, request.cmd)

  def analyze_error(self, response, request):
    """Implements virtual function :func:`entrezpy.base.analyzer.analyze_error`."""
    self.logger.debug(json.dumps({'response':response, 'request-dump':request.dump_internals()}))

  def get_linkset_unit(self, elink_cmd):
    if elink_cmd == 'neighbor':
      return entrezpy.elink.linkset.unit.neighbor.Neighbor()
    if elink_cmd == 'neighbor_score':
      return entrezpy.elink.linkset.unit.neighborscore.NeighborScore()
    if elink_cmd == 'neighbor_history':
      return entrezpy.elink.linkset.unit.neighborhistory.NeighborHistory()

    self.isLinkList = True
    if elink_cmd == 'acheck':
      return entrezpy.elink.linkset.unit.linklist.LinkList()
    if elink_cmd == 'ncheck':
      return entrezpy.elink.linkset.unit.linkin.LinkIn()
    if elink_cmd == 'lcheck':
      return entrezpy.elink.linkset.unit.linkout.LinkOut()
    if elink_cmd == 'llinks':
      return entrezpy.elink.linkset.unit.linkoutnonlibattribute.LinkOutNonlibAttributes()
    if elink_cmd == 'llinkslib':
      return entrezpy.elink.linkset.unit.linkoutallattribute.LinkOutAllAttribute()
    if elink_cmd == 'prlinks':
      return entrezpy.elink.linkset.unit.linkoutprovider.LinkOutProvider()

  def analyze_result(self, response, request):
    """
    Implements virtual method :meth:`entrezpy.base.analyzer.analyze_result` and
    checks used elink command to run according result parser.
    """
    self.init_result(response, request)
    if request.cmd != 'llinkslib' and request.retmode != 'json':
      sys.exit(self.logger.error(json.dumps({'unknown cmd':request.cmd,
                                             'format':request.retmode,
                                             'action':abort})))
    if request.retmode == 'json':
      self.logger.debug(json.dumps({'response':response}))
    else:
      self.logger.debug(json.dumps({'response':response.getvalue()}))

    lset_unit = self.get_linkset_unit(request.cmd)
    if request.cmd == 'llinkslib':  # only available as XML, groan
      self.parse_llinkslib(response, lset_unit)
    elif not self.isLinkList:
      self.analyze_links(response['linksets'], lset_unit)
    elif self.isLinkList:
      self.analyze_linklist(response['linksets'], lset_unit)
    else:
      sys.exit(self.logger.error(json.dumps({'unknown elink cmd':request.cmd,
                                             'action':'abort'})))

  def analyze_linklist(self, linksets, lset_unit):
    """
    Parses ELink responses listing link information for UIDs.

    :param dict linksets: 'linkset' part in an ELink JSON response from NCBI.
    :param lset_unit: Elink LinkSet unit instance
    """
    for i in linksets:
      if 'idurllist' in i:
        for j in i.get('idurllist'):
          lset = entrezpy.elink.linkset.linked.LinkedLinkset(j['id'], i['dbfrom'], canLink=False)
          self.logger.debug(json.dumps({'created':lset.dump()}))
          for k in j['objurls']:
            lset.add_linkunit(lset_unit.new(k))
            self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
          self.result.add_linkset(lset)
      elif 'idlinksets' in i['idchecklist']:
        for j in i['idchecklist'].get('idlinksets'):
          lset = entrezpy.elink.linkset.linked.LinkedLinkset(j['id'], i['dbfrom'], canLink=False)
          self.logger.debug(json.dumps({'created':lset.dump()}))
          for k in j['linkinfos']:
            lset.add_linkunit(lset_unit.new(k['dbto'], k['linkname'], k.get('menutag'),
                                            k.get('htmltag'), k.get('priority')))
            self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
          self.result.add_linkset(lset)
      elif 'ids' in i['idchecklist']:
        for j in i['idchecklist'].get('ids'):
          lset = entrezpy.elink.linkset.linked.LinkedLinkset(j['value'], i['dbfrom'], canLink=False)
          self.logger.debug(json.dumps({'created':lset.dump()}))
          if 'hasneighbor' in j:
            lset.add_linkunit(lset_unit.new(i['dbfrom'], j['hasneighbor']))
            self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
          if 'haslinkout' in j:
            lset.add_linkunit(lset_unit.new(i['dbfrom'], j['haslinkout']))
            self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
          self.result.add_linkset(lset)

  def analyze_links(self, linksets, lset_unit):
    """
    Parses ELink responses with links  as UIDs or History server references.

    :param dict linksets: 'linkset' part in an ELink JSON response from NCBI.
    :param lset_unit: Elink LinkSet unit instance
    """
    for i in linksets:
      #assume 1-to-many link as default
      lset = entrezpy.elink.linkset.linked.LinkedLinkset(i['ids'][0], i['dbfrom'])
      if len(i['ids']) > 1: # OK, it's many-to-many
        lset = entrezpy.elink.linkset.relaxed.RelaxedLinkset(i['ids'], i['dbfrom'])
      self.logger.debug(json.dumps({'created':lset.dump()}))
      if 'linksetdbs' in i:
        for j in i['linksetdbs']:
          if 'ERROR' in j:
            self.logger.error(json.dumps({'response':j['ERROR']}))
            self.hasErrorResponse = True
          if 'links' in j:
            for k in j['links']:
              lset.add_linkunit(lset_unit.new(k, j['dbto'], j['linkname']))
              self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
      elif 'linksetdbhistories' in i:
        for j in i['linksetdbhistories']:
          lset.add_linkunit(lset_unit.new(j['dbto'], j['linkname'], i['webenv'], j['querykey']))
          self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
      else:
        self.logger.warning(json.dumps({'Empty linkset'}))
        continue
      self.result.add_linkset(lset)

  def parse_llinkslib(self, response, lset_unit, lset=None):
    """
    Exclusive XML parser for 'llinkslib' responses. Its approach is ugly but
    parses the XML. The cmd parametes is always 'llinkslib' but retains the
    calling signature.

    :param io.StringIO response: XML response from Entrez
    :param lset_unit: Elink LinkSet unit instance
    """
    provider_tagmap = {'iconurl', 'id', 'url', 'name', 'nameabbr'}
    unit_tagmap = {'iconurl', 'url', 'name', 'nameabbr', 'attribute',
                   'category', 'linkname', 'subjecttype'}
    unit = {'attributes' : [], 'provider' : {}}
    dbfrom = None
    isLinkset = False
    isObjurl = False
    isProvider = False
    for event, elem in xml.etree.ElementTree.iterparse(response, events=['start','end']):
      if event == 'start':
        if elem.tag == 'LinkSet':
          isLinkset = True
        if elem.tag == 'ObjUrl':
          isObjurl = True
          unit = {'attributes':[], 'provider':{}}

      if event == 'end':
        if elem.tag == 'LinkSet':
          isLinkset = False
        if elem.tag == 'ObjUrl':
          isObjurl = False
          lset.add_linkunit(lset_unit.new(unit))
          self.logger.debug(json.dumps({'added':lset.linkunits[-1].dump()}))
        if elem.tag == 'IdUrlSet':
          self.result.add_linkset(lset)

      if isLinkset and not isObjurl:
        if event == 'end' and elem.tag == 'DbFrom':
          dbfrom = elem.text
        if elem.tag == 'Id' and not isObjurl:
          lset = entrezpy.elink.linkset.linked.LinkedLinkset(int(elem.text), dbfrom, canLink=False)
          self.logger.debug(json.dumps({'created':lset.dump()}))

      if isLinkset and isObjurl:
        if elem.tag == 'Provider':
          isProvider = bool(event == 'start')

        if event == 'end' and elem.tag.lower() in unit_tagmap:
          if elem.tag.lower() == 'attribute':
            unit['attributes'].append(elem.text)
          elif isProvider and elem.tag.lower() in provider_tagmap:
            unit['provider'][elem.tag.lower()] = elem.text
          else:
            unit[elem.tag.lower()] = elem.text
          elem.clear()
