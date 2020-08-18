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

.. module:: entrezpy.base.monitor
  :synopsis: Exports class QueryMonitor implementing monitoring of entrezpy
    queries and requsts

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import sys
import threading
import time

import entrezpy.log.logger


class QueryMonitor:
  """
  The QueryMonitor class implements the monitoring of entrezpy requests in
  entrezpy queries. It controls individual Observers which are linked to one
  entrezpy query.
  """

  logger = None
  observers = {}

  class Observer(threading.Thread):
    """
    The Observer class implements the observation of one entrezpy query. It
    uses Python's multithreading deamon when using multithreading.
    """

    def __init__(self):
      super().__init__(daemon=True)
      self.expected_requests = 0
      self.processed_requests = 0
      self.doObserve = True
      self.requests = []
      self.duration = None

    def recall(self):
      """Stops an observation for a query"""
      self.doObserve = False
      for i in self.requests:
        i.report_status(self.processed_requests, self.expected_requests)
      self.join()

    def dispatch(self, parameter):
      """
      Starts observation

      :param parameter: query parameter
      """
      self.expected_requests = parameter.expected_requests
      if not self.is_alive():
        self.start()

    def observe(self, request):
      """Adds one query request for observation"""
      self.requests.append(request)

    def run(self):
      """Observes requests from an entrezpy query"""
      while self.doObserve:
        for i in self.requests:
          i.report_status(self.processed_requests, self.expected_requests)
        time.sleep(1)

  def __init__(self, query):
    """Inits observer and registers query for monitoring."""
    self.register_query(query)
    QueryMonitor.logger = entrezpy.log.logger.get_class_logger(QueryMonitor)
    #self.locks = {}

  def register_query(self, query_id):
    """
    Adds a query for observation

    :param query: entrezpy query
    :type  query: :class:`entrezpy.base.query.EutilsQuery`
    """
    #self.locks[query_id] = threading.Lock()
    if query_id in QueryMonitor.observers:
      sys.exit(QueryMonitor.logger.error(json.dumps({'Duplicate query_id':query_id})))
    QueryMonitor.observers[query_id] = self.Observer()

  def get_observer(self, query_id):
    """
    Returns an observer for a specific query.

    :param str query_id: entrezpy query id
    :rtype: :class:`base.mnonitor.QueryMonitor.Observer`
    """
    if query_id in QueryMonitor.observers:
      return QueryMonitor.observers[query_id]
    sys.exit(QueryMonitor.logger.error(json.dumps({'No observer for query_id':query_id})))

  def dispatch_observer(self, query_id, parameter):
    """
    Start the observer for an entrezpy query

    :param query: entrezpy query
    :type  query: :class:`entrezpy.base.query.EutilsQuery`
    :param parameter: query parameter
    :type  parameter: 'class':`entrezpy.base.EutilsParameter`
    """
    QueryMonitor.logger.debug(json.dumps({'dispatching observer for':query_id,
                                          'parameter':parameter.dump()}))
    self.get_observer(query_id).dispatch(parameter)

  def recall_observer(self, query_id):
    """
    Stops the observer for an entrezpy query

    :param query: entrezpy query
    :type  query: :class:`entrezpy.base.query.EutilsQuery`
    """
    QueryMonitor.logger.debug(json.dumps({'recalling observer for':query_id}))
    self.get_observer(query_id).recall()

  def update_observer(self, query_id, parameter):
    """
    Function updating the settings for a thread. Honestly, I have no idea if
    the lock is really required. It works without locks, just updating the
    parameter.

    :param query: entrezpy query
    :type  query: :class:`entrezpy.base.query.EutilsQuery`
    :param parameter: query parameter
    :type  parameter: 'class':`entrezpy.base.EutilsParameter`
    """
    QueryMonitor.logger.debug(json.dumps({'updating observer for':query_id,
                                          'parameter':parameter.dump()}))
    self.get_observer(query_id).expected_requests = parameter.expected_requests
