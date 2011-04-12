# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import Validator, CombinedValidator, ValidationError

class SUTValidator(Validator):

    STR_ERROR = 'error'
    MSG_ERROR = 'Test Error'

    def validate(self, value):
        if value == self.STR_ERROR:
            raise ValidationError(self.MSG_ERROR)
        return value

class SUTCombinedValidator(CombinedValidator):

    __combined_fields__ = ('field1', 'field2')

    def validate(self, value):
        if value[self.field1] == value[self.field2]:
            raise ValidationError("Test Error")


class _TestValidator(object):

    VALIDATOR = None

    def data_ok(self, **kwargs):
        expected = self.data if 'expected' not in kwargs else kwargs['expected']
        assert_equals(expected, self.VALIDATOR.validate(self.data))

    @raises(ValidationError)
    def data_error(self, error):
        try:
            self.VALIDATOR.validate(self.data)
        except ValidationError as ve:
            assert_equals(error, ve.error)
            raise
