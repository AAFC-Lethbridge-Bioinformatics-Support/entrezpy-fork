.. entrezpy documentation master file, created by
   sphinx-quickstart on Wed Feb 20 15:36:47 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Entrezpy: NCBI Entrez databases at your fingertips
====================================================

.. image:: https://img.shields.io/pypi/pyversions/entrezpy.svg?style=popout-square   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/l/entrezpy.svg?style=popout-square   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/v/entrezpy.svg?style=popout-square   :alt: PyPI

.. image:: https://img.shields.io/pypi/format/entrezpy.svg?style=popout-square   :alt: PyPI - Format

.. image:: https://img.shields.io/pypi/status/entrezpy.svg?style=popout-square   :alt: PyPI - Status

Synopsis
--------
.. code::

  $ pip install entrezpy --user

>>> import entrezpy.conduit
>>> c = entrezpy.conduit.Conduit('myemail')
>>> fetch_influenza = c.new_pipeline()
>>> sid = fetch_influenza.add_search({'db' : 'nucleotide', 'term' : 'H3N2 [organism] AND HA', 'rettype':'count', 'sort' : 'Date Released', 'mindate': 2000, 'maxdate':2019, 'datetype' : 'pdat'})
>>> fid = fetch_influenza.add_fetch({'retmax' : 10, 'retmode' : 'text', 'rettype': 'fasta'}, dependency=sid)
>>> c.run(fetch_influenza)

Entrezpy is a dedicated Python library to interact with NCBI_ :term:`Entrez`
databases [Entrez2016]_ via the E-Utilities [Sayers2018]_. Entrezpy facilitates
the implementation of queries to query or download data from the Entrez
databases, e.g. search for specific sequences or publiations or fetch your
favorite genome. For more complex queries ``entrezpy`` offers the class
:class:`entrezpy.conduit.Conduit` to run query pipelines or reuse previous queries.

Supported E-Utility functions:

 - :ref:`esearch`
 - :ref:`efetch`
 - :ref:`elink`
 - :ref:`epost`
 - :ref:`esummary`

Entrez pipeline design helper class:

 - :ref:`conduit_mod`

NCBI Entrez utilities and asociated parameters

 - https://dataguide.nlm.nih.gov/eutilities/utilities.html

Licence and Copyright
---------------------

``entrezpy`` is licensed under the `GNU Lesser General Public License v3
(LGPLv3)`_ or later.

Concerning the copyright of the material available through E-Utilities, please
read their disclaimer and copyright statement at
https://www.ncbi.nlm.nih.gov/home/about/policies/.



Source code
-----------

 - https://gitlab.com/ncbipy/entrezpy

::

  git clone https://gitlab.com/ncbipy/entrezpy.git

Contact
-------

To report bugs and/or errors, please open an issue at
https://gitlab.com/ncbipy/entrezpy or contact me at: jan.buchmann@sydney.edu.au

Of course, feel free to fork the code, improve it, and/or open a pull request.

.. _ncbi-apikey:

NCBI API key
------------

NCBI offers API keys to allow more requests per second. For more details and
rational see [Sayers2018]_. ``entrezpy`` checks for NCBI API keys as follows:

  - The NCBI API key can be passed as parameter to ``entrezpy`` classes
  - Entrezpy checks for the environment variable ``$NCBI_API_KEY``
  - The enviroment variable, e.g. ``NCBI_API_KEY``, can be passed via the
    ``apikey_var`` parameter to any derived
    :class:`entrezpy.base.query.EutilsQuery` class.

Work in progress
----------------

 - easier logging configuration via file

 - simplify Elink results

 - Deploy cleaner testing

 - Status indicating of request

References
----------

.. .. target-notes::

.. [Entrez2016] https://doi.org/10.1093/nar/gkw1071

.. [Sayers2018] https://www.ncbi.nlm.nih.gov/books/NBK25497

.. _NCBI: http://www.ncbi.nlm.nih.gov/

.. _GNU Lesser General Public License v3 (LGPLv3): https://www.gnu.org/licenses/lgpl-3.0.en.html


Manual
======

.. toctree::
  :maxdepth: 2

  setup/installation
  tutorials/tutorial

``Entrezpy`` E-Utility functions
================================

.. toctree::
  :maxdepth: 1
  :caption: Entrezpy functions

  functions/esearch_func
  functions/efetch_func
  functions/elink_func
  functions/esummary_func
  functions/epost_func

``Entrezpy`` In-depth
=====================
.. toctree::
  :maxdepth: 1
  :caption: Entrezpy In-depth

  indepth/entrezpy_basis
  indepth/eutils_entrezpy
  indepth/eutils_historyserver
  indepth/entrezdb


Reference
=========
.. toctree::
  :maxdepth: 2
  :caption: Entrezpy module references:

  module_references/base
  module_references/elink
  module_references/epost
  module_references/esearch
  module_references/efetch
  module_references/requester
  module_references/conduit


Glossary
========
.. toctree::
  :maxdepth: 0
  :caption: Glossary:

  glossary/glossary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
