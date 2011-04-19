#-*- coding: utf-8 -*-
from rome.validators import Int
from rome.language import _

from tests import _TestValidator

class TestInt(_TestValidator):

    VALIDATOR = Int()

    def test_valid(self):
        self.data = 2
        self.data_ok()

    def test_invalid_float(self):
        self.data = 2.03
        self.data_error(_('This is not an integer'))

    def test_invalid_string(self):
        self.data = '2'
        self.data_error(_('This is not an integer'))

