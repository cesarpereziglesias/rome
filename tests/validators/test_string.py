# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import ValidationError
from rome.validators import Number

class TestNumber(object):

    def test_valid_int(self):
        value = 8
        assert_equals(value, Number().validate(value))

    def test_valid_float(self):
        value = 8.5
        assert_equals(value, Number().validate(value))

    def test_valid_string_int(self):
        assert_equals(1, Number().validate("1"))

    def test_valid_string_float(self):
        assert_equals(1.6, Number().validate("1.6"))
        
    @raises(ValidationError)
    def test_invalid_number(self):
        try:
            Number().validate('foo')
        except ValidationError as e:
            assert_equals("This is not a number", e.error)
            raise

