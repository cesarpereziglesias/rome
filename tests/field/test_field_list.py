#-*- coding: utf-8 -*-
from rome import FieldList
from rome.language import _

from tests import _TestValidator, SUTValidator

class TestFieldList(_TestValidator):

    VALIDATOR = FieldList(SUTValidator(), min=2, max=3)

    def test_valid(self):
        self.data = ['foo', 'bar', 'baz']
        self.data_ok()

    def test_simple_invalid(self):
        self.data = ['foo', 'error', 'baz']
        self.data_error([None, 'Test Error', None])

    def test_multiple_invalid(self):
        self.data = ['foo', 'error', 'error']
        self.data_error([None, 'Test Error', 'Test Error'])

    def test_max_error(self):
        self.data = ['foo', 'bar', 'baz', 'foo2']
        self.data_error(_('%(max)i items maximum permitted') % {'max': 3})

    def test_min_error(self):
        self.data = ['foo']
        self.data_error(_('%(min)i items minimum permitted') % {'min': 2})

