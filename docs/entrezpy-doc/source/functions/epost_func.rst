.. _epost:

Epost
=====

:class:`entrezpy.epost.eposter.Eposter` implements the E-Utility
`EPost` [0]_. `Eposter` queries post UIDs onto the Entrez History server
and return the corresponding WebEnv and query_key. If an exisitng ``WebEnv`` is
passed as parameter, the posted  UIDs will be added to this ``WebEnv`` by
increasing its ``query_key``.

Usage
-----
.. code::

  import entrezpy.epost.eposter

  e = entrezpy.epost.eposter.Eposter(tool,
                                     email,
                                     apikey=None,
                                     apikey_var=None,
                                     threads=None,
                                     qid=None)

  analyzer = e.inquire({'db' : 'pubmed','id' : [12466850])
  print(analyzer.get_result().get_link_parameters())

``Eposter``
~~~~~~~~~~~~~

:class:`entrezpy.epost.eposter.Eposter`

 :param str tool: string with no internal spaces uniquely identifying the
                  software producing the request, i.e. your tool/pipeline.
 :param str email: a complete and valid e-mail address of the software developer
                   and not that of a third-party end user. ``entrezpy`` is a
                   library, not a tool.
 :param str apikey:     :ref:`ncbi-apikey`
 :param str apikey_var: :ref:`ncbi-apikey`
 :param int threads:    number of threads
 :param str qid:        Unique Epost query id. Will be generated if not given.

Supported E-Utility parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parameters are passed as dictionary to
:meth:`entrezpy.epost.eposter.Eposter.inquire` and are expected to be the
same as those for the E-Utility [0]. For example:

``{{'db' : 'pubmed','id' : [11237011,12466850]}``

=============   ==============    =====================================
Parameter                         Type
=============   ==============    =====================================
**E-Utility**
..              ``db``            ``str``
..              ``id``            ``list``
..              ``WebEnv``        ``string``
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
2. UIDs are posted to NCBI
4. If no errors were encountered, returns the analyzer with the result storing
   the WebEnv and query_key for the UIDs.

References
----------

.. [0] https://dataguide.nlm.nih.gov/eutilities/utilities.html#epost
