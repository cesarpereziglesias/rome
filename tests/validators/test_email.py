#-*- coding: utf-8 -*-
from rome.validators import Email
from tests import _TestValidator

class TestEmail(_TestValidator):

    VALIDATOR = Email()

    def test_valid(self):
        self.data = 'foo@host.com'
        self.data_ok()

    def test_no_at(self):
        self.data = 'foo.com'
        self.data_error('This is not a valid email')

    def test_no_user(self):
        self.data = '@foo.com'
        self.data_error('This is not a valid email')

    def test_not_domain(self):
        self.data = 'foo@'
        self.data_error('This is not a valid email')

    def test_no_dot(self):
        self.data = 'foo@host'
        self.data_error('This is not a valid email')
