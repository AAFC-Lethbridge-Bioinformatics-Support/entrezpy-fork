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

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import os
import time
import json

default_config = {
  'disable_existing_loggers': False,
  'version': 1,
  'formatters':
  {
    'default':
    {
      'format': '%(asctime)s %(threadName)s [%(levelname)s] %(name)s: %(message)s'
    },
  },
  'handlers':
  {
    'console':
    {
      'class': 'logging.StreamHandler',
      'stream' : 'ext://sys.stderr',
      'formatter': 'default'
    }
  },
  'loggers':
  {
    '':
    {
      'handlers': ['console']
    }
  }
}
