#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2017, 2018 The University of Sydney
#  \description:
#-------------------------------------------------------------------------------

import sys
import time
import socket
import logging
import json
import urllib.parse
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class Requester:

  def __init__(self, wait, max_retries=9, init_timeout=10, timeout_max=60, timeout_step=5):
    self.wait = wait
    self.max_retries = max_retries
    self.init_timeout = init_timeout
    self.timeout_max = timeout_max
    self.timeout_step = timeout_step
    logger.info(json.dumps({"Requester-setttings":{"wait [s]":self.wait,
                                                   "timeout-min":self.init_timeout,
                                                   "timeout-max":self.timeout_max,
                                                   "timeout-step-increase":self.timeout_step,
                                                   "retries-max":self.max_retries}}))
  def request(self, req):
    retries = 0
    success = False
    req_timeout = self.init_timeout
    while success == False:
      wait = self.wait
      try:
        data = urllib.parse.urlencode(req.prepare_qry(), doseq=True).encode('utf-8')
        req.qry_url = data.decode()
        req.set_status_success()
        logger.debug(json.dumps({"Request":{"try":retries,"req-url":req.url,"qry-url":req.qry_url}}))
        return urllib.request.urlopen(urllib.request.Request(req.url, data=data), timeout=req_timeout)
      except urllib.error.URLError as url_err:
        log_msg = {"URL-error":{"code":url_err.code,"msg":url_err.reason}}
        req.set_request_error(url_err.reason)
        if url_err.code == 400: # Bad request form, we can stop right now
          logger.debug(json.dumps(log_msg["URL-error"].update({"action":"abort"})))
          sys.exit()
        logger.debug(json.dumps(log_msg["URL-error"].update({"action":"retry"})))
        retries += 1
        wait = 2
      except urllib.error.HTTPError as http_err:
        logger.debug(json.dumps({"HTTP-error":{"code":http_err.code, "msg":http_err.reason,"action":"retry"}}))
        retries += 1
        wait = 1
      except socket.timeout as timeout_err:
        req_timeout += self.timeout_step
        log_msg = {"Timeout-error":{"msg":"hit timeout","action":"retry", "wait":wait,
                                    "timeout": req_timeout,"increase":self.timeout_step}}
        logger.info(json.dumps(log_msg))
        if req_timeout > self.timeout_max:
          logger.info(json.dumps({"MaxTimeout-error":{"action":"giving up on this request","timeout": req_timeout}}))
          req.set_request_error("MaxTimeout")
          return None
      else:
        if retries > self.max_retries:
          logger.info(json.dumps({"MaxRetry-error":{"msg":"Reached max retries","action": "giving up on this request",
                                                    "retry": retries,"max":self.max_retries}}))
          req.set_request_error("MaxRetry")
          return None
        success = True
      time.sleep(wait)

  def fmt_log(self, msg):
    return json.dumps(msg)
