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

Overview
++++++++

This tutorial explains how to write a simple sequence docsum fetcher using
|Conduit| and by adjust |EutilsResult| and |EutilsAnalyzer|. It is based on a
esearch followed by fetching the data as ``docsum`` JSON. This tutorial is very
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
|docsum| data in JSON using the EUtil ``esummary`` after performing an
``esearch`` step using accessions numbers as query. Instead of using efetch, we
will  use ``esummary`` and replace the default analyzer with our own.

In |entrezpy|, a result (or query), is the sum of all individual requests
required to obtain the whole query. ``esummary`` fetches data in batches. In this
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

  $ esearch -db nuccore -query HOU142311 | esummary -mode json

The entry should start and end as shown in :numref:`Listing %s <docsum-json-example>`.

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
(analogous to a C/C++ struct [#fn-struct]_) to represent a |docsum| record.
Becuase we fetch data in JSON format, the class performs a rather dull parsing.
The nested Subtype class handles the ``subtype`` and ``subname`` attributes
in a |docsum| response.

.. literalinclude:: ../../../../../examples/tutorials/seqmetadat/seqmetadata-fetcher.py
  :caption: Implementing a |docsum| data record
  :name: lst:docsum-datrec
  :linenos:
  :language: python
  :lines: 51-98


Implement |DocsumResult|
........................

We have to extend the :ref:`virtual methods  <virtualmethod>` declared in
|EutilsResult|. The documentation informs us about the required parameters and
expected return values.

In addition, we declare the method :meth:`PubmedResult.add_docsum` to
handle adding new |docsum| data record instances as defined in
:numref:`Listing %s <lst:docsum-datrec>`. The |docsum| methods in this
tutorial are trivial and we can implement the class in one go

.. literalinclude:: ../../../../../examples/tutorials/seqmetadat/seqmetadata-fetcher.py
  :caption: Implementing |DocsumResult|
  :name: lst:docsum-result
  :linenos:
  :language: python
  :lines: 100-146
  :emphasize-lines: 1, 10, 14, 19, 26, 33, 43

* Line 1: inherit the base class |EutilsResult|
* Line 10-12: initialize |DocsumResult| instance with the required
    parameters and attributes. We don't need any information from the
    response, e.g. WebEnv.
* Line 14-17: implement :meth:`entrezpy.base.result.EutilsResult.size`
* Line 19-24: implement :meth:`entrezpy.base.result.EutilsResult.isEmpty`
* Line 26-31: implement :meth:`entrezpy.base.result.EutilsResult.get_link_parameter`
* Line 33-41: implement :meth:`entrezpy.base.result.EutilsResult.dump`
* Line 43-46: specific |PubmedResult| method to store individual |DocsumResult|
    instances

.. note:: The fetch result for |docsum| records  has no WebEnv value and is
  missing the originating database since ``esummary``  is usually the last
  query within a series of ``Eutils`` queries.  Therefore, we implement a
  warning, informing the user linking is not  possible.

Implementing |DocsumAnalyzer|
.............................

We have to extend the :ref:`virtual methods  <virtualmethod>` declared in
|EutilsAnalyzer|. The documentation informs us about the required parameters
and expected return values.

.. literalinclude:: ../../../../../examples/tutorials/seqmetadat/seqmetadata-fetcher.py
  :caption: Implementing |PubmedAnalyzer|
  :linenos:
  :language: python
  :lines: 147-172
  :emphasize-lines: 1, 5, 8, 14, 20

* Line 1: Inherit the base class |EutilsAnalyzer|
* Lines 5-6: initialize |PubmedResult| instance.
* Lines 8-12: declare :meth:`entrezpy.base.analyzer.EutilsAnalyzer.init_result`
* Lines 14-18: decalre :meth:`entrezpy.base.analyzer.EutilsAnalyzer.analyze_error`
* Lines 20-25: declare :meth:`entrezpy.base.analyzer.EutilsAnalyzer.analyze_result`

Compared to the :ref:`pubmed analyzer <pubmed-analyzer>`, parsing the JOSN
output is very easy. If you already have a parser, you can use an object
composition approach [#fn-oocomp]. Further, you can add a method in
``analyze_result`` to store the processed data in a database or
implementing checkpoints.

Putting everything together
+++++++++++++++++++++++++++

The completed implementation is shown in :numref:`Listing %s <docsum-fetcher>`.

.. literalinclude:: ../../../../../examples/tutorials/seqmetadat/seqmetadata-fetcher.py
  :caption: Complete |docsum| fetcher
  :name: docsum-fetcher
  :linenos:
  :language: python
  :lines: 1,34-

The implementaion can be invoked as shown in :numref:`Listing %s <fetch-docsum>`.

.. code-block:: bash
  :caption: Fetching |docsum| data for several accessions
  :name: fetch-docsum

  $ cat "NC_016134.3" > accs
  $ cat "HOU142311" >> accs
  $ cat accs | python seqmetadata-fetcher.py --email email -db nuccore

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
