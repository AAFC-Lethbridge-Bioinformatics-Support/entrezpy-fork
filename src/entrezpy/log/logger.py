"""
..
  Copyright 2018,2019,2020 The University of Sydney
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

.. module:: logger

  :synopsis:
    This module is part of entrezpy. It configures logging via Python's
    :mod:`logging`.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import time
import logging
import logging.config


import entrezpy.log.conf


def get_root():
  return 'entrezpy'

logging.config.dictConfig(entrezpy.log.conf.configure(get_root()))
#logger = logging.getLogger(get_root())
#logger = logging.getLogger(get_root())
