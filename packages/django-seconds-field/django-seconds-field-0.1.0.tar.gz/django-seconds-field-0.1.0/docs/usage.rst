Usage
=====

**models.py**

.. code:: python

  from django.db import models
  from django_seconds_field import SecondsField

  class FooBar(models.Model):
      ttl = SecondsField()
