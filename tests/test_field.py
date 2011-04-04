#-*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import Field, Schema

class TestField(object):

    @raises(Exception)
    def test_error_definition(self):
        try:
            class SUTSchema(Schema):
                field = Field(None, mandatory=True, mandatory_if=lambda x: x)
        except Exception as e:
            assert_equals("mandatory and mandatory_if can't be setted at the same time", e.args[0])
            raise

    def test_no_error_definition(self):
        class SUTSchema(Schema):
            field1 = Field(None, mandatory=True)
            field2 = Field(None, mandatory_if=lambda x: x)
