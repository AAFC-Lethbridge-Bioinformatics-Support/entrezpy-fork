.. _docsumtut:
Fetching sequence metadata from Entrez
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. topic:: Prerequisites

  * Python 3.6 or higher is assumed.
  * |entrezpy| is either installed via PyPi or cloned from the ``git``
    repository  (:ref:`install`).
  * basic familiarity with `object oriented Python <oopython_>`_, i.e. inheritance
  * read the tutorial :ref:`pubmedtut`
  * The full implementation can be found in the repository at
    `examples/tutorials/seqmetadata/seqmetadata-fetcher.py <implement>`_

.. topic:: Acknowledgment

  I'd like to thank <contib> for proposing this scenario.

Overview
++++++++

This tutorial explains how to write a simple sequence docsum fetcher using
|Conduit| and by adjust |EutilsResult| and |EutilsAnalyzer|. It is based on a
esearch followed by fetching the data as docsum JSON. This tutorial is very
similar as :ref:`pubmedtut`, the main difference being parsing JSON and using
two steps in |Conduit|. The main steps are very similar and the reader is should
look there for more details.

.. topic:: Outline

  * develop a |Conduit| pipline
  * implement a |Docsum| data structure
  * inherit |EutilsResult| and |EutilsAnalyzer|
  * implement the required virtual methods
  * add methods to derived classes

The `Efetch Entrez Utility <eutils_>`_ is NCBI's utility responsible for
fetching data records. Its `manual <eutils_>`_ lists all possible databases and
which records (Record type) can be fetched in which format. We'll fetch
|docsum| data in JSON after performing an ``esearch`` step using accessions
numbers as query.

In |entrezpy|, a result (or query), is the sum of all individual requests
required to obtain the whole query. ``efetch`` fetches data in batches. In this
example, all batches are collected prior to printing the infomration to standard
output. The method :meth:`DocsumAnalyzer.analyze_result` can be adjusted to
store or analyze the results from each batch as soon as the are fetched.

.. _virtualmethod:
.. rubric:: A quick note on virtual functions

|entrezpy| is heavily based on virtual methods [#fn_wpvf]_. A virtual method is
declared in the the base class but implemented in the derived class. Every
class inheriting the base class has to implement the virtual functions using
the same signature and return the same result type as the base class. To
implement the method in the inherited class, you need to look up the method in
the base class.

|docsum| data structure
+++++++++++++++++++++++

Before we start to write our implementation, we need to understand the
structure of the received data. This can be done using the `EDirect tools
<edirect_>`_ from NCBI. The result is printed to the standard output. For its
examination, it can be either stored into a file, or preferably, piped to a
pager, e.g. ``less`` [#fn-less]_ or ``more`` [#fn-more]_. These are usually
installed on most \*NIX systems.

.. code-block:: bash
  :caption: Fetching |docsum| data record for accession HOU142311 using EDirect's
            ``esearch`` and ``efetch``.
  :name: docsum-tut-efetch-example

  $ esearch -db nuccore -query HOU142311 | efetch -format docsum -mode json

The entry should start and end as shown in :numref:`Listing %s <26378223-xml-example>`.

.. literalinclude:: HOU142311.json
  :language: json
  :caption: JSON |docsum| data record for accession HOU142311. Only the first
            few attributes lines are shown for brevity.
  :name: docsum-json-example
  :linenos:
  :lines: 1-38, 140-

The first step is to write a program to fetch the requested records. This can
be done using the |Conduit| class.

Simple Conduit pipeline to fetch |docsum| Records
+++++++++++++++++++++++++++++++++++++++++++++++++

We will write simple |entrezpy| pipeline named ``seqmetadata-fetcher.py`` using
|Conduit| to test and run our implementations. A simple |Conduit| pipeline
requires two arguments:

  * user email
  * accession numbers


.. literalinclude:: ../../../../../examples/tutorials/seqmetadat/seqmetadata-fetcher.py
  :caption: Basic |Conduit| pipeline to fetch |docsum| data records. The required
            arguments are parsed by ArgumentParser.
  :linenos:
  :language: python
  :name: basic-conduit
  :lines: 1,33-50, 173-194

* Lines 1-17:  import standard Python libraries and ``entrezpy`` modules
* Lines 21-35: Setup argument parser
* Line 37:  create new |Conduit| instance with an email address.
* Line 38:  New pipeline instance :meth:`entrezpy.conduit.Conduit.new_pipeline`
* Line 39:  add search request to the  pipeline with the databse name from the
            user passed argument and a search strin assembled from standard
            input. Store the query id in ``sid``.
            :meth:`entrezpy.conduit.Conduit.Pipeline.add_search`
* Line 40   add summary step with the search query as dependency.
            (:meth:`entrezpy.conduit.Conduit.Pipeline.add_summary`)
* Line 22:  run pipeline using :meth:`entrezpy.conduit.Conduit.run`

We need to implement the DocsumAnalyzer, but before we have to design a |docsum|
data structure.

How to store |docsum| data records
++++++++++++++++++++++++++++++++++

The data records can be stored in different ways, but using a class  facilitates
collecting and retrieving the requested data. We implement a simple class
(analogous to a C/C++ struct [#fn-struct]_) to represent a |pubmed| record.

.. literalinclude:: ../../../../../examples/tutorials/seqmetadat/seqmetadata-fetcher.py
  :caption: Implementing a |docsum| data record
  :name: lst:pmed-datrec
  :linenos:
  :language: python
  :lines: 51-98



Defining |PubmedResult| and |PubmedAnalyzer|
++++++++++++++++++++++++++++++++++++++++++++

From the documentation or publication, we know that |EutilsAnalyzer| parses
responses and stores results in |EutilsResult|. Therefore, we need to derive
and adjust these classes for our |PubmedResult| and |PubmedAnalyzer|
classes. We will add these classes to our program ``pubmed-fetcher.py``. The
documentation tells us what the required parameters for each class are and the
virtual methods we need to implement.

Implement |PubmedResult|
........................

We have to extend the :ref:`virtual methods  <virtualmethod>` declared in
|EutilsResult|. The documentation informs us about the required parameters and
expected return values.

In addition, we declare the method :meth:`PubmedResult.add_pubmed_record` to
handle adding new |pubmed| data record instances as defined in
:numref:`Listing %s <lst:pmed-datrec>`. The |PubmedResult| methods in this
tutorial are trivial since and we can implement the class in onw go

.. literalinclude:: ../../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :caption: Implementing |PubmedResult|
  :linenos:
  :language: python
  :lines: 64-110
  :emphasize-lines: 1, 10, 14, 19, 26, 33, 43

* Line 1: inherit the base class |EutilsResult|
* Line 10-12: initialize |PubmedResult| instance with the required
    parameters and attributes. We don't need any information from the
    response, e.g. WebEnv.
* Line 14-17: implement :meth:`entrezpy.base.result.EutilsResult.size`
* Line 19-24: implement :meth:`entrezpy.base.result.EutilsResult.isEmpty`
* Line 26-31: implement :meth:`entrezpy.base.result.EutilsResult.get_link_parameter`
* Line 33-41: implement :meth:`entrezpy.base.result.EutilsResult.dump`
* Line 43-46: specific |PubmedResult| method to store individual |PubmedRecord|
    instances

.. note:: Linking |pubmed| records for subsequent searches is better handled by
  creating a pipeline performing ``esearch`` queries followed by ``elink``
  queries and a final ``efetch`` query. The fetch result for |pubmed| records
  has no WebEnv value and is missing the originating database since ``efetch``
  is usually the last query within a series of ``Eutils`` queries. You can test
  this using the following EDirect pipeline:
  ``$ efetch -db pubmed -id 20148030 | elink -target nuccore``
  Therefore, we implement a warning, informing the user linking is not
  possible. Nevertheless, the method could return any parsed information, e.g.
  nucleotide UIDs, and used as parameter for a subsequent fetch. However, some
  features could not be used, e.g. the Entrez ``history`` server.

Implementing |PubmedAnalyzer|
.............................

We have to extend the :ref:`virtual methods  <virtualmethod>` declared in
|EutilsAnalyzer|. The documentation informs us about the required parameters
and expected return values.

.. literalinclude:: ../../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :caption: Implementing |PubmedAnalyzer|
  :linenos:
  :language: python
  :lines: 111-191
  :emphasize-lines: 1, 5, 8, 14, 21

* Line 1: Inherit the base class |EutilsAnalyzer|
* Lines 5-6: initialize |PubmedResult| instance.
* Lines 8-12: declare :meth:`entrezpy.base.analyzer.EutilsAnalyzer.init_result`
* Lines 14-19: decalre :meth:`entrezpy.base.analyzer.EutilsAnalyzer.analyze_error`
* Lines 21-69: declare :meth:`entrezpy.base.analyzer.EutilsAnalyzer.analyze_result`

The XML parser is the critical, and most likely most complex, piece to
implement. However, if you want to parse your Entrez results you anyway need to
develop a parser. If you already have a parser, you can use an object
composition approach [#fn-oocomp].
Further, you can add a method in ``analyze_result`` to store the processed
data in a database or implementing checkpoints.

.. note:: Explaining the XML parser is beyond the scope of this tutorial
          (and there are likely better approaches, anyways).

Putting everything together
+++++++++++++++++++++++++++

The completed implementation is shown in :numref:`Listing %s <pubmed-fetcher>`.

.. literalinclude:: ../../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :caption: Complete |pubmed| fetcher to extract author and citations.
  :name: pubmed-fetcher
  :linenos:
  :language: python
  :lines: 1,34-
  :emphasize-lines: 163,164,166, 168-172,174-181

* Line 163: Adjust argumetn processing to allow several comma-separarted PMIDs
* Line 164: add our implemented |PubmedAnalyzer| as parameter to analzye
            results as described in :meth:`entrezpy.conduit.Conduit.Pipeline.add_fetch`
* Line 166: run the pipeline and store the analyzer in ``a``
* Lines 168-172: Testing mthods
* Line 174: get |PubmedResult| instance
* Lines 175-181: process fetched data records into columns

The implementaion can be invoked as shown in :numref:`Listing %s <fetch-pmids>`.

.. code-block:: bash
  :caption: Fetching and formatting data records for several different PMIDs
  :name: fetch-pmids

  $ python pubmed-fetcher.py you@email 6,15430309,31077305,27880757,26378223| column -s= -t |less

You'll notice that not all data records have all fields. This is because they
are missing in these records or some tags have different names.

Running ``pubmed-fetcher.py`` with UID 20148030 will fail
(:numref:`Listing %s <fetch-error-pmid>`).

.. code-block:: bash
  :caption: Fetching the data record PMID20148030 results in an error
  :name: fetch-error-pmid

  $ python pubmed-fetcher.py you@email 20148030

The reason for this is can be found in the requested XML. Running the command
in :numref:`Listing %s <grep-error-pmid>` hints the problem. Adjusting and
fixing is a task left for interested readers.

.. code-block:: bash
  :caption: Hint to find teh reason why  PMID 20148030 fails
  :name: grep-error-pmid

  $ efetch -db pubmed -id 20148030  -mode xml | grep -A7 \<AuthorList

.. rubric:: Footnotes

.. [#fn_wpvf] https://en.wikipedia.org/wiki/Virtual_function
.. [#fn-less] http://www.greenwoodsoftware.com/less/
.. [#fn-more] https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/
.. [#fn-struct] https://en.cppreference.com/w/c/language/struct
.. [#fn-oocpmp] https://en.wikipedia.org/wiki/Object_composition

.. _oopython: https://docs.python.org/3/tutorial/classes.html
.. _eutils: https://dataguide.nlm.nih.gov/eutilities/utilities.html#efetch
.. _edirect: https://www.ncbi.nlm.nih.gov/books/NBK179288/
.. _implement: https://gitlab.com/ncbipy/entrezpy/blob/master/examples/tutorials/seqmedata/seqmedata-fetcher.py
