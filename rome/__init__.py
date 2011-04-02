# -*- coding: utf-8 -*-
"""
"""

class Validator(object):

    def validate(self, value):
        raise Exception("Not Implemented")


class MetaSchema(type):

    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        cls.fields = {}
        for attr, attr_v in attrs.iteritems():
            if isinstance(attr_v, Validator):
                cls.fields[attr] = attr_v
        return cls


class Schema(Validator):

    __metaclass__ = MetaSchema

    def validate(self, value):
        pass
