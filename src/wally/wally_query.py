#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import io
import os
import sys
import uuid
import base64
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class WallyQuery:

  def __init__(self, category, parameter, dependency=None, analyzer=None):
    if not parameter and not dependency:
      PinaxQuery.logger.error(json.dumps({__name__:{"msg": "Missing parameters",
                                                    "parameter": {"parameter":parameter,
                                                                  "dependency":dependency.id},
                                                    "action":"abort"}}))
      sys.exit()
    if not parameter:
      parameter = {}
    self.id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode()
    self.category = category
    self.parameter = parameter
    self.dependency =  dependency
    self.analyzer = analyzer

  def resolve_dependency(self, analyzers):
    if self.dependency:
      parameter = analyzers[self.dependency].result.get_link_parameter()
      if self.category == 'elink':
        parameter['dbfrom'] = parameter['db']
      parameter.update(self.parameter)
      self.parameter = parameter
      #assume parameters = []
