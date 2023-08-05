.. image:: https://img.shields.io/pypi/v/django-createuser.svg
   :target: https://pypi.python.org/pypi/django-createuser
.. image:: https://travis-ci.org/dex4er/django-createuser.svg?branch=master
   :target: https://travis-ci.org/dex4er/django-createuser
.. image:: https://readthedocs.org/projects/django-createuser/badge/?version=latest
   :target: http://django-createuser.readthedocs.org/en/latest/
.. image:: https://img.shields.io/pypi/pyversions/django-createuser.svg
   :target: https://www.python.org/
.. image:: https://img.shields.io/pypi/djversions/django-createuser.svg
   :target: https://www.djangoproject.com/

django-createuser
=================

``django-createuser`` is a package that allows to create users for Django
application with ``./manage.py`` command.


Installation
------------

Install with ``pip`` or ``pipenv``:

.. code:: python

  pip install django-createuser

Add ``django_createuser`` to your installed apps in your
settings.py file:

.. code:: python

  INSTALLED_APPS = [
      'django_createuser',
      ...
  ]


Commands
--------

createuser
^^^^^^^^^^

Used to create a user.

positional arguments:

  +--------------+-----------------+
  | ``username`` | Login; required |
  +--------------+-----------------+

optional arguments:

  -h, --help            show this help message and exit
  --email EMAIL         Email; required
  --first_name FIRST_NAME
                        First name; optional
  --last_name LAST_NAME
                        Last name; optional
  --password PASSWORD   Password; optional
  --is-staff            Staff status; optional, default is False
  --is-superuser        Superuser status; optional, default is False
  -g GROUPS, --groups GROUPS
                        List of user's groups; optional, comma is a separator
  --database DATABASE   Specifies the database to use; optional, default is
                        ``"default"``
  --version             show program's version number and exit
  -v LEVEL, --verbosity LEVEL
                        Verbosity level; 0=minimal output, 1=normal output,
                        2=verbose output, 3=very verbose output
  --settings SETTINGS   The Python path to a settings module, e.g.
                        ``"myproject.settings.main"``. If this isn't provided,
                        the ``DJANGO_SETTINGS_MODULE`` environment variable
                        will be used.
  --pythonpath PYTHONPATH
                        A directory to add to the Python path, e.g.
                        ``"/home/djangoprojects/myproject"``.
  --traceback           Raise on ``CommandError`` exceptions
  --no-color            Don't colorize the command output.
  --force-color         Force colorization of the command output.


Documentation
-------------

See http://django-createuser.readthedocs.org/


License
-------

Copyright © 2019, Piotr Roszatycki

This software is distributed under the GNU Lesser General Public License (LGPL
3 or greater).
