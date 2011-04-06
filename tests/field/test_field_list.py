#-*- coding: utf-8 -*-
from rome import FieldList

from tests import _TestValidator, SUTValidator

class TestFieldList(_TestValidator):

    VALIDATOR = FieldList(SUTValidator())

    def test_valid(self):
        self.data = ['foo', 'bar', 'baz']
        self.data_ok()

    def test_simple_invalid(self):
        self.data = ['foo', 'error', 'baz']
        self.data_error([None, 'Test Error', None])

    def test_multiple_invalid(self):
        self.data = ['foo', 'error', 'error']
        self.data_error([None, 'Test Error', 'Test Error'])
