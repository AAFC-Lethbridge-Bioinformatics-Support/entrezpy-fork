"""
..
  Copyright 2018 The University of Sydney

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

.. module:: entrezpy.base.request
  :synopsis: Exports the base class for entrezpy requests in NCBI E-Utils
    queries

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
import time

import entrezpy.log.logger


class EutilsRequest:
  """EutilsRequest is the base class for requests from
  :class:`entrezpy.base.query.EutilsQuery`.

  EutilsRequests instantiate in :meth:`entrezpy.base.query.EutilsQuery.inquire`
  before being added to the request pool by
  :meth:`entrezpy.base.query.EutilsQuery.add_request`. Each EutilsRequest
  triggers an answer at the NCBI Entrez servers if no connection errors occure.

  :class:`EutilsRequest` stores the required  information for POST requests.
  Its status can be queried from outside by
  :func:`entrezpy.base.request.EutilsRequest.get_observation`. EutilsRequest
  instances store information not present in the server response and is
  required by :class:`entrezpy.base.analyzer.EutilsAnalyzer` to parse responses
  and errors correctly. Several instance attributes are not required for a POST
  request but help debugging.

  Each request is automatoically assigned an id to identify and  trace requests
  using the query id and request id.

  :param str eutil: eutil function for this request, e.g. efetch.fcgi
  :param str db: database for request
  """

  def __init__(self, eutil, db):
    """ Initializes a new request with initial attributes as part of a query in
    :class:`entrezpy.base.query.EutilsQuery`.

    :ivar str tool: tool name to which this request belongs
    :ivar str url: full Eutil url
    :ivar str contact: use email
    :ivar str apikey: NBCI apikey
    :ivar str query_id: :attr:`entrezpy.base.query.EutilsQuery.query_id`  which
      initiated this request
    :ivar int status: request status : 0->success, 1->Fail,2->Queued
    :ivar int size: size of request, e.g. number of UIDs
    :ivar float start_time: start time of request in seconds since epoch
    :ivar duration: duration for this request in seconds
    :ivar doseq: set doseq parameter in :meth:`entrezpy.request.Request.request`

    .. note:: :attr:`.status` is work in progress.
    """
    self.eutil = eutil
    self.db = db
    self.id = None
    self.query_id = None
    self.tool = None
    self.url = None
    self.contact = None
    self.apikey = None
    self.status = 2
    self.request_error = None
    self.size = 1
    self.start_time = None
    self.duration = None
    self.doseq = True
    self.logger = entrezpy.log.logger.get_class_logger(EutilsRequest)

  def get_post_parameter(self):
    """
    Virtual function returning the POST parameters for the request from required
    attributes.

    :rtype: dict
    :raises NotImplemetedError:
    """
    raise NotImplementedError()

  def prepare_base_qry(self, extend=None):
    """
    Returns instance attributes required for every POST request.

    :param dict extend: parameters extending basic parameters
    :return: base parameters for POST request
    :rtype: dict
    """
    base = {'email' : self.contact, 'tool' : self.tool, 'db' : self.db}
    if self.apikey:
      base.update({'api_key' : self.apikey})
    if extend:
      base.update(extend)
    return base

  def set_status_success(self):
    """Set status if request succeeded"""
    self.status = 0

  def set_status_fail(self):
    """Set status if request failed"""
    self.status = 1

  def report_status(self, processed_requests=None, expected_requests=None):
    """
    Reports request status when triggered
    """
    self.logger.info(json.dumps({'query':self.query_id,
      'request':self.id, 'status':self.status}))
    self.logger.debug(json.dumps({'status': self.dump_internals()}))

  def get_request_id(self):
    """
    :returns: full request id
    :rtype: str
    """
    return '.'.join([str(self.query_id), str(self.id)])

  def set_request_error(self, error):
    """
    Sets request error and HTTP/URL error message

    :param str error: HTTP/URL error
    """
    self.request_error = error
    self.status = 1

  def start_stopwatch(self):
    """Starts time to measure request duration."""
    self.start_time = time.time()

  def calc_duration(self):
    """Calculates request duration"""
    self.duration = time.time() - self.start_time

  def dump_internals(self, extend=None):
    """
    Dumps internal attributes for request.

    :param dict extend: extend dump with additional information
    """
    if extend is None:
      extend = {}
    reqdump = {'eutil':self.eutil, 'db':self.db, 'id':self.id, 'query_id':self.query_id,
               'tool':self.tool, 'url':self.url, 'email':self.contact, 'size':self.size,
               'request_error':self.request_error, 'apikey':'no'}
    if self.apikey is not None:
      reqdump['apikey'] = 'yes'
    return dict(extend, **reqdump)
