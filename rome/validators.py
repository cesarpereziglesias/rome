# -*- coding: utf-8 -*-
import re

from rome import Validator, ValidationError
from rome.language import _

class String(Validator):

    __errors__ = {'not_string': _("This is not a String"),
                  'empty': _('Please enter a value'),
                  'exact_length': _("Value length must be %(length)i exactly"),
                  'max_exceeded': _("Value length must be %(max)i or less"),
                  'min_not_reached': _("Value length must be %(min)i or more")}

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)
        self.max = kwargs.get('max', None)
        self.min = kwargs.get('min', None)
        self.empty = kwargs.get('empty', True)

        if self.max is not None and self.min is not None and self.min > self.max:
            raise ValueError("Max value must be greater than min")

    def validate(self, value):
        if not isinstance(value, basestring):
            self._validation_error('not_string')

        self.attr_validate(value)

        return value

    def attr_validate(self, value):
        if not self.empty and value == '':
            self._validation_error('empty')

        if self.max is not None:
            if self.min == self.max and self.max != len(value):
                self._validation_error('exact_length', length=self.max)
            if len(value) > self.max:
                self._validation_error('max_exceeded', max=self.max)

        if self.min is not None:
            if len(value) < self.min:
                self._validation_error('min_not_reached', min=self.min)


class Number(Validator):

    __errors__ = {'not_number': _('This is not a number')}

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
            self._validation_error('not_number')


class Int(Validator):

    __errors__ = {'not_int': _('This is not an integer')}

    def validate(self, value):
        if isinstance(value, int):
            return value
        self._validation_error('not_int')


class In(Validator):

    __errors__ = {'not_in': _('Value must be in list [%(values)s]')}

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)
        self._values = args

    def validate(self, value):
        if value not in self._values:
            self._validation_error('not_in', values=', '.join(self._values))
        return value


class Email(Validator):

    __errors__ = {'no_valid': _('This is not a valid email')}

    # RFC 2822
    REGEXP = '[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])'

    def validate(self, value):
        if not re.match(self.REGEXP, value):
            self._validation_error('no_valid')
        return value
