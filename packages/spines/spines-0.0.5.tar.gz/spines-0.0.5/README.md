# Spines


**Backbones for parameterized models.**


[![Build Status](https://travis-ci.org/douglasdaly/spines.svg?branch=master)](https://travis-ci.org/douglasdaly/spines)
[![Coverage Status](https://coveralls.io/repos/github/douglasdaly/spines/badge.svg)](https://coveralls.io/github/douglasdaly/spines)
[![Documentation Status](https://readthedocs.org/projects/spines/badge/?version=latest)](https://spines.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/spines.svg)](https://pypi.org/project/spines/)
[![Status](https://img.shields.io/pypi/status/spines.svg)](https://pypi.org/project/spines/)
[![Python Versions](https://img.shields.io/pypi/pyversions/spines.svg)](https://pypi.org/project/spines/)


![Spines Logo](./docs/_static/images/spines_logo_256.png "Spines Logo")


## About

Spines was built to provide a skeleton for Model classes: a common
interface for users to build models around (with some tools and
utilities which take advantage of those commonalities).  It's core Model
class is similar, in structure, to some of scikit-learn's underlying
Estimator classes - but with a single set of unified functions for all
models, namely:

- Build
- Fit
- Predict
- Score
- Error

The predict method is the only one that's required to be implemented,
though the others are likely useful most of the time (and often required
to take advantage of some of the additional utilities provided by
spines).

Spines also incorporates automatic version management for your models -
something akin to a very lightweight git - but for individual models.
It also caches results generated during various iterations of the
development/fitting process so that they're not lost during - something
that can (and often does) happen during very iterative model development
work.


## Installing

To install spines use your package manager of choice, an example using 
`pipenv` would be:

```bash
$ pipenv install spines
```


## Documentation

The latest documentation is hosted on 
[read the docs](https://spines.readthedocs.io/ "Spines ReadTheDocs").


## License

This project is licensed under the MIT License, for more information see 
the [LICENSE](https://github.com/douglasdaly/spines/blob/master/LICENSE) 
file.
