#-*- coding: utf-8 -*-
from rome.validators import In

from tests import _TestValidator

class TestIn(_TestValidator):

    VALUES = ['foo', 'bar']
    VALIDATOR = In(*VALUES)

    def test_valid(self):
        self.data = 'foo'
        self.data_ok()

    def test_invalid(self):
        self.data = 'baz'
        self.data_error('Value must be in list [%s]' % ', '.join(self.VALUES))
