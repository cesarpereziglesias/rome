# -*- coding: utf-8 -*-
from nose.tools import assert_equals

from rome.validators import String

from tests import _TestValidator

class TestString(_TestValidator):

    def test_valid(self):
        self.VALIDATOR = String()
        self.data = 'foo'
        self.data_ok()

    def test_between(self):
        self.VALIDATOR = String(max=5, min=2, empty=False)
        self.data = 'fooo'
        self.data_ok()

    def test_none(self):
        self.VALIDATOR = String()
        self.data = None
        self.data_error('This is not a String')


    def test_empty(self):
        self.VALIDATOR = String(empty=False)
        self.data = ''
        self.data_error('Please enter a value')

    def test_not_string(self):
        self.VALIDATOR = String()
        self.data = 9
        self.data_error('This is not a String')

    def test_wrong_interval(self):
        try:
            String(max=4, min=6).validate('foo')
        except ValueError as e:
            assert_equals('Max value must be greater than min', e.args[0])

    def test_exact(self):
        self.VALIDATOR = String(max=4, min=4)
        self.data = 'foo'
        self.data_error('Value length must be %(num)i exactly' % {'num': 4})

    def test_wrong_max(self):
        self.VALIDATOR = String(max=2)
        self.data = 'foo'
        self.data_error('Value length must be %(num)i or less' % {'num': 2})

    def test_wrong_min(self):
        self.VALIDATOR = String(min=4)
        self.data = 'foo'
        self.data_error('Value length must be %(num)i or more' % {'num': 4})
