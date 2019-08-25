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
