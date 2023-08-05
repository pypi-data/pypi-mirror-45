.. image:: https://img.shields.io/pypi/status/socklet.svg
   :target: https://pypi.org/project/socklet/

.. image:: https://img.shields.io/pypi/l/socklet.svg
   :target: https://pypi.org/project/socklet/

.. image:: https://img.shields.io/pypi/pyversions/socklet.svg
   :target: https://pypi.org/project/socklet/

.. image:: https://img.shields.io/pypi/v/socklet.svg
   :target: https://pypi.org/project/socklet/

.. image:: https://img.shields.io/pypi/dm/socklet.svg
   :target: https://pypi.org/project/socklet/

Usage
=====

This tool can be used to bridge a Socket.IO 0.9 connection to WebSocket.

Installation
============

From PyPI
---------
::

   pip install socklet

From Source
-----------
::

   ./setup.py install

Configuration
=============

A configuration file can be saved to ``~/.config/socklet/config.ini`` to avoid specifying the connection details for each invocation.
Of course, ``$XDG_CONFIG_HOME`` can be set to change your configuration path.
::

    [CLIENT]
    Host = https://example.com
    Port = 443

    [SERVER]
    Host = localhost
    Port = 8765

Development
===========

The source code is located on `GitLab <https://gitlab.com/two-many-tabs/socklet>`_.
To check out the repository, the following command can be used.
::

   git clone https://gitlab.com/two-many-tabs/socklet.git
