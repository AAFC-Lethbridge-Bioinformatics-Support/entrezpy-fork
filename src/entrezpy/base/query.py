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

.. module:: entrezpy.base.query
  :synopsis: Exports the base class for entrezpy queries to NCBI E-Utils

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import atexit
import base64
import json
import os
import uuid
import queue
import threading

import entrezpy.requester.monitor
import entrezpy.requester.requester
import entrezpy.requester.requestpool
import entrezpy.log.logger


class EutilsQuery:
  """ EutilsQuery implements the base class for all entrezpy queries to
  E-Utils. It handles the information required by every query, e.g. base query
  url, email address, allowed requests per second, apikey,  etc. It declares
  the virtual method :meth:`.inquire` which needs to be implemented by every
  request since they differ among queries.

  An NCBI API key will bet set as follows:

  - passed as argument during initialization
  - check enviromental variable passed as argument
  - check enviromental variable NCBI_API_KEY

  Upon initalization, following parameters are set:

  - set unique query id
  - check for / set NCBI apikey
  - initialize :class:`entrezpy.requester.requester.Requester` with allowed
    requests per second
  - assemble Eutil url for desire EUtils function
  - initialize Multithreading queue and register query at
    :class:`entrezpy.base.monitor.QueryMonitor` for logging

  Multithreading is handled using the nested classes
  :class:`entrezpy.base.query.EutilsQuery.RequestPool` and
  :class:`entrezpy.base.query.EutilsQuery.ThreadedRequester`."""

  base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
  """Base url for all Eutil request"""


  def __init__(self, eutil, tool, email, apikey=None, apikey_var=None, threads=None, qid=None):
    """Inits EutilsQuery instance with eutil, toolname, email, apikey,
    apikey_envar, threads and qid.

    :param str eutil: name of eutil function on EUtils server
    :param str tool: tool name
    :param str email: user email
    :param str apikey: NCBI apikey
    :param str apikey_var: enviroment variable storing NCBI apikey
    :param int threads: set threads for multithreading
    :param str qid: unique query id

    :ivar id: unique query id
    :ivar base_url: unique query id
    :ivar int requests_per_sec:  default limit of requests/sec (set by NCBI)
    :ivar int max_requests_per_sec:  max.requests/sec with apikeyby (set NCBI)
    :ivar str url:  full URL for Eutil function
    :ivar str contact:  user email (required by NCBI)
    :ivar str tool:  tool name (required by NCBI)
    :ivar str apikey:  NCBI apikey
    :ivar int num_threads:  number of threads to use
    :ivar list failed_requests: store failed requests for analysis if desired
    :ivar request_pool: :class:`entrezpy.base.query.EutilsQuery.RequestPool` instance
    :ivar int request_counter: requests counter for a EutilsQuery instance
    """
    self.id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8') if not qid else qid
    self.eutil = eutil
    self.requests_per_sec = 3
    self.max_requests_per_sec = 10
    self.url = '/'.join([EutilsQuery.base_url, self.eutil])
    self.contact = email
    self.tool = tool
    self.apikey = self.check_ncbi_apikey(apikey, apikey_var)
    self.num_threads = 0 if not threads else threads
    self.failed_requests = []
    self.request_counter = 0
    self.query_monitor = entrezpy.requester.monitor.QueryMonitor(self.id)
    self.request_pool = entrezpy.requester.requestpool.RequestPool(self.num_threads,
                                                                   self.failed_requests,
                                                                   self.query_monitor,
                                                                   entrezpy.requester.requester.Requester(1/self.requests_per_sec))
    self.logger = entrezpy.log.logger.get_class_logger(EutilsQuery)
    self.logger.debug(json.dumps({'init':self.dump()}))

  def inquire(self, parameter, analyzer):
    """Virtual function starting query. Each query requires its own implementation.

    :param dict parameter: E-Utilities parameters
    :param analzyer: query response analyzer
    :type  analzyer: :class:`entrezpy.base.analyzer.EutilsAnalzyer`
    :returns: analyzer
    :rtype: :class:`entrezpy.base.analyzer.EutilsAnalzyer`
    """
    raise NotImplementedError("{} requires inquire() implementation".format(__name__))

  def check_requests(self):
    """Virtual function testing and handling failed requests. These requests
    fail due to HTTP/URL issues and stored
    :attr:`entrezpy.base.query.EutilsQuery.failed_requests`
    """
    raise NotImplementedError("{} requires check_failed_requests() implementation".format(__name__))

  def check_ncbi_apikey(self, apikey=None, env_var=None):
    """Checks and sets NCBI apikey.

    :param str apikey: NCBI apikey
    :param str env_var: enviromental variable storing NCBI apikey
    """
    if 'NCBI_API_KEY' in os.environ:
      self.requests_per_sec = self.max_requests_per_sec
      return os.environ['NCBI_API_KEY']
    if apikey:
      self.requests_per_sec = self.max_requests_per_sec
      return apikey
    if env_var and (env_var in os.environ):
      self.requests_per_sec = self.max_requests_per_sec
      return os.environ[env_var]
    return None

  def prepare_request(self, request):
    """Prepares request for sending to E-Utilities with require quey attributes.

    :param request: entrezpy request instance
    :type  request: :class:`entrezpy.base.request.EutilsRequest`
    :returns: request instance with EUtils parameters
    :rtype: :class:`entrezpy.base.request.EutilsRequest`
    """
    request.id = self.request_counter
    request.query_id = self.id
    request.contact = self.contact
    request.url = self.url
    request.tool = self.tool
    request.apikey = self.apikey
    request.status = 2
    return request

  def add_request(self, request, analyzer):
    """Adds one request and corresponding analyzer to the request pool.

    :param request: entrezpy request instance
    :type  request: :class:`entrezpy.base.request.EutilsRequest`
    :param analzyer: entrezpy analyzer instance
    :type analyzer: :class:`entrezpy.base.analzyer.EutilsAnalyzer`
    """
    self.request_pool.add_request(self.prepare_request(request), analyzer)
    self.request_counter += 1

  def monitor_start(self, query_parameters):
    """Starts query monitoring

    :param query_parameters: query parameters
    :type query_parameters: :class:`entrezpy.base.parameter.EutilsParameter`
    """
    self.query_monitor.dispatch_observer(self.id, query_parameters)

  def monitor_stop(self):
    """Stops query monitoring"""
    self.query_monitor.recall_observer(self.id)

  def monitor_update(self, updated_query_parameters):
    """Updates query monitoring parameters if follow up requests are required.

    :param updated_query_parameters: updated query parameters
    :type  updated_query_parameters: :class:`entrezpy.base.parameter.EutilsParameter`
    """
    self.query_monitor.update_observer(self.id, updated_query_parameters)

  def hasFailedRequests(self):
    """Reports if at least one request failed."""
    if self.failed_requests:
      return True
    return False

  def dump(self):
    """Dump all attributes"""
    return {'id':self.id, 'base_url':EutilsQuery.base_url, 'eutil':self.eutil,
            'url':self.url, 'req/sec':self.requests_per_sec, 'tool':self.tool,
            'contact':self.contact, 'apikey':self.apikey,
            'threads':self.num_threads}

  def isGoodQuery(self):
    """
    Tests for request errors

      :rtype: bool
    """
    if not self.failed_requests:
      self.logger.debug(json.dumps({'query':self.id, 'status':'OK'}))
      return True
    self.logger.debug(json.dumps({'query':self.id, 'status':'failed',
      'request-dumps':[x.dump_internals() for x in self.failed_requests]}))
    return False
