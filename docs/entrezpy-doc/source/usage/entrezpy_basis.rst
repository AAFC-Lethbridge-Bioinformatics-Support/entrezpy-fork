Entrezpy architcture
=======================

Queries and requests
--------------------
Entrezpy queries are build from at least one request. A search for all virus
sequences in the Entrez database 'nucleotides' is one query and has one initial
request, the search itself. However, this search will return more UIDs than can
be fetched in one go and to obtain all UIDs, several requests are required.

Basic functions
---------------
Each function is a collection of inherited classes interacting with each other.
Each class implements a specific task of a query. The basic classes required for
an entrezpy query are found in src/entrezpy/entrezpy_base.

Entrezpy tasks describing a query
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error handling
--------------

Logging
-------

