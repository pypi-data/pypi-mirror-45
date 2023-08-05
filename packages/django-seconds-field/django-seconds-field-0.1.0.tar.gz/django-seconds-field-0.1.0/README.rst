.. image:: https://img.shields.io/pypi/v/django-seconds-field.svg
   :target: https://pypi.python.org/pypi/django-seconds-field
.. image:: https://travis-ci.org/dex4er/django-seconds-field.svg?branch=master
   :target: https://travis-ci.org/dex4er/django-seconds-field
.. image:: https://readthedocs.org/projects/django-seconds-field/badge/?version=latest
   :target: http://django-seconds-field.readthedocs.org/en/latest/
.. image:: https://img.shields.io/pypi/pyversions/django-seconds-field.svg
   :target: https://www.python.org/
.. image:: https://img.shields.io/pypi/djversions/django-seconds-field.svg
   :target: https://www.djangoproject.com/

django-seconds-field
====================

``django-seconds-field`` provides additional ``SecondsField`` type for Django
model which stores ``datetime.timedelta`` object as a number of seconds in a
database's ``INTEGER`` type.


Installation
------------

Install with ``pip`` or ``pipenv``:

.. code:: python

  pip install django-seconds-field


Usage
-----

**models.py**

.. code:: python

  from django.db import models
  from django_seconds_field import SecondsField

  class FooBar(models.Model):
      ttl = SecondsField()


Documentation
-------------

See http://django-seconds-field.readthedocs.org/


License
-------

Copyright © 2019, Piotr Roszatycki

This software is distributed under the GNU Lesser General Public License (LGPL
3 or greater).
