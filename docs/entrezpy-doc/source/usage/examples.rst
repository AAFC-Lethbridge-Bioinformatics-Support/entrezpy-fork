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


Wally
-----

.. _tutorialpipeline:

Pipelines
~~~~~~~~~

Wally pipelines store a sequence of E-Utility queries. Let's create a simple
Wally pipeline to fetch sequences for virus nulceotide sequences. This requires
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
     dependency. Wally will automatically set the 'db', 'WebEnv' and
     'query_key' parameters for the fetch step. In addition, we specify that we
     want the sequences as text FASTA format.

  3. The last step is to run the queries in the pipeline. This is done py
     passing the pipeline to Wally's run method which will request the queries.
     If no request errors have occured, Wally returns the default analyzer
     for this type of query.
     Sine this uses the default Efetch analzyer, results are just printed to
     the standard output.



.. code-block:: python
  :linenos:

  import entrezpy.wally

  w = entrezpy.wally.Wally('email')
  get_sequences = w.new_pipeline()

  sid = get_sequenced.add_search({'db' : 'nucleotide', 'term' : 'viruses[Organism]', 'rettype' : 'count'})

  get_sequences.add_fetch({'retmode' : 'text', 'rettype' : 'fasta'}, dependency=sid)

  analyzer = w.run(get_sequences)


Line 1: Import the wally module

Line 3: Create a Wally instance with the required email address

Line 4: Create a new pipeline and store it in get_sequences

Line 6: Add search query to the pipeline and store its id in ''sid''

Line 10: Add fetch query to the pipeline

Line 13: Run pipeline and store the resulting analyzer


Linking within and between Entrezpy databases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using multiple links in a Wally pipeline requires to run an Esearch afterwards
to keep track of the proper UIDs. This is a quirk of the E-Eutilties
(Entrez-Direct uses the same trick).

  1. Search the Pubmed Enrez database

  2. Increase the number of possible UIDs by searching pubmed again using the
     first UIDs to find publications linked to initial search

  3. Link the Pubmed UIDs to ``nuccore`` UIDs

  4. Fetch the found UIDs from ``nuccore``

The following code shows howto use multiple links within a Wally pipeline.

.. code-block:: python
  :linenos:

  import entrezpy.wally

  w = entrezpy.wally.Wally(args.email)
  find_genomes = w.new_pipeline()

  sid = find_genomes.add_search({'db':'pubmed', 'term' : 'capsid AND infection', 'rettype':'count'})

  lid1 = find_genomes.add_link({'cmd':'neighbor_history', 'db':'pubmed'}, dependency=sid)
  lid1 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid1)

  lid2 = find_genomes.add_link({'db':'nuccore', 'cmd':'neighbor_history'}, dependency=lid1)
  lid2 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid2)

  find_genomes.add_fetch({'retmode':'xml', 'rettype':'fasta'}, dependency=lid2)
  a = w.run(find_genomes)


Lines 1 - 4: Analogoues as shown in :ref:`tutorialpipeline`

Line 6: Addsa search query to the Wally pipline in Entrez database pubmed
        without downloading UIDs and    store it in ``sid``

Line 8: Add a link query to the Wally pipline to link the UIDs found in search
        ``sid`` to ``pubmed`` and store the result on the history server.  Store
        the query in lid1

Line 9: Update the link results for later use and store in the history server.
        Overwrite ``lid1`` with the updated query.

Line 11: Link the pubmed UIDs to nuccore and store in the history server. Store
         the query in ``lid2``.

Line 12: Update the link results for later use and store in the history server.
         Overwirte ``lid2`` with the updated query

Line 14: Add fetch step to Wally pipeline with the last link result as
         dependency. Request the data as FASTA sequences in XML format
         (Tinyseq XML).

Line 15:  Run the pipeline.

Adjusting
---------

Implementing a simple EfetchAnalzyer
-------------------------------------

  WIP, but see ``examples/entrezpy-example.wally.fetch-genome.py``, lines 74-85.
