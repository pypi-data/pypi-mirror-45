pytest-neo
==========

.. image:: https://img.shields.io/pypi/v/pytest-neo.svg
    :target: https://pypi.org/project/pytest-neo/

.. image:: https://img.shields.io/pypi/pyversions/pytest-neo.svg
    :target: https://pypi.org/project/pytest-neo/

.. image:: https://codecov.io/gh/MyGodIsHe/pytest-neo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/MyGodIsHe/pytest-neo
    :alt: Code coverage Status

.. image:: https://travis-ci.org/MyGodIsHe/pytest-neo.svg?branch=master
    :target: https://travis-ci.org/MyGodIsHe/pytest-neo


pytest-neo is a plugin for `py.test`_ that shows tests like screen of
Matrix.

Requirements
------------

You will need the following prerequisites in order to use pytest-neo:

-  Python 2.7, 3.4 or newer
-  pytest 2.9.0 or newer

Installation
------------

To install pytest-neo:

::

   $ pip install pytest-neo

Then run your tests with:

::

   $ py.test

If you would like to run tests without pytest-neo, use:

::

   $ py.test -p no:neo

.. _py.test: http://pytest.org
