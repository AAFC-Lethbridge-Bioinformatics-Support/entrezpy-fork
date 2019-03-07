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

## Basic entrezpy query for Wally
# It's responsible for storing and resolving query dependencies
class WallyQuery:

  ##Ctor
  # @param[in] category str query category
  # @param[in] parameter dict dictionary with Eutils parameters
  # @param[in] dependency uuid.uuid4() query id from earlier query
  # @param[in] analyzers analyzer intance for this query
  def __init__(self, category, parameter, dependency=None, analyzer=None):
    if not parameter and not dependency:
      logger.error(json.dumps({__name__:{"msg": "Missing parameters",
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

  ## resolve dependencies
  # If earlier requets are given as dependencies as well as new parameters, the
  # new parameters will overwrite those from the dependency.
  # @param[in] analyzers dictionary global Wally.analzyers dictionary
  def resolve_dependency(self, analyzers):
    if self.dependency:
      parameter = analyzers[self.dependency].result.get_link_parameter()
      if self.category == 'elink':
        parameter['dbfrom'] = parameter['db']
      parameter.update(self.parameter)
      self.parameter = parameter
      #assume parameters = []
