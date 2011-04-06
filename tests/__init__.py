# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import Validator, ValidationError

class SUTValidator(Validator):

    STR_ERROR = 'error'
    MSG_ERROR = 'Test Error'

    def validate(self, value):
        if value == self.STR_ERROR:
            raise ValidationError(self.MSG_ERROR)
        return value


class _TestValidator(object):

    VALIDATOR = None

    def data_ok(self):
        assert_equals(self.data, self.VALIDATOR.validate(self.data))

    @raises(ValidationError)
    def data_error(self, error):
        try:
            self.VALIDATOR.validate(self.data)
        except ValidationError as ve:
            assert_equals(error, ve.error)
            raise
