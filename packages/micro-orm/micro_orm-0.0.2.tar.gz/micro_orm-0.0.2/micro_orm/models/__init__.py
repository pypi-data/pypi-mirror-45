# -*- coding: utf-8 -*-

import re

from micro_orm.query import QueryManager
from micro_orm.fields import AbstractField


class AbstractModel(object):
    query_manager_class = QueryManager
    __fields__ = dict()

    def __init__(self, **kwargs):
        if not hasattr(self, '__table__'):
            class_name = self.__class__.__name__
            matches = re.findall(r'[A-Z][^A-Z]*', class_name)
            self.__table__ = "_".join([match.lower() for match in matches])

        self.query_manager = self.query_manager_class(self.__table__, self.__class__)
        self.objects = self.query_manager.objects
        fields = tuple([name for name in dir(self) if isinstance(getattr(self, name), AbstractField)])
        self.__fields__ = {field_name: getattr(self, field_name) for field_name in fields}
        [setattr(self, key, kwargs.get(key)) for key in fields]

    def get_table(self):
        return self.__table__

    def __validate_data__(self):
        for field_name in self.__fields__.keys():
            field = getattr(self, field_name)

            if not isinstance(field, AbstractField):
                self.__fields__.get(field_name).validate(field)

    def __getattr__(self, item):
        value = super(AbstractModel, self).__getattribute__(item)

        if item not in ('__fields__', '__table__') and \
                not isinstance(value, AbstractField) and item in self.__fields__.keys():
            value = self.__fields__[item].output_format(value)

        return value

    def to_dict(self):
        fields = tuple([name for name in dir(self) if name in self.__fields__.keys()])
        return {field_name: getattr(self, field_name) for field_name in fields}

    def to_dict_with_table_names(self):
        fields = tuple([name for name in dir(self) if name is self.__fields__.keys()])
        right_fields = tuple([
            self.__fields__[field_name].dialect_name
            if self.__fields__[field_name].dialect_name is not None
            else field_name for field_name in fields
        ])
        return {right_fields[i]: getattr(self, fields[i]) for i in range(0, len(fields))}

    def save(self):
        new_instance = self.objects.save(self)

        for field in new_instance.__fields__.keys():
            setattr(self, field, getattr(new_instance, field))

    def drop(self, force=False):
        drop_status = self.objects.drop(self, force)

        if drop_status is True:
            del self

        else:
            for field in drop_status.__fields__.keys():
                setattr(self, field, getattr(drop_status, field))
