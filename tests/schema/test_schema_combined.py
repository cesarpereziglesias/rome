#-*- coding: utf-8 -*-
from rome import Schema, Field, FieldCombined

from tests import SUTValidator, SUTCombinedValidator, _TestValidator

class SUTSchema(Schema):

    field1 = Field(SUTValidator())
    field2 = Field(SUTValidator())
    field1_field2 = FieldCombined(SUTCombinedValidator('field1', 'field2'))

    field3 = Field(SUTValidator())
    field4 = Field(SUTValidator())
    field3_field4 = FieldCombined(SUTCombinedValidator('field3', 'field4'),
                                  destination='field3')

class TestSchemaCombinedFields(_TestValidator):

    VALIDATOR = SUTSchema()

    def test_valid(self):
        self.data = {'field1': 'foo', 'field2': 'baz', 'field3': 'foo', 'field4': 'baz'}
        self.data_ok()

    def test_invalid(self):
        self.data = {'field1': 'foo', 'field2': 'foo', 'field3': 'foo', 'field4': 'foo'}
        self.data_error({'field1_field2': 'Test Error',
                         'field3': 'Test Error'})

    def test_invalid_field_no_error_in_combined(self):
        self.data = {'field1': 'error', 'field2': 'error', 'field3': 'error', 'field4': 'error'}
        self.data_error({'field1': 'Test Error', 'field2': 'Test Error', 'field3': 'Test Error',
                         'field4': 'Test Error'})

