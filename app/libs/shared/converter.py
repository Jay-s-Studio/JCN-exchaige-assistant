import dataclasses
import inspect
import re
import typing
import uuid
from copy import deepcopy
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
from enum import IntEnum
from json import JSONDecodeError
from typing import TypeVar, List, Type, Union, Any

import ujson

from chatbot.libs.exceptions import (
    ValidationError,
    ConvertError,
    IntError,
    FloatError,
    BoolError,
    DateError,
    DateTimeError,
    UUIDError,
    ListError
)
from chatbot.libs.reflection import dinspect
from chatbot.libs.shared import validator

T = TypeVar('T')


class Converter:

    @classmethod
    def to_int(cls, value: Union[str, int, float], default: int = None, raise_error: bool = False):
        """
        :param value:
        :param default:
        :param raise_error:
        :return:
        """
        if isinstance(value, int):
            return value
        if validator.is_int(value):
            return int(value)
        if raise_error:
            raise IntError(value)
        return default or value

    @classmethod
    def to_bool(cls, value: Union[str, bool], default: bool = None, raise_error: bool = False):
        """
        :param raise_error:
        :param value:
        :param default:
        :return:
        """
        if isinstance(value, bool):
            return value
        if validator.is_bool(value):
            return value.lower() == 'true'
        if raise_error:
            raise BoolError(value)
        if default is not None:
            return default or value
        return False

    @classmethod
    def to_float(cls, value, default: float = None, raise_error: bool = False):
        if validator.is_number(value):
            return float(value)
        if raise_error:
            raise FloatError(value)
        return default or value

    @classmethod
    def to_datetime(cls, value, default=None, raise_error: bool = False):
        """
        :param raise_error:
        :param value:
        :param default:
        :return:
        """
        if isinstance(value, datetime):
            return value
        if validator.is_datetime(value):
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if validator.is_datetime_minute(value):
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        if validator.is_date(value):
            return datetime.strptime(value, '%Y-%m-%d')
        if raise_error:
            raise DateTimeError(value)
        return default or value

    @classmethod
    def to_date(cls, value: Any, default: date = None, raise_error: bool = False):
        """
        :param raise_error:
        :param value:
        :param default:
        :return:
        """
        if isinstance(value, date):
            return value
        if validator.is_date(value):
            dt = datetime.strptime(value, '%Y-%m-%d')
            return date(dt.year, dt.month, dt.day)
        if raise_error:
            raise DateError(value)
        return default or value

    @classmethod
    def to_hms(cls, value, default: tuple = (0, 0, 0), raise_error: bool = False):
        """
        :param value:
        :param default:
        :param raise_error:
        :return:
        """
        if isinstance(value, int) or isinstance(value, float):
            m, s = divmod(value, 60)
            h, m = divmod(m, 60)
            return int(h), int(m), format(s, ".1f")
        if raise_error:
            raise TypeError(f'{value} is not a valid int or float type')
        return default

    @classmethod
    def to_uuid(cls, value, default=None, raise_error: bool = False):
        if isinstance(value, uuid.UUID):
            return value
        if validator.is_uuid(value):
            return uuid.UUID(value)
        if raise_error:
            raise UUIDError(value)
        return default

    @classmethod
    def to_uuid_hex(cls, value):
        result = cls.to_uuid(value)
        if not result:
            return result
        return result.hex

    @classmethod
    def to_list(cls, value: Union[str, list], separator: str = ',', default_value: list = None):
        if not value:
            return default_value
        if isinstance(value, list):
            return value
        if isinstance(value, set):
            return list(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, str):
            return re.split(separator, value)
        raise ListError(value)

    @classmethod
    def convert(cls, expected: Type[T], actual: Any) -> T:
        """
        :param expected:
        :param actual:
        :return:
        """
        if not expected or expected == Any:
            return actual
        if actual is None:
            return None
        generic_type = dinspect.get_generic_type(expected)
        if generic_type:
            underlying_types = dinspect.get_generic_underlying_types(expected)
            if generic_type == Union:
                if type(actual) in underlying_types:
                    return actual
                for union_type in underlying_types:
                    if type(None) == union_type:
                        continue
                    try:
                        return cls.convert(union_type, actual)
                    except ValidationError:
                        pass
            elif generic_type in (list, tuple, set):
                if isinstance(actual, (list, tuple, set)):
                    return generic_type([cls.convert(underlying_types[0], item) for item in actual])
                elif isinstance(actual, str):
                    return cls.convert(generic_type, actual)
            raise ConvertError(actual, expected)
        if inspect.isclass(expected) and issubclass(expected, IntEnum):
            return expected(int(actual))
        if inspect.isclass(expected) and issubclass(expected, Enum):
            # noinspection PyArgumentList
            return expected(actual)
        if isinstance(actual, list):
            return actual
        if isinstance(actual, dict):
            return actual
        if isinstance(actual, str) and (expected == dict or expected == list):
            if actual == '[]':
                return []
            if actual == '{}':
                return {}
            try:
                return ujson.loads(actual)
            except JSONDecodeError:
                raise ConvertError(actual, 'JSON')
        if isinstance(actual, expected):
            return actual
        if dataclasses.is_dataclass(expected):
            if isinstance(actual, dict):
                return cls.as_dataclass(actual, as_class=expected)
            raise ConvertError(actual, expected)
        if expected is int:
            return cls.to_int(actual, raise_error=True)
        if expected is float:
            return cls.to_float(actual, raise_error=True)
        if expected is bool:
            return cls.to_bool(actual, raise_error=True)
        if expected is datetime:
            return cls.to_datetime(actual, raise_error=True)
        if expected is date:
            return cls.to_date(actual, raise_error=True)
        if expected is str:
            if isinstance(actual, (list, dict)):
                return ujson.dumps(actual, ensure_ascii=False)
            return str(actual)
        if issubclass(expected, type(actual)):
            try:
                return expected(actual)
            except Exception:
                raise ConvertError(actual, expected)
        raise ConvertError(actual, expected)

    @classmethod
    def format_value(cls, value: Any):
        if isinstance(value, uuid.UUID):
            return str(value)
        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, Decimal):
            return int(value)
        return value

    @classmethod
    def as_dataclass(
        cls,
        item: Union[dict, Type[T], Type[dataclasses.dataclass], list],
        as_class: Type[T],
        use_default: bool = True,
        **kwargs
    ) -> T:
        """
        :param item:
        :param as_class:
        :param use_default:
        :return:
        """
        if isinstance(item, as_class):
            return item
        if item is not None and not isinstance(item, dict):
            raise TypeError(f'item {item} must be dict')
        if not as_class:
            raise TypeError('as_class is not none')
        if not dataclasses.is_dataclass(as_class):
            raise TypeError(f'as_class {type(as_class)} must be dataclass')
        _kwargs = dict(
            use_default=True,
            **kwargs
        )
        data = {}
        copy_item = deepcopy(item) or {}
        for field in dataclasses.fields(as_class):  # type: dataclasses.Field
            value = copy_item.pop(field.name, None)
            if value is None and use_default:
                if field.default is not None:
                    data[field.name] = field.default
                else:
                    data[field.name] = None
                continue
            if value is None:
                data[field.name] = None
                continue
            underlying_type = dinspect.get_generic_list_underlying(field.type)
            if underlying_type and dataclasses.is_dataclass(underlying_type):
                data[field.name] = cls.as_dataclasses(value, underlying_type, **_kwargs)
            elif inspect.isclass(field.type) and issubclass(field.type, Enum):
                data[field.name] = field.type(value)
            elif dataclasses.is_dataclass(field.type):
                data[field.name] = cls.as_dataclass(value, field.type, **_kwargs)
            elif field.type != type(value):
                data[field.name] = cls.format_value(value)
            else:
                data[field.name] = value
        if kwargs:
            data.update(kwargs)
        dt = as_class(**data)
        setattr(dt, '__raw__', item)
        return dt

    @classmethod
    def as_dataclasses(
        cls,
        items: List[dict],
        as_class: Type[T],
        use_default: bool = True,
        **kwargs
    ) -> List[T] or None:
        """
        :param items:
        :param as_class:
        :param use_default:
        :param kwargs:
        :return:
        """
        if items is None:
            return None
        _dataclasses = []
        for item in items:
            _dataclasses.append(cls.as_dataclass(
                item,
                as_class=as_class,
                use_default=use_default,
                **kwargs
            ))
        return _dataclasses

    @classmethod
    def as_json(
        cls,
        _dataclass: Any,
        ignore_none: bool = True,
        ignore_empty: bool = False,
        remove_key_prefix: str = None,
        use_default_value: bool = True,
        use_raw_data: bool = False,
        omit: List[str] = None
    ) -> Union[dict, list]:
        """
        :param _dataclass:
        :param ignore_none:
        :param ignore_empty:
        :param remove_key_prefix:
        :param use_default_value:
        :param use_raw_data:
        :param omit:
        :return:
        """
        if not _dataclass:
            return _dataclass

        data = {}

        def remove_prefix(_key: str):
            if not remove_key_prefix:
                return _key
            if not isinstance(_key, str):
                return _key
            return _key.lstrip(remove_key_prefix)

        kwargs = dict(
            ignore_none=ignore_none,
            ignore_empty=ignore_empty,
            remove_key_prefix=remove_key_prefix,
            use_default_value=use_default_value,
            use_raw_data=use_raw_data,
            omit=omit
        )
        if isinstance(_dataclass, dict):
            for key, value in _dataclass.items():
                if omit and key in omit:
                    continue
                if ignore_none and value is None:
                    continue
                if ignore_empty and not value and value != 0:
                    continue
                if isinstance(value, list):
                    data[remove_prefix(key)] = [cls.as_json(item, **kwargs) for item in value]
                else:
                    data[remove_prefix(key)] = cls.as_json(value, **kwargs)
            return data
        elif isinstance(_dataclass, (list, set, tuple)):
            return [cls.as_json(item, **kwargs) for item in _dataclass]
        elif dataclasses.is_dataclass(_dataclass):
            for field in dataclasses.fields(_dataclass):  # type:dataclasses.Field
                if omit and field.name in omit:
                    continue
                key = remove_prefix(field.name)
                if (
                    use_raw_data and
                    hasattr(_dataclass, '__raw__') and
                    key not in _dataclass.__raw__
                ):
                    continue
                value = getattr(_dataclass, field.name)
                if value is None and use_default_value:
                    if (
                        field.default_factory and
                        not isinstance(field.default_factory, dataclasses.MISSING)
                    ):
                        value = field.default_factory()

                if value is None:
                    if ignore_none:
                        continue
                    data[key] = None
                    continue
                if ignore_empty and not value and value != 0:
                    continue
                if dinspect.is_generic_type(field.type):
                    generic_type = dinspect.get_generic_type(field.type)
                    if generic_type is dict:
                        data[key] = cls.as_json(value, **kwargs)
                    elif generic_type is list:
                        data[key] = [cls.as_json(item, **kwargs) for item in value]
                    elif generic_type is Union:
                        is_success = False
                        union_types = dinspect.get_union_underlying(field.type)
                        if type(value) in union_types:
                            data[key] = value
                            continue
                        for utype in union_types:
                            try:
                                data[key] = cls.convert(utype, value)
                                is_success = True
                            except Exception:
                                pass
                        if not is_success:
                            raise TypeError(
                                f'Field {field.name} value {value} cannot be converted '
                                f'to {field.type} type, please make sure the annotation type and '
                                f'value type are the same')
                elif inspect.isclass(field.type) and issubclass(field.type, Enum):
                    if not isinstance(value, Enum):
                        raise TypeError(
                            f'The field {field.name} value {value} is not an enum {field.type}'
                            f' type, please make sure that the annotation type is consistent '
                            f'with the default value type'
                        )
                    data[key] = value.value
                elif dataclasses.is_dataclass(field.type):
                    data[key] = cls.as_json(value, **kwargs)
                elif field.type == typing.Any:
                    data[key] = cls.as_json(value, **kwargs)
                else:
                    data[key] = cls.format_value(value)
            return data
        return cls.format_value(_dataclass)


__all__ = [
    'Converter',
]
