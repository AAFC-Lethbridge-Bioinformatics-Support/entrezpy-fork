# README

## Synopsis
entrezpy is a dedicated Python library to query and retrieve data from Entrez
databases at NCBI in analysis pipelines. It supports multi-threading, has no
external dependencies, and simplifies the construction of complex queries. Its
design allows to adjust for specific data types and formats without the need to
change the underlying functions.

## Installation

### Cloning repository

Repository without wiki:

- `git clone https://gitlab.com/ncbipy/entrezpy.git`

Whole repository:

- `git >=2.13`:
    - `git clone --recurse-submodules -j2 https://gitlab.com/ncbipy/entrezpy.git`

- `git >= 1.65`:
    - `git clone --recursive  https://gitlab.com/ncbipy/entrezpy.git`

- `git < 1.65`:

    0. `git clone https://gitlab.com/ncbipy/entrezpy.git`
    1. `cd ncbipy_eutils`
    2. `git submodule update --init --recursive`

### Import
  For example, import the esearch library add following lines to your code:
```
sys.path.insert(1, os.path.join(sys.path[0], 'path/to/entrezpy/src'))
import esearch.esearcher
import esearch.esearch_analyzer
```
### Examples

Ready to use examples using ncbipy-eutils are given in the repository
[https://gitlab.com/ncbipy/entrezpy.git].