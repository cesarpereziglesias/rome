# -*- coding: utf-8 -*-
from rome import Validator, ValidationError

class String(Validator):

    def validate(self, value):
        pass

class Number(Validator):

    def validate(self, value):
        try:
            f_result = float(value)
            try:
                i_result = int(value)
                return i_result if i_result == f_result else f_result
            except ValueError:
                pass
            return f_result
        except ValueError:
            raise ValidationError("This is not a number")
