EEmeter: tools for calculating metered energy savings
=====================================================

.. image:: https://travis-ci.org/openeemeter/eemeter.svg?branch=master
  :target: https://travis-ci.org/openeemeter/eemeter
  :alt: Build Status

.. image:: https://img.shields.io/github/license/openeemeter/eemeter.svg
  :target: https://github.com/openeemeter/eemeter
  :alt: License

.. image:: https://readthedocs.org/projects/eemeter/badge/?version=master
  :target: https://eemeter.readthedocs.io/?badge=master
  :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/eemeter.svg
  :target: https://pypi.python.org/pypi/eemeter
  :alt: PyPI Version

.. image:: https://codecov.io/gh/openeemeter/eemeter/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/openeemeter/eemeter
  :alt: Code Coverage Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/ambv/black
  :alt: Code Style

---------------

**EEmeter** — open source implementations of standard methods for calculating
metered energy savings.

The eemeter contains the reference implementation of the CalTRACK methods for
computing metered energy usage differences at sites with building efficiency
interventions or at control sites without known interventions.

Installation
------------

EEmeter is a python package and can be installed with pip.

::

    $ pip install eemeter

Features
--------

- Candidate model selection
- Data sufficiency checking
- Reference implementation of standard methods

  - CalTRACK Daily Method
  - CalTRACK Monthly Method

- Flexible sources of temperature data. See `EEweather <https://eeweather.readthedocs.io>`_.
- Model serialization
- First-class warnings reporting
- Pandas dataframe support
- Visualization tools

Command-line Usage
------------------

Once installed, ``eemeter`` can be run from the command-line. To see all available commands, run ``eemeter --help``.

Use CalTRACK methods on sample data::

    $ eemeter caltrack --sample=il-electricity-cdd-hdd-daily

Save output::

    $ eemeter caltrack --sample=il-electricity-cdd-only-billing_monthly --output-file=/path/to/output.json

Load custom data (see ``eemeter.meter_data_from_csv`` and ``eemeter.temperature_data_from_csv`` for formatting)::

    $ eemeter caltrack --meter-file=/path/to/meter/data.csv --temperature-file=/path/to/temperature/data.csv

Do not fit CDD-based candidate models (intended for gas data)::

    $ eemeter caltrack --sample=il-gas-hdd-only-billing_bimonthly --no-fit-cdd
