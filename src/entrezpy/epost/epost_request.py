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

.. module:: epost_request
  :synopsis: Exports class EpostRequest class implementing individual requests
    from :class:`entrezpy.elink.elink_query.ElinkQuery`

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json

import entrezpy.base.request
import entrezpy.log.logger


class EpostRequest(entrezpy.base.request.EutilsRequest):
  """ EpostRequest implements a single request as part of an Epost
  query. It stores and prepares the parameters for a single request.
  See :class:`entrezpy.epost.epost_parameter.EpostParameter` for parameter
  description.

  :param parameter: request parameter
  :param type: :class:`entrezpy.epost.epost_parameter.EpostParameter`
  """

  logger = None

  def __init__(self, eutil, parameter):
    super().__init__(eutil, parameter.db)
    self.uids = parameter.uids
    self.size = len(parameter.uids)
    self.webenv = parameter.webenv
    self.retmode = parameter.retmode
    EpostRequest.logger = entrezpy.log.logger.get_class_logger(EpostRequest)
    EpostRequest.logger.debug(json.dumps({'init': self.dump()}))

  def get_post_parameter(self):
    """Implements :meth:`entrezpy.base.request.EutilsRequest.get_post_parameter`"""
    return self.prepare_base_qry(extend={'id':','.join(str(x) for x in self.uids),
                                         'WebEnv':self.webenv})

  def dump(self):
    """
    Dump instance attributes

    :rtype: dict
    """
    return self.dump_internals({'retmode':self.retmode, 'WebEnv':self.webenv})

  def report_status(self, isrequest=None, expectedRequests=None):
    """Reports the current status the the request"""
    EpostRequest.logger.debug((json.dumps({'queryid':self.query_id, 'reqid':self.id,
      'status':self.status, 'duration':self.duration,
      'error':self.request_error, 'url':self.url})))
