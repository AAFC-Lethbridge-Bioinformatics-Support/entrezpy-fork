.. _install:

Installation
============

``entrezpy`` can be installed or included into your own pipeline using two
approaches: :ref:`pipyinstall` or :ref:`syspathinstall`.

Requirements
------------

- `Python <https://www.python.org/>`_ version >= 3.6
- `Python Standard Library <https://docs.python.org/3/library/index.html#the-python-standard-library>`_ :
   *The standard library should be installed with  Python. Just in
   case, these modules from the Python Standard Library are required:*
  - base64
  - io
  - json
  - logging
  - math
  - os
  - queue
  - random
  - socket
  - sys
  - threading
  - time
  - urllib
  - uuid
  - xml.etree.ElementTree

Test your Python version
------------------------
Test if we have at least **Python 3.6** :

.. code:: python

$ python

>>> import sys
>>> sys.version_info
>>> sys.version_info(major=3, minor=6, micro=6, releaselevel='final', serial=0)
                           ^        ^


.. _pipyinstall:

PyPi
----
Install ``entrezpy`` via PyPi and check:

.. code::

  $ pip install entrezpy --user

Test if we can import ``entrezpy``:

.. code::

  $ python

>>> import entrezpy

.. _syspathinstall:

Append to ``sys.path``
----------------------
Add ``entrezpy`` to your pipeline via `sys.path`. This requires to clone
the source code adjusting `sys.path`.

Assuming following directory structure where entrezpy was cloned into
``include``:

::

  $ git clone https://gitlab.com/ncbipy/entrezpy.git project_root/include

  project_root
  |
  |-- src
  |   `-- pipeline.py
  `-- include
      `-- entrezpy
          `-- src
              `-- entrezpy
                  `-- efetch

Importing the module ``efetcher`` in ``pipeline.py`` by adjust ``sys.path`` in
``project_root/src/pipeline.py``

.. code::

  sys.path.insert(1, os.path.join(sys.path[0], '../include/entrezpy/src'))
  import entrezpy.efetch.efetcher

  ef = entrezpy.efetch.efetcher.Efetcher('toolname', 'email')

Test ``entrezpy``
-----------------
Run the examples in the git repository in ``entrezpy/examples``, e.g:

::

  $ ./path/to/entrezpy/examples/entrezpy-example.elink.py --email you@email

To adjust the examples for testing an installation via PyPi, remove the
``sys.path`` line in the examples prior to invoking them, e.g.

.. code:: bash

  for i in entrezpy/examples/*.py; do                 \
    fname=$(basename $i | sed 's/\.py/\.adjust.py/'); \
    sed '/sys.path.insert/d' $i > $fname;             \
    chmod +x $fname;                                  \
  done;

The examples print the results onto the standard output and additional
information onto standard error. Currently, we propose to run the examples and
redirecting standard error to a file. For example, testing ``efetch``,
run ``examples/entrezpy-example.efetch.py`` as follows:

::

  ./examples/entrezpy-example.efetch.py --email you@email 2> efetch.stderr

``efetch.stderr`` can be monitored as follows:

::

  tail -f efetch.stderr
