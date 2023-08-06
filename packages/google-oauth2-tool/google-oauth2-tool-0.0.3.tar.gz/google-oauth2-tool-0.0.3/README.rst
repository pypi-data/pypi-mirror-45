Create OAuth2 key file from OAuth2 client id file
=================================================

Simple wrapper for oauth2client.tools module.


.. image:: https://travis-ci.org/dlancer/google-oauth2-tool.svg?branch=master
    :target: https://travis-ci.org/dlancer/google-oauth2-tool/
    :alt: Build status

.. image:: https://img.shields.io/pypi/v/google-oauth2-tool.svg
    :target: https://pypi.python.org/pypi/google-oauth2-tool/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/format/google-oauth2-tool.svg
    :target: https://pypi.python.org/pypi/google-oauth2-tool/
    :alt: Download format

.. image:: https://img.shields.io/pypi/l/google-oauth2-tool.svg
    :target: https://pypi.python.org/pypi/google-oauth2-tool/
    :alt: License

Installation
============


PIP
---

You can install the latest stable package running this command::

    $ pip install google_oauth2_tool


Also you can install the development version running this command::

    $ pip install git+http://github.com/dlancer/google_oauth2_tool.git@dev


Usage
=====

Before you start you should:

1. Create Google OAuth2 client id key in the Google Developers console.

2. Create file with required Google API scopes.

From command line::

    $ oauth2_tool --help

    $ oauth2_tool --source=client_id.json --scope=scopes.txt --destination=oauth2_key.json [--strip=true]
