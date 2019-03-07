#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import sys
import json
import threading
import logging
import time

logger = logging.getLogger(__name__)

class QueryMonitor:

  class Observer(threading.Thread):

    def __init__(self, query):
      super().__init__(daemon=True)
      self.expected_requests = 0
      self.processed_requests = 0
      self.doObserve = True
      self.requests = []
      self.duration = None

    def recall(self):
      self.doObserve = False
      print('\n', file=sys.stderr)
      for i in self.requests:
          print(i.get_observation(), file=sys.stderr)
      self.join()

    def dispatch(self, parameter):
      self.expected_requests = parameter.expected_requests
      if not self.is_alive():
        self.start()

    def observe(self, request):
      self.requests.append(request)

    def run(self):
      while self.doObserve:
        for i in self.requests:
          print("{0}/{1}\t{2}".format(self.processed_requests, self.expected_requests, i.get_observation()),end='\r', file=sys.stderr)
        time.sleep(1)

  def __init__(self):
    self.observers = {}
    self.locks = {}

  def register_query(self, query):
    self.locks[query.id] = threading.Lock()
    self.observers[query.id] = self.Observer(query)

  def get_observer(self, query_id):
    return self.observers.get(query_id, None)

  def dispatch_observer(self, query, parameter):
    o = self.observers.get(query.id, None)
    o.dispatch(parameter)

  def recall_observer(self, query):
    o = self.observers.get(query.id, None)
    o.recall()

  ## Function updating the settings for a thread
  # Honestly, I have no idea if the lock is really required. It works without
  # locks but it looks to me cleaner to stop a thread, update it, continue
  # instead of just updating the parameter.
  def update_observer(self, query, parameter):
    #self.locks[query.id].acquire()
    self.observers[query.id].expected_requests = parameter.expected_requests
    #self.locks[query.id].release()
