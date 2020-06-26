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
