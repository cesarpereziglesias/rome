#-*- coding: utf-8 -*-
from rome import Field, Schema, Validator

from tests import _TestValidator
from tests.schema import SUTValidator

class SUTSchemaNode(Schema):

    def guide_condition(self, value):
        return self.guide == 'mandatory_condition'

    field = Field(SUTValidator(), mandatory=True)
    field_guide = Field(SUTValidator(), mandatory=guide_condition)


class SUTSchemaRoot(Schema):

    guide = Field(SUTValidator(), mandatory=True)
    node = Field(SUTSchemaNode(dependencies=('guide',)), mandatory=True)


class TestNestedSchema(_TestValidator):

    VALIDATOR = SUTSchemaRoot()

    def test_valid(self):
        self.data = {'guide': 'foo', 'node': {'field': 'foo'}}
        self.data_ok()

    def test_root_invalid(self):
        self.data = {'guide': 'foo'}
        self.data_error({'node': 'Missing value'})

    def test_node_invalid(self):
        self.data = {'guide': 'foo', 'node': {}}
        self.data_error({'node': {'field': 'Missing value'}})

    def test_mandatory_depends_root(self):
        self.data = {'guide': 'mandatory_condition', 'node': {'field': 'foo'}}
        self.data_error({'node': {'field_guide': 'Missing value'}})
