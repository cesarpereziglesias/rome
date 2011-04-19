#-*- coding: utf-8 -*-
from rome.validators import In
from rome.language import _

from tests import _TestValidator

class TestIn(_TestValidator):

    VALUES = ['foo', 'bar']
    VALIDATOR = In(*VALUES)

    def test_valid(self):
        self.data = 'foo'
        self.data_ok()

    def test_invalid(self):
        self.data = 'baz'
        self.data_error(_('Value must be in list [%(values)s]') %
                            {'values': ', '.join(self.VALUES)})
