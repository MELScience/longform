# coding: utf-8
"""
===============
longform.fields
===============

"""

from django.db import models

from .helpers import process_text


class LongformField(models.TextField):
    def __init__(self, *args, **kwargs):
        raw_field_name = kwargs.pop('raw_field', None)
        if not raw_field_name:
            raise TypeError("{} requires a 'raw_field' argument"
                            .format(self.__class__.__name__))
        sanitize = kwargs.pop('sanitize', True)
        strip_outer_p = kwargs.pop('strip_outer_p', False)

        # self.raw_field_name = raw_field.field_name

        self.raw_field_name = raw_field_name
        self.sanitize = sanitize
        self.strip_outer_p = strip_outer_p

        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        raw = getattr(model_instance, self.raw_field_name)

        formatted = process_text(raw,
                                 sanitize=self.sanitize,
                                 strip_outer_p=self.strip_outer_p)
        setattr(model_instance, self.attname, formatted)

        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        kwargs['raw_field'] = self.raw_field_name
        kwargs['sanitize'] = self.sanitize
        kwargs['strip_outer_p'] = self.strip_outer_p

        return name, path, args, kwargs
