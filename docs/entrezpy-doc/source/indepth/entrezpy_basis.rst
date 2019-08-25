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
an entrezpy query are found in ``src/entrezpy/base`` of the repository.

Each query starts with passing E-Utils parameters as dictionary into the
``iquire`` method of the query, which are derived from
:meth:`entrezpy.base.query.EutilsQuery.inquire`.

The first step in :meth:`inquire` is to instantiate a parameter object derived
from :class:`entrezpy.base.parameter.EutilsParameter`.
The parameters get checked for errors and if none are found, an instance of
:class:`entrezpy.base.parameter.EutilsParameter` is returned. The attributes of
:class:`entrezpy.base.parameter.EutilsParameter` configure the query and the
required number of :class:`entrezpy.base.request.EutilsRequest` is added to the
queue.

Each request is sent to the corresponding  E-Utility and its response received
. All responses from within a query are analyzed by the same instance of a
:class:`entrezpy.base.analzyer.EutilsAnalyzer`. The analyzer stores results in
an instance of :class:`entrezpy.base.result.EutilsResult`.


Error handling
--------------

The primary approach of ``entrezpy`` is abort if an error has be been
encountered since it's not known what the developer had in mind when deploying
``entrezpy``.

``entrezpy`` aborts if :

  - errors are found in the parameters
  - HTTP error 400

``entrezpy`` continues, but warns, if:

  - empty result
  - after 10 retries to obtain request

Logging
-------

WIP
