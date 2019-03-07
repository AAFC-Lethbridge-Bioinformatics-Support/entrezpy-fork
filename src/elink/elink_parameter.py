#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys
import math
import json
import logging

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import entrezpy_base.parameter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

## ElinkParameter implements checks and configures an EftechQuery().
# ElinkParameter inherits entrezpy_base.parameter.EutilsParameter.
# A link query knows its size due to the id parameter or earlier result
# stored on the Entrez history server using WebEnv and query_key.
# The default retmode (fetch format) is set to JSON and the default command
# (cmd) to neighbor.
# ELink has no set maximum for the number of UIDs which can be linked. This
# fixes the query_size, request_size and expected_requests to 1
class ElinkParameter(entrezpy_base.parameter.EutilsParameter):

  ## These commands can work without a db parameter
  nodb_cmds = {'acheck', 'ncheck', 'lcheck', 'llinks', 'llinkslib', 'prlinks'}
  retmodes = {'llinkslib' : 'xml'}

  def __init__(self, parameter):
    super().__init__(parameter)
    self.cmd = parameter.get('cmd', 'neighbor')
    self.dbfrom = parameter.get('dbfrom')
    self.uids = parameter.get('id', [])
    self.retmode = ElinkParameter.retmodes.get(self.cmd, parameter.get('retmode', 'json'))
    self.linkname = parameter.get('linkname')
    self.term = parameter.get('term')
    self.holding = parameter.get('holding')
    self.datetype = parameter.get('datetype')
    self.reldate = parameter.get('reldate')
    self.mindate = parameter.get('mindate')
    self.maxdate = parameter.get('maxdate')
    self.query_size = 1
    self.request_size = 1
    self.expected_requests = 1
    if parameter.get('retmode') == 'ref':
      logger.info(json.dumps({__name__:"retmode ref is not used. Check documentation."}))
      parameter['retmode'] = 'json'
    self.retmode = ElinkParameter.retmodes.get(self.cmd, parameter.get('retmode', 'json'))
    self.check()

  ## Implemented check() function
  # Testing for required parameters and aborting if they are missing/wrong
  # When using the history server, elink queries require WebEnv and query_key
  def check(self):
    if self.cmd not in ElinkParameter.nodb_cmds and not self.haveDb():
      logger.error(json.dumps({__name__+": error":{"msg": "Missing parameter", "parameter":
                                                              {"db":self.db,"cmd":self.cmd},
                                                              "action":"abort"}}))
      sys.exit()
    if self.dbfrom == None:
      logger.error(json.dumps({__name__+": error":{"msg": "Missing parameter",
                                                         "parameter": {"dbfrom":self.dbfrom},
                                                          "action":"abort"}}))
      sys.exit()

    if not self.uids and not self.haveWebenv and not self.haveQuerykey:
      logger.error(json.dumps({__name__+": error":{"msg": "Missing required parameters",
                                                          "parameters": {"ids":self.uids,
                                                                         "QueryKey":self.querykey,
                                                                         "WebEnv":self.webenv},
                                                           "action":"abort"}}))
      sys.exit()

  def dump(self):
    return {'db' : self.db,
            'WebEnv':self.webenv,
            'query_key' : self.querykey,
            'dbfrom' : self.dbfrom,
            'cmd' : self.cmd,
            'uids' : self.uids,
            'retmode' : self.retmode,
            'linkname' : self.linkname,
            'term' : self.term,
            'holding' : self.holding,
            'datetype' : self.datetype,
            'reldate' : self.reldate,
            'mindate' : self.mindate,
            'maxdate' : self.maxdate,
            'query_size' : self.query_size,
            'request_size' : self.request_size,
            'expected_requets' : self.expected_requests}
