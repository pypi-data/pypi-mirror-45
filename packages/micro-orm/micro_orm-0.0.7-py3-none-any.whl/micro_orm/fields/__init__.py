# -*- coding: utf-8 -*-

from datetime import datetime
import json

from .exceptions import *


class AbstractField(object):
    def __init__(self, dialect_name=None, nullable=False, primary_key=False):
        self.dialect_name = dialect_name
        self.nullable = nullable
        self.primary_key = primary_key

    def validate(self, value):
        if value is None and self.nullable is False:
            raise NotNullFieldError()

    def format(self, value):
        if self.nullable and value is None:
            return "NULL"

        return str(value)

    def output_format(self, value):
        return value

    def format_from_db(self, value):
        return value


class BigIntField(AbstractField):
    def format_from_db(self, value):
        return int(value) if value is not None else None


class VarcharField(AbstractField):
    def __init__(self, max_length=255, dialect_name=None, nullable=False):
        super(VarcharField, self).__init__(dialect_name, nullable)
        self.max_length = max_length

    def validate(self, value):
        super(VarcharField, self).validate(value)

        if value is not None and len(value) > self.max_length:
            raise TooLargeContent()

    def format(self, value):
        value = super(VarcharField, self).format(value)

        if value != 'NULL':
            value = "'{}'".format(value)

        return value


class DateTimeField(AbstractField):
    def __init__(self, dialect_name=None, nullable=False, auto_now=False, auto_now_add=False, soft_delete_field=False):
        super(DateTimeField, self).__init__(dialect_name, nullable)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        self.soft_delete_field = soft_delete_field

    def validate(self, value):
        if not self.auto_now and not self.auto_now_add:
            super(DateTimeField, self).validate(value)

        if (not self.auto_now_add and not self.auto_now and value is not None) and not isinstance(value, datetime):
            raise NoDateTimeGiven()

    def format(self, value):
        if self.nullable and value is None:
            value = "NULL"

        if value != 'NULL' and isinstance(value, datetime):
            value = "'{}'".format(value.strftime('%Y-%m-%d %H:%M:%S'))

        return value

    def output_format(self, value):
        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S') if value is not None else None

    def format_from_db(self, value):
        return self.output_format(value)


class IntField(AbstractField):
    def output_format(self, value):
        return int(value) if value is not None else None


class TextField(AbstractField):
    def format(self, value):
        value = super(TextField, self).format(value)

        if value != 'NULL':
            value = "'{}'".format(value)

        return value


class BooleanField(AbstractField):
    def validate(self, value):
        if value is None and self.nullable is False:
            raise NotNullFieldError()

        if value not in [True, 1, "1"] and value not in [False, 0, "0"]:
            raise NoBooleanGiven()

    def format(self, value):
        if self.nullable and value is None:
            value = "NULL"

        if value != 'NULL' and isinstance(value, bool):
            return "1" if value is True else "0"

        return value

    def output_format(self, value):
        return None if value in ['NULL', 'null', None] else value in ["1", 1]


class FloatField(AbstractField):
    def format(self, value):
        return super(FloatField, self).format(float(value))

    def output_format(self, value):
        return float(value) if value is not None else None

    def format_from_db(self, value):
        return self.output_format(value)


class ListField(AbstractField):
    def validate(self, value):
        super(ListField, self).validate(value)

        if not isinstance(value, (list, tuple,)):
            raise NoListOrTupleGiven()

    def format(self, value):
        if self.nullable and value is None:
            value = "NULL"

        if value != 'NULL' and isinstance(value, (list, tuple,)):
            return "'{}'".format(json.dumps(value))

        return value

    def output_format(self, value):
        return json.loads(value) if value is not None else None

    def format_from_db(self, value):
        return self.output_format(value)
