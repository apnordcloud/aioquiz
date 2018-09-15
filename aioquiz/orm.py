#!/usr/bin/env python3.5
# encoding: utf-8
from abc import abstractmethod
from datetime import datetime
import json
import logging
import re

import asyncpg
from asyncpg.exceptions import DatatypeMismatchError
from asyncpg.exceptions import PostgresSyntaxError
from asyncpg.exceptions import UndefinedColumnError
from asyncpg.exceptions import UniqueViolationError
from asyncpg.exceptions import ForeignKeyViolationError
from asyncpg.exceptions import InvalidTextRepresentationError

from config import DB
from utils import color_print

psql_cfg = {
    'user': DB.USER,
    'database': DB.DB,
    'host': DB.HOST,
    'password': DB.PASSWORD
}

db = None  # Perhaps make a 'db' class instead of using a global variable?


# noinspection PyBroadException
async def make_a_query(query, retry=False):
    global db
    if ';' in query:
        query = query.replace(';', '')
    try:
        if not db:
            db = await asyncpg.connect(**psql_cfg)
        try:
            return await db.fetch(query)
        except (
            DatatypeMismatchError,
        ):
            logging.exception('queering db: %s', query)
        except (PostgresSyntaxError, UndefinedColumnError):
            logging.warning('queering db: %s', query)
            raise
    except (UniqueViolationError, PostgresSyntaxError, UndefinedColumnError):
        raise
    except InvalidTextRepresentationError:
        logging.warning('queering db: %s', query)
        raise
    except ConnectionRefusedError:
        logging.error('DataBase is not UP!')
        color_print('DataBase is not UP!', color='red')
    except:
        if retry:
            logging.exception('connecting to db')
        db = None
        if not retry:
            return await make_a_query(query, retry=True)
    return False


class DoesNotExist(Exception):
    @staticmethod
    async def to_dict():
        return {'msg': 'Does not exist', 'success': False}


class StringLiteral:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return self.content


# noinspection PyProtectedMember
class Table(object):
    _restricted_keys = []
    _soft_restricted_keys = []

    def __init__(self, **kwargs):
        for field in self._schema:
            name = field.name
            if name not in kwargs:
                if field.default is not None:
                    setattr(self, name, field.default)
                elif field.required and name != 'id':
                    raise Exception('No {} provided'.format(name))
            else:
                setattr(self, name, kwargs[field.name])

    def __str__(self):
        return '<' + self._name + ' ' + ' '.join([('{}={}'.format(prop.name, getattr(self, prop.name))) for prop in self._schema if not prop.name.startswith('time')]) + '>'

    def __repr__(self):
        return self.__str__()

    @classmethod
    def _gen_schema(cls):
        return ', '.join(str(field) for field in cls._schema)

    @classmethod
    def _in_schema(cls, name):
        return any(field.name == name for field in cls._schema)

    @property
    @abstractmethod
    def _name(self):
        pass

    @property
    @abstractmethod
    def _schema(self):
        pass

    @classmethod
    async def _table_exists(cls):
        # Bardziej elegancko byłoby przekazać to cls._name jako parametr do zapytania. Dotyczy wszystkich zapytań typu
        # ... WHERE X = <jakis_parametr>
        exists = await make_a_query(
            """SELECT EXISTS (
                    SELECT 1
                    FROM   information_schema.tables
                    WHERE  tables.table_name = '{}'
                )
            """.format(cls._name)
        )
        return exists[0]['exists'] == True

    @classmethod
    async def create_table(cls):
        if not await cls._table_exists():
            unique = ", UNIQUE ({})".format(", ".join(cls._unique)) if hasattr(cls, '_unique') else ''
            querry = """CREATE TABLE {} ( {} {})""".format(
                cls._name,
                cls._gen_schema(),
                unique
            )
            await make_a_query(querry)
            color_print('{} table created'.format(cls._name), color='green')
        else:
            print('{} table already exists'.format(cls._name))

    @classmethod
    async def get_by_id(cls, uid):
        resp = await make_a_query(
            """SELECT * FROM {} WHERE id = {}""".format(cls._name, uid)
        )
        return cls(**dict(resp[0]))

    @classmethod
    async def get_all(cls, suffix=""):
        resp = await make_a_query("""SELECT * FROM {} {}""".format(cls._name, suffix))
        return [cls(**dict(r)) for r in resp]

    @classmethod
    async def get_by_field_value(cls, field, value):
        if isinstance(value, str):
            resp = await make_a_query("""SELECT * FROM {} WHERE {}='{}'""".format(cls._name, field, value))
        else:
            resp = await make_a_query("""SELECT * FROM {} WHERE {}={}""".format(cls._name, field, value))
        return [cls(**dict(r)) for r in resp]

    @classmethod
    async def get_by_join(cls, *args, **kwargs):
        allowed_fields = [c.name for c in cls._schema]

        tables = "{}, {}".format(cls._name, ", ".join(args))
        query = """SELECT {} FROM {} WHERE""".format(
            ", ".join(allowed_fields),
            tables
        )

        for i, kw in enumerate(kwargs):
            if isinstance(kwargs[kw], (dict, list)):
                kwargs[kw] = json.dumps(kwargs[kw])
            if isinstance(kwargs[kw], str):
                query += " {}='{}'".format(kw, kwargs[kw])
            else:
                query += " {}={}".format(kw, kwargs[kw])
            if i + 1 < len(kwargs):
                query += " AND "

        resp = await make_a_query(query)
        return [cls(**dict(r)) for r in resp]

    @classmethod
    async def get_by_many_field_value(cls, **kwargs):
        if not kwargs:
            return await cls.get_all()
        query = """SELECT * FROM {} WHERE """.format(cls._name)
        for i, kw in enumerate(kwargs):
            if isinstance(kwargs[kw], (dict, list)):
                kwargs[kw] = json.dumps(kwargs[kw])
            if isinstance(kwargs[kw], str):
                query += """ {}='{}'""".format(kw, kwargs[kw])
            else:
                query += """  {}={}""".format(kw, kwargs[kw])
            if i + 1 < len(kwargs):
                query += """ AND """
        resp = await make_a_query(query)
        if not resp:
            return resp
        return [cls(**dict(r)) for r in resp]

    @classmethod
    async def delete_by_many_fields(cls, **kwargs):
        query = """DELETE FROM {} WHERE """.format(cls._name)
        for i, key in enumerate(kwargs):
            query += """ {}='{}'""".format(key, kwargs[key])

            if i + 1 < len(kwargs):
                query += """ OR """
        resp = await make_a_query(query)

    @classmethod
    async def get_first_by_many_field_value(cls, **kwargs):
        # Lepiej byłoby już w samym zapytaniu dać coś w stylu LIMIT 1, poza tym przydałoby się ORDER BY
        data = await cls.get_by_many_field_value(**kwargs)
        try:
            return data[0]
        except Exception as err:
            raise DoesNotExist

    @classmethod
    async def get_first(cls, field, value):
        # Jak wyżej
        data = await cls.get_by_field_value(field, value)
        try:
            return data[0]
        except Exception as err:
            raise DoesNotExist

    @classmethod
    def _format_create(cls, clsi):
        keys = []
        values = """"""
        for prop in cls._schema:
            if prop.name != 'id':
                keys.append(prop.name)
                try:
                    val = getattr(clsi, prop.name)
                except AttributeError:
                    if not prop.required:
                        val = 'null'
                    else:
                        raise
                if isinstance(prop.type, (String, CodeString)):
                    val = prop.type.format(val)
                    values += """\'{}\'""".format(val.replace("'", "\"").replace('"', "\""))
                elif isinstance(prop.type, DateTime):
                    val = getattr(clsi, prop.name)
                    values += "'"
                    values += str(val)
                    values += "'"
                else:
                    values += str(val)
                values += ', '
        return ', '.join(keys), values[:-2]

    @classmethod
    async def _create(cls, data):
        resp = await make_a_query(
            """INSERT INTO {} ({}) VALUES ({})""".format(
                cls._name,
                *cls._format_create(data)
            )
        )
        if cls._in_schema('id'):
            resp = await make_a_query(
                """SELECT id FROM {} ORDER BY id DESC limit 1""".format(cls._name)
            )
            return resp[0]['id']
        return resp

    async def create(self):
        try:
            resp = await self._create(self)
            if self._in_schema('id'):
                self.id = resp
            return resp
        except (UniqueViolationError, PostgresSyntaxError, UndefinedColumnError):
            raise
        except Exception as e:
            logging.exception('Error creating {}'.format(self._name))
            return isinstance(e, TypeError)

    async def update_or_create(self, *args, verbose=False, get_insta=False):
        kw = {arg: getattr(self, arg) for arg in args}
        try:
            inst = await self.get_first_by_many_field_value(**kw)
        except DoesNotExist:
            inst = None
        if inst:
            await inst.update(**kw)
            if get_insta:
                return inst, True
            if hasattr(inst, 'id'):
                if verbose:
                    return inst.id, True
                return inst.id
            else:
                if verbose:
                    return True, True
                return True
        else:
            resp = await self.create()
            if get_insta:
                insta = await self.get_by_id(resp)
                return insta, True
            if verbose:
                return resp, False
            return resp

    @classmethod
    def _format_update(cls, clsi):
        try:
            return ', '.join([
                ("{}='{}'".format(prop.name, prop.type.format(getattr(clsi, prop.name))))
                for prop in cls._schema if not prop.name.startswith('time_created') and prop.name != 'id' and (prop.required or getattr(clsi, prop.name))
            ])
        except:
            logging.exception('_format_update' + str(clsi))

    @classmethod
    def _format_kwargs(cls, **kwargs):
        querry = ''
        for i, kw in enumerate(kwargs):
            if isinstance(kwargs[kw], str):
                querry += """ {}='{}'""".format(kw, kwargs[kw])
            else:
                querry += """ {}={}""".format(kw, kwargs[kw])
            if i + 1 < len(kwargs):
                querry += """ AND """
        return querry

    @classmethod
    async def _update(cls, data, **kwargs):
        if hasattr(data, 'id'):
            querry = """
                UPDATE {} SET {}
                WHERE id = {}
            """.format(cls._name, cls._format_update(data), data.id)
            resp = await make_a_query(querry)
        else:
            wheres = cls._format_kwargs(**kwargs)
            resp = await make_a_query(
                """UPDATE {} SET {} WHERE {}""".format(cls._name, cls._format_update(data), wheres)
            )
        return resp

    async def update(self, **kwargs):
        return await self._update(self, **kwargs)

    async def update_from_dict(self, data_dict):
        for key, value in data_dict.items():
            if self._in_schema(key) and key not in self._restricted_keys + ['create_date', 'last_login']:
                setattr(self, key, value)
        return await self.update()

    async def to_dict(self, include_soft=False):
        restricted_keys = self._restricted_keys if include_soft else self._restricted_keys + self._soft_restricted_keys
        return {
            field.name: getattr(self, field.name)
            for field in self._schema
            if field.name not in restricted_keys
        }

    @classmethod
    async def count_all(cls):
        resp = await make_a_query(
            """SELECT COUNT(*) FROM {}""".format(cls._name)
        )
        return dict(resp[0])['count']

    @classmethod
    async def count_by_field(cls, append='', **kwargs):
        resp = await make_a_query(
            """SELECT COUNT(*) FROM {} WHERE """.format(cls._name) + cls._format_kwargs(**kwargs) + append
        )
        return dict(resp[0])['count']

    @classmethod
    async def group_by_field(cls, name, **kwargs):
        query = """SELECT {name}, COUNT(*) FROM {table} """.format(table=cls._name, name=name)
        if kwargs:
            query += ' WHERE ' + cls._format_kwargs(**kwargs)
        query += """ GROUP BY {name}""".format(name=name)
        resp = await make_a_query(
            query
        )
        return dict(resp)

    @classmethod
    async def _delete(cls, data, **kwargs):
        try:
            if hasattr(data, 'id'):
                resp = await make_a_query(
                    """DELETE FROM {}
                    WHERE id={}
                    """.format(cls._name, data.id))
            else:
                resp = await make_a_query("""DELETE FROM {} WHERE {}""".format(cls._name, cls._format_kwargs(**kwargs)))
            return resp
        except ForeignKeyViolationError:
            logging.error('Could not delete {} id: {}'.format(cls._name, data.id))
        except:
            logging.exception('Could not delete')
        return False

    async def delete(self, **kwargs):
        await self._delete(self, **kwargs)

    @classmethod
    async def detele_by_id(cls, uid):
        try:
            resp = await make_a_query(
                """DELETE FROM {} WHERE id={}""".format(cls._name, uid)
            )
            return resp
        except ForeignKeyViolationError:
            logging.error('Could not delete {} id: {}'.format(cls._name, uid))
        except:
            logging.exception('Could not delete')
        return False

    def _add_new_column(self):
        """
        ALTER TABLE users ADD COLUMN lang character varying(20) NOT NULL DEFAULT 'pl';
        ALTER TABLE exercise_answare ADD COLUMN first_answare character varying(5000) NOT NULL DEFAULT '';
        ALTER TABLE users ADD COLUMN magic_string character varying(50) NOT NULL DEFAULT '';
        ALTER TABLE users ADD COLUMN magic_string_date timestamp;
        ALTER TABLE quiz ADD COLUMN active bool;
        ALTER TABLE users ADD COLUMN gdpr bool DEFAULT false;
        """
        pass

    def _rename_column(self):
        """
        ALTER TABLE exercise RENAME COLUMN possible_answare TO possible_answer;
        ALTER TABLE exercise_answer RENAME COLUMN answare TO answer;
        ALTER TABLE exercise_answer RENAME COLUMN first_answare TO first_answer;
        ALTER TABLE question RENAME COLUMN answares TO answer;
        ALTER TABLE question RENAME COLUMN possible_answare TO possible_answer;
        ALTER TABLE question_answer RENAME COLUMN answare TO answer;
        ALTER TABLE live_quiz_answer RENAME COLUMN answare TO answer;
        ALTER TABLE question RENAME COLUMN answer TO answers;
        """
        pass

    def _rename_table(self):
        """
        ALTER TABLE exercise_answare RENAME TO exercise_answer;
        ALTER TABLE question_answare RENAME TO question_answer;
        ALTER TABLE live_quiz_answare RENAME TO live_quiz_answer;
        """
        pass

    @classmethod
    async def sum(cls, field, **kwargs):
        query = """SELECT SUM({}) FROM {} WHERE {}""".format(
            field,
            cls._name,
            cls._format_kwargs(**kwargs)
        )
        resp = await make_a_query(query)
        return resp[0]['sum']


class Column:
    def __init__(
            self,
            name,
            type_,
            primary_key=False,
            required=True,
            default=None,
            unique=False
    ):
        self.name = name
        self.type = type_
        self.primary_key = primary_key
        self.required = required
        self.unique = unique
        self.default = default() if callable(default) else default

    def __str__(self):
        if self.unique:
            return '{} {} UNIQUE NOT NULL'.format(self.name, str(self.type))
        elif not self.primary_key:
            return '{} {}'.format(self.name, str(self.type))
        return '{} serial primary key'.format(self.name)


class ColumnType:
    @classmethod
    def __str__(cls):
        return cls._type

    @property
    @abstractmethod
    def _type(self):
        pass

    @property
    @abstractmethod
    def _py_type(self):
        pass

    @classmethod
    def validate(cls, data):
        return isinstance(data, cls._py_type)

    def format(self, data):
        return data


class Integer(ColumnType):
    _type = 'integer'
    _py_type = int


class Float(ColumnType):
    _type = 'float'
    _py_type = float


class String(ColumnType):
    _type = 'varchar({})'
    _py_type = str

    def __init__(self, length):
        self.length = length

    def __str__(self):
        return self._type.format(self.length)

    def validate(self, data):
        if super().validate(data) and len(data) <= self.length:
            return re.match("^[\sA-Za-z0-9_-]*$", data)
        return False

    def format(self, data):
        try:
            if isinstance(data, str):
                data = data.replace("'", "\"").replace('"', "\"")
                return data
            return json.dumps(data)
        except:
            logging.exception('String formatting')


class CodeString(String):
    _type = 'varchar({})'
    _py_type = str

    def validate(self, data):
        if isinstance(data, self._py_type):
            return re.match(
                "^[\s\(\)A-Za-z0-9\-_\.\+\*\\\/:=\'\{\},<\"\^\[\]]*",
                data
            )
        return False


class Boolean(ColumnType):
    _type = 'boolean'
    _py_type = bool


class DateTime(ColumnType):
    _type = 'timestamp'
    _py_type = datetime

    def validate(self, data):
        if super().validate(data):
            return re.match("^[0-9\.:/]*$", data)
        return False

    def format(self, data):
        return str(data).split('.')[0]


class ForeignKey(ColumnType):
    _type = 'integer references {} (id)'
    _py_type = int

    def __init__(self, f_key):
        self.f_key = f_key

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._type.format(self.f_key)
