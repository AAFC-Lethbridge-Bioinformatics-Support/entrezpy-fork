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

.. module:: entrezpy.elink.linkset.unit.linkin
   :synopsis:
    Exports class LinkIn impelementing Elink results for acheck command.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

import entrezpy.elink.linkset.unit.linksetunit

class LinkIn(entrezpy.elink.linkset.unit.linksetunit.LinksetUnit):
  """
  Inits new link result unit for the acheck command.

  :param str dbto: name of target database
  :param str hasneighbor: Y or N indicating if the linked UID has outgoing
  links.
  """

  @classmethod
  def new(cls, dbto, hasneighbor):
    """
    Returns new instance.

    :rtype: `entrezpy.elink.linkset.unit.linksetunit.linkin.LinkIn`
    """
    return cls(dbto, hasneighbor)

  def __init__(self, dbto, hasneighbor):
    super().__init__(dbto, None)
    self.hasneighbor = bool(hasneighbor == 'Y')

  def dump(self):
    return dict({'hasneighbor' : self.hasneighbor}, **self.basic_dump())
