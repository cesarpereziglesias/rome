# -*- coding: utf-8 -*-
from rome import Validator, ValidationError

class String(Validator):

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)
        self.max = kwargs.get('max', None)
        self.min = kwargs.get('min', None)
        self.empty = kwargs.get('empty', True)

        if self.max is not None and self.min is not None and self.min > self.max:
            raise ValueError("Max value must be greater than min")

    def validate(self, value):
        if not isinstance(value, basestring):
            raise  ValidationError("This is not a String")

        self.attr_validate(value)

        return value

    def attr_validate(self, value):
        if not self.empty and value == '':
            raise ValidationError('Please enter a value')

        if self.max is not None:
            if self.min == self.max and self.max != len(value):
                raise ValidationError("Value length must be %i exactly" % self.max)
            if len(value) > self.max:
                raise ValidationError("Value length must be %i or less" % self.max)

        if self.min is not None:
            if len(value) < self.min:
                raise ValidationError("Value length must be %i or more" % self.min)


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


class In(Validator):

    def __init__(self, values, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)
        self._values = values

    def validate(self, value):
        if value not in self._values:
            raise ValidationError('Value must be in list [%s]' % ', '.join(self._values))
        return value
