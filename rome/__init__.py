# -*- coding: utf-8 -*-
"""
"""

class ValidationError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.error = msg


class Validator(object):

    def validate(self, value):
        raise NotImplementedError()


class MetaSchema(type):

    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        cls._fields = {}
        for attr, attr_v in attrs.iteritems():
            if isinstance(attr_v, Validator):
                MetaSchema.__set_validator(cls, attr, attr_v)
        return cls

    def __set_validator(cls, attr, attr_v):
        at, mandatory = (attr[1:], False) if attr.startswith("_") else (attr, True)
        cls._fields[at] = {'validator': attr_v, 'mandatory': mandatory}


class Schema(Validator):

    __metaclass__ = MetaSchema

    def validate(self, value):
        errors = {}
        result = {}
        for field, validator in self._fields.iteritems():
            try:
                if field in value:
                    result[field] = validator['validator'].validate(value[field])
                elif validator['mandatory']:
                    raise ValidationError('Missing value')
            except ValidationError as ve:
                errors[field] = ve.error

        if errors:
            raise ValidationError(errors)

        return result
