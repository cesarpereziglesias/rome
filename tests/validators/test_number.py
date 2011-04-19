# -*- coding: utf-8 -*-
from nose.tools import assert_equals

from rome.validators import Number
from rome.language import _

from tests import _TestValidator

class TestNumber(_TestValidator):

    VALIDATOR = Number()

    def test_valid_int(self):
        self.data = 8
        self.data_ok()

    def test_valid_float(self):
        self.data = 8.5
        self.data_ok()

    def test_valid_string_int(self):
        assert_equals(1, Number().validate("1"))

    def test_valid_string_float(self):
        assert_equals(1.6, Number().validate("1.6"))

    def test_invalid_number(self):
        self.data = 'foo'
        self.data_error(_("This is not a number"))
