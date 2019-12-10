.. _esummary:

Esummary
========

:class:`entrezpy.esummary.esummarizer.Esummarizer` implements the E-Utility
`ESummary` [0]_. `Esummarizer` fetches document summaries for UIDs in the
requested database. Summaries can contain abstracts, experimental details, etc

Usage
-----
.. code::

  import entrezpy.esummary.esummarizer

  e = entrezpy.esummary.esummarizer.Esummarizer(tool,
                                                email,
                                                apikey=None,
                                                apikey_var=None,
                                                threads=None,
                                                qid=None)

  analyzer = e.inquire('db' : 'pubmed', 'id' : [11850928, 11482001])
  print(analyzer.get_result().summaries)

``Esummarizer``
~~~~~~~~~~~~~~~

:class:`entrezpy.esummary.esummarizer.Esummarizer`

 :param str tool: string with no internal spaces uniquely identifying the
                  software producing the request, i.e. your tool/pipeline.
 :param str email: a complete and valid e-mail address of the software developer
                   and not that of a third-party end user. ``entrezpy`` is a
                   library, not a tool.
 :param str apikey:     :ref:`ncbi-apikey`
 :param str apikey_var: :ref:`ncbi-apikey`
 :param int threads:    number of threads
 :param str qid:        Unique Esummary query id. Will be generated if not given.

Supported E-Utility parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parameters are passed as dictionary to
:meth:`entrezpy.esummary.esummarizer.Esummarizer.inquire` and are expected to be the
same as those for the E-Utility [0]. For example:

``{{'db' : 'pubmed','id' : [11237011,12466850]}``

=============   ==============    =====================================
Parameter                         Type
=============   ==============    =====================================
**E-Utility**
..              ``db``            ``str``
..              ``id``            ``list``
..              ``WebEnv``        ``string``
..              ``retstart``      ``int``
..              ``retmax``        ``int``
..              ``retmode``       JSON, enforced by ``entrezpy``
=============   ==============    =====================================

Not supported E-Utility parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
=============   ==============    =====================================
Parameter                         Type
=============   ==============    =====================================
**E-Utility**
..              ``retmode``       JSON, enforced by ``entrezpy``
..              ``version``       XML specific parameter
=============   ==============    =====================================

Result
------
Instance of :class:`entrezpy.esummary.esummary_result.EsummaryResult`.

If ``retmax`` = 0 or ``retmode`` = ``count`` no :term:`UIDs` are returned. If
``usehistory`` is ``True`` (default), :term:`WebEnv` and :term:`query_key` for
the request is returned.


- :attr:`count`     : number of found :term:`UIDs` for request
- :attr:`retmax`    : number of :term:`UIDs` to retrieve
- :attr:`retstart`  : number of first :term:`UID` to retrieve
- :attr:`uids`      : list of fetched :term:`UIDs`

Approach
--------

#. Parameters are checked and the request size is configured
#. UIDs are posted to NCBI
#. If no errors were encountered, returns the analyzer with the result storing
   the WebEnv and query_key for the UIDs.

References
----------

.. [0] https://dataguide.nlm.nih.gov/eutilities/utilities.html#esummary
