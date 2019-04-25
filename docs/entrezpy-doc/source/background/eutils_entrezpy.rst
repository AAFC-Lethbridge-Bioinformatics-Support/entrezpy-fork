E-Utilities by ``entrezpy``
===========================

``Entrezpy`` assembles POST parameters [#]_, [#]_, creates the correspondong
requests to interact with the E-Utilities, and reads the received responses.
Entrezpy implements E-Utility functions as queries consisting of at least one
request:

.. code::

        Query
  +...............+
  |               |
  0 1 2 3 4 5 6 7 8
  |     | |     | |
  +-----+ +-----+ +
     R0     R1    R2
      \     |     /
       +----+----+
            |
            v
 entrezpy.base.analyzer.EutilsAnalyzer()

The example depicts the relation  between a query and requests in Entrepy.
The example query consists of 9 data records. Using a request size of 4 data
records, ``Entrezpy`` resolves this query using two requests (R0 - R1) with the
given size and adjusts the size of the last query (R2).

Each query passes all request and responses through the same instance of its
corresponding :class:`entrezpy.base.analyzer.EutilsAnalyzer`. The ``analyzer``
can be passed as argument to each entrezpy query. Each request is analyzed as
soon as it is received. The ``analzyer`` base class
:class:`entrezpy.base.analyzer.EutilsAnalyzer` can be inherited and adjusted
for specific formats or tasks

Entrezpy offers default analzyers, but most likely you want, or have to,
implement a specific Efetche analzyer. You can use
:class:`entrezpy.efetch.efetch_analyzer.EfetchAnalyzer` as template.

References
----------

.. [#] https://en.wikipedia.org/wiki/POST_(HTTP)

.. [#] https://tools.ietf.org/html/rfc7231#section-4.3.3
