Commands
========

createuser
----------

Used to create a user.

.. program:: createuser

.. option:: username

Login; required

.. option:: -h, --help

show this help message and exit

.. option:: --email EMAIL

Email; required

.. option:: --first_name FIRST_NAME

First name; optional

.. option:: --last_name LAST_NAME

Last name; optional

.. option:: --password PASSWORD

Password; optional

.. option:: --is-staff

Staff status; optional, default is False

.. option:: --is-superuser

Superuser status; optional, default is False

.. option:: -g GROUPS, --groups GROUPS

List of user's groups; optional, comma is a separator

.. option:: --database DATABASE

Specifies the database to use; optional, default is ``"default"``

.. option:: --version

show program's version number and exit

.. option:: -v LEVEL, --verbosity LEVEL

Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very
verbose output

.. option:: --settings SETTINGS

The Python path to a settings module, e.g. ``"myproject.settings.main"``. If
this isn't provided, the ``DJANGO_SETTINGS_MODULE`` environment variable will
be used.

.. option:: --pythonpath PYTHONPATH

A directory to add to the Python path, e.g.
``"/home/djangoprojects/myproject"``.

.. option:: --traceback

Raise on ``CommandError`` exceptions

.. option:: --no-color

Don't colorize the command output.

.. option:: --force-color

Force colorization of the command output.
