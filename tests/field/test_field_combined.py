#-*- coding: utf-8 -*-
from nose.tools import assert_equals, raises

from rome import FieldCombined, CombinedValidator
from tests import _TestValidator, SUTValidator, SUTCombinedValidator

class TestFieldCombined(_TestValidator):

    @raises(TypeError)
    def test_multiple_validators(self):
        try:
            FieldCombined(SUTCombinedValidator('field1', 'field2'),
                          SUTCombinedValidator('field1', 'field2'))
        except TypeError as te:
            assert_equals("FieldCombined accepts only one validator", te.args[0])
            raise

    @raises(TypeError)
    def test_not_combined_validator(self):
        try:
            FieldCombined(SUTValidator())
        except TypeError as te:
            assert_equals("FieldCombined accepts only CombinedValidator validators", te.args[0])
            raise
