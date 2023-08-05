pl-simpledsapp_moc
================================

.. image:: https://badge.fury.io/py/simpledsapp_moc.svg
    :target: https://badge.fury.io/py/simpledsapp_moc

.. image:: https://travis-ci.org/FNNDSC/simpledsapp_moc.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/simpledsapp_moc

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-simpledsapp_moc

.. contents:: Table of Contents


Abstract
--------

A simple DS type ChRIS application specifically created for the Massachusetts Open Cloud remote computing environment.


Synopsis
--------

.. code::

    python simpledsapp_moc.py                                       \
        [--prefix <filePrefixString>]                               \
        [--sleepLength <sleepLength>]                               \
        [--ignoreInputDir]                                          \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Description
-----------

``simpledsapp_moc.py`` is a ChRIS-based application that basically does an explicit copy of each file in  an input directory to the output directory, prefixing an optional string to each filename.

Agruments
---------

.. code::

    [--prefix <prefixString>]
    If specified, a prefix string to append to each file copied.

    [--sleepLength <sleepLength>]
    If specified, sleep for <sleepLength> seconds before starting script processing. This is to simulate a possibly long running  process.

    [--ignoreInputDir] 
    If specified, ignore the input directory. Simply write a single json  file to the output dir that is a timestamp. Useful if the input  directory contains large nested file trees.

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install simpledsapp_moc

and run with

.. code:: bash

    simpledsapp_moc.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    simpledsapp_moc.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-simpledsapp_moc simpledsapp_moc.py                \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-simpledsapp_moc simpledsapp_moc.py                \
            --man                                                       \
            /incoming /outgoing

Examples
--------





