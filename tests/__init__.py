# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import ValidationError

class _TestValidator(object):

    VALIDATOR = None

    @raises(ValidationError)
    def data_error(self, error):
        try:
            self.VALIDATOR.validate(self.data)
        except ValidationError as ve:
            assert_equals(error, ve.error)
            raise
