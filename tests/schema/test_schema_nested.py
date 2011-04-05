#-*- coding: utf-8 -*-
from rome import Field, Schema, Validator

from tests import _TestValidator
from tests.schema import SUTValidator

class SUTSchemaNode(Schema):

    field = Field(SUTValidator(), mandatory=True)


class SUTSchemaRoot(Schema):

    node = Field(SUTSchemaNode(), mandatory=True)


class TestSimpleSchema(_TestValidator):

    VALIDATOR = SUTSchemaRoot()

    def test_valid(self):
        self.data = {'node': {'field': 'foo'}}
        self.data_ok()

    def test_root_invalid(self):
        self.data = {}
        self.data_error({'node': 'Missing value'})

    def test_node_invalid(self):
        self.data = {'node': {}}
        self.data_error({'node': {'field': 'Missing value'}})

