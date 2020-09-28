"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import threading

import entrezpy.requester.requester
import entrezpy.log.logger


class ThreadedRequester(threading.Thread):
  """
  ThreadedRequester handles multitthreaded request. It inherits from
  :class:`threading.Thread`. Requests are fetched  from
  :class:`entrezpy.base.query.EutilsQuery.RequestPool` and processed in
  :meth:`.run`.
  """

  def __init__(self, requests, failed_requests, monitor, requester, stop_event, lock):
    """Inits :class:`.ThreadedRequester` to handle multithreaded requests.

    :param reference requests:
      :attr:`entrezpy.base.query.EutilsQuery.RequestPool.requests`
    :type reference failed_request:
      :attr:`entrezpy.base.query.EutilsQuery.failed_requests`
    """
    super().__init__(daemon=True)
    self.requests = requests
    self.failed_requests = failed_requests
    self.monitor = monitor
    self.requester = requester
    self.stop_event = stop_event
    self.lock = lock
    self.logger = entrezpy.log.logger.get_class_logger(ThreadedRequester)

  def run(self):
    """Overwrite :meth:`threading.Thread.run` for multithreaded requests."""
    while not self.requests.empty() or not self.stop_event.is_set():
      request, analyzer = self.requests.get()
      if self.stop_event.is_set():
        self.logger.info(json.dumps({'received stop signal':'aborting'}))
        break
      self.run_one_request(request, analyzer)
      self.logger.info(json.dumps({'query':request.query_id,
                                   'request':request.id,
                                   'status': request.status}))
      self.requests.task_done()

  def run_one_request(self, request, analyzer):
    """
    Processes one request from the queue and logs its progress.

    :param request: single entrezpy request
    :type  request: :class:`entrezpy.base.request.EutilsRequest`
    """
    self.lock.acquire()
    self.logger.debug(json.dumps({'lock':self.lock.locked()}))
    request.start_stopwatch()
    o = self.monitor.get_observer(request.query_id)
    o.observe(request)
    response = self.requester.request(request)
    request.calc_duration()
    o.processed_requests += 1
    self.logger.debug(response)
    if response:
      analyzer.parse(response, request)
    else:
      self.failed_requests.append(request)
    self.lock.release()
    self.logger.debug(json.dumps({'lock':self.lock.locked()}))
