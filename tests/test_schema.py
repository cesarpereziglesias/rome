# -*- coding: utf-8 -*-
from nose.tools import assert_equals

from rome import Schema, Validator, ValidationError

class SUTValidator(Validator):

    def validate(self, value):
        if value == 'error':
            raise ValidationError('Test Error')
        return value


class SUTSchema(Schema):

    field1 = SUTValidator()
    field2 = SUTValidator()


class TestSchema(object):

    def setup(self):
        self.schema = SUTSchema()

    def test_fields(self):
        assert_equals(2, len(self.schema._fields))

    def test_valid(self):
        value = {'field1': 'foo', 'field2': 'bar'}
        assert_equals(value, self.schema.validate(value))

    def test_invalid_one_error(self):
        value = {'field1': 'foo', 'field2': 'error'}
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field2': 'Test Error'}, ve.error)

    def test_invalid_multiple_error(self):
        value = {'field1': 'error', 'field2': 'error'}
        try:
            self.schema.validate(value)
        except ValidationError as ve:
            assert_equals({'field1': 'Test Error',
                           'field2': 'Test Error'},
                          ve.error)
