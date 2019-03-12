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

.. module:: entrezpy.efetch.efetch_analyzer
  :synopsis: Exports the class EfetchAnalyzer implementing the analysis of
    Efetch Eutils results.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import json
import logging

import entrezpy.base.analyzer


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class EfetchAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
  """EfetchAnalyzer implements a basic analysis of Efetch E-Utils responses.
  Stores results in a :class:`entrezpy.efetch.efetch_result.EfetchResult`
  instance.

  .. note:: This is a very superficial analyzer for documentation and
  educational purposes. In almost all cases a more specific analyzer has to be
  implement in deriving :class:`entrezpy.efetch.efetch_analyzer.EfetchAnalzyer`
  and implementing :meth:`entrezpy.base.analyzer.EutilsAnalzyer.analyze_result`
  and :meth:`entrezpy.base.analyzer.EutilsAnalzyer.analyze_error`.
  """

  def __init__(self):
    """:ivar result: :class:`entrezpy.efetch.efetch_result.EfetchResult`"""
    super().__init__()
    self.result = None

  def analyze_result(self, response, request):
    if request.rettype == 'json':
      self.result += response
    else:
      self.result += response.getvalue()

  def analyze_error(self, response, request):
    logger.info(json.dumps({__name__:{'Response': {'dump' : request.dump(),
                                                   'error' : response}}}))

    logger.debug(json.dumps({__name__:{'Response-Error': {
                                       'request-dump' : request.dump_internals(),
                                       'error' : response}}}))
