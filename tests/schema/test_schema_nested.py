#-*- coding: utf-8 -*-
from rome import Field, Schema, Validator
from rome.language import _

from tests import _TestValidator, SUTValidator

class SUTSchemaNode(Schema):

    def guide_condition(self, value):
        return self.guide == 'mandatory_condition'

    field = Field(SUTValidator())
    field_guide = Field(SUTValidator(), mandatory=guide_condition)


class SUTSchemaRoot(Schema):

    guide = Field(SUTValidator())
    node = Field(SUTSchemaNode(dependencies=('guide',)))


class TestNestedSchema(_TestValidator):

    VALIDATOR = SUTSchemaRoot()

    def test_valid(self):
        self.data = {'guide': 'foo', 'node': {'field': 'foo'}}
        self.data_ok()

    def test_root_invalid(self):
        self.data = {'guide': 'foo'}
        self.data_error({'node': _('Missing value')})

    def test_node_invalid(self):
        self.data = {'guide': 'foo', 'node': {}}
        self.data_error({'node': {'field': _('Missing value')}})

    def test_mandatory_depends_root(self):
        self.data = {'guide': 'mandatory_condition', 'node': {'field': 'foo'}}
        self.data_error({'node': {'field_guide': _('Missing value')}})


from rome import FieldList
from rome.validators import String

class Child(Schema):

    def exists_in_document(self, values):
        return isinstance(self.parent, basestring)

    def not_exists_in_document(self, values):
        return not(self.exists_in_document(values))

    identifier = Field(String(empty=False))

    parent = Field(String(empty=False),
        mandatory=not_exists_in_document,
        forbidden=exists_in_document
    )

class Document(Schema):
    parent = Field(String(empty=False), mandatory=False)
    children = FieldList(Child(dependencies=('parent',)))

class TestNestedSchemaWithOptionalFields(_TestValidator):
    VALIDATOR = Document()

    def test_schemas_should_be_reread(self):
        self.data = {
            'parent': 'foo',
            'children': [
                {'identifier': 'bar'},
                {'identifier': 'baz'}
            ]
        }

        self.data_ok()

        self.data = {
            'children': [
                {'identifier': 'bar', 'parent': 'bar'},
                {'identifier': 'baz', 'parent': 'baz'}
            ]
        }

        self.data_ok()
