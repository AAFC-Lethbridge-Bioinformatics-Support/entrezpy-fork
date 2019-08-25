.. _tutorials:

Entrezpy tutorials
==================

.. _tutorialesearch:

Esearch
-------

Esearch searches the specified Entrez database for data records matching the
query. It can return the found UIDs or a WebEnv/query_key referencing for the
UIDs

.. toctree::
  :maxdepth: 2

  esearch/esearch_uids
  esearch/esearch_histserv


.. _tutorialconduit:

Conduit
-------

The Conduit module facilitates creating pipelines to link individual Eutils
request, i.e. linking the results of an Esearch to the corresponding  nucleotide
data records.

.. toctree::
  :maxdepth: 2

  conduit/pipeline
  conduit/linking



Extending ``entrezpy``
----------------------

``entrezpy`` can be extended by inheriting its base classes. This will be the
case when the final step is to fetch data records and do something with them,
e.g. processing them for a database or parsing for specific information.

.. toctree::
  :maxdepth: 2

  extending/pubmed


