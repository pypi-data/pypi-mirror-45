django-customer-billing
============

[![Build Status](https://travis-ci.org/skioo/django-customer-billing.svg?branch=master)](https://travis-ci.org/skioo/django-customer-billing)
[![PyPI version](https://badge.fury.io/py/django-customer-billing.svg)](https://badge.fury.io/py/django-customer-billing)
[![Requirements Status](https://requires.io/github/skioo/django-customer-billing/requirements.svg?branch=master)](https://requires.io/github/skioo/django-customer-billing/requirements/?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)


Requirements
------------

* Python: 3.5 and over
* Django: 2.0 and over


Usage
-----

Add billing to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'billing.apps.BillingConfig,
        ...
    )


Run the migrations: 

    ./manage.py migrate


Development
-----------

To install all dependencies:

    python setup.py develop
    
To update all dependencies:

    python setup.py develop -U

To run unit tests:

    pip install pytest-django
    pytest

To lint, typecheck, unit test:

    tox

To generate a diagram representing the state-machines:

    pip install graphviz
    ./manage.py graph_transitions -o docs/state-machines.png


To install the version being developed into another django project:

    pip install -e <path-to-this-directory>
