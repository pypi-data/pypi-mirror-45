=============================
test_django_cookie_app
=============================

.. image:: https://badge.fury.io/py/test_django_cookie_app.svg
    :target: https://badge.fury.io/py/test_django_cookie_app

.. image:: https://travis-ci.org/greatbharat/test_django_cookie_app.svg?branch=master
    :target: https://travis-ci.org/greatbharat/test_django_cookie_app

.. image:: https://codecov.io/gh/greatbharat/test_django_cookie_app/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/greatbharat/test_django_cookie_app

Learning DjangoCookieCuttterApp

Documentation
-------------

The full documentation is at https://test_django_cookie_app.readthedocs.io.

Quickstart
----------

Install test_django_cookie_app::

    pip install test_django_cookie_app

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'test_django_cookie_app.apps.TestDjangoCookieAppConfig',
        ...
    )

Add test_django_cookie_app's URL patterns:

.. code-block:: python

    from test_django_cookie_app import urls as test_django_cookie_app_urls


    urlpatterns = [
        ...
        url(r'^', include(test_django_cookie_app_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
