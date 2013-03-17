Install
=========

Working Environment
-------------------

Those instructions assume that you are using a Debian install.

The recommended way to run this is to use a virtualenv. If you don't want
to, I'm afraid you're on your own, as unfortunately managing dependencies
for web development project is a real pain. You are strongly advised to use
virtualenvwrapper, a nice interface to help you manage your virtual
environments.

To install the system dependencies, as root, use::

    $ apt-get install virtualenvwrapper libpq-dev python-dev

Setting up a database
---------------------

See :doc:`the dedicated page <install_postgres>`

Virtualenv with virtualenvwrapper
---------------------------------

In Linux and Mac OSX, you can install virtualenvwrapper_, which will take
care of managing your virtual environments and adding the project path to
the `site-directory` for you::

    $ mkvirtualenv mentors
    $ cd mentors # you should get to the level where manage.py is
    $ add2virtualenv .

.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/

Installation of Dependencies
----------------------------

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*

Running the project
-------------------

When you are in your virtualenv, and the right dependencies have been
installed, you can run the project. You need to have a PostgreSQL database
available, too.

You first need to set your custom settings. You can override them using
environment variables. This allows us to keep a common settings file,
while keeping passwords out of the repo.

Useful variables to consider are:

SECRET_KEY
    The secret key used by django to cryptographically sign stuff
    (needs to be set for production, a default is provided for
    local testing, but is not secure!)

DATABASE_HOST
    The hostname for the database server (default: ``localhost``)

DATABASE_PORT
    The port for the database server (default: empty)

DATABASE_NAME
    The name of the database (default: ``mentors``)

DATABASE_USER
    The user for the database server (default: ``mentors``)

DATABASE_PASS
    The password for the database server (default: empty)

EMAIL_HOST
    Your SMTP server (default: ``localhost``)

EMAIL_PORT
    The port your SMTP server listens to (default: ``25``)

EMAIL_HOST_USER
    The user you need to identify to the SMTP server (default: empty)

EMAIL_HOST_PASSWORD
    The SMTP password (default: empty, no authentication is made)

SERVER_EMAIL
    The From: address for emails sent by django (default:
    ``support@mentors.debian.net``)

Those variables can helpfully be set in the initialisation files of
your virtualenv, e.g. `~/.virtualenvs/mentors/bin/activate`.

Once the variables are set, you are ready to setup the database for
use by django::
    
    $ django-admin.py syncdb --settings=mentors.settings.local
    $ django-admin.py migrate --settings=mentors.settings.local

To avoid typing `--settings=mentors.settings.local` all the time, you
can export the `DJANGO_SETTINGS_MODULE` environment variable.

You can now create a new superuser::

    $ django-admin.py createsuperuser --settings=mentors.settings.local

Once you're done, you should be able to run the django development
server::
    
    $ django-admin.py runserver --settings=mentors.settings.local

You can then point your browser to `the right address`_ and enjoy your
fresh install.

.. _`the right address`: http://localhost:8000/

