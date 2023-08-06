# LibIndic Payyans


[![Build Status](https://travis-ci.org/libindic/payyans.svg?branch=master)](https://travis-ci.org/libindic/payyans)
[![Coverage Status](https://coveralls.io/repos/github/libindic/payyans/badge.svg?branch=master)](https://coveralls.io/github/libindic/payyans?branch=master)


LibIndic's Payyans module may be used to convert texts encoded in ASCII format
to Unicode and vice-versa. More fonts can be added by placing their maps in
`libindic/payyans/maps` folder.

## Installation
1. Clone the repository `git clone https://github.com/libindic/payyans.git`
2. Change to the cloned directory `cd payyans`
3. Run setup.py to create installable source `python setup.py sdist`
4. Install using pip `pip install dist/libindic-payyans*.tar.gz`

## Usage
```
>>> from libindic.payyans import Payyans
>>> instance = Payyans()
>>> result = instance.ASCII2Unicode("aebmfw", "ambili")
>>> print(result)
മലയാളം
>>> result2 = instance.Unicode2ASCII(u"കേരളം", "ambili")
>>> print(result2)
tIcfw
```

For more details read the [docs](http://payyans.rtfd.org/)
