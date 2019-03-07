#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2017,2018 The University of Sydney
#  \description  The base class for NCBI requests to Edirect. The specific
#               function, e.g. search or fetch, need to be implemented in the
#                child class
#-------------------------------------------------------------------------------

import io
import os
import sys
import json
import uuid
import base64
import atexit
import queue
import threading
import collections
import time

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import requester.requester
from . import monitor

class EutilsQuery:
  ## Base class for E-Utilities queries
  # While EutilsQuery cannot work by itself, it serves as base class
  # for all queries by handling the the information required by
  # every query, e.g. base query url, email address, allowed requests per
  # second  etc.
  # Multithreading of requests is handles using the two nested classes
  # QueryRequester and RequestPool.
  # The virtual function inquire() needs to be implemented by every request since
  # they differ slightly among queries.

  ## query requester will hold the reference to Requester() instance
  query_requester = None

  ## query_monitor references the monitor/logging instance of monitor.QueryMonitor()
  query_monitor = monitor.QueryMonitor()

  ## Nested threading class to handle a singel request
  # It inherits from threading.Thread
  # The class gets query requests from the request pool and calls the Requester
  class QueryRequester(threading.Thread):
    ## Constructor
    # A request thread running as daemon
    #@param[in] requests        reference to the RequestPool() instance
    #@param[in] failed_requests reference to the list storing failed requests
    def __init__(self, requests, failed_requests):
      super().__init__(daemon=True)
      self.requests = requests
      self.failed_requests = failed_requests
      self.start()

    ## Overwritten run method from threading.Thread
    # It calls Requester.request() referenced as
    # EutilsQuery.query_requester and starts  observation/logging for this
    # request
    def run(self):
      while True:
        req, analyzer = self.requests.get()
        req.start_stopwatch()
        o = EutilsQuery.query_monitor.get_observer(req.query_id)
        o.observe(req)
        response = EutilsQuery.query_requester.request(req)
        if response:
          analyzer.parse(response, req)
        else:
          self.failed_requests.append(req)
        req.calc_duration()
        o.processed_requests += 1
        self.requests.task_done()

  ## Nested Threading Pool for requests
  # This class initiates the threading pool, handles adding requests to the pool
  # and waits until all threads finish. A request consist of a tuple
  # containing the request and corresponding analyzer. Failed requests are
  # stored separately to handle them later by EutilsQuery. If the number of
  # threads is 0, threading is disabled and the single_run() function is
  # used.
  class RequestPool:
    ## Ctor
    # Initiates a threading pool with a specific number of threads
    # @param[in] num_threads     int  number of threads to keep ready
    # @param[in] failed_requests list reference to list to store failed requests
    def __init__(self, num_threads, failed_requests):
      self.requests = queue.Queue(num_threads)
      self.failed_requests = failed_requests
      atexit.register(self.destructor)
      self.no_threads = True
      if num_threads > 0:
        self.no_threads = False
        for i in range(num_threads):
          EutilsQuery.QueryRequester(self.requests, self.failed_requests)

    ## Function to add a request into the threading pool. Threading requests
    # are expected as (request, analzyer)tuple
    # @param[in] request  an EutilsQuery() instance
    # @param[in] analyzer reference to the proper EutilsAnalyzer() instance
    def add_request(self, request, analyzer):
      self.requests.put((request, analyzer))

    ## Empty threading pool and wait until all requests finish
    def drain(self):
      if self.no_threads:
        self.run_single()
      else:
        self.requests.join()

    ## Function to run requests not threaded.
    # This is useful in cases where analyzers are calling methods or classes
    # which are not thread-safe, e.g. Sqlite3
    def run_single(self):
      while not self.requests.empty():
        req, analyzer = self.requests.get()
        req.start_stopwatch()
        o = EutilsQuery.query_monitor.get_observer(req.query_id)
        o.observe(req)
        response = EutilsQuery.query_requester.request(req)
        if response:
          analyzer.parse(response, req)
        else:
          self.failed_requests.append(req)
        req.calc_duration()
        o.processed_requests += 1

    def destructor(self):
      # ToDo: try to sutdonw all ongoing threads when exiting due to
      # an error caught. deamon porcesses don't always stop when the main
      # program exits and hang aroud. atexit.register(self.desctructor) seems
      # to be a way to implement a dectructor.
      pass

  ## Ctor
  # Initializes an EutilsQuery() instance
  # @param resturl, str, url to the corresponding E-Utility
  # @param tool, str, tool name, required by NCBI
  # @param email, str, User email, required by NCBI
  # @param apikey, str, NCBI apikey if available.
  # @param threads, int, Number of threads to use on the Threading pool
  # @param id, str, user defined id. Will be generated if not given
  def __init__(self, resturl, tool, email, apikey=None, threads=None, id=None):
    self.id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode() if not id else id
    self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    self.requests_per_sec = 3       # Default, w/o apikey
    self.max_requests_per_sec = 10  # with apikey
    self.url = '/'.join([self.base_url, resturl])
    self.contact = email
    self.tool = tool
    self.apikey = self.check_ncbi_apikey(apikey)
    self.num_threads = 0 if not threads else threads
    self.failed_requests = []
    self.request_pool = EutilsQuery.RequestPool(self.num_threads, self.failed_requests)
    self.request_counter = 0
    EutilsQuery.query_requester = requester.requester.Requester(1/self.requests_per_sec)
    EutilsQuery.query_monitor.register_query(self)

  ## Check if an NCBI apikey is present as enviroment variable
  # The enviroment variable NCBI_API_KEY is checked by default
  # @param apikey, string, NCBI apikey
  # @param env_var, enviroment variable storing NCBI apikey
  def check_ncbi_apikey(self, apikey=None, env_var=None): #not as clean as could be
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

  ## Function to add a request to the threading pool
  # Populating the threading pool with the (request, analyzer) tuple and
  # increment the request number required for its id
  # @param[in] request, EutilsRequest()
  # @param[in] analzyer, reference to the analyzer instance
  def add_request(self, request, analyzer):
    self.request_pool.add_request(self.prepare_request(request), analyzer)
    self.request_counter += 1

  ## Function to prepare a request to send to E-Utilities
  # Add with the informations every request needs
  # @param[in, out] request finalize EutilsRequest() instance
  def prepare_request(self, request):
    request.id = self.request_counter
    request.query_id = self.id
    request.contact = self.contact
    request.url = self.url
    request.tool = self.tool
    request.apikey = self.apikey
    return request

  ## Helper function to start the monitoring of the query
  # @param[in] query_parameters EutilsParameter() instance for this query
  def monitor_start(self, query_parameters):
    EutilsQuery.query_monitor.dispatch_observer(self, query_parameters)

  ## Helper function to update monitoring parameter of the query
  # This is nesseceary if follow up requests are required, e.g. large
  # Esearch() queries
  # @param[in] updated_query_parameters updated EutilsParameter() instance for this query
  def monitor_update(self, updated_query_parameters):
    EutilsQuery.query_monitor.update_observer(self, updated_query_parameters)

  ## Helper function to stop the monitoring of the query
  def monitor_stop(self):
    EutilsQuery.query_monitor.recall_observer(self)

  ## Virtual function which kicks off the query
  # Each query requires its own implementation since they vary.
  # @param[in] parameter  dictionary E-Utilities parameters as dictionary with
  # corresponding query parameters.
  #@param[in,out] analyzer EutilsAnalyzer instance adjusted for query
  def inquire(self, parameter, analyzer):
    raise NotImplementedError("{} requires inquire() implementation".format(__name__))

  ## Virtual function testing and handling failed requests
  # These are requests which failed due to HTPP/URL issues. Failed
  # requests are stored in the list self.failed_requests which is populated
  # by EutilsQuery.RequestPool
  def check_requests(self):
    raise NotImplementedError("{} requires check_failed_requests() implementation".format(__name__))

  ## Helper function reporting presen/absence of failed requests
  # It checks if EutilsQuery.RequestPool populated the failed request list
  def hasFailedRequests(self):
    if self.failed_requests:
      return True
    return False
