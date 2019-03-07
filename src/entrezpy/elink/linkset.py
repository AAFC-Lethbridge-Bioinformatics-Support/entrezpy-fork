#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import sys
import json

class LinkedLinkset:

    def __init__(self, dbfrom, dbto, uid, links, linkname):
      if len(uid) > 1:
        sys.exit("Dev:Something went wrong. Don't expect multiple uids when linking one-to-one")
      self.category = 'linked'
      self.dbfrom = dbfrom
      self.dbto = dbto
      self.links = {uid[0] : links}
      self.linknames = {linkname : [uid[0]]}

    def add_links(self, uid, links, linkname):
      if uid[0] not in self.links: # this should never happen, as fas as I understand
        #print("Dev: multiple uids for a 1-to-1 linked linkset. Apparently, I don't understand")
        self.links[uid[0]] = []
      self.links[uid[0]] += links
      if linkname not in self.linknames:
        self.linknames[linkname] = []
      self.linknames[linkname] += uid

    def dump(self):
      return json.dumps({'category': self.category,
                         'dbfrom':self.dbfrom,
                         'dbto':self.dbto,
                         'links':self.links,
                         'linknames':self.linknames})

class LooseLinkset:

    def __init__(self, dbfrom, dbto, uids, links, linkname):
      self.category = 'loose'
      self.dbfrom = dbfrom
      self.dbto = dbto
      self.uids = {x : 0 for x in uids}
      self.links = {x:[linkname] for x in links}

    def add_links(self, uids, links, linkname):
      for i in uids:
        self.uids[i] = 0
      for i in self.links:
        if i not in self.links:
          self.links[i] = []
        self.links[i].append(linkname)

    def dump(self):
      return json.dumps({'category': self.category,
                         'dbfrom':self.dbfrom,
                         'dbto':self.dbto,
                         'links':self.links,
                         'uids':self.uids})

class NeighborScore:

  def __init__(self, dbfrom, dbto, uids, links, linkname):
    self.category = 'score'
    self.dbfrom = dbfrom
    self.dbto = dbto
    self.linkname = linkname
    self.uids = uids
    self.links = {int(x['id']): int(x['score']) for x in links}

  def dump(self):
    return json.dumps({'category': self.category,
                        'dbfrom' : self.dbfrom,
                        'dbto' : self.dbto,
                        'links' : self.links,
                        'uids' : self.uids,
                        'linkname' : self.linkname})

class LinksetHistory:

    class HistoryLink:

      def __init__(self, linkname, querykey):
        self.linkname = linkname
        self.querykey = querykey

    def __init__(self, dbfrom, webenv):
      self.category = 'history'
      self.dbfrom = dbfrom
      self.webenv = webenv
      self.links = {}

    def add_history_link(self, dbto, linkname, querykey):
      if dbto not in self.links:
        self.links[dbto] = []
      self.links[dbto].append(self.HistoryLink(linkname, querykey))

    def dump(self):
      lnks = {}
      for i in self.links:
        lnks[i] = []
        for j in self.links[i]:
          lnks[i].append({'linkname':j.linkname, 'querykey':j.querykey})
      return ({'category' : self.category,
               'dbfrom':self.dbfrom,
               'webenv':self.webenv,
               'links':lnks})

class LinkInfo:

  class LinkInfoDatabase:

    def __init__(self, dbto, linkname, menutag, htmltag, priority):
      self.dbto = dbto
      self.linkname = linkname
      self.menutag= menutag
      self.htmltag = htmltag
      self.priority = priority

    def dump(self):
      return {'dbto': self.dbto, 'linkname':self.linkname,
                        'menutag': self.menutag, 'htmltag':self.htmltag,
                        'priority':self.priority}

  def __init__(self, uid, dbfrom, linkinfos):
    self.category = 'linkinfo'
    self.uid = uid
    self.dbfrom = dbfrom
    self.linkinfos = []
    self.add_linkinfos(linkinfos)

  def add_linkinfos(self, linkinfos):
    for i in linkinfos:
      self.linkinfos.append(self.LinkInfoDatabase(i['dbto'], i['linkname'],
                                                  i.get('menutag'), i.get('htmltag'),
                                                  i.get('priority')))

  def dump(self):
    return json.dumps({'category': self.category,
                       'id' : self.uid,
                       'dbfrom':self.dbfrom,
                       'linkinfos':[x.dump() for x in self.linkinfos]})

class DbLinkCheck:

  def __init__(self, dbfrom, cmd):
    self.linkstyle = 'hasneighbor'
    if cmd == 'lcheck':
      self.linkstyle = 'haslinkout'
    self.dbfrom = dbfrom
    self.ids = {}

  def add_ids(self, ids):
    self.ids.update({x['value'] : x[self.linkstyle] for x in ids})

  def dump(self):
    return json.dumps({'dbfrom' : self.dbfrom, 'ids' : self.ids})

class LinkOutProvider:

  def __init__(self, dbfrom):
    self.dbfrom = dbfrom
    self.urls = {}

  def add_urllist(self, urllist):
    for i in urllist:
      self.urls[i['id']] = i['objurls']

  def dump(self):
    print(len(self.urls))
    return json.dumps({'dbfrom' : self.dbfrom, 'urllist' : self.urls})
