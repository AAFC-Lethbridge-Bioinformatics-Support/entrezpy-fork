"""
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

.. module:: bare
   :synopsis: This module is part of entrezpy. It exports the bare Linkset for
              Elinker() results and handles the required linksetunits.

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

from entrezpy.elink.linkset.unit import neighbor
from entrezpy.elink.linkset.unit import neighbor_score
from entrezpy.elink.linkset.unit import neighbor_history
from entrezpy.elink.linkset.unit import linklist
from entrezpy.elink.linkset.unit import linkin
from entrezpy.elink.linkset.unit import linkout
from entrezpy.elink.linkset.unit import linkout_nonlib_attribute
from entrezpy.elink.linkset.unit import linkout_all_attribute
from entrezpy.elink.linkset.unit import linkout_provider

class LinkSet:
  """The LinkSet class implements the base class for all Elink result outputs.

  ELink reports relations between UIDs from a source database (dbfrom) and a
  target database (dbto), e.g. which UID from the 'gene' database corresponds
  to a protein sequence in the 'protein' database.

  The LinkSet class stores and return references to classes implementing the
  result of specific Elink commands, e.g. 'cmd=neighbor'. These are stored in
  link_linksets and list_linksets to help the ElinkAnalyzer use the proper
  parser.

  LinkSet instances store the information about a linked database as a
  LinkSetUnit instance in its linkunits list. LinkSet instances can occur in
  two categories: linked and relaxed.

    Linked represent one-to-many UID relationships where one UID links to
    several UIDs. This occurs when UID in the db parameter are concatenated by
    id, i.e. id=19880848&id=19822630. Elinker tries to use this behavior by
    default.

    Relaxed represent many-to-many relationships where several source UID are
    linked to several target uids. This occurs when UIDs in the db parameter
    are concatenated by commas, i.e. id=19880848,19822630. This can be forced
    by setting the Elinker parameter 'linked' to False.

  :param category: LinKSet category
  :type category: str
  :param dbfrom: name of database to link from
  :type dbfrom: str
  :param canLink: linkunits can be used for automated follow-up parameter
  :type canLink: boolean
  """

  link_linksets = {'neighbor' : neighbor.NeighborLinksetUnit,
                   'neighbor_score' : neighbor_score.NeighborScoreLinkset,
                   'neighbor_history' : neighbor_history.NeighborHistoryLinkset}

  list_linksets = {'acheck' : linklist.LinkList,
                   'ncheck' : linkin.LinkIn,
                   'lcheck' : linkout.LinkOut,
                   'llinks' : linkout_nonlib_attribute.LinkOutNonlibAttributes,
                   'llinkslib' : linkout_all_attribute.LinkOutAllAttribute,
                   'prlinks' : linkout_provider.LinkOutProvider}

  @staticmethod
  def new_unit(elink_cmd):
    """ Return reference to class implementing ELink command result unit."""
    if elink_cmd in LinkSet.link_linksets:
      return LinkSet.link_linksets[elink_cmd]
    if elink_cmd in LinkSet.list_linksets:
      return LinkSet.list_linksets[elink_cmd]
    return None

  def __init__(self, category, dbfrom, canLink):
    """Initiating a LinkSet with category, source database, and inidcate ability
      to generate automated follow-up parameters."""
    self.category = category
    self.db = dbfrom
    self.linkunits = []
    self.canLink = canLink

  def add_linkunit(self, lsetunit):
    """Store populated :class:`entrezpy.elink.linkset.unit.LinksetUnit`"""
    self.linkunits.append(lsetunit)

  def size(self):
    return len(self.linkunits)

  def base_dump(self):
    return {'dbfrom' : self.db, 'category' : self.category,
            'size' : self.size(), 'linkunits' : [x.dump() for x in self.linkunits]}

  def dump(self):
    """ Virtual function to dump attributes in derived instances."""
    raise NotImplementedError()
