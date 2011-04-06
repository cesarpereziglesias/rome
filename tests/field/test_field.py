#-*- coding: utf-8 -*-
from rome import Field

from tests import _TestValidator, SUTValidator

class SUTValidator1(SUTValidator):

    STR_ERROR = '1'
    MSG_ERROR = 'Test Error 1'


class SUTValidator2(SUTValidator):

    STR_ERROR = '2'
    MSG_ERROR = 'Test Error 2'


class TestField(_TestValidator):

    SIMPLE_VALIDATOR = Field(SUTValidator1())
    MULTIPLE_VALIDATOR = Field(SUTValidator1(), SUTValidator2())

    def test_simple_validator_valid(self):
        self.VALIDATOR = self.SIMPLE_VALIDATOR
        self.data = '3'
        self.data_ok()

    def test_simple_validator_error(self):
        self.VALIDATOR = self.SIMPLE_VALIDATOR
        self.data = '1'
        self.data_error("Test Error 1")

    def test_multiple_validator_valid(self):
        self.VALIDATOR = self.MULTIPLE_VALIDATOR
        self.data = '3'
        self.data_ok()

    def test_multiple_validator_error_in_first(self):
        self.VALIDATOR = self.MULTIPLE_VALIDATOR
        self.data = '1'
        self.data_error("Test Error 1")

    def test_multiple_validator_error_in_second(self):
        self.VALIDATOR = self.MULTIPLE_VALIDATOR
        self.data = '2'
        self.data_error("Test Error 2")
