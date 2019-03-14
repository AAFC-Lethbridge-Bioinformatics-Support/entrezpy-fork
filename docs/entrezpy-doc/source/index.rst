.. entrezpy documentation master file, created by
   sphinx-quickstart on Wed Feb 20 15:36:47 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Entrezpy: NCBI's Entrez databases at your fingertips
====================================================

Synopsis
========
Entrezpy is a dedicated Python library to interact with NCBI's Entrez databases
via the E-Utilities. Entrezpy faciliatets to create either single queries, e.g.
search for specific sequences or publiations, fetch your favorite sequence.
In addition, a helper class helps to craeta more complex queries which can be
run in an analogous fashion to piping on the commanbd line.

Supported E-Utility functions:

 - Esearch
 - Efetch
 - Epost
 - Elink
 - Esummary

>>> import entrezpy
>>> e = entrezpy.efetch.efetcher.Efetcher('efetcher', 'you@email')
>>> a = e.inquire({'db': 'nucleotide', 'id': [5], 'rettype':'fasta'})

Manual
======

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  setup/installation
  usage/eutils_functions
  usage/examples
  usage/entrezpy_basis
  background/entrezdb

Adjusting
=========


Module reference
================
.. toctree::
  :maxdepth: 1

  module_references/base
  module_references/elink
  module_references/epost
  module_references/esearch
  module_references/efetch
  module_references/requester


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
