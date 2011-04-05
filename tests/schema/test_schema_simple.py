# -*- coding: utf-8 -*-
from nose.tools import assert_equals

from rome import Field, Schema, Validator, ValidationError

from tests import _TestValidator
from tests.schema import SUTValidator

class SUTSchema(Schema):

    def field1_is_A(self, values):
        return values.get('field1', None) == 'A'

    field1 = Field(SUTValidator(), mandatory=True)
    field2 = Field(SUTValidator(), mandatory=True)
    field3 = Field(SUTValidator())
    field4 = Field(SUTValidator(), mandatory_if=field1_is_A)


class TestSimpleSchema(_TestValidator):

    VALIDATOR = SUTSchema()

    def test_fields(self):
        assert_equals(4, len(self.VALIDATOR._fields))

    def test_valid(self):
        self.data = {'field1': 'foo', 'field2': 'bar'}
        self.data_ok()

    def test_invalid_one_error(self):
        self.data = {'field1': 'foo', 'field2': 'error'}
        self.data_error({'field2': 'Test Error'})

    def test_invalid_multiple_error(self):
        self.data = {'field1': 'error', 'field2': 'error'}
        self.data_error({'field1': 'Test Error',
                         'field2': 'Test Error'})

    def test_validate_not_mandatory_field(self):
        self.data = {'field1': 'foo', 'field2': 'bar', 'field3': 'baz'}
        assert_equals(self.data, self.VALIDATOR.validate(self.data))
        self.data['field3'] = 'error'
        self.data_error({'field3': 'Test Error'})

    def test_missing_one_value(self):
        self.data = {'field1': 'foo'}
        self.data_error({'field2': 'Missing value'})

    def test_missing_multiple_value(self):
        self.data = {'field3': 'foo'}
        self.data_error({'field1': 'Missing value',
                         'field2': 'Missing value'})

    def test_missing_field_mandatory_optional(self):
        self.data = {'field1': 'A', 'field2': 'foo'}
        self.data_error({'field4': 'Missing value'})

