Entrezpy tutorials
==================

Wally
-----

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

Line 3: Create a new pipeline and store it in get_sequences

Line 6: Add search query to the pipeline and store its id in ''sid''

Line 10: Add fetch query to the pipeline

Line 13: Run pipeline and store the resulting analyzer

Linking within and between Entrezpy databases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using multiple links in a Wally pipeline requires to run an Esearch afterwwards
to keep track of the proper UIDs. This is a quirk of the E-Eutilties
(Entrez-Direct uses the same trick).

The following code shows howto use multiple links within a Wally pipeline::

  import entrezpy.wally

  w = entrezpy.wally.Wally(args.email, args.apikey, args.apikey_envar, threads=args.threads)

  find_genomes = w.new_pipeline()

  sid = find_genomes.add_search({'db':'pubmed', 'term' : 'capsid AND infection', 'rettype':'count'})
  lid1 = find_genomes.add_link({'cmd':'neighbor_history', 'db':'pubmed'}, dependency=sid)
  lid1_1 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid1)
  lid2 = find_genomes.add_link({'db':'nuccore', 'cmd':'neighbor_history'}, dependency=lid1_1)
  lid2_1 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid2)
  lid3 = find_genomes.add_search({'rettype': 'count', 'cmd':'neighbor_history'}, dependency=lid2_1)
  find_genomes.add_fetch({'retmode':'xml', 'rettype':'fasta'}, dependency=lid3)
  a = w.run(find_genomes)
