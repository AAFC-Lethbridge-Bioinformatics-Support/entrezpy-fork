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
  :synopsis: This module configures logging via Python's :mod:`logging`.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import time
import logging
import logging.config


import entrezpy.log.conf


CONFIG = {'level':'INFO', 'quiet':True, 'propagate':True}
"""Store logger settings"""

def get_root():
  """Returns the module root"""
  return 'entrezpy'

def resolve_class_namespace(cls):
  """Resolves namespace for logger"""
  return f"{cls.__module__}.{cls.__qualname__}"

def get_class_logger(cls):
  """Prepares logger for given class """
  logger = logging.getLogger(f"{cls.__module__}.{cls.__qualname__}")
  logger.propagate = CONFIG['propagate']
  if CONFIG['quiet'] is True:
    logger.addHandler(logging.NullHandler())
    return logger
  logging.config.dictConfig(entrezpy.log.conf.default_config)
  logger.setLevel(CONFIG['level'])
  return logger

def set_level(level):
  """Sets logging level for applications using entrezpy."""
  CONFIG['level'] = level
  CONFIG['quiet'] = False
