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

## EpostParameter implements checks and configures an EpostQuery().
# EpostParameter inherits entrezpy_base.parameter.EutilsParameter.
# An EPost query posts uids to the history server. If no WebEnv is given,
# a new WebEnv with query key is creted and returned. If a WebEvn is is given,
# the uids will be added to this webenv and an associated query key returned.
# This sets request_size = 1 and expected_requests = 1 and the query size
# is the length of passed uids.
# The documentation on Epost [0] doesn't mention any maximum uids to post.
#
# [0] : https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EPost
class EpostParameter(entrezpy_base.parameter.EutilsParameter):

  def __init__(self, parameter):
    super().__init__(parameter)
    self.uids = parameter.get('id', [])
    self.retmode = parameter.get('retmode', 'xml')
    self.query_size = len(self.uids)
    self.request_size = 1
    self.expected_requests = 1
    self.check()

  def check(self):
    if not self.haveDb():
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing parameter", "parameter":
                                                              {"term":self.db,"action":"abort"}}}))
      sys.exit()
    if self.query_size == 0:
      logger.error(json.dumps({"Parameter-error":{"msg": "Missing uids",
                                                         "parameter": {"uids":self.uids,
                                                         "action":"abort"}}}))
      sys.exit()
