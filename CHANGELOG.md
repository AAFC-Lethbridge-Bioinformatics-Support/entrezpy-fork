# Changelog

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
(or tries as best as it can)

## [Unreleased](https://gitlab.com/ncbipy/entrezpy/compare/2.0.2...master)

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
