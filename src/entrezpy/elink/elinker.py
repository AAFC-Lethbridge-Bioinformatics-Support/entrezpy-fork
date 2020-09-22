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

.. module:: elinker
   :synopsis: Exports ELinker class implementing Elink queries.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import json


import entrezpy.base.query
import entrezpy.elink.elink_parameter
import entrezpy.elink.elink_request
import entrezpy.elink.elink_analyzer
import entrezpy.log.logger


class Elinker(entrezpy.base.query.EutilsQuery):
  """Elinker implements elink queries to E-Utilities [0].
  Elinker implements the inquire() method to link data sets on NCBI Entrez
  servers. All parameters described in [0] are acccepted. Elink queries consist
  of one request linking UIDs or an earlier requests on the history server
  within the same or different Entrez database. [0]:
  https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink

  :param str tool: tool name
  :param str email: user email
  :param str apikey: NCBI apikey
  :param str apikey_var: enviroment variable storing NCBI apikey
  :param int threads: set threads for multithreading
  :param str qid: unique query id
  """

  def __init__(self, tool, email, apikey=None, apikey_var=None, threads=None, qid=None):
    super().__init__('elink.fcgi', tool, email, apikey=apikey, threads=threads, qid=qid)
    self.logger = entrezpy.log.logger.get_class_logger(Elinker)
    self.logger.debug(json.dumps({'init':self.dump()}))

  def inquire(self, parameter, analyzer=entrezpy.elink.elink_analyzer.ElinkAnalyzer()):
    """ Implements virtual function inquire()

      1. Prepares parameter instance :class:`entrezpy.elink.elink_parameter.ElinkerParameter`
      2. Starts threading monitor :func:`monitor_start`
      3. Adds ElinkRequests to queue :func:`add_request`
      4. Runs and analyzes all requests
      5. Checks for errors :func:`check_requests`

    :param dict parameter: ELink parameter
    :param analyzer analyzer: analyzer for Elink Results, default is
      :class:`entrezpy.elink.elink_analyzer.ElinkAnalyzer`
    :return: analyzer  or None if request errors have been encountered
    :rtype: :class:`entrezpy.base.analyzer.EntrezpyAnalyzer` instance or None
    """
    p = entrezpy.elink.elink_parameter.ElinkParameter(parameter)
    self.logger.debug(json.dumps({'parameter':p.dump()}))
    self.monitor_start(p)
    self.add_request(entrezpy.elink.elink_request.ElinkRequest(self.eutil, p), analyzer)
    self.request_pool.drain()
    self.monitor_stop()
    if self.isGoodQuery():
      return analyzer
    return None
