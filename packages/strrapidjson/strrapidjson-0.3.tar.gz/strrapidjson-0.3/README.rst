strrapidjson
============

About
-----
**strrapidjson** is a fork of the `pyrapidjson`_ library (version 0.5.1), which in turn is a Python 2.7+ wrapper for `rapidjson`_.
For Python 3+ `python-rapidjson`_ is another alternative.

.. _`pyrapidjson`: https://github.com/hhatto/pyrapidjson
.. _`rapidjson`: https://github.com/miloyip/rapidjson
.. _`python-rapidjson`: https://github.com/python-rapidjson/python-rapidjson

Main design goal of this library is to avoid using unicode() conversions in Python 2,
sticking to (usually UTF8-encoded) str() instead.

* When decoding, library always creates str() objects
* When encoding, *ensure_ascii=False* is applied by default

There are performance advantages to avoiding conversion to unicode() objects when that is not needed.

Performance-wise, **strrapidjson** is faster than the standard library **json** module and comparable
to **ujson** and **simplejson** packages.


Installation
------------
from pip::

    $ pip install strrapidjson


from pip+Github::

    $ pip install git+https://github.com/aarki/strrapidjson


clone and run locally (rexcursive to pull rapidjson submodule)::

    $ git clone --recursive https://github.com/aarki/strrapidjson.git
    $ cd strrapidjson
    $ python setup.py install


Requirements
------------
Python2.7.
Not tested in Python3+ after forking from pyrapidjson


Usage
-----

Drop-in replacement for Python **json** module although function arguments to **dump**/**load** are not supported.

Example::

    >>> import strrapidjson
    >>> strrapidjson.loads('[1, 2, {"test": "hoge"}]')
    >>> [1, 2, {'test': 'hoge'}]
    >>> strrapidjson.dumps([1, 2, {"foo": "bar"}])
    '[1,2,{"foo":"bar"}]'
    >>>


Links
-----
* PyPI_
* GitHub_

.. _PyPI: https://pypi.org/project/strrapidjson/
.. _GitHub: https://github.com/aarki/strrapidjson

