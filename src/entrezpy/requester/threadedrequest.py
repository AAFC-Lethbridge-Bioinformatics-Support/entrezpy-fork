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

  logger = None

  def __init__(self, requests, failed_requests, monitor, requester):
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
    ThreadedRequester.logger = entrezpy.log.logger.get_class_logger(ThreadedRequester)
    self.start()

  def run(self):
    """Overwrite :meth:`threading.Thread.run` for multithreaded requests."""
    while True:
      request, analyzer = self.requests.get()
      response = self.requester.run_one_request(request, self.monitor)
      ThreadedRequester.logger.info(json.dumps({'query_id':request.query_id,
                                                'status': request.status}))
      if response:
        analyzer.parse(response, request)
      else:
        self.failed_requests.append(request)
      self.requests.task_done()

