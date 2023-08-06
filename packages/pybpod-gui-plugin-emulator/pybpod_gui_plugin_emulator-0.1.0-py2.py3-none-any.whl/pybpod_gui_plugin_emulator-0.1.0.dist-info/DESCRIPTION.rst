========
Overview
========



Emulator for PyBpod to work with the Bpod's State Machine ports.

At the moment, the Emulator for PyBpod module works by overriding inputs and outputs on a running task protocol.
This will interact directly with a running State Machine in Bpod. As such, any event or state change that
would occur naturally from any of those input or output changes, will occur.


* Free software: MIT license

Current Features
================

* Allows to override the Port components (i.e., LED, Poke and Valve)
* BNC In and Out value override
* Wire inputs and outputs override for Bpod 0.7
* Override Serial message for the connected modules (sends a bytes message)
* Messages are sent while the State Machine is running, triggering the events
  and/or state changes as if the values were coming from the real inputs/outputs.


Installation
============

Please see :ref:`installation` page.

Documentation
=============

https://pybpod-gui-plugin-emulator.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

0.1.0 (2019-05-03)
------------------

* First release on PyPI.
* Added support for Bpod version detection and automatic UI adaptation
  to the different input/output ports and connected modules
* Ports components can be overriden (i.e., LED, Poke and Valve)
* BNC In and Out value override
* Wire inputs and outputs override for Bpod 0.7
* Override Serial message for the connected modules (bytes message)


