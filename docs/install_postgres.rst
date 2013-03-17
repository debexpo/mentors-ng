Setting up a postgresql database for mentors.d.n
================================================

Setting up a database with the right user and access lists is quite simple.

Installing the database server
------------------------------

As root, you need to install `postgresql-server`::
    
    apt-get install postgresql-server

Setting up a new user
---------------------

As the postgres user, you can create a new user::
    
    sudo -u postgres createuser mentors

You don't want that user to create databases, roles or whatnot, so just answer
no to all the questions.

Once the user is created, it doesn't have a password. PostgreSQL likes to
default to ident for its authentication, which means another daemon to setup.
This project uses password authentication on the local socket by default.

To set a password, use::
    
    sudo -u postgres psql -c "ALTER USER mentors WITH PASSWORD '<password>';"

You should then be able to log in to postgresql using the local INET socket::
    
    psql -h localhost -U mentors -W

Setting up a database
---------------------

Finally, you need to set up a *mentors* database owned by the mentors user,
using the UTF-8 encoding::
    
    sudo -u postgres createdb -E UTF-8 -O mentors mentors

You can now continue with :doc:`the rest of the setup instructions <install>`.
