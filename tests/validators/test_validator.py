# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import Validator, CombinedValidator, ValidationError

from tests import SUTValidator

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


class SUTCombinedValidator(CombinedValidator):

    __combined_fields__ = ('foo', 'bar')

    def validate(self, value):
        return value[self.foo], value[self.bar]

class TestCombinedValidator(object):

    @raises(TypeError)
    def test_bad_contruction(self):
        SUTCombinedValidator()

    def test_valid(self):
        validator = SUTCombinedValidator('field1', 'field2')
        value = {'field1': 'value1', 'field2': 'value2'}
        assert_equals((value['field1'], value['field2']),
                      validator.validate(value))

class TestValidatorErrors(object):

    def test_default_errors(self):
        validator = SUTValidator()
        assert_equals({'test_error': 'Test Error'}, validator.get_list_errors())

    def test_custom_errors(self):
        ERROR_TEXT = 'Test Custom Error'
        validator = SUTValidator(errors={'test_error': ERROR_TEXT})
        assert_equals({'test_error': ERROR_TEXT}, validator.get_list_errors())

    def test_custom_inexistent_error(self):
        validator = SUTValidator(errors={'foo_error': 'Foo Error'})
        assert_equals({'test_error': 'Test Error'}, validator.get_list_errors())
