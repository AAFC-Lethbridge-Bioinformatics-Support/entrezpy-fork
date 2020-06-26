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
