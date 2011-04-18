# -*- coding: utf-8 -*-
"""
"""
from copy import copy
from itertools import chain

class ValidationError(Exception):

    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.error = msg


class Validator(object):

    def __init__(self, *args, **kwargs):
        self.__dependencies__ = kwargs.get('dependencies', [])

    def validate(self, value, **kwargs):
        raise NotImplementedError()


class CombinedValidator(Validator):

    __combined_fields__ = ()

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, dependencies=args, **kwargs)

        if len(self.__combined_fields__) != len(args):
            raise TypeError('__init__() takes exactly %(expected)d arguments (%(given)d given)' %
                            {'expected': len(self.__combined_fields__), 'given': len(args)})

        for combined_field, field in zip(self.__combined_fields__, args):
            setattr(self, combined_field, field)


class Field(Validator):

    def __init__(self, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)

        self.mandatory = kwargs.get('mandatory', True)
        self.forbidden = kwargs.get('forbidden', None)
        self.validators = [validator for validator in args if isinstance(validator, Validator)]
        if 'default' in kwargs:
            self.default = kwargs['default']

        self._compose_dependencies()

    def _compose_dependencies(self):
        [self.__dependencies__.append(dep) for dep in \
            chain.from_iterable([validator.__dependencies__ for validator in self.validators]) \
            if dep not in self.__dependencies__]

    def validate(self, value, dependencies={}):
        result = value
        for validator in self.validators:
            self._add_dependencies(validator, dependencies)
            result = validator.validate(value)
        return result

    def _add_dependencies(self, validator, dependencies):
        for dep in validator.__dependencies__:
            dep in dependencies and setattr(validator, dep, dependencies[dep])


class FieldConstant(Field):

    def __init__(self, value, *args, **kwargs):
        Validator.__init__(self, *args, **kwargs)
        self.value = value


class FieldCombined(Field):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("FieldCombined accepts only one validator")

        Field.__init__(self, *args, **kwargs)
        self.destination = kwargs.get('destination', None)

        if not isinstance(self.validators[0], CombinedValidator):
            raise TypeError("FieldCombined accepts only CombinedValidator validators")

    def _add_dependencies(self, validator, dependencies):
        pass


class FieldList(Field):

    def __init__(self, *args, **kwargs):
        Field.__init__(self, *args, **kwargs)
        self.max = kwargs.get('max', None)
        self.min = kwargs.get('min', None)

    def validate(self, value, dependencies={}):
        errors = []
        result = []

        self._check_length(value)

        for item in value if isinstance(value, (list, tuple)) else [value]:
            try:
                result.append(Field.validate(self, item, dependencies=dependencies))
                errors.append(None)
            except ValidationError as ve:
                errors.append(ve.error)
        if any(errors):
            raise ValidationError(errors)

        return result

    def _check_length(self, values):
        if self.max is not None and len(values) > self.max:
            raise ValidationError("%d items maximum permitted" % self.max)
        if self.min is not None and len(values) < self.min:
            raise ValidationError("%d items minimum permitted" % self.min)


class MetaSchema(type):

    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        cls._constant_fields = copy(getattr(cls, '_constant_fields', {}))
        cls._fields = copy(getattr(cls, '_fields', {}))
        cls._combined_fields = copy(getattr(cls, '_combined_fields', {}))

        for attr, field in attrs.iteritems():
            if isinstance(field, FieldConstant):
                cls._constant_fields[attr] = field
            elif isinstance(field, FieldCombined):
                cls._combined_fields[attr] = field
            elif isinstance(field, Field):
                cls._fields[attr] = field
            elif attr in cls._fields and field is None:
                # Remove field
                del(cls._fields[attr])
        return cls


class Schema(Validator):

    __metaclass__ = MetaSchema

    def validate(self, value):
        errors = {}
        result = {}

        self.__constant_fields_validation(value, result)

        self.__regular_fields_validation(value, result, errors)

        self.__combined_fields_validation(value, result, errors)

        if errors:
            raise ValidationError(errors)

        return result

    def __constant_fields_validation(self, value, result):
        for field, validator in self._constant_fields.iteritems():
            result[field] = validator.value

    def __regular_fields_validation(self, value, result, errors):
        for field, validator in self._fields.iteritems():
            try:
                if field in value or hasattr(validator, 'default'):
                    self.__is_forbidden(validator, value)
                    test_value = value[field] if field in value else validator.default
                    deps = self.__lookup_dependencies(validator.__dependencies__, value, result)
                    result[field] = validator.validate(test_value, dependencies=deps)
                elif self.__is_mandatory(validator, value):
                    raise ValidationError('Missing value')
            except ValidationError as ve:
                errors[field] = ve.error

    def __combined_fields_validation(self, value, result, errors):
        for field, validator in self._combined_fields.iteritems():
            try:
                if set(validator.__dependencies__).isdisjoint(errors.keys()):
                    deps = self.__lookup_dependencies(validator.__dependencies__, value, result)
                    validator.validate(value, dependencies=deps)
            except ValidationError as ve:
                errors[field if validator.destination is None else validator.destination] = ve.error

    def __is_forbidden(self, field, values):
        if hasattr(field, 'forbidden') and callable(field.forbidden) and field.forbidden(self, values):
            raise ValidationError("Forbidden by conditions")

    def __is_mandatory(self, field, values):
        if callable(field.mandatory):
            return field.mandatory(self, values)
        else:
            return field.mandatory

    def __lookup_dependencies(self, dependencies, values, result):
        return dict([(dep, values[dep] if dep in values else result[dep]) for dep in dependencies \
                if dep in values or dep in result])
