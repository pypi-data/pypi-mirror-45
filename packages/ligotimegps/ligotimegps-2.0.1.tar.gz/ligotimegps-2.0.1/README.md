[![PyPI version](https://badge.fury.io/py/ligotimegps.svg)](http://badge.fury.io/py/ligotimegps)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1180873.svg)](https://doi.org/10.5281/zenodo.1180873)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/ligotimegps.svg)](https://travis-ci.org/gwpy/ligotimegps)
[![Unix Build Status](https://travis-ci.org/gwpy/ligotimegps.svg?branch=master)](https://travis-ci.org/gwpy/ligotimegps)
[![Windows Build status](https://ci.appveyor.com/api/projects/status/6axppguvhsfepgjf?svg=true)](https://ci.appveyor.com/project/gwpy/ligotimegps)
[![Coverage Status](https://coveralls.io/repos/github/gwpy/ligotimegps/badge.svg?branch=master)](https://coveralls.io/github/gwpy/ligotimegps?branch=master)

This module provides a pure-python version of the `LIGOTimeGPS` class, used to represent GPS times (number of seconds elapsed since GPS epoch) with nanoseconds precision.

This module is primarily for use as a drop-in replacement for the 'official' `lal.LIGOTimeGPS` class (provided by the SWIG-python bindings of [LAL](//wiki.ligo.org/DASWG/LALSuite)) for use on those environments where LAL is not available, or building LAL is unnecessary for the application (e.g. testing).

The code provided here is much slower than the C-implementation provided by LAL, so if you really care about performance, don't use this module.

## How to install

```bash
pip install ligotimegps
```

## How to use

```python
>>> from ligotimegps import LIGOTimeGPS
>>> t = LIGOTimeGPS(12345, 67890)
>>> print(t)
12345.00006789
```
