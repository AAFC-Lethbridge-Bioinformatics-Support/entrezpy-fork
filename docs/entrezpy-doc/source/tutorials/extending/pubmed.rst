Fetching publication information from Entrez
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prerequisites
+++++++++++++

- ``entrezpy`` is either installed via PyPi or cloned from the ``git``
    repository. ADD URL

- basic familiarity with object oriented Python, i.e. inheritance ADD URL

- Python 3.6 or higher is assumed.

Overview
++++++++

This tutorial explains how to adjust the entrezpy classes  ``EutilsResult`` and
``EutilsAnalyzer`` to fetch Pubmed data records. To this end, we need to
develop a specific ``EutilsAnalyzer`` and ``EutilsResult`` class which can be
used in Conduit. I'd like to thank <proposing person> for pointing out the need
for this tutorial.


In this tutorial, we will:

- fetch an example entry to determine its structure
- write a simple Conduit pipeline to fetch Pubmed records
- implement a ``EutilsResult`` class for Pubmed records
- implement a ``EutilsAnalyzer`` class Pubmed requests
- implement the required data structures.


The [Efetch Entrez Utility](https://dataguide.nlm.nih.gov/eutilities/utilities.html#efetch) is
responsible to fetch publications. Its manual (the link) lists all possible
databases and which records (Record type) can be fetched in which format. For
the first example, we'll fetch Pubmed data in XML, specifically, the author and
the corresponding references. The first example we'll use is the seminal
publication from Barbara McClintock describing the AC/Ds elements in Maize. The
correspondong Pubed ID (PMID) is 15430309.


In ``entrezpy``, a result (or query) is the sum of all individual requests
required to obtain the whole query. If you want to analyze the number of
citations for a specific author, the result is the number of citations which
you obtained using a query . To obtain the final number, you have to parse
several Pubmed records. Therefore, ``entrezpy`` requires a result
``EutilsResult`` class to store the partial results from a query.

.. _virtualmethod:

**A quick note on virtual functions**

``entrezpy`` is heavily based on virtual methods
(https://en.wikipedia.org/wiki/Virtual_function). A virtual method is not
declared in the the base class but implemented in the derived class. Every
class inheriting the base class has to implement the virtual functions using
the same signature and return the same result type as the base class. To
implement the method in the inherited class, you need to look up the method in
the base class.

Pubmed data structure
+++++++++++++++++++++

Before we start to write our implementation, we need to understand the structure
of the received data. This can be done using the EDirect tools from
NCBI. The result is printed to the standard output. For its examination, it can
be either stored into a file, or prefereably, piped to a pager, e.g. ``less``
[http://www.greenwoodsoftware.com/less/] or ``more``
[https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/]. These are usually
installed on most \*NIX systems.

.. code-block:: bash
  :linenos:
  :name: tut-efetch-example

  $ efetch -db pubmed -id 15430309 -mode XML | less

The entry should start and end as the code block below. Data not related to the
author and references has been removed for the sake of clearity.

.. literalinclude:: linking-mcclintock.xml
  :language: xml
  :linenos:

This shows us the XML fields, specifically the `tags`,  present in a typical
Pubmed record. The root tag for each batch of fetched data records is
``<PubmedArticleSet>`` and each individual data record is described in the nested
tags ``<PubmedArticle>``. We are interested in the following tags nested within
``<PubmedArticle>``:

  - ``<AuthorList>``
  - ``<ReferenceList>``

The first step is to write a program to fetch the requested records. This can
be done using the class:`entrezpy.conduit.Conduit` class.

Simple Conduit pipeline to fetch Pubmed Records
+++++++++++++++++++++++++++++++++++++++++++++++

We will write simple entrezpy pipeline named ``pubmed-fetcher.py`` using
``entrezpy.conduit.Conduit()`` to test our implementations. A simple conduit
pipeline requires two arguments:

  - user email
  - PMID (here 15430309)

.. literalinclude:: simple-conduit.tutorial.py
  :linenos:
  :language: python
  :lines: 1-4,8-15, 73-76, 79-

- Lines 3-4: import standard Python libraries

- Lines 10-12: import the conduit module (adjust as necessary)

- Line 16: create new conduit instance (with an email address as first argument)

- Line 17: create new pipeline ``fetch_pubmed``

- Line 18: add fetch request to the ``fetch_pubmed`` pipeline

- Line 19: run pipeline

Let's test this program to see if all modules are found and fetching works.

``$ python pubmed-fetcher.py your@email 15430309``

Since we didn't specify an analzyer yet, we epxect the raw XML output is printed
to the standard output. So far, this produces the same output as the EDirect
``efetch`` command above.

If this command fails and/or no output is printed to the standard output,
something went wrong. Possible issues may include  no internet connection,
wrongly installed ``entrezpy``, wrong import statements, or bad permissions.

If everything went smoothly, we built ourself a simple and working pipeline to
fetch Pubmed data from NCBI's Entrez database. We can now start to implement our
specific ``EutilsResult`` and ``EutilsAnalyzer`` classes. However, before we
implement these classes, we need to decide how want to store a Pubmed data
record.

How to store PubMed data records
++++++++++++++++++++++++++++++++

The data records can be stored in different ways, but using a class  facilitates
collecting and retrieving the requested data. We implement a simple class
(analogous to a C/C++ struct) to represent a Pubmed record.

.. literalinclude:: simple-conduit.tutorial.py
  :linenos:
  :language: python
  :lines: 18-28

Further, we will use the ``dict``  ``pubmed_records`` as attribute of
``PubmedResult`` to store ``PubmedRecord`` instances using the PMID as key to
avoid duplications.


Prototyping ``PumedResult`` and ``PumedAnalyzer``
+++++++++++++++++++++++++++++++++++++++++++++++++

From the documentation or publication ADD URL, we know that ``EutilsAnalyzer``
parses the response and stores results in ``EutilsResults``. Therefore, we need
to derive and adjust these classes for our ``PubmedResult`` and
``PubmedAnalzyer`` classes. We will add these classes to our program
``pubmed-fetcher.py``. The documentation tells us what the required parameters
for each class are and the virtual methods we need to implement. We will not
add any functionality yet, only prototyping the classes first and than add the
required functionality.

The ``PubmedAnalyzer`` prototype
................................

.. literalinclude:: simple-conduit.tutorial.py
  :linenos:
  :language: python
  :lines: 56-71

- Line 1: Inherit the base class ``EutilsAnalyzer``
- Lines 6-7: Initialize an instance of PubmedResult.
- Lines 9-16: Adding the required methods to obtain a working analzyer.

We have to extend these methods:

- :meth:`init_result`: initialize a result instance
- :meth:`analyze_error`: what to do if Entrez returns an error. These are not
                         ``entrezpy`` errors but error messages returned from
                         Entrez.
- :meth:`analyze_result`: parse and handle an Entrez response


The ``PubmedResult`` prototype
..............................

.. literalinclude:: simple-conduit.tutorial.py
  :linenos:
  :language: python
  :lines: 30-54

- Line 1: Inherit the base class ``EutilsResult``
- Line 11-13: Initialize an instance of PubmedResult with the required
              parameters and attributes.


We have to extend these :ref:`virtual methods  <virtualmethod>`. The
documentation informs us about the required parameters and expected return
values.

 - :meth:`entrezpy.base.result.EutilsResult.size`: returns number of parsed data records
 - :meth:`dump`: return attributes for logging and debugging
 - :meth:`isEmpty`: return is any records have been parsed.
 - :meth:`get_link_parameter`: return Elink parameters

Please note: linking Pubmed records is better handled by creating a pipeline
performing an ``esearch`` query followed by one of several  ``elink`` queries
and a final ``efetch`` query. The fetch result for Pubmed records has no WebEnv
since these step is usually the last within a series of Eutils queries, i.e.
the final result. Therefore, we will implement a warning, informing the user
this is not possible here. Nevertheless, the method could return the PMID of
the citations to allow linking. But this method could not use the Entrez
``history`` server.

Putting everything together
+++++++++++++++++++++++++++

The finished implementations are shown in the listing below. Please consult the
corresponding method documentations describing the required parameters and
method signatures. Explaining the XML parser is beyond the scope of this
tutorial (and there are likely better approaches).

.. literalinclude:: ../../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :linenos:
  :language: python
  :emphasize-lines: 119-12
  :lines: 1,36-

- Line 119: add our implemented ``PubmedAnalzyer`` as parameter to the
            :class:`entrezpy.conduit.Conduit` pipeline as described in
            :meth:`entrezpy.conduit.Conduit.Pipeline.add_fetch`
- Line 121: :meth:`entrezpy.conduit.Conduit.run` returns our analyzer

Running the this example will return our analyzer. Uncomment line 122 and
run ``pubmed-efetch.py`` (the address will most likely differ.

:: code-block

  $ python pubmed-fetcher.py you@email  15430309
  <__main__.PubmedAnalyzer object at 0x7f0ff11711d0>

The lines 123-125 loop over the obtained Pubmed Records. Line 119 shows a
modification allowing several comma spearated PMIDs, e.g.

:: code-block

$ python pubmed-fetcher.py jan 15430309,20148030

However, you'll notice that the author list is missing. The reason for this is
can be found in the requested XML. Fixing this is a task left for  the reader.
