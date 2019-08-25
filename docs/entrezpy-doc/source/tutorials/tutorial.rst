.. _tutorials:

Entrezpy tutorials
==================

.. _tutorialesearch:

Esearch
-------

Esearch searches the specified Entrez database for data records matching the
query. It can return the found UIDs or a WebEnv/query_key referencing for the
UIDs

Esearch returning UIDs
~~~~~~~~~~~~~~~~~~~~~~

Search the nucleotide database for virus sequences and fetch the first 110,000
UIDs.

1. Create an Esearcher instance

2. Run the query and store the analyzer

3. Print the fetched UIDs

.. code-block:: python
  :linenos:

  import entrezpy.esearch.esearcher

  e = entrezpy.esearch.esearcher.Esearcher('esearcher', 'email')
  a = es.inquire('db':'nucleotide','term':'viruses[orgn]', 'retmax': 110000, 'rettype': 'uilist')
  print(a.get_result().uids)

Line 1: Import the esearcher module

Line 3: Instantiate an esearcher instance with the required parameter
        tool (using 'esearcher') and email

Line 4: Run query to search the database ``nucleotide``, using the term
        ``viruses[orgn]``, limit the result to the first 110,000 UIDs, and
        request UIDs. Store the returned default analyzer in ``a``.

Line 5: Print the fetched UIDs

Esearch returning History server reference to UIDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Same example as above, but in place of UIDs ``WebeEnv`` and ``query_key`` are
returned. By default, entrezpy uses the history server (setting the POST
parameter ``usehistory=y``) and is not required to be passed as parameter
explicitly.

.. code-block:: python
  :linenos:

  import entrezpy.esearch.esearcher

  e = entrezpy.esearch.esearcher.Esearcher('esearcher', 'email')
  a = es.inquire('db':'nucleotide','term':'viruses[orgn]', 'retmax': 110000)
  print(a.size())
  print(a.reference().webenv, a.reference().querykey)



Line 1: Import the esearcher module

Line 3: Instantiate an esearcher instance with the required parameter
        tool (using 'esearcher') and email

Line 4: Run query to search the database ``nucleotide``, using the term
        ``viruses[orgn]`` and limit the result to the first 110,000 UIDs.
        Store the returned default analyzer in ``a``

Line 5: Print the number of fetched UIDs, which should be 0
Line 6: Print the ``WebEnv`` and ``query_key``


Conduit
-------

.. _tutorialpipeline:

Pipelines
~~~~~~~~~

Conduit pipelines store a sequence of E-Utility queries. Let's create a simple
Conduit pipeline to fetch sequences for virus nulceotide sequences. This requires
to (i) search the nucleotide database which will return the found UIDs (data
records), and (ii) fetch the found UIDs.

  1. The first step in the pipeline is to search the Entrez nucleotide database
     for viruses sequences (Line 6). We add a search query to the pipeline and
     store its id for later use. We set the parameter ``rettype`` to ``count``
     to avoid downloading the UIDs and limit the number of UIDs to 100 with
     'retmax'. The result will tell us how many UIDs were found and a reference
     to the Entrez History server which we can use later to fetch the
     sequences.


  2. The second step in our pipline is the actual step to download the found
     sequences. We add a fetch step to our pipeline and use its id as
     dependency. Conduit will automatically set the 'db', 'WebEnv' and
     'query_key' parameters for the fetch step. In addition, we specify that we
     want the sequences as text FASTA format.

  3. The last step is to run the queries in the pipeline. This is done py
     passing the pipeline to Conduit's run method which will request the queries.
     If no request errors have occured, Conduit returns the default analyzer
     for this type of query.
     Sine this uses the default Efetch analzyer, results are just printed to
     the standard output.



.. code-block:: python
  :linenos:

  import entrezpy.conduit

  w = entrezpy.conduit.Conduit('email')
  get_sequences = w.new_pipeline()

  sid = get_sequenced.add_search({'db' : 'nucleotide', 'term' : 'viruses[Organism]', 'rettype' : 'count'})

  get_sequences.add_fetch({'retmode' : 'text', 'rettype' : 'fasta'}, dependency=sid)

  analyzer = w.run(get_sequences)


Line 1: Import the conduit module

Line 3: Create a Conduit instance with the required email address

Line 4: Create a new pipeline and store it in get_sequences

Line 6: Add search query to the pipeline and store its id in ''sid''

Line 10: Add fetch query to the pipeline

Line 13: Run pipeline and store the resulting analyzer


Linking within and between Entrezpy databases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using multiple links in a Conduit pipeline requires to run an Esearch afterwards
to keep track of the proper UIDs. This is a quirk of the E-Eutilties
(Entrez-Direct uses the same trick).

  1. Search the Pubmed Enrez database

  2. Increase the number of possible UIDs by searching pubmed again using the
     first UIDs to find publications linked to initial search

  3. Link the Pubmed UIDs to ``nuccore`` UIDs

  4. Fetch the found UIDs from ``nuccore``

The following code shows howto use multiple links within a Conduit pipeline.

.. code-block:: python
  :linenos:

  import entrezpy.conduit

  w = entrezpy.conduit.Conduit(args.email)
  find_genomes = w.new_pipeline()

  sid = find_genomes.add_search({'db':'pubmed', 'term' : 'capsid AND infection', 'rettype':'count'})

  lid1 = find_genomes.add_link({'cmd':'neighbor_history', 'db':'pubmed'}, dependency=sid)
  lid1 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid1)

  lid2 = find_genomes.add_link({'db':'nuccore', 'cmd':'neighbor_history'}, dependency=lid1)
  lid2 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid2)

  find_genomes.add_fetch({'retmode':'xml', 'rettype':'fasta'}, dependency=lid2)
  a = w.run(find_genomes)


Lines 1 - 4: Analogoues as shown in :ref:`tutorialpipeline`

Line 6: Addsa search query to the Conduit pipline in Entrez database pubmed
        without downloading UIDs and    store it in ``sid``

Line 8: Add a link query to the Conduit pipline to link the UIDs found in search
        ``sid`` to ``pubmed`` and store the result on the history server.  Store
        the query in lid1

Line 9: Update the link results for later use and store in the history server.
        Overwrite ``lid1`` with the updated query.

Line 11: Link the pubmed UIDs to nuccore and store in the history server. Store
         the query in ``lid2``.

Line 12: Update the link results for later use and store in the history server.
         Overwirte ``lid2`` with the updated query

Line 14: Add fetch step to Conduit pipeline with the last link result as
         dependency. Request the data as FASTA sequences in XML format
         (Tinyseq XML).

Line 15:  Run the pipeline.

Extending `entrezpy`
--------------------

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

- fetch an example entry to determine its structure
- write simple Conduit pipleine to fetch Pubmed records
- implement a EutilsResult class for Pubmed records
- implement a EutilsAnalyzer class Pubmed requsts

Syntax
++++++

- ``$ ls`` indicates a command on the the command line, here ``ls``.


This tutorial explains how to adjust the entrezpy classes  ``EutilsResult`` and
``EutilsAnalyzer`` to fetch Pubmed data records. To this end, we need to develop
a specific EutilsAnalyzer and EutilsResult class which can be used in Conduit.
We will write a simple Conduit pipeline which will fetch the record. The fetched
records will be stored and analyzed using our implemented classes.

The [Efetch Entrez Utility](https://dataguide.nlm.nih.gov/eutilities/utilities.html#efetch) is
responsible to fetch publications. Its manual (the link) lists all possible
databases and which records (Record type) can be fetched in which format. For
the first example, we'll fetch Pubmed data in XML, specifically, the author and
the corresponding references. The first example we'll use is the seminal
publication from Barbara McClintock describing the AC/Ds elements in Maize. The
correspondong Pubed ID (PMID) is 15430309.


In ``entrezpy``, a result is the sum of all individual requests. If you want to
analyze the number of citations for a specific author, the result is the number
of cirtations and to obtain this you have to parse several Pubmed records.
Therefore, ``entrezpy`` requires a result class. Thereofore, we need to store
individual results within a result class.

Pubmed data structure
+++++++++++++++++++++

Before we start to write our implementation, we need to understand the structure
of the received data. This can be done using the EDirect tools from
NCBI. The result is printed to the standard output. For its examination, it can
be either stored into a file, or prefereably, piped to a pager, e.g. ``less``
[http://www.greenwoodsoftware.com/less/] or ``more``
[https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/]. These are usually
installed on most \*NIX systems.

.. _tut-efetch-example:

.. code-block:: bash
  :linenos:
  :name: tut-efetch-example

  $ efetch -db pubmed -id 15430309 -mode XML | less

The entry should start and end as the code block below. Data not related to the
author and references has been removed for the sake of clearity.

.. code-block:: XML
  :linenos:

  <?xml version="1.0" ?>
  <!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2019//EN" "https://dtd.nlm.nih.gov/
  <PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation Status="MEDLINE" IndexingMethod="Automated" Owner="NLM">
            <PMID Version="1">15430309</PMID>
    <!- SKIPPED DATA ->
      <AuthorList CompleteYN="Y">
        <Author ValidYN="Y">
          <LastName>McCLINTOCK</LastName>
          <ForeName>B</ForeName>
          <Initials>B</Initials>
        </Author>
     </AuthorList>
  <!- SKIPPED DATA ->
      <ReferenceList>
        <Reference>
            <Citation>Genetics. 1941 Mar;26(2):234-82</Citation>
            <ArticleIdList>
                <ArticleId IdType="pubmed">17247004</ArticleId>
            </ArticleIdList>
        </Reference>
      <!- SKIPPED DATA ->
      <ReferenceList>
  <!- SKIPPED DATA ->
    </PubmedArticle>
  </PubmedArticleSet>


This shows us the XML fields, specifically the `tags`,  present in a typical
Pubmed record. The root tag for each batch of fetched data records is
``<PubmedArticleSet>`` and each individual data record is described in the nested
tags ``<PubmedArticle>``. We are interested in the following tags nested within
``<PubmedArticle>``:

  - ``<AuthorList>``
  - ``<ReferenceList>``

Before we can start with the actual implementation, we need to write a
program to fetch the requested records. This can be done using the Conduit class.

Simple Conduit pipeline to fetch Pubmed Records
+++++++++++++++++++++++++++++++++++++++++++++++

 - write simple conduit pipelne program
 - inherit required base classes

A simple conduit pipeline requiring two arguments:

  - user email
  - PMID (here 15430309)

.. literalinclude:: ../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :linenos:
  :language: python
  :lines: 36-45,62-65,70-

- Lines 1-3: import standard Pyhton libraries

- Lines 6-9: import entrezpy (adjust as described)

- Lines 10: import conduit (adjust as described)

- Line 14: create new conduit instance

- Line 15: create new pipeline

- Line 16: add fetch request to the pipeline

- Line 17: run pipeline

Let's test this program to see if all modules are found and fetching works:

``$ python pubmed-fetcher.py your@email 15430309``

Since we didn't specify an analzyer yet, we epxect the raw XML output is printed
to the standard output. So far, this produces the same output as the efetch
command above.

If this command fails and/or now output is printed to the standard output,
something went wrong with your ``entrezpy`` installation or ``entrezpy`` module
import.

We can now start to implement our specific ``EutilsResult`` and
``EutilsAnalyzer`` classes. From the documentation or publication ADD URL, we
know that EutilsAnalzyer parses the response and stores results in
EutilsResults. Therefore, we need to derive and adjust these classes for our
needs. Initially, we will just add the bare minimum to test if we can inherit
the base classes.

.. code-block:: python
  :linenos:

  import os
  import sys


  # If enrezpy is installed via PyPi uncomment the next line and remove the next after that
  # import entrezpy
  sys.path.insert(1, os.path.join(sys.path[0], '../../../src'))
  import entrezpy.conduit
  import entrezpy.base.result
  import entrezpy.base.analyzer


  class PubmedAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):

    def __init__():
      super().__init__()

  class PubmedResult(entrezpy.base.result.EutilsResult):

    def __init__():
      super().__init__()


  def main():
    c = entrezpy.conduit.Conduit(sys.argv[1])
  # cut for brevity
This listing shows the newly added classes and not the whole code.

- Lines 14-17 and Lines 19-22 create our bare classes.

Rerun the program to make sure the required entrezpy base modules are loaded.
The result should be identical to the previuos run.

If there were no errors, we know can query Entrez databases and our
classes ``PubmedAnalyzer`` and ``PubmedResult`` can inherit their base classes.
However, before we inplement these classes, we need to decide how want to store
a Pubmed data record.

How to store PubMed data records
++++++++++++++++++++++++++++++++
The data records can be stored in different ways, but using a class  we can
facilitate collecting and retrieving the requested data. We implement a
sinmple class to represent a Pubmed record as follows, similar to a struct in
C/C++. Furfther, we use the ``dict``  ``pubmed_records`` in ``PubmedResult`` to
store ``PubmedRecord`` instances using the PMID as key. This avoids duplicates
and faciliates lookup later.

.. literalinclude:: ../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :linenos:
  :language: python
  :lines: 49-55

Implement ``PumedResult``
+++++++++++++++++++++++++

As mentioned above, a result in ``entrezpy`` is the sum of all individual
requests. We already decided to use a ``dict`` to store individual publication
records. The EutilsResult documentation ADD URL shows us the requred aprameter
for its constructor:

- function name: name for the function produing this result (req)
- qid:  the query id (req)
- db: the queried Entrez database (req)
- webenv: the WebEnv of the response (opt)
- querykey: the query key of the corresponding WebEnv (opt)

Firther, we need to implement four virtual methods.

.. literalinclude:: ../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :linenos:
  :language: python
  :lines: 57-78

- Lines 5-8: Inherit hte base class and instatniate a PiubmedResult instance
             with the required arguments obtained rom the response and request.

- Lines 10-11: Implemnts the virtual method ``size()`` to return the number
               of stored Pubmed records.

- Lines 13-16: Implements the virtual method ``isEmpty()`` which returns a boolean to
               indicate if any records have been fetched at all.

- Lines 18-19: Implements the virtual  method ``get_link_parameter()`` which
               should return the required parameters for Elink. We will skip
               this method for now.

- Lines 21-22: Implements a specific PubmedResult method to store individual
               PubmedResult instances in pubmed_records

Implement class ``PumedAnalyzer``
+++++++++++++++++++++++++++++++++

The ``PubmedAnalyzer`` class will parse all responses and prepare them for
``PumedResult``. The documentation for ``PubmedAnalyzer`` indicates
three virtual methods we need to implement.

- ``init_result(self, response, request)``: initialize a result instance if none exists
- ``analyze_error(self, response, request)``: what to do if an error ocured
- ``analyze_result(self, response, request)``: convert the reponse into a way we can parse it

The first method we implement is init_result. So far, we know that we have a
``PubmedResult`` class. We will adjust this method later, but for now we can
implement it in a convieniente way so we can focus on the bigger analysis
methods.


We create an instance of our PubmedResult class as an analyzer attribute. The
result attribute is documented in the EutilsAnalyzer documentation. We will
elaboraet this method later, bit first we implement parsing the reponses from
Entrez.

The second method we implement is the error handling:.

.. literalinclude:: ../../../../examples/tutorials/pubmed/pubmed-fetcher.py
  :linenos:
  :language: python
  :lines: 50-61

Since we request results in XML, we can print the error directly to STDOUT. When
fetching numerous documents, you can log this output to follow up errors. Of
course, you can, and likely should, implement a more complete error handling,
but this is outsie the scope of this tutorial.
The default error efetch_analzyer() has a method to recognize between JSON and
XML and can be copied if required.


Next, we implement is the parsing of the responses. We need to decide how to
implement a Pubmed record. We implement a class to represent a Pubmed record as
follows:

.. code-block:: python
  :linenos:

  class PubmedRecord:

    def __init__(self):
      self.pmid = None
      self.title = None
      self.authors = [{'fname': None, 'lname': None}]
      self.citations = []


Implement ``PumedResult`` class from ``EutilsResult`` class
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

- implement a single result
- decide how to store single results
- implement required virtual functions

We know are structure of PubMed records (see above) and the name of the tags we
want to extract. We crated our two classes ``PubmedAnalyzer`` and
``PubmedResult``.  Now it's time to extend them.

We start with ``PubmedResult``.



After having implemneted a single data record, we need to think how to store
several records in ``PumedResult``. A reasonable choice is to store individual
records in an array, or list.

We can now start to write our ``PumedResult`` class.
  We can get al the required infoirmations

of the response inherit the base class and set the attributes to store individual PubMed records:

.. literalinclude:: ../../../../examples/tutorials/pubmed/pubmed_result.py
  :linenos:
  :language: python
  :lines: 1

Lines 1-3: import standard Python libraries.

Lines 5-7: import entrezpy and the base class. Adjust as described.

Line 11: define the PubmedResult class and inherit the base class


Now its time to take a closer look at the class ``EutilsResults`` since
the class ``PumedResult`` is derived from it. The class ``EutilsResults`` is
implemented in ``src/entrezpy/base/result.py`` and protoypes four virtual
classes which we need to implement in our derived class ``PumedResult``:

  - ``size()``: return the number of fetched Pubmed records
  - ``dump()``: Dumps all instance attributes for debugging and logging
  - ``get_link_parameter()``: Linking results using ``EutilsELink`` requires to
                              define the required attributes.
  - ``isEmpty()``: What indicates an empty result. Empty results are not
                    failed results since the requets worked but did not return
                    any records because none were found.

.. code-block:: python

  def size(self):
    """Returns result size in the corresponfong ResultSize unit

    :rtype: int
    :raises NotImplementedError: if implementation is missing"""
    raise NotImplementedError("Help! Require implementation")

  def dump(self):
    """Dumps all instance attributes

    :rtype: dict
    :raises NotImplementedError: if implementation is missing"""
    raise NotImplementedError("Help! Require implementation")

  def get_link_parameter(self, reqnum=0):
    """Assembles parameters for automated follow-ups. Use the query key from
    the first request by default.

    :param int reqnum: request number for which query_key should be returned
    :return: EUtils parameters
    :rtype: dict
    :raises NotImplementedError: if implementation is missing"""
    raise NotImplementedError("Help! Require implementation")

  def isEmpty(self):
    """Indicates empty result.

    :rtype: bool
    :raises NotImplementedError: if implementation is missing"""
    raise NotImplementedError("Help! Require implementation")










20148030

WIP, but see ``examples/entrezpy-example.conduit.fetch-genome.py``, lines 74-85.
20148030

# getting result from console
sys.stdout = old_stdout
xml_string = result.getvalue()
root = ET.fromstring(xml_string)
res = root.findall("./PubmedArticle/MedlineCitation/Article/Abstract/AbstractText")
abstracts = []
for item in res:
    abstracts.append(item.text)
return abstracts
