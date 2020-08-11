"""
..
  Copyright 2020 The University of Sydney
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

.. module:: classlogger

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import sys
import logging


import entrezpy.log.logger


def resolve_namespace(cls):
  """Resolves namespace for logger"""
  #return f"{entrezpy.log.logger.get_root()}.{cls.__module__}.{cls.__qualname__}"
  return f"{cls.__module__}.{cls.__qualname__}"


class ClassLogger:

  def __init__(self, cls=None, verbosity:int=0):
    if cls is None:
      sys.exit("Require class as parameter. Abort.")
    self.logger = logging.getLogger(resolve_namespace(cls))
    self.level = self.set_level(verbosity)
    print(self.level)
    print(self.logger)

  def set_level(self, verbosity):
    if verbosity == 0:
      self.logger.setLevel(0)
    elif verbosity == 1:
      self.logger.setLevel(20)
    else:
      self.logger.setLevel(10)
    return self.logger.isEnabledFor(self.logger.getEffectiveLevel())

  def log(self, msg):
    self.logger.debug(msg)
    #sys.exit()



