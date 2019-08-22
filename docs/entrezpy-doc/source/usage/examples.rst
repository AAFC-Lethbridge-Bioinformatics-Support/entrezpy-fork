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

Implementing a simple EfetchAnalzyer to obtain publication information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This shows how to adjust classes derieved from `EutilsResult`, `EutilsAnalyzer`.

The goal is to fetch PubMed information related specific articles. To this end,
we need to develop a specific EutilsAnalyzer and EutilsResult class which can be
used in Conduit.

The [Efetch Entrez Utility](https://dataguide.nlm.nih.gov/eutilities/utilities.html#efetch)
is responsible to fetch publications. Its manual (the link) lists all possible
databses and which records (Record type) can be fetched in which format. For
the first example, we'll fetch Pubmed data in XML, specifically, the author and
the corresponding references. The first example we'll use is the seminal
publication from Barbara McClintock describing the AC/Ds elements in Maize. The
correspondong Pubed ID (PMID) is 15430309.

Before we start to write an EutilsAnalyzer, we need to understand the structure
of the received data. This can be done using the EDirect tools from NCBI and
piping its results to a pager, e.g. `less`

.. code-block:: bash
  :linenos:

  efetch -db pubmed -id 20148030 -mode XML | less

it shows us the XML fields, specifically the `tags`  present in a typical
Pubmed record  Please note, the abstract is missing which is common for older
publications.

We now know how such records are structured and the name of the tags we want
to extract. Now we can start to extend entrepy.
First, we need to design a EutilsResult class to store publication records.

The base class for `EutilsResults` is implemented in
`src/entrezpy/base/result.py`. We will inherit this class and implement its four
virtual classes in our derived class, called `PumedResult`.
Looking the

sie methods
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
