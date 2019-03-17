E-Utilities by ``entrezpy``
===========================

Entrezpy implements E-Utility functions as queries consisting of at least one
request:

.. code::

        Query
  ................
  |               |
  0 1 2 3 4 5 6 7 8
  |     | |     | |
  +-----+ +-----+ +
     R0     R1    R2


The example depicts the relation  between a query and requests in Entrepy.
The example query consists of 9 data sets using a request size of 4.
``Entrezpy`` resolves this query using two requests (R0 - R1) with the given
size and adjusts the size of the last query (R2).



ELink
-----
Elinker implements ELink queries to E-Utilities [0]. Elinker inherits
query.EutilsQuery and implements the inquire() method to link data sets on NCBI
Entrez servers. All parameters described in [0] are acccepted. Elink queries
can link results

 - between differnt databases within Entrez
 - earlier queries on the Entrez History server
 - to links outside NCBI Entrez, e.g. journal articles.

[0]: https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ELink

Elinker parameters
~~~~~~~~~~~~~~~~~~

ELinker results
~~~~~~~~~~~~~~~
Elink is very versatile, resulting in slightly different results depending on
the use link command. Nevertheless, results can be divided into two categories:

 - linking results: results which can be used out of the box in requests,
   i.e. linking UIDs within Entrez databases.

 - list results: lists with addtional information for the UIDs, e.g.
   links pointing outside Entrez.

Entrezpy can distinguish between them and will prepare a follow-up query if
possible. Entrezpy doesn't prepare follow-up queries for links outside Entrez.
For example, links to journal articles, e.g. DOIs, can point to articles behind
a paywall.

Overall structure
+++++++++++++++++

  ::

   class ElinkResult(result.EutilsResult):

      def __init__(self):
      super().__init__('elink')
      self.linksets = []
      self.cmd = None

      # not showing remaining lines

Entrezpy Elinker results are implemented in ElinkerResult. ElinkerResult stores
Linksets inall received  have the efollowing over structure:



inquire()
---------
analyer instance as default parametes vs as given parameter
