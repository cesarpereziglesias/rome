#-*- coding: utf-8 -*-
from rome import Schema, FieldConstant

from tests import _TestValidator

class SUTSchema(Schema):

    field = FieldConstant('foo')

class TestFieldConstant(_TestValidator):

    VALIDATOR = SUTSchema()

    def test_constant(self):
        self.data = {}
        self.data_ok(expected={'field': 'foo'})



