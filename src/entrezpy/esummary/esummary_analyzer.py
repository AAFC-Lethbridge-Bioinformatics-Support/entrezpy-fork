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

.. module:: entrezpy.esummary.esummary_analyzer
   :synopsis: Exports class EsummaryAnalyzer implementing entrezpy Esummary
    queries to NCBI E-Utility Esummary

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import io
import os
import sys
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import entrezpy.base.analyzer
import entrezpy.esummary.esummary_result

class EsummaryAnalzyer(entrezpy.base.analyzer.EutilsAnalyzer):

  def __init__(self):
    super().__init__()
    self.result = None

  def analyze_result(self, response, request):
    if not self.result:
      self.result = entrezpy.esummary.esummary_result.EsummaryResult(db=request.db,
                                                   querykey=request.querykey,
                                                   webenv=request.webenv)
    self.result.uids += response['result']['uids']
    for i in response['result']['uids']:
      self.result.add_summary(i, response['result'])
    response.pop('result')

  def analyze_error(self, response, request):
    if 'error' in response:
      self.error = response['error']
    if 'esummaryresult' in response:
      self.error = response['esummaryresult']
    logger.info(json.dumps({__name__:{"Response-Error":
                                        {
                                          "tool": request.tool,
                                          "request-id": request.id,
                                          "query-id":request.query_id,
                                          "error": self.error
                                        }}}))
    logger.debug(json.dumps({__name__:{"Response-Error":
                                        {
                                          "tool": request.tool,
                                          "request-id": request.id,
                                          "query-id":request.query_id,
                                          "error": self.error,
                                          "request-dump":request.dump_internals()
                                        }}}))
