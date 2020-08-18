"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import atexit
import json
import queue

import entrezpy.requester.threadedrequest
import entrezpy.log.logger


class RequestPool:
    """ Threading Pool for requests. This class inits the threading pool,
    adds requests waits until all threads finish. A request consist of a tuple
    with the request and corresponding analyzer. Failed requests are stored
    separately to handle them later. If the number of threads is 0, use
    :meth:`entrezpy.base.query.EutilsQuery.RequestPool.run_single`. Otherwise,
    call :class:`entrezpy.base.query.EutilsQuery.ThreadedRequester`
    This is useful in cases where analyzers are calling not thread-safe methods
    or classes, e.g. Sqlite3
    """

    def __init__(self, num_threads, failed_requests, monitor, requester):
      """
      Initiates a threading pool with a given number of threads.

      :param int num_threads: number of threads
      :param reference failed_requests:
        :attr:`entrezpy.base.query.EutilsQuery.failed_requests`
      :ivar requests: request queue
      :type requests: :class:`queue.Queue`
      """
      self.requests = queue.Queue(num_threads)
      self.failed_requests = failed_requests
      self.requester = requester
      self.monitor = monitor
      self.threads = num_threads
      atexit.register(self.destructor)
      if self.useThreads():
        self.logger.debug(json.dumps({'Threading': 'yes'}))
        for _ in range(num_threads):
          entrezpy.requester.threadedrequest.ThreadedRequester(
            self.requests, self.failed_requests, self.monitor, self.requester)
      self.logger = entrezpy.log.logger.get_class_logger(RequestPool)

    def useThreads(self):
      if self.threads > 0:
        return True
      return False

    def add_request(self, request, analyzer):
      """Adds one request into the threading pool as
      **tuple**\ (`request`, `analzyer`).

      :param  request: entrezpy request instance
      :type   request: :class:`entrezpy.base.request.EutilsRequest`
      :param analyzer: entrezpy analyzer instance
      :type  analyzer: :class:`entrezpy.base.analyzer.EutilsAnalyzer`
      """
      self.requests.put((request, analyzer))

    def drain(self):
      """Empty threading pool and wait until all requests finish"""
      if self.useThreads():
        self.logger.debug(json.dumps({'Threads in pool': self.threads}))
        self.requests.join()
      else:
        self.logger.debug(json.dumps({'Threading':'no'}))
        self.run_single()

    def run_single(self):
      """Run single threaded requests."""
      while not self.requests.empty():
        request, analyzer = self.requests.get()
        response = self.requester.run_one_request(request, self.monitor)
        if response:
          analyzer.parse(response, request)
        else:
          self.failed_requests.append(request)

    def destructor(self):
      """ Shutdown all ongoing threads when exiting due to an error.

      .. note::
        Deamon processes don't always stop when the main
        program exits and hang aroud. atexit.register(self.desctructor) seems
        to be a way to implement a dectructor. Currently not used.
      """
      pass
