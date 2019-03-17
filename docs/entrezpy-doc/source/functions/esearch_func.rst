.. _esearch:

Esearch
=======

:class:`entrezpy.esearch.esearcher.Esearcher` implements the E-Utility
`ESearch` [0]_. `Esearcher` queries return UIDs for data in the requested
Entrez database or WebEnv/QueryKey references from the Entrez History server.


Usage
-----
.. code::

  import entrezpy.esearch.esearcher.Esearcher

  e = entrezpy.esearch.esearcher.Esearcher(tool,
                                           email,
                                           apikey=None,
                                           apikey_var=None,
                                           threads=None,
                                           qid=None)
  analyzer = e.inquire({'db' : 'pubmed',
                        'id' : [17284678, 9997],
                        'retmode' : 'text',
                        'rettype' : 'abstract'})
  print(analyzer.count, analyzer.retmax, analyzer.retstart, analyzer.uids)

``Esearcher``
~~~~~~~~~~~~~

:class:`entrezpy.esearch.esearcher.Esearcher`

 :param str tool: string with no internal spaces uniquely identifying the
                  software producing the request, i.e. your tool/pipeline.
 :param str email: a complete and valid e-mail address of the software developer
                   and not that of a third-party end user. ``entrezpy`` is this
                   is a library, not a tool.
 :param str apikey:     :ref:`ncbi-apikey`
 :param str apikey_var: :ref:`ncbi-apikey`
 :param int threads:    number of threads
 :param str qid:        Unique Esearch query id. Will be generated if not given.

Supported E-Utility parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parameters are passed as dictionary to
:meth:`entrezpy.esearch.esearcher.Esearcher.inquire` and are expected to be the
same as those for the E-Utility [0]. For example:

``{'db' : 'nucleotide', 'term' : 'viruses[orgn]', 'reqsize' : 100, 'retmax' : 99, 'idtype' : 'acc'}``

``Esearcher`` introduces one additional parameter ``reqsize``. It sets the size
of a request. Numbers grater than the maximum allowed by NCBI will be set to
the maximum.

=============   ==============    =====================================
Parameter                         Type
=============   ==============    =====================================
**E-Utility**
..              ``db``            ``str``
..              ``WebEnv``        ``str``
..              ``query_key``     ``int``
..              ``uilist``        ``bool``
..              ``retmax``        ``int``
..              ``retstart``      ``int``
..              ``usehistory``    ``bool``
..              ``term``          ``str``
..              ``sort``          ``str``
..              ``field``         ``str``
..              ``reldate``       ``int``
..              ``datetype``      ``str`` (YYYY/MM/DD, YYYY/MM, YYYY)
..              ``mindate``       ``str`` (YYYY/MM/DD, YYYY/MM, YYYY)
..              ``maxdate``       ``str`` (YYYY/MM/DD, YYYY/MM, YYYY)
..              ``idtype``        ``bool``
..              ``retmode``       ```json``,  enforced by ``Esearcher``
**Esearcher**   ``reqsize``       ``int``
=============   ==============    =====================================


Result
------
Instance of :class:`entrezpy.esearch.esearch_result.EsearchResult`.

If ``retmax`` = 0 or ``retmode`` = ``count`` no :term:`UIDs` are returned. If
``usehistory`` is ``True`` (default), :term:`WebEnv` and :term:`query_key` for
the request is returned.


- :attr:`count`     : number of found :term:`UIDs` for request
- :attr:`retmax`    : number of :term:`UIDs` to retrieve
- :attr:`retstart`  : number of first :term:`UID` to retrieve
- :attr:`uids`      : list of fetched :term:`UIDs`

Approach
--------

1. Parameters are checked and the request size is configured
2. Initial search is requested
3. If more search requests are required, Parameter is adjusted and the
   remaining requests are done
4. If no errors were encountered, returns the analyzer with the result for all
   requests

References
----------

.. [0] https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
