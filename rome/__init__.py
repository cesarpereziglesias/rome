# -*- coding: utf-8 -*-
"""
"""

class ValidationError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.error = msg


class Validator(object):

    def validate(self, value):
        raise Exception("Not Implemented")


class MetaSchema(type):

    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        cls._fields = {}
        for attr, attr_v in attrs.iteritems():
            if isinstance(attr_v, Validator):
                cls._fields[attr] = attr_v
        return cls


class Schema(Validator):

    __metaclass__ = MetaSchema

    def validate(self, value):
        pass
