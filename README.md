mentors.debian.net
==================

This is a reboot of the mentors.debian.net codebase, using django.

Why start from scratch?
-----------------------

The Pylons legacy of the previous codebase is hard to bear, and motivation
was (very) low to make it cleaner. This is an attempt at reviving the
project, from a clean slate.

Don't worry, the good parts of the current debexpo codebase will be kept.

How do I run it?
----------------

You should use a virtualenv (python virtual environment), as this is the
way to go to ensure a consistent environment across all deployments.

We provide you with a requirements.txt file that you can feed to pip in
order to install all the dependencies at once:

    pip install -r requirements.txt

When this is done, you need to fill in the configuration template in
mentors/settings/prod_sample.py and save it as mentors/settings/prod.py.
You can use
    python manage.py generate_secret_key
to generate a secret key for your settings file.

You are now all set to create your database:

    python manage.py syncdb
    python manage.py migrate

To collect the static files from all apps, run:
    python manage.py collectstatic

Finally, you can run the project:
    python manage.py runserver

How do I contribute?
--------------------

TODO.

Long story short is, please submit patches via the debexpo-devel mailing list,
or send us a heads-up on IRC #debexpo (irc.debian.org).

In your first contribution, please add yourself to the AUTHORS and COPYING
files. When adding files, don't forget the copyright notices.
