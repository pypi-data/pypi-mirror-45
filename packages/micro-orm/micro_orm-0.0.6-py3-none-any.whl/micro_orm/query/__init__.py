# -*- coding: utf-8 -*-

import pymysql

from datetime import datetime

from .exceptions import *


class QuerySet(object):
    def __init__(self, initial_query):
        self.__initial_query__ = initial_query
        self.__init_content__()

    def __init_content__(self):
        self.filters = list()
        self.order_by = None
        self.set_parameters = list()
        self.limit = None
        self.parameters = list()
        self.values = list()

    def query(self, get_as_all=False):
        from ..micro_orm import main

        if main is None:
            raise Exception()

        query = self.__initial_query__
        delete_word = "DELETE"
        update_word = "UPDATE"
        insert_word = "INSERT"
        select_word = "SELECT"
        special_words = (delete_word, update_word, insert_word, select_word,)

        right = False

        for special_word in special_words:
            right = special_word in query

            if right:
                break

        if not right:
            raise WrongQueryGiven()

        if insert_word in query and len(self.values) > 0:
            query = query.format(
                ", ".join(self.parameters),
                ", ".join(self.values)
            )

        if update_word in query and len(self.set_parameters) > 0:
            query += " {}".format(", ".join(self.set_parameters))

        if len(self.filters) > 0 and insert_word not in query:
            query += " {}".format("WHERE {}".format(" AND ".join(self.filters)))

        if select_word in query:
            if self.order_by is not None:
                query += " {}".format(self.order_by)

            if self.limit is not None:
                query += " {}".format(self.limit)

        db_name = main.db_name
        host = main.db_host
        name = main.db_user
        password = main.db_password
        charset = "utf8mb4"
        conn = pymysql.connect(host, user=name, passwd=password, db=db_name, connect_timeout=5, charset=charset)

        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            row_count = cur.execute(query)

            if select_word not in query:
                conn.commit()

            else:
                if row_count > 0:

                    if self.limit is None or get_as_all:
                        self.__init_content__()
                        return cur.fetchall()

                    else:
                        self.__init_content__()
                        return cur.fetchone()

                raise NoContentFound()

            if insert_word in query:
                row_count = cur.execute("SELECT LAST_INSERT_ID() as new_id")

                if row_count > 0:
                    self.__init_content__()
                    return cur.fetchone().get('new_id')

            self.__init_content__()
            return True


class QueryManager(object):
    class Objects:
        query_set = None

        def __init__(self, table, model_class):
            self.__table_name__ = table
            self.__model_class__ = model_class

        def __init_drop_query__(self):
            self.query_set = QuerySet("DELETE FROM {}".format(self.__table_name__))
            return self.query_set

        def __init_update_query__(self):
            self.query_set = QuerySet("UPDATE {} SET".format(self.__table_name__))
            return self.query_set

        def __init_insert_query__(self):
            self.query_set = QuerySet("INSERT INTO {} ({}) VALUES ({})".format(self.__table_name__, "{}", "{}"))
            return self.query_set

        def __init_query__(self):
            query = "SELECT {} FROM {}".format("{}", self.__table_name__)
            fields = list()

            for field_name in self.__model_class__().__fields__.keys():
                field_instance = self.__model_class__().__fields__[field_name]
                fields.append("{} AS {}".format(
                    field_instance.dialect_name if field_instance.dialect_name is not None else field_name,
                    field_name
                ))

            self.query_set = QuerySet(query.format(", ".join(fields)))
            return self.query_set

        def filter(self, **kwargs):
            filters = list()

            if len(kwargs.keys()) == 0:
                raise NoFilterGiven()

            for field in kwargs.keys():
                is_special = field.find("__") != -1
                field_name = field
                special = None

                if is_special:
                    special = field[field.find("__") + 2:]
                    field_name = field[:field.find("__")]

                if field_name not in self.__model_class__().__fields__.keys():
                    raise FieldNotFoundException(
                        "Field {} does not exists in model {}".format(field_name, self.__model_class__))

                field_instance = self.__model_class__().__fields__[field_name]
                field_name = field_name if field_instance.dialect_name is None else field_instance.dialect_name

                value = kwargs.get(field)

                if not is_special:
                    filters.append("{} = {}".format(
                        field_name,
                        field_instance.format(value)
                    ))

                else:
                    if special in ('isnull', 'isnot', 'isdifferent'):
                        if special == 'isnull':
                            if isinstance(value, bool):
                                filters.append("{} IS {}NULL".format(
                                    field_name,
                                    "NOT " if value is False else ""
                                ))

                            else:
                                raise WrongSpecialGiven("Not given a boolean for {} filter".format(field))

                        else:
                            filters.append("{} != {}".format(
                                field_name,
                                field_instance.format(value)
                            ))

            self.query_set = self.__init_query__() if self.query_set is None else self.query_set
            self.query_set.filters += filters
            return self

        def order_by(self, **kwargs):
            if len(kwargs.keys()) == 0:
                raise NoOrderByAttributeGiven()

            if len(kwargs.keys()) > 1:
                raise TooMuchOrderByAttributesGiven()

            field = [key for key in kwargs.keys()][0]
            value = kwargs.get(field)

            if field in self.__model_class__().__fields__.keys():
                field_instance = self.__model_class__().__fields__[field]
                field = field if field_instance.dialect_name is None else field_instance.dialect_name
                if isinstance(value, str) and value.upper() in ('DESC', 'ASC',):
                    order_by = "ORDER BY {} {}".format(
                        field,
                        value.upper()
                    )

                else:
                    raise WrongOrderByAttribute("Attribute {} is wrong for order by".format(value))

            else:
                raise FieldNotFoundException(
                    "Field {} does not exists in model {}".format(field, self.__model_class__))

            self.query_set = self.__init_query__() if self.query_set is None else self.query_set
            self.query_set.order_by = order_by
            return self

        def all(self):
            self.query_set = self.__init_query__() if self.query_set is None else self.query_set
            data = list()

            for row in self.query_set.query(True):
                print(row)
                data.append(self.__model_class__(**{
                    field_name: self.__model_class__().__fields__[field_name].format_from_db(row.get(field_name))
                    for field_name in row.keys()
                }))

            self.query_set = None
            return data

        def get(self):
            return self.first()

        def first(self):
            self.query_set = self.__init_query__() if self.query_set is None else self.query_set
            self.query_set.limit = 'LIMIT 1'
            row = self.query_set.query()
            data = self.__model_class__(**{
                field_name: self.__model_class__().__fields__[field_name].format_from_db(row.get(field_name))
                for field_name in row.keys()
            })
            self.query_set = None
            return data

        def last(self):
            self.query_set = self.__init_query__() if self.query_set is None else self.query_set
            self.query_set.limit = 'LIMIT 1'

            if self.query_set.order_by:
                asc_word = "ASC"
                desc_word = "DESC"
                words = {
                    asc_word: desc_word,
                    desc_word: asc_word
                }

                for word in words.keys():
                    if word in self.query_set.order_by:
                        self.query_set.order_by.replace(word, words.get(word))

            else:
                self.query_set.order_by = "ORDER BY 1 DESC"

            row = self.query_set.query()
            data = self.__model_class__(**{
                field_name: self.__model_class__().__fields__[field_name].format_from_db(row.get(field_name))
                for field_name in row.keys()
            })
            self.query_set = None
            return data

        def save(self, model_instance):
            if not isinstance(model_instance, self.__model_class__):
                raise WrongInstanceToSave()

            pk_found = not all([not field.primary_key for field in model_instance.__fields__.values()])
            pk = None

            insert = not pk_found

            if pk_found:
                for field_name in model_instance.__fields__.keys():
                    if model_instance.__fields__[field_name].primary_key:
                        pk = field_name

                insert = getattr(model_instance, pk, None) is None

                if not insert:
                    try:
                        self.filter(**{pk: getattr(model_instance, pk)}).get()
                        self.query_set = None

                    except NoContentFound:
                        insert = True

                    finally:
                        self.query_set = None

            model_instance.__validate_data__()
            field_names = list(model_instance.__fields__.keys())
            valid_field = [
                not model_instance.__fields__[field_name].primary_key
                and (
                        not hasattr(model_instance.__fields__[field_name], 'auto_now') or
                        not model_instance.__fields__[field_name].auto_now
                ) and (
                        not hasattr(model_instance.__fields__[field_name], 'auto_now_add') or
                        not model_instance.__fields__[field_name].auto_now_add
                ) for field_name in field_names
            ]
            values = [
                model_instance.__fields__[field_names[i]].format(getattr(model_instance, field_names[i]))
                for i in range(0, len(field_names)) if valid_field[i]
            ]
            field_names = [
                field_names[i] if model_instance.__fields__[field_names[i]].dialect_name is None
                else model_instance.__fields__[field_names[i]].dialect_name
                for i in range(0, len(field_names)) if valid_field[i]
            ]

            if insert:
                self.query_set = self.__init_insert_query__()
                self.query_set.parameters = field_names
                self.query_set.values = values
                new_id = self.query_set.query()
                self.query_set = None

                if pk_found:
                    model_instance = self.filter(**{pk: new_id}).get()

            else:
                self.query_set = self.__init_update_query__()
                self.filter(**{pk: getattr(model_instance, pk)})
                self.query_set.set_parameters = [
                    "{} = {}".format(field_names[i], values[i])
                    for i in range(0, len(field_names))
                ]
                self.query_set.query()
                self.query_set = None
                model_instance = self.filter(**{pk: getattr(model_instance, pk)}).get()

            return model_instance

        def drop(self, model_instance, force=False):
            if not isinstance(model_instance, self.__model_class__):
                raise WrongInstanceToDrop()

            soft_delete_object = not all(
                not (hasattr(field, 'soft_delete_field') and field.soft_delete_field)
                for field in model_instance.__fields__.values()
            )
            soft_delete_field = None

            if soft_delete_object:
                for field_name in model_instance.__fields__.keys():
                    field = model_instance.__fields__[field_name]

                    if hasattr(field, 'soft_delete_field') and field.soft_delete_field:
                        soft_delete_field = field_name

            pk_found = not all([not field.primary_key for field in model_instance.__fields__.values()])
            pk = None

            normal_delete = not pk_found

            if pk_found:
                for field_name in model_instance.__fields__.keys():
                    if model_instance.__fields__[field_name].primary_key:
                        pk = field_name

                normal_delete = getattr(model_instance, pk, None) is not None

                if normal_delete:
                    try:
                        self.filter(**{pk: getattr(model_instance, pk)}).get()
                        self.query_set = None

                    except NoContentFound:
                        normal_delete = False

                    finally:
                        self.query_set = None

            if (not soft_delete_object or not normal_delete) or force:
                self.query_set = self.__init_drop_query__()

                if normal_delete:
                    self.filter(**{pk: getattr(model_instance, pk)})

                else:
                    self.filter(**{field_name: getattr(model_instance, field_name)
                                   for field_name in model_instance.__fields__.keys()})

                self.query_set.query()
                return True

            setattr(model_instance, soft_delete_field, datetime.utcnow())
            model_instance = self.save(model_instance)
            return model_instance

    def __init__(self, table, model_class):
        self.__model__ = model_class
        self.objects = self.Objects(table, self.__model__)
