# -*- coding: utf-8 -*-
from rome import Validator, ValidationError

class SUTValidator(Validator):

    def validate(self, value):
        if value == 'error':
            raise ValidationError('Test Error')
        return value
