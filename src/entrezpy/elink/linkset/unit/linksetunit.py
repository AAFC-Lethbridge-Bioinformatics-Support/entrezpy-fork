# Copyright 2018, 2019 The University of Sydney
# This file is part of entrezpy.
#
#  Entrezpy is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Entrezpy is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with entrezpy.  If not, see <https://www.gnu.org/licenses/>.
"""
.. module:: linksetunit
   :synopsis: This module is part of entrezpy. It exports the basic LinksetUnit
              for LinkSet().

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


class LinksetUnit:
  """
  The LinksetUnit class implements the base class for all LinksetUnits.
  LinksetUnits atore the information for UIDs linked to one or several source
  UIDs. LinksetUnit instances are handled by LinkSet instances. Almost all
  LinksetUnits have a dbto and linkname parameter. Some exceptions exists and
  these parameters are than set to None.

  :param str dbto: name of linked database
  :param str linkname: linkname
  """
  def __init__(self, dbto, linkname):
    """Inits LinksetUnit instance with the linked database name and linkname
    :attribute str dbto: name of target database
    """
    self.db = dbto
    self.linkname = linkname

  def dump(self):
    """ Virtual function to dump attributes in derived instances.

      :return: dict -- all attributes of LinksetUnit instance
    """
    raise NotImplementedError()

  def basic_dump(self):
    """
      :return: dict -- all basis attributes of LinksetUnit instance
    """
    return {'dbto' : self.db, 'linkname' : self.linkname}
