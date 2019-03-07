E-Utils function implemented by entrezpy
========================================
Entrezpy implements the following E-Utils functions to interact with NCBI's
Entrez databases. The functions share the same underlying structure as described
in entrezpy_base. All functions accept a dictionary mapping the same parameters
as the corresponding E-Utility, e.g. the parameters for ESearch () are the
same as thos for entrezpy's Esearcher().

All entrezpy functions understand the correspondong E-Utils parameters. To allow
increased versatilty, some entrezpy function have parametsr allowing
fine-tuning, e.g. Elink.


ESearch
-------

Esearcher parameters
~~~~~~~~~~~~~~~~~~

ESearch result
~~~~~~~~~~~~~~

EFetch
------

EFetch parameters
~~~~~~~~~~~~~~~~~~

EFetch result
~~~~~~~~~~~~~

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
class Linkset
`-

inquire()
---------
analyer instance as default parametes vs as given parameter
