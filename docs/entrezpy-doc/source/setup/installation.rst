Installation
============

Entrezpy is a library which facilitates interacting with NCBI Entrez databases
via NCBI's E-Utils. To use it, Entrezpy has to be in Python's module search
path (sys.path), whoch can be achives using two approaches:
one of the two po. Two possibilities are:

  - PyPi
  - git clone and adjust sys.path in your tool

Adjusting the path is preferred since it can be directly incorporated into the
project, skipping the PyPi step.

Using PyPi
----------


Append to sys.path
------------------
 - git clone https://gitlab.com/ncbipy/entrezpy.git path/to/entrezpy
 - sys.path.insert(1, os.path.join(sys.path[0], 'path/to/entrezpy'))

Example
~~~~~~~
Project structure:

  ::

    project_root
    |
    |-- src
    |  `-- main_tool

The entrezpy libary can be imported by adjusting
