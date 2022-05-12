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

.. module:: entrezpy.requester.requester
  :synopsis: Exports class Requester handling HTTP requests for entrezpy.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import http
import sys
import random
import json
import time
import socket
import logging
import urllib.parse
import urllib.request
import urllib.error
import http.client as httplib
import ssl

import entrezpy.log.logger


class Requester:
  """Requester implements the sendong of HTTP POST requests and the receiving
  of the result. It checks for request connection errors and performs retries
  when possible. If the maximum number of retries is reached, the request is
  conisdered failed.  In case of connections errors, abort if the error is not
  due to timeout. The initial timeout is increased insteps until the maximum
  timeout has been reached.

  :param float wait: wait time in seconds between requests
  :param int max_retries: number of rertries before giving up.
  :param int init_timeout: number of seconds before the initial request is consid
                           considered a timeout error
  :param int timeout_max: maximum requet timeout before giving up
  :param int timeout_steps: increase value for timeout errors
  """

  def __init__(self, wait, max_retries=20, init_timeout=90, timeout_max=180, timeout_step=5):
    self.wait = wait
    self.max_retries = max_retries
    self.init_timeout = init_timeout
    self.timeout_max = timeout_max
    self.timeout_step = timeout_step
    self.logger = entrezpy.log.logger.get_class_logger(Requester)
    self.logger.debug(json.dumps({'init':{'wait[s]':self.wait,
                                          'timeout[s]':self.init_timeout,
                                          'timeoutMax[s]':self.timeout_max,
                                          'timeoutStep[s]':self.timeout_step,
                                          'retries':self.max_retries}}))

  def request(self, req):
    """Request the request

    :param req: entrezpy request
    :type  req: :class:`entrezpy.base.request.EutilsRequest`
    """
    retries = 0
    req_timeout = self.init_timeout
    data = urllib.parse.urlencode(req.get_post_parameter(),
                                  doseq=req.doseq).encode('utf-8')
    req.qry_url = data.decode()
    response = None
    while retries < self.max_retries:
      self.logger.debug(json.dumps({'try':retries}))
      wait = self.wait
      try:
        self.logger.debug(json.dumps({'request':{'qry-url':req.qry_url,
                                                 'req-id':req.id,
                                                 'req-query':req.query_id,
                                                 'req-url':req.url,
                                                 'try' : retries}}))
        req.set_status_success()
        response = urllib.request.urlopen(urllib.request.Request(req.url,data=data),
                                          timeout=req_timeout)
        response = response.read().decode('utf-8')
      except urllib.error.HTTPError as http_err:
        log_msg = {'code' : http_err.code, 'reason' : http_err.reason}
        req.set_request_error(http_err.reason)
        if http_err.code == 400: # Bad request form, stop right now
          log_msg.update({'action':'abort'})
          sys.exit(self.logger.error(json.dumps({'HTTP-error':log_msg})))
        log_msg.update({'action' : 'retry'})
        self.logger.warning(json.dumps({'HTTP-error':log_msg}))
        retries += 1
        wait = random.randint(1, 3)
      except socket.gaierror:
        self.logger.warning(json.dumps({'socket.gaierror':{'action':'retry'}}))
        retries += 1
        wait = random.randint(2, 4)
      except urllib.error.URLError as url_err:
        # req.set_request_error(url_err.reason) TODO: fix json not serializing error objects
        req.set_request_error("urllib.error.URLError")
        self.logger.error(json.dumps({'urllib.error.URLError': {'action':'retry'}}))
        retries += 1
        wait = random.randint(1, 3)
      except socket.timeout:
        req_timeout += self.timeout_step
        self.logger.warning(json.dumps({'timeout':{'action':'retry'}}))
        self.logger.debug(json.dumps({'timeout':{'action':'retry',
                                                 'wait':wait,
                                                 'timeout':req_timeout,
                                                 'step':self.timeout_step}}))
        retries += 1
        if req_timeout > self.timeout_max:
          self.logger.warning(json.dumps({'maxTimeout':{'action':'giving up request'}}))
          self.logger.debug(json.dumps({'maxTimeout':{'action':'giving up',
                                                      'timeout':req_timeout}}))
          req.set_request_error("maxTimeout")
          return None
      except httplib.IncompleteRead:
          self.logger.warning(json.dumps({'httplib.IncompleteRead':{'action':'retry'}}))
          retries += 1
          wait = random.randint(1, 3)
      except ssl.SSLError:
          self.logger.warning(json.dumps({'ssl.SSLError':{'action':'retry'}}))
          retries += 1
          wait = random.randint(1, 3)
      except http.client.RemoteDisconnected:
          self.logger.warning(json.dumps({'http.client.RemoteDisconnected':{'action':'retry'}}))
          retries += 1
          wait = random.randint(3, 5)
      else:
        return response
      finally:
        time.sleep(wait)
    # Should print this only if while failed
    self.logger.error(json.dumps({'maxRetry':{'action':'giving up request'}}))
    self.logger.debug(json.dumps({'maxRetry':{'retries':retries,
                                              'action':'giving up request',
                                              'max':self.max_retries}}))
    req.set_request_error("maxRetry")
    return None


  def run_one_request(self, request, monitor):
    """
    Processes one request from the queue and logs its progress.

    :param request: single entrezpy request
    :type  request: :class:`entrezpy.base.request.EutilsRequest`
    """
    request.start_stopwatch()
    o = monitor.get_observer(request.query_id)
    o.observe(request)
    response = self.request(request)
    request.calc_duration()
    o.processed_requests += 1
    self.logger.debug((response, response.status, response.read(), response.read().decode('utf-8')))
    return response
