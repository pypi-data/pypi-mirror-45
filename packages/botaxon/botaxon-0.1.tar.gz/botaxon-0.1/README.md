botaxon
=======

[![License](https://img.shields.io/github/license/ggueret/botaxon.svg)](https://github.com/ggueret/botaxon/blob/master/LICENSE)
[![Build Status](https://img.shields.io/travis/ggueret/botaxon/master.svg)](https://travis-ci.org/ggueret/botaxon)
[![Coverage Status](https://img.shields.io/coveralls/github/ggueret/botaxon/master.svg)](https://coveralls.io/github/ggueret/botaxon?branch=master)

botaxon is a taxonomic parser for (sub)species botanical names.

It has been used against 3 million names.
It aims to be fast and efficient.


Usage
-----

```python
>>> import botaxon

>>> botaxon.load("Plumeria")
Genus(name='Plumeria', is_hybrid=False)

>>> botaxon.load("Ocimum × citriodorum")
Species(genus=Genus(name='Ocimum', is_hybrid=False), name='citriodorum', is_hybrid=True)

>>> botaxon.load("Cannabis sativa var. indica")
Variety(species=Species(genus=Genus(name='Cannabis', is_hybrid=False), name='sativa', is_hybrid=False), name='indica')
```