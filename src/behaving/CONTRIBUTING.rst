Contributing to behaving
========================

* fork the project
* do your stuff
* make sure all tests pass and add new ones demonstrating your contribution
* update the documentation if necessary
* update ``CHANGES.txt`` with your github user id
* make a pull request!

Setting up a development environment
------------------------------------

After you clone the *behaving* repository you end up with a python package including a buildout configuration.
It is assumed you already have the tools installed for android and iOS development. If you don't you should still be able to work on the non-mobile parts of behaving.

To set things up run:

::

    python bootstrap.py
    ./bin/buildout

This will download and setup everything you need and also build the mobile test apps on iOS and android.

Running tests
-------------

Run *supervisord* which will make manage running the SMS, mail & GCM mock servers and an HTTP server for testing.

::

    ./bin/supervisord


You don't need to run supervisor again but you can control it by ``./bin/supervisorctl``

With supervisor running you can run all tests:

::

    ./bin/test

Any command line arguments to test will be passed to *behave*, so you can do things like:

::

    ./bin/test --tags=ios

to run all iOS tests or

::

    ./bin/test --no-capture

to be able to get a ``pdb`` prompt for instance.