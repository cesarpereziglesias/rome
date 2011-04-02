# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import Validator, ValidationError

class SUTValidatorNotImplemented(Validator):
    pass

class SUTValidatorImplemented(Validator):

    def validate(self, value):
        return value

class TestValidator(object):

    @raises(NotImplementedError)
    def test_not_implemented(self):
        SUTValidatorNotImplemented().validate('foo')

    def test_implemented(self):
        SUTValidatorImplemented().validate('foo')

