"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import atexit
import json
import signal
import queue
import time
import threading

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
    self.stop_event = threading.Event()
    self.logger = entrezpy.log.logger.get_class_logger(RequestPool)
    self.lock = threading.Lock()
    atexit.register(self.destructor)
    if self.useThreads():
      self.dispatch_workers()
    signal.signal(signal.SIGINT, self.sigint_handler)

  def useThreads(self):
    if self.threads > 0:
      return True
    return False

  def dispatch_workers(self):
    for _ in range(self.threads):
      w = entrezpy.requester.threadedrequest.ThreadedRequester(
        self.requests, self.failed_requests, self.monitor, self.requester, self.stop_event, self.lock)
      w.start()
      self.logger.debug(json.dumps({'thread':w.name, 'status':'started'}))
    self.logger.debug(json.dumps({'threading workers':'dispatched'}))

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
      self.logger.debug(json.dumps({'threads':self.threads}))
      self.logger.debug(json.dumps({'threads':'draining request pool'}))
      self.requests.join()
    else:
      self.logger.debug(json.dumps({'threads':'none'}))
      self.run_single()

  #def check_threads(self, stop_event):
    #while True:
      #for i in threading.enumerate():
        #self.logger.debug(json.dumps({'threads':i}))
        #time.sleep(0.5)

  def run_single(self):
    """Run single threaded requests."""
    while not self.requests.empty():
      request, analyzer = self.requests.get()
      response = self.run_one_request(request)
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

  def sigint_handler(self, sigint, frame):
    self.logger.debug(json.dumps({'sigint detected':'stopping threads'}))
    self.stop_event.set()
    self.logger.debug(json.dumps({'sigint detected':'waiting for threads to stop'}))
    time.sleep(1)
    sys.exit(self.logger.info(json.dumps({'sigint detected':'aborting'})))


  def run_one_request(self, request):
    """
    Processes one request from the queue and logs its progress.

    :param request: single entrezpy request
    :type  request: :class:`entrezpy.base.request.EutilsRequest`
    """
    request.start_stopwatch()
    o = self.monitor.get_observer(request.query_id)
    o.observe(request)
    response = self.requester.request(request)
    request.calc_duration()
    o.processed_requests += 1
    #self.logger.debug((response, response.status, response.read(), response.read().decode('utf-8')))
    return response
