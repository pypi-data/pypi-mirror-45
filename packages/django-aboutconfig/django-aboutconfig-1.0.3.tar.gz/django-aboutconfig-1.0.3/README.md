Django-Aboutconfig
==================

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Codeship](https://codeship.com/projects/49cf7540-11ab-0134-4d7f-228fbb5b3c99/status?branch=default)](https://codeship.com/projects/157317)
[![codecov](https://codecov.io/bb/impala/django-aboutconfig/branch/default/graph/badge.svg)](https://codecov.io/bb/impala/django-aboutconfig/branch/default)
[![PyPI version](https://badge.fury.io/py/django-aboutconfig.svg)](https://pypi.python.org/pypi/django-aboutconfig)
[![Openhub](https://www.openhub.net/p/django-aboutconfig/widgets/project_thin_badge.gif)](https://www.openhub.net/p/django-aboutconfig)


A firefox-like about:config implementation for one-off settings in Django apps.

#### Compatible Python versions
3.4+

#### Compatible Django versions
1.11, 2.0 - 2.2


## Installation

You can install `aboutconfig` either from source or via pip:

    pip install django-aboutconfig

The only thing you need to do to configure it is add it to your `INSTALLED_APPS` like all other
django applications:

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        ...
        'aboutconfig'
    ]

Then just run `manage.py migrate` and you're good to go.

**Note:** `aboutconfig` relies on having a good caching mechanism to be fast (all configured values
are preloaded into cache on start-up). You should ideally have something like memcached
configured to avoid slowdowns. [See Django documentation for details](https://docs.djangoproject.com/en/stable/topics/cache/).


## Usage

By default, `aboutconfig` comes with four supported data-types: integer, boolean, string and
decimal. All data types are configurable and you can add your own if necesessary.

To add some configuration values, head over to the django admin and add an instance of the `Config`
model.

Having done this, you can access the configuration value via `aboutconfig.get_config()` in Python
code or the `get_config` template filter (load `config` before using).

### Python code:

    from aboutconfig import get_config

    def my_view(request):
        # some code...
        admin_email = get_config('admin.details.email')
        # some more code...


### Template code:

    {% load config %}

    The website admin's email is {{ 'admin.details.email'|get_config }}.

    >>> An assignment tag also exists for convenience:

    {% get_config 'admin.details.email' as email %}
    The website admin's email is <a href="mailto:{{ email }}">{{ email }}</a>.
