#-------------------------------------------------------------------------------
#  \author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \description: Base class for Edirect results
#  \copyright: 2018 The University of Sydney
#-------------------------------------------------------------------------------

import uuid
import base64

class EutilsResult:

  def __init__(self, typ, db=None, uids=[], webenv=None, querykey=0):
    self.id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode()
    self.typ = typ
    self.db = db
    self.uids = uids
    self.webenv = webenv
    self.querykey = int(querykey)

  def isSuccess(self):
    raise NotImplementedError("Help! Require implementation")

  def dump(self):
    raise NotImplementedError("Help! Require implementation")

  def get_link_parameter(self):
    raise NotImplementedError("Help! Require implementation")
