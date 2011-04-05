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

    def __init__ (self, dependencies=(), **kwargs):
        self.__dependencies__ = dependencies

    def validate(self, value):
        errors = {}
        result = {}
        for field, field_v in self._fields.iteritems():
            try:
                if field in value:
                    self.__add_dependencies(field_v.validator, value)
                    result[field] = field_v.validator.validate(value[field])
                elif self.__is_mandatory(field_v, value):
                    raise ValidationError('Missing value')
            except ValidationError as ve:
                errors[field] = ve.error

        if errors:
            raise ValidationError(errors)

        return result

    def __is_mandatory(self, field, values):
        return (field.mandatory_if is not None and field.mandatory_if(self, values)) or field.mandatory

    def __add_dependencies(self, schema, value):
        if not isinstance(schema, Schema):
            return

        for dependencie in schema.__dependencies__:
            if dependencie in value:
                setattr(schema, dependencie, value[dependencie])
