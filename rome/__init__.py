# -*- coding: utf-8 -*-
"""
"""
from copy import copy

class ValidationError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.error = msg


class Validator(object):

    def validate(self, value):
        raise NotImplementedError()


class Field(object):

    def __init__(self, validator, *args, **kwargs):
        if 'mandatory' in kwargs and 'mandatory_if' in kwargs:
            raise Exception("mandatory and mandatory_if can't be setted at the same time")

        self.mandatory = kwargs.get('mandatory', False)
        self.mandatory_if = kwargs.get('mandatory_if', None)

        self.validator = validator


class MetaSchema(type):

    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        cls._fields = copy(getattr(cls, '_fields', {}))

        for attr, attr_v in attrs.iteritems():
            if isinstance(attr_v, Field):
                cls._fields[attr] = attr_v
        return cls


class Schema(Validator):

    __metaclass__ = MetaSchema

    def validate(self, value):
        errors = {}
        result = {}
        for field, field_v in self._fields.iteritems():
            try:
                if field in value:
                    result[field] = field_v.validator.validate(value[field])
                elif (field_v.mandatory_if is not None and field_v.mandatory_if(self, value)) \
                        or field_v.mandatory:
                    raise ValidationError('Missing value')
            except ValidationError as ve:
                errors[field] = ve.error

        if errors:
            raise ValidationError(errors)

        return result
