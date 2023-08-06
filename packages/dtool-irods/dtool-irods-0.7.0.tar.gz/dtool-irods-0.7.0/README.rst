Add iRODS support to dtool
==========================

.. image:: https://badge.fury.io/py/dtool-irods.svg
   :target: http://badge.fury.io/py/dtool-irods
   :alt: PyPi package

- GitHub: https://github.com/jic-dtool/dtool-irods
- PyPI: https://pypi.python.org/pypi/dtool-irods
- Free software: MIT License


Features
--------

- Copy datasets to and from iRODS
- List all the datasets in an iRODS zone
- Create datasets directly in iRODS

Installation
------------

To install the dtool-irods package.

.. code-block:: bash

    pip install dtool-irods


Usage
-----

To copy a dataset from local disk (``my-dataset``) to an iRODS zone
(``/data_raw``) one can use the command below.

.. code-block::

    dtool copy ./my-dataset /data_raw irods

To list all the datasets in an iRODS zone one can use the command below.

.. code-block::

    dtool ls /data_raw irods

See the `dtool documentation <http://dtool.readthedocs.io>`_ for more detail.


Configuring the local dtool iRODS cache
---------------------------------------

When fetching items from a dataset, for example using the ``dtool item fetch``
command, the content of the item is cached in a file on local disk. The default
cache directory is ``~/.cache/dtool/irods``.

One may want to change this directory. For example, if working on a HPC cluster
to set it to a directory that lives on fast solid state disk. This can be achieved
by setting the ``DTOOL_IRODS_CACHE_DIRECTORY`` environment variable. For example

.. code-block::

    mkdir -p /tmp/dtool/irods
    export DTOOL_IRODS_CACHE_DIRECTORY=/tmp/dtool/irods

Alternatively, when using the ``dtool`` command line interface one can add the
``DTOOL_IRODS_CACHE_DIRECTORY`` key to the ``~/.config/dtool/dtool.json`` file.
For example,

.. code-block:: json

    {
       "DTOOL_IRODS_CACHE_DIRECTORY": "/tmp/dtool/irods"
    }

If the file does not exist one may need to create it.


Related packages
----------------

- `dtoolcore <https://github.com/jic-dtool/dtoolcore>`_
- `dtool-cli <https://github.com/jic-dtool/dtool-cli>`_
- `dtool-symlink <https://github.com/jic-dtool/dtool-symlink>`_
