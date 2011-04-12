#-*- coding: utf-8 -*-
from rome import Schema, Field

from tests import SUTValidator, _TestValidator

class SUTSchema(Schema):

    field = Field(SUTValidator(), default='foo')

class TestFieldDefaults(_TestValidator):

    VALIDATOR = SUTSchema()

    def test_given_value(self):
        value = 'bar'
        self.data = {'field': 'bar'}
        self.data_ok()

    def test_no_given_value(self):
        self.data = {}
        self.data_ok(expected={'field': 'foo'})

class SUTSchemaConstant(Schema):

    field = Field(default='foo')

class TestFieldConstant(_TestValidator):

    VALIDATOR = SUTSchemaConstant()

    def test_constant(self):
        self.data = {}
        self.data_ok(expected={'field': 'foo'})
