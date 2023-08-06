# matyimodule
[![PyPI](https://img.shields.io/pypi/v/matyimodule.svg)](https://pypi.python.org/pypi/matyimodule)
[![Build Status](https://travis-ci.org/MatyiFKBT/matyimodule.svg?branch=master)](https://travis-ci.org/MatyiFKBT/matyimodule)

Ez csak egy minta, hogy hogyan lehet python csomagot létrehozni, és
közzétenni, hogy mások egyszerűen használhassák.
## Használat
### Python
`pip install matyimodule`
``` python
import matyimodule as m
a = m.mark() # markdown-t ad vissza
print(a)
>>> '<p>Matyi vagyok <em>cső</em></p>'
```
### Parancssor
``` bash
$ matyicommand

> siker.
```
## Feltöltés
```bash
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```