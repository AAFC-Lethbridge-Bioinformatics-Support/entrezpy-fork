#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \description: The EfetchRequest class which inherits entrezpy_base.request. It
#                assembles Efetch requests and stores the results.
#  \copyright 2017,2018 The University of Sydney
#-------------------------------------------------------------------------------

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../'))
import entrezpy_base.request

class EfetchRequest(entrezpy_base.request.EutilsRequest):

  def __init__(self, parameter, start, size):
    super().__init__('efetch', parameter.db)
    self.start = start
    self.size = size
    self.uids = parameter.uids[start:start+size]
    self.webenv = parameter.webenv
    self.querykey = parameter.querykey
    self.rettype = parameter.rettype
    self.retmode = parameter.retmode
    self.strand = parameter.strand
    self.seqstart = parameter.seqstart
    self.seqstop = parameter.seqstop
    self.complexity = parameter.complexity

  def prepare_qry(self):
    qry = self.prepare_base_qry()
    if self.retmode != None:
      qry.update({'retmode' : self.retmode})
    if self.rettype != None:
      qry.update({'rettype' : self.rettype})
    if self.strand != None:
      qry.update({'strand' : self.strand})
    if self.seqstart != None:
      qry.update({'seq_start' : self.seqstart})
    if self.seqstop != None:
      qry.update({'seq_stop' : self.seqstop})
    if self.complexity != None:
      qry.update({'complexity' : self.complexity})

    if self.webenv and self.querykey:
      qry.update({'WebEnv' : self.webenv, 'query_key' : self.querykey,
                  'retstart' : self.start,'retmax' : self.size})
    else:
      qry.update({'id' : ','.join(str(x) for x in self.uids)})
    return qry

  def get_request_info(self):
    return {'db' : self.db,
            'uids' : self.uids,
            'num_uids' : len(self.uids),
            'webenv' : self.webenv,
            'querykey' : self.querykey,
            'rettype' : self.rettype,
            'retmode' :self.retmode,
            'retmax' : self.size,
            'retstart' : self.start,
            'strand' : self.strand,
            'seqstart' : self.seqstart,
            'seqstop' : self.seqstop,
            'complexity' : self.complexity}

  def get_observation(self):
    cols = [self.query_id, self.id, self.start, self.size, self.status, self.duration]
    if self.request_error != None:
      cols.append(self.request_error)
    return '\t'.join(str(x) for x in cols)
