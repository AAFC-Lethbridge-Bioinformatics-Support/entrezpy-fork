"""
..
  Copyright 2018, 2019 The University of Sydney
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

.. module:: entrezpy.epost.epost_analyzer
  :synopsis: Exports class EpostAnalzyer implementing the analysis of Epost
    query results.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json
import xml.etree.ElementTree

import entrezpy.base.analyzer
import entrezpy.epost.epost_result
import entrezpy.log.logger


class EpostAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """EpostAnalyzer implements the analysis of EPost responses from E-Utils.
  Epost puts UIDs onto the History server and returnes the corresponding
  WebEnv and QueryKey. Epost does only XML as response, therefore a dictionary
  imitating a JSON input is assembled and passed as result to
  :class:`entrezpy.epost.epost_result.EpostResult`
  """

  def __init__(self):
    super().__init__()
    self.logger = entrezpy.log.logger.get_class_logger(EpostAnalyzer)

  def init_result(self, response, request):
    """Implements :meth:`entrezpy.base.analyzer.EutilsAnalyzer.init_result` and
       inits :class:`entrezpy.epost.epost_result.EpostResult`.
    """
    if not self.result:
      self.result = entrezpy.epost.epost_result.EpostResult(response, request)

  def analyze_result(self, response, request):
    """Implements :meth:`entrezpy.base.analyzer.EutilsAnalyzer.analyze_result`.
      The response is one WebEnv and QueryKey and the result can be initiated
      after parsing them.

      :param response: EUtils response
      :param request: entrezpy request
    """
    epost_res = {}
    for event, elem in xml.etree.ElementTree.iterparse(response, events=["end"]):
      if event == 'end' and elem.tag == 'QueryKey':
        epost_res['querykey'] = int(elem.text)
      if event == 'end' and elem.tag == 'WebEnv':
        epost_res['webenv'] = elem.text
      elem.clear()
    self.init_result(epost_res, request)

  def analyze_error(self, response, request):
    """Implements :meth:`entrezpy.base.analyzer.EutilsAnalyzer.analyze_error`.

      :param response: EUtils response
      :param request: entrezpy request
    """
    error = None
    for _, elem in xml.etree.ElementTree.iterparse(response, events=["end"]):
      if elem.tag == 'ERROR':
        error = elem.text
        break
      elem.clear()
    self.logger.error(json.dumps({'tool':request.tool, 'error':error,
                                  'requestid':request.id, 'queryid':request.query_id,
                                  'request-dump':request.dump_internals()}))
