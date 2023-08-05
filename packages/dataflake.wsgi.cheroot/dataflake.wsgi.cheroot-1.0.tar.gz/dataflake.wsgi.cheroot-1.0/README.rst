.. image:: https://travis-ci.com/dataflake/dataflake.wsgi.cheroot.svg?branch=master
   :target: https://travis-ci.com/dataflake/dataflake.wsgi.cheroot

.. image:: https://coveralls.io/repos/github/dataflake/dataflake.wsgi.cheroot/badge.svg?branch=master
   :target: https://coveralls.io/github/dataflake/dataflake.wsgi.cheroot?branch=master

.. image:: https://readthedocs.org/projects/dataflakewsgicheroot/badge/?version=latest
   :target: https://dataflakewsgicheroot.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/dataflake.wsgi.cheroot.svg
   :target: https://pypi.org/project/dataflake.wsgi.cheroot/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/dataflake.wsgi.cheroot.svg
   :target: https://pypi.org/project/dataflake.wsgi.cheroot/
   :alt: Supported Python versions


dataflake.wsgi.cheroot
======================

This package provides a PasteDeploy-compatible entry point to easily integrate
the `cheroot WSGI server <https://github.com/cherrypy/cheroot>`_ into an
environment that uses PasteDeploy-style ``.ini`` files to compose a WSGI
application.

It also includes a script to create a basic WSGI configuration file for Zope,
similar to Zope's own ``mkwsgiinstance``, but specifying ``cheroot`` instead of
``waitress`` as WSGI server.
