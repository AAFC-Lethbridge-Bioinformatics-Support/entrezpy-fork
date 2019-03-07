#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2017 The University of Sydney
#-------------------------------------------------------------------------------

import time

## EutilsRequest is the base class for requests created by EutilsQuery.
# The EutilsRequest are finalized by EutilsQuery before added to the request
# pool before. Each EutilsRequest triggers an answer at the NCBI Entrez servers
# if no connection errors occured.
# An EutilsRequest() instance has all the information to format a POST request
# query. The requests status can be queried from outside, i.e. by the
# QueryMonitor(), using the get_observation() function.
# The EutilsAnalyzer needs the EutilsQuery and response from the server to
# analyze the requested data correctly since EutilsQuery contains additional
# information which is not available in the returned result, e.g. the queried
# database.  Such information is required to create query pipelines using WebEnv
# and query_key.
class EutilsRequest:

  ## Ctor
  # Initializes a new query and populats is with the initial attributes.
  # The request id is used to trace requests and given by EutilsQuery.
  # The status attribute is work in progress.
  # @param[in] typ str string indicating the query type for this request
  # @param[in] db str target database for this request
  def __init__(self, typ, db):
    self.typ = typ
    self.db = db
    self.id = None
    self.query_id = None
    self.tool = None
    self.url = None
    self.qry_url = None
    self.contact = None
    self.status = 3 # 0: success, 1: Fail, 3 Queued
    self.request_error = None
    self.size = 1
    self.apikey = None
    self.start_time = None
    self.duration = None

  ## Function to return the attributes required by each request.
  # Simple extension of the requred attribute for specific queries can by
  # added using extend
  # @param extend dict dictionary to extend basic query with specific attributes
  # @return base dict dictionary representing basic query data to send to server
  def prepare_base_qry(self, extend=None):
    base = {'email' : self.contact, 'tool' : self.tool, 'db' : self.db}
    if self.apikey:
      base.update({'api_key' : self.apikey})
    if extend:
      base.update(extend)
    return base

  ## Function to set success status of query
  def set_status_success(self):
    self.status = 0
  ## Function to set fail status of query
  def set_status_fail(self):
    self.status = 1

  ## Function to query attributes of request for monitoring
  # @return tab-delimited string with request status
  def get_observation(self):
    cols = [self.query_id, self.id, self.typ, self.size, self.status, self.duration]
    if self.request_error:
      cols += [self.request_error, self.url, self.qry_url]
    return '\t'.join(str(x) for x in cols)

  ## Function to get request id
  # @return string with assembled request id
  def get_request_id(self):
    return '.'.join([str(self.query_id), str(self.id)])

  ## Function set indicate request error due to a HTTP/URL error
  #@param[in] error string error description
  def set_request_error(self, error):
    self.request_error = error
    self.status = 1

  ## Function to start measering duration of the request
  def start_stopwatch(self):
    self.start_time = time.time()

  ##Function to stop and calculate the duration of the request
  def calc_duration(self):
    self.duration = time.time() - self.start_time

  ##Function to dump internal attributes for every request
  # @return dictionary with all internal attributes
  def dump_internals(self, extend=None):
    reqdump = {"typ" : self.typ,
               "db" : self.db,
               "id" : self.id,
               "query_id" : self.query_id,
               "tool" : self.tool,
               "url" : self.url,
               "query_url" : self.qry_url,
               "email" : self.contact,
               "request_error" : self.request_error,
               "size" : self.size,
               "apikey" : self.apikey}
    if extend:
      reqdump.update(extend)
    return reqdump
