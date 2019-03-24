.. image:: https://readthedocs.org/projects/entrezpy/badge/?version=master
  :target: https://entrezpy.readthedocs.io/en/master/?badge=master
  :alt: Documentation Status

Entrezpy README
===============

Synopsis
--------

.. code::

  $ pip install entrezpy --user

>>> import entrezpy.wally
>>> w = entrezpy.wally.Wally('myemail')
>>> fetch_influenza = w.new_pipeline()
>>> sid = fetch_influenza.add_search({'db' : 'nucleotide', 'term' : 'H3N2 [organism] AND HA', 'rettype':'count', 'sort' : 'Date Released', 'mindate': 2000, 'maxdate':2019, 'datetype' : 'pdat'})
>>> fid = fetch_influenza.add_fetch({'retmax' : 10, 'retmode' : 'text', 'rettype': 'fasta'}, dependency=sid)
>>> w.run(fetch_influenza)

Entrezpy is a dedicated Python library to interact with NCBI_ Entrez
databases [Entrez2016]_ via the E-Utilities ([Sayers2018]_, E-Utilities_).
Entrezpy facilitates the implementation of queries to query or download data
from the Entrez databases, e.g. search for specific sequences or publications
or fetch your favorite genome. For more complex queries ``entrezpy`` offers the
class ``entrezpy.wally.Wally`` to run query pipelines or cache results.

Licence and Copyright
---------------------

``entrezpy`` is licensed under the `GNU Lesser General Public License v3
(LGPLv3)`_ or later. Please see https://www.ncbi.nlm.nih.gov/home/about/policies/
concerning the copyright of the material available through E-Utilities.


Installation
------------

**Entrezpy requires at least Python 3.6 and the Standars Python Library.**

PyPi
~~~~
Install ``entrezpy`` via PyPi and check:

.. code::

  $ pip install entrezpy --user

If you want to incude entrezpy as part of your pipeline, check the documentation
(https://entrezpy.readthedocs.io/en/master/setup/installation.html#append-to-sys-path)

Documentation
-------------

Entrezpy is fully documented using Spinx
(http://www.sphinx-doc.org/en/stable/). The manual, usage examples and module
reference can be found here: http://entrezpy.readthedocs.io/

References
----------

.. .. target-notes::

.. [Entrez2016] https://doi.org/10.1093/nar/gkw1071

.. [Sayers2018] https://www.ncbi.nlm.nih.gov/books/NBK25497

.. _NCBI: http://www.ncbi.nlm.nih.gov/

.. _GNU Lesser General Public License v3 (LGPLv3): https://www.gnu.org/licenses/lgpl-3.0.en.html

.. _E-Utilities: https://dataguide.nlm.nih.gov/eutilities/utilities.html
