# Changelog

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(or tries as best as it can)

## [Unreleased](https://gitlab.com/ncbipy/entrezpy/compare/2.1.2...master)

## [2.1.2](https://gitlab.com/ncbipy/entrezpy/compare/2.1.0...2.1.2) - 2021-03-24

### Fixed

  - Not declared local variable in base analyzer aborting fetch commands

## [2.1.0](https://gitlab.com/ncbipy/entrezpy/compare/2.0.5...2.1.0)

### New

  - Applications can control the level of logging

### Changed

  - Using explicit threading locks for queries


## [2.0.5](https://gitlab.com/ncbipy/entrezpy/compare/2.0.4...2.0.5) - 2020-06-05

### Fixed

  - Typo in EsummaryAnalyzer

## [2.0.4](https://gitlab.com/ncbipy/entrezpy/compare/2.0.3...2.0.4) - 2020-05-18

### Fixed

  - Adjust max retmax values for Efetch and Essumary

## [2.0.3](https://gitlab.com/ncbipy/entrezpy/compare/2.0.2...2.0.3)

### Fixed

  - Adjust retmax for FASTA efetch to fetch all requested entries (Issue #6)

## [2.0.2](https://gitlab.com/ncbipy/entrezpy/compare/2.0.1...2.0.2) - 2019-08-25

### Fixed

  - set error flag in `entrezpy.base.analyzer.EutilsAnalyzer.parse()` before
    passing error to `entrezpy.base.analyzer.EutilsAnalyzer.analyze_error()`.

### Changed

  - Sphinx documentation reordering

### Added

  - Tutorial for extending `entrezpy` by adjusting `EutilsResult` and `EutilsAnalyzer`

## [2.0.1](https://gitlab.com/ncbipy/entrezpy/compare/2.0.0...2.0.1) - 2019-04-30

### Fixed

  - efetch example

## [2.0.0](https://gitlab.com/ncbipy/entrezpy/compare/1.0.0...2.0.0) - 2019-04-30

### Changed

  - Rename Wally to Conduit: `entrezpy.wally.Wally -> entrezpy.conduit.Conduit`
  - Update examples
  - Revise manuscript

## [1.0.0](https://gitlab.com/ncbipy/entrezpy/tree/1.0.0) - 2019-03-26

### Added

 - Initial release
 - Pypi version 1.0
 - Manuscript
 - readthedocs documentation
