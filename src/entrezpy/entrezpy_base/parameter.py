#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import sys

## class EutilsParameter is the base for all eutils query parameters.
#
# An EutilsParameter requires a dictionary with valid E-Utilities parameters for
# the corresponding query. The parameters use in almost all queries are taken
# directly. Setting and testing query specific parameters need to be implemented
# in the correspondingly inherited class
#
# Simple helper functions are presented to test the common parmameters db,
# WebEnv, query_key and usehistory.
#
# Important: usehistory, the parameter controlling the use of the Entrez history
#            server, is set to True (use it) by default since it is heavily
#            used in linked queries. It can be set to False which will disable
#            the histry server use. But it's not recommended.
#
# The function haveExpectedRequests() test of the number of requests has been
# calculated.
#
# The virtual functions check() and dump() need implementation since they can
# vary between queries. check() is expected to run after all parameters have
# been set.
class EutilsParameter:

  ## Ctor
  # Check for parameter dictionary and set most common parameters
  # @param [in] parameter, dict, E-Utilities parameter as key=value
  def __init__(self, parameter=None):
    if not parameter:
      sys.exit("{} requires paramater as initial argment bit none was given. Abort")
    self.db = parameter.get('db')
    self.webenv = parameter.get('WebEnv')
    self.querykey = parameter.get('query_key', 0)
    self.expected_requests = 0

  ## Virtual function to run a check before starting the query.
  # Since this is a crucial step, check() is expected to abort when it fails.
  def check(self):
    raise NotImplementedError("{}.check() is virtual and requires implementation".format(__name__))

  def haveDb(self):
    if self.db:
      return True
    return False

  def haveWebenv(self):
    if self.webenv:
      return True
    return False

  def haveQuerykey(self):
    if self.querykey:
      return True
    return False

  def useHistory(self):
    if self.usehistory:
      return True
    return False

  ## Check if the size of the query has been calculated.
  def haveExpectedRequets(self):
    if self.expected_requests > 0:
      return True
    return False

  ## dump attributes of EutilsParameter()
  # Used for debugging puposes
  def dump(self):
    raise NotImplementedError("{}.dump() is virtual and requires implementation".format(__name__))
