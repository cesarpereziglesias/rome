# -*- coding: utf-8 -*-
"""
"""
from copy import copy
from itertools import chain

class ValidationError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.error = msg


class Validator(object):

    def __init__(self, *args, **kwargs):
        self.__dependencies__ = kwargs.get('dependencies', [])

    def validate(self, value, **kwargs):
        raise NotImplementedError()


class Field(Validator):

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)

        self.mandatory = kwargs.get('mandatory', False)
        self.validators = [validator for validator in args if isinstance(validator, Validator)]

        self.__compose_dependencies()

    def __compose_dependencies(self):
        [self.__dependencies__.append(dep) for dep in \
            chain.from_iterable([validator.__dependencies__ for validator in self.validators]) \
            if dep not in self.__dependencies__]

    def validate(self, value, dependencies={}):
        result = value
        for validator in self.validators:
            self.__add_dependencies(validator, dependencies)
            result = validator.validate(value)
        return result

    def __add_dependencies(self, validator, dependencies):
        for dep in validator.__dependencies__:
            dep in dependencies and setattr(validator, dep, dependencies[dep])


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
                    deps = dict([(dep, value[dep]) for dep in field_v.__dependencies__])
                    result[field] = field_v.validate(value[field], dependencies=deps)
                elif self.__is_mandatory(field_v, value):
                    raise ValidationError('Missing value')
            except ValidationError as ve:
                errors[field] = ve.error

        if errors:
            raise ValidationError(errors)

        return result

    def __is_mandatory(self, field, values):
        if callable(field.mandatory):
            return field.mandatory(self, values)
        else:
            return field.mandatory
