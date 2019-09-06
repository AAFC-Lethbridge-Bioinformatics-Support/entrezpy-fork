.. _pubmedtut:

Fetching publication information from Entrez
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. topic:: Prerequisites

  * Python 3.6 or higher is assumed.
  * |entrezpy| is either installed via PyPi or cloned from the ``git``
    repository  (:ref:`install`).
  * basic familiarity with `object oriented Python <oopython_>`_, i.e. inheritance
  * The full implementation can be found in the repository at
    `examples/tutorials/pubmed/pubmed-fetcher.py <implement>`_

.. topic:: Acknowledgment

  I'd like to thank Pedram Hosseini (pdr[dot]hosseini[at]gmail[dot]com) for
  pointing out the requirement for this tutorial.

Overview
++++++++

This tutorial explains how to write a simple |pubmed| data record fetcher using
|Conduit| and by adjust |EutilsResult| and |EutilsAnalyzer|.

.. topic:: Outline

  * develop a |Conduit| pipline
  * implement a |pubmed| data structure
  * inherit |EutilsResult| and |EutilsAnalyzer|
  * implement the required virtual methods
  * add methods to derived classes

The `Efetch Entrez Utility <eutils_>`_ is NCBI's utility responsible for
fetching data records. Its `manual <eutils_>`_ lists all possible databases and
which records (Record type) can be fetched in which format. For the first
example, we'll fetch |pubmed| data in XML, specifically, the UID, authors,
title, abstract, and citations. We will test and develop the pipeline using
the article  the article with |pubmed| ID (PMID) 26378223 because it has all the
required fields. In the end we will see that not all fields are always present.

In |entrezpy|, a result (or query), is the sum of all individual requests
required to obtain the whole query. If you want to analyze the number of
citations for a specific author, the result is the number of citations which
you obtained using a query. To obtain the final number, you have to parse
several |pubmed| records. Therefore, |entrezpy| requires a result
|EutilsResult| class to store the partial results obtained from a query.

.. _virtualmethod:
.. rubric:: A quick note on virtual functions

|entrezpy| is heavily based on virtual methods [#fn_wpvf]_. A virtual method is
declared in the the base class but implemented in the derived class. Every
class inheriting the base class has to implement the virtual functions using
the same signature and return the same result type as the base class. To
implement the method in the inherited class, you need to look up the method in
the base class.

|pubmed| data structure
+++++++++++++++++++++++

Before we start to write our implementation, we need to understand the
structure of the received data. This can be done using the `EDirect tools
<edirect_>`_ from NCBI. The result is printed to the standard output. For its
examination, it can be either stored into a file, or preferably, piped to a
pager, e.g. ``less`` [#fn-less]_ or ``more`` [#fn-more]_. These are usually
installed on most \*NIX systems.

.. code-block:: bash
  :caption: Fetching |pubmed| data record for PMID 26378223 using EDirect's
            ``efetch``
  :name: tut-efetch-example

  $ efetch -db pubmed -id 26378223 -mode XML | less

The entry should start and end as shown in :numref:`Listing %s <26378223-xml-example>`.

.. literalinclude:: 26378223.xml
  :language: xml
  :caption: XML |pubmed| data record for publication PMID26378223. Data not
            related to authors, abstract, title, and references has been
            removed for clarity.
  :name: 26378223-xml-example
  :linenos:

This shows us the XML fields, specifically the ``tags``,  present in a typical
|pubmed| record. The root tag for each batch of fetched data records is
``<PubmedArticleSet>`` and each individual data record is described in the nested
tags ``<PubmedArticle>``. We are interested in the following tags nested within
``<PubmedArticle>``:

  * ``<ArticleTitle>``
  * ``<Abstract>``
  * ``<AuthorList>``
  * ``<ReferenceList>``

The first step is to write a program to fetch the requested records. This can
be done using the |Conduit| class.

Simple Conduit pipeline to fetch |pubmed| Records
+++++++++++++++++++++++++++++++++++++++++++++++++

We will write simple |entrezpy| pipeline named ``pubmed-fetcher.py`` using
|Conduit| to test and run our implementations. A simple |Conduit| pipeline
requires two arguments:

  * user email
  * PMID (here 15430309)

.. literalinclude:: simple-conduit.tutorial.py
  :caption: Basic |Conduit| pipeline to fetch |pubmed| data records. The required
            arguments are positional arguments given at the command line.
  :linenos:
  :language: python
  :name: basic-conduit
  :lines: 1-16, 54-
  :emphasize-lines: 15, 19-22

* Lines 3-4:  import standard Python libraries
* Lines 12-15:  import the module :mod:`entrezpy.conduit` (adjust as necessary)
* Line 19:  create new |Conduit| instance with an email address from the first
            command line argument
* Line 20:  create new pipeline ``fetch_pubmed`` using
            :meth:`entrezpy.conduit.Conduit.new_pipeline`
* Line 21:  add fetch request to the ``fetch_pubmed`` pipeline with the PMID
            from the second command line argument using
            :meth:`entrezpy.conduit.Conduit.Pipeline.add_fetch`
* Line 22:  run pipeline using :meth:`entrezpy.conduit.Conduit.run`

Let's test this program to see if all modules are found and conduit works.

``$ python pubmed-fetcher.py your@email 15430309``

Since we didn't specify an analyzer yet, we expect the raw XML output is printed
to the standard output. So far, this produces the same output as
:numref:`Listing %s <tut-efetch-example>`.

If this command fails and/or no output is printed to the standard output,
something went wrong. Possible issues may include  no internet connection,
wrongly installed |entrezpy|, wrong import statements, or bad permissions.

If everything went smoothly, we wrote a basic but working pipeline to
fetch |pubmed| data from NCBI's Entrez database. We can now start to implement our
specific |EutilsResult| and |EutilsAnalyzer| classes. However, before we
implement these classes, we need to decide how want to store a |pubmed| data
record.

How to store |pubmed| data records
++++++++++++++++++++++++++++++++++

The data records can be stored in different ways, but using a class  facilitates
collecting and retrieving the requested data. We implement a simple class
(analogous to a C/C++ struct [#fn-struct]_) to represent a |pubmed| record.

.. literalinclude:: ../../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :caption: Implementing a |pubmed| data record
  :name: lst:pmed-datrec
  :linenos:
  :language: python
  :lines: 52-63

Further, we will use the ``dict`` ``pubmed_records`` as attribute of
|PubmedResult| to store |PubmedRecord| instances using the PMID as key to
avoid duplicates.

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
tutorial are trivial since and we can implement the class in one go

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
  :name: pubmed-analyzer
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

* Line 163: Adjust argument processing to allow several comma-separated PMIDs
* Line 164: add our implemented |PubmedAnalyzer| as parameter to analyze
            results as described in :meth:`entrezpy.conduit.Conduit.Pipeline.add_fetch`
* Line 166: run the pipeline and store the analyzer in ``a``
* Lines 168-172: Testing methods
* Line 174: get |PubmedResult| instance
* Lines 175-181: process fetched data records into columns

The implementation can be invoked as shown in :numref:`Listing %s <fetch-pmids>`.

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
  :caption: Hint to find the reason why  PMID 20148030 fails
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
.. _implement: https://gitlab.com/ncbipy/entrezpy/blob/master/examples/tutorials/pubmed/pubmed-fetcher.py
