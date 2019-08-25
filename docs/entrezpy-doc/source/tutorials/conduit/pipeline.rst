.. _tutorialpipeline:

Conduit pipelines
~~~~~~~~~~~~~~~~~

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
