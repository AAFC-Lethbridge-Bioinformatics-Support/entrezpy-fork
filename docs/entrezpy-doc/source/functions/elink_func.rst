.. _elink:

Elink
=====

:class:`entrezpy.elink.elinker.Elinker` implements the E-Utility
`ELink` [#]_. Elink queries can link results

 - between different databases within :term:`Entrez`
 - earlier queries on the Entrez History server
 - to links outside :term:`NCBI` :term:`Entrez`, e.g. journal articles.

``Elinker`` queries return UIDs for data in the requested Entrez database or
WebEnv/QueryKey reference from the Entrez History server.

If an Elink query is part of a Wally pipeline, a search query has to run
uisng the Elink query as dependency to obtain the proper UIDs. See ::

Usage
-----
.. code::

  import entrezpy.elink.elinker.Elinker

  e = entrezpy.elink.elinker.Elinker(tool,
                                           email,
                                           apikey=None,
                                           apikey_var=None,
                                           threads=None,
                                           qid=None)
  analyzer = e.inquire{'dbfrom' : 'protein',
                       'db' : 'gene',
                       'id' : [15718680, 157427902]}

  .. print(analyzer.count, analyzer.retmax, analyzer.retstart, analyzer.uids)

``Elinker``
~~~~~~~~~~~~~

:class:`entrezpy.elink.elinker.Elinker`

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
:meth:`entrezpy.elink.elinker.Elinker.inquire` and are expected to be the
same as those for the E-Utility [0]. For example:

``{'db' : 'nucleotide', 'dbfrom' : 'protein, 'cmd' : 'neighbor'}``

``Elinker`` introduces one additional parameter ``link``. It forces Elinker to
create 1-to-many UID links.

.. note ::

  ``retmode : ref`` for the Elink command ``prlinks`` is not supported since
  this returns only the link outside Entrez databases.


=============   ==============    =====================================
Parameter                         Type
=============   ==============    =====================================
**E-Utility**
..              ``db``            ``str``
..              ``dbfrom``        ``str``
..              ``id``            ``list``
..              ``cmd``           ``str``
..              ``linkname``      ``str``
..              ``term``          ``str``
..              ``holding``       ``str``
..              ``term``          ``str``
..              ``datetype``      ``str``
..              ``reldate``       ``int``
..              ``reldate``       ``int``
..              ``mindate``       ``str`` (YYYY/MM/DD, YYYY/MM, YYYY)
..              ``maxdate``       ``str`` (YYYY/MM/DD, YYYY/MM, YYYY)
..              ``retmode``       ``str``
**Elinker**     ``link``          ``bool``
=============   ==============    =====================================

Elink linknames
~~~~~~~~~~~~~~~

Elink linknames allow to specifiy a subset from the linked database. This can
greatly incrase the spceificity of your link. By default, ``entrepy`` Elinker
uses linkname for the commands ``neighbor``, ``neighbor_history``, and
``neighbor_score``. If no linkname is given, the name of ``dbfrom`` and ``db``
are joined to ``dbfrom_db``.

For all possible linkname, refer to [#]_.

Result
------
Instance of :class:`entrezpy.elink.linkset.ElinkResult`.

Every results are stored as link sets :class:`entrezpy.elink.LinkSets.bare.Linkset`
which are either linked (:class:`entrezpy.elink.LinkSets.linked.LinkedLinkset`)
and store 1-to-many UID links  or relaxed
(:class:`entrezpy.elink.LinkSets.relaxed.RelaxedLinkset`), storing many-to-many
UID links.

Approach
--------

1. Parameters are checked and the request size is configured
2. Link is requested
3. If no errors were encountered, returns the analyzer with the link result


References
----------

.. [#] https://dataguide.nlm.nih.gov/eutilities/utilities.html#elink
.. [#] https://eutils.ncbi.nlm.nih.gov/entrez/query/static/entrezlinks.html
