#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2017,2018 The University of Sydney
#  \bug Error handling is wonky
#  \description Base class to parse and analyze EDirect results.
#-------------------------------------------------------------------------------
import io
import json
import xml.etree.ElementTree

## EutilsAnalyzer is the base class for an entrezpy analyzer.
# It prepares the response based on the requested format and checks for
# E-Utilities errors.
# The function parse() is invoked after every request by the corresponding
# query class, e.g. Esearcher. This allwos to analyze data as it arrives and not
# to wait until a large query has been fetched. Such an approach allows
# to implement an analyzer which can store already download data to
# establish checkpoints. Or to react otherwise based on the analyzed data.
#
# Since the responses from NCBI are not very well documented, there is a fair
# bit of ongoing testing and guessing. These functions will be extended as new
# errors are encountered.
# Upon recoginxing errors, the hasErrorResponse attribute is ste to True.
#
# Two virtual classes need implementation to support the specific query:
# analyze_error() and analyze_result()

class EutilsAnalyzer:

  ## Known formats to EutilsAnalyzer
  known_fmts = {'xml' : 0, 'json' : 0, 'text' : 0}

  def __init__(self):
    self.hasErrorResponse = False

  ## fuction called by the corresponding query class after a request
  # @param[in] raw_response urllib.request.Request() instance
  # @param[in] request      EutilsRequest() instance
  def parse(self, raw_response, request):
    if request.retmode not in EutilsAnalyzer.known_fmts:
      raise NotImplementedError("Unknown format: {}".format(request.retmode))
    response = self.convert_response(raw_response, request)
    if self.isErrorResponse(response, request):
      self.analyze_error(response, request)
    else:
      self.analyze_result(response, request)

  ## Function converting the urllib.request.Request() into the expected format
  # The expected format is deduced from request and set via the retmode
  # parameter passed to EutilsQuery.inquire()
  #@param[in] raw_response urllib.request.Request() instance
  #@param[in] request      EutilsRequest() instance
  #@return JSON object if epxecting JSON
  #@return io.stringIO if expecting XML or text
  def convert_response(self, raw_response, request):
    if request.retmode == 'json':
      return json.loads(raw_response.read())
    return io.StringIO(raw_response.read().decode('utf-8'))

  ## Function checking for error messages sent by NCBI Entrez Servers
  # If errors are found, the hasErrorResponse is set
  #@param[in] response  converted response
  #@param[in] request   EutilsRequest() instance
  #@return self.hasErrorResponse indicating if error have been found
  def isErrorResponse(self, response, request):
    if request.retmode == 'xml':
      self.hasErrorResponse = self.check_error_xml(response)
      response.seek(0)
    if request.retmode == 'json':
      self.hasErrorResponse = self.check_error_json(response)
    return self.hasErrorResponse

  ## Function to check errors in XML responses
  def check_error_xml(self, response):
    for _, elem in xml.etree.ElementTree.iterparse(response, events=["end"]):
      if elem.tag == 'ERROR':
        elem.clear()
        return True
      elem.clear()
    return False

  ## Function to check errors in JSON responses
  def check_error_json(self, response):
    if response['header']['type'] == 'esearch' and 'ERROR' in response['esearchresult']:
      return True
    if response['header']['type'] == 'elink' and 'ERROR' in response:
      return True
    if 'esummaryresult' in response:
      if response['esummaryresult'][0].split(' ')[0] == 'Invalid':
        return True
    if 'error' in response:
      return True
    return False

  ## Function to test if reponse has errors
  #@return True  if no errors are found
  #@return False if errors are found
  def isSuccess(self):
    if self.hasErrorResponse:
      return False
    return True

  ## Virtual function to handle error responses
  def analyze_error(self, response, request):
    raise NotImplementedError("Require implementation of analyze_error()")

  ## Virtual function to handle good responses
  def analyze_result(self, response, request):
    raise NotImplementedError("Require implementation of analyze_result()")
