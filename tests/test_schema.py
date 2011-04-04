# -*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import Field, Schema, Validator, ValidationError

class SUTValidator(Validator):

    def validate(self, value):
        if value == 'error':
            raise ValidationError('Test Error')
        return value


class SUTSchema(Schema):

    field1 = Field(SUTValidator(), mandatory=True)
    field2 = Field(SUTValidator(), mandatory=True)
    field3 = Field(SUTValidator())


class TestSchema(object):

    def setup(self):
        self.schema = SUTSchema()

    def test_fields(self):
        assert_equals(3, len(self.schema._fields))

    def test_valid(self):
        value = {'field1': 'foo', 'field2': 'bar'}
        assert_equals(value, self.schema.validate(value))

    def test_invalid_one_error(self):
        value = {'field1': 'foo', 'field2': 'error'}
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field2': 'Test Error'}, ve.error)

    @raises(ValidationError)
    def test_invalid_multiple_error(self):
        value = {'field1': 'error', 'field2': 'error'}
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field1': 'Test Error',
                           'field2': 'Test Error'},
                          ve.error)
            raise

    @raises(ValidationError)
    def test_validate_not_mandatory_field(self):
        value = {'field1': 'foo', 'field2': 'bar', 'field3': 'baz'}
        assert_equals(value, self.schema.validate(value))
        value['field3'] = 'error'
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field3': 'Test Error'},
                          ve.error)
            raise

    @raises(ValidationError)
    def test_missing_one_value(self):
        value = {'field1': 'foo'}
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field2': 'Missing value'},
                          ve.error)
            raise

    @raises(ValidationError)
    def test_missing_multiple_value(self):
        value = {'field3': 'foo'}
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field1': 'Missing value',
                           'field2': 'Missing value'},
                          ve.error)
            raise
