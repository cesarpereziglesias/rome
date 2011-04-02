# -*- coding: utf-8 -*-
from nose.tools import assert_equals

from rome import Schema, Validator

class SUTValidator(Validator):
        pass


class SUTSchema(Schema):

    field = SUTValidator()


class TestSchema(object):

    def test_fields(self):
        schema = SUTSchema()
        assert_equals(1, len(schema._fields))
