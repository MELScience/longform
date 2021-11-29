# coding: utf-8
"""
===================
testsapp.foo.models
===================

"""

from django.db import models


class LongformModel(models.Model):
    id = models.AutoField(primary_key=True)
    text_raw = models.TextField()
    text = models.TextField()

    class Meta:
        db_table = 'longform_longformmodel'


class LongformModelArgs(models.Model):
    id = models.AutoField(primary_key=True)
    text_raw = models.TextField()
    text = models.TextField()

    class Meta:
        db_table = 'longform_longformmodelargs'
