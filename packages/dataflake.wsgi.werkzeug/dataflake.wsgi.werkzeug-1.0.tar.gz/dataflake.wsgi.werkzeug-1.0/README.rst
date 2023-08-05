.. image:: https://travis-ci.com/dataflake/dataflake.wsgi.werkzeug.svg?branch=master
   :target: https://travis-ci.com/dataflake/dataflake.wsgi.werkzeug

.. image:: https://coveralls.io/repos/github/dataflake/dataflake.wsgi.werkzeug/badge.svg?branch=master
   :target: https://coveralls.io/github/dataflake/dataflake.wsgi.werkzeug?branch=master

.. image:: https://readthedocs.org/projects/dataflakewsgiwerkzeug/badge/?version=latest
   :target: https://dataflakewsgiwerkzeug.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/dataflake.wsgi.werkzeug.svg
   :target: https://pypi.org/project/dataflake.wsgi.werkzeug/
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/dataflake.wsgi.werkzeug.svg
   :target: https://pypi.org/project/dataflake.wsgi.werkzeug/
   :alt: Supported Python versions


dataflake.wsgi.werkzeug
======================

This package provides a PasteDeploy-compatible entry point to easily integrate
the `werkzeug WSGI server <https://werkzeug.palletsprojects.com>`_ into an
environment that uses PasteDeploy-style ``.ini`` files to compose a WSGI
application.

A second entry point will enable the ``werkzeug`` debugger, so you get nice
clickable tracebacks with the ability to open a console prompt at any point in
the stack. The debugger is `explained in the werkzeug documentation 
<https://werkzeug.palletsprojects.com/debug/>`_ and **should never be running 
in production**.

It also includes a script to create a basic WSGI configuration file for Zope,
similar to Zope's own ``mkwsgiinstance``, but specifying ``werkzeug`` instead of
``waitress`` as WSGI server.
