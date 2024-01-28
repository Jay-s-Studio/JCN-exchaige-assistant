import asyncio
import functools
import typing
from typing import Any


def is_generic_type(obj: Any):
    if not obj:
        return False
    return hasattr(obj, '__origin__')


def is_generic_type_of(obj: Any, type_of: Any):
    if not obj:
        return False
    if hasattr(obj, '__origin__') and obj.__origin__ == type_of:
        return True
    return False


def is_generic_list(obj: Any):
    return is_generic_type_of(obj, list)


def is_generic_set(obj: Any):
    return is_generic_type_of(obj, set)


def is_generic_tuple(obj: Any):
    return is_generic_type_of(obj, tuple)


def is_generic_union(obj: Any):
    return is_generic_type_of(obj, typing.Union)


def get_generic_list_underlying(obj: Any):
    if not is_generic_list(obj):
        return None
    return obj.__args__[0]


def get_generic_underlying_types(obj):
    """
    :param obj:
    :return:
    """
    if not obj:
        return None
    if hasattr(obj, '__origin__'):
        return obj.__args__
    return None


def get_generic_type(obj):
    """
    :param obj:
    :return:
    """
    if not obj:
        return None
    if hasattr(obj, '__origin__'):
        return obj.__origin__
    return None


def get_union_underlying(obj: Any):
    if is_generic_union(obj):
        return obj.__args__
    return []


def is_coroutine(func: Any):
    if asyncio.iscoroutinefunction(func) or \
            (isinstance(func, functools.partial) and asyncio.iscoroutinefunction(func.func)):
        return True
    return False


async def call(func: Any, params: typing.Dict[str, Any]):
    if is_coroutine(func):
        if params is None:
            return await func()
        return await func(**params)
    if params is None:
        return func()
    return func(**params)


def is_optianal(obj: Any):
    if not obj:
        return False
    if hasattr(obj, '__origin__') and obj.__origin__ == typing.Union:
        if type(None) in obj.__args__ and len(obj.__args__) == 2:
            return True
    return False


def get_optianal_underlying(obj: Any):
    if not is_optianal(obj):
        return None
    if type(None) != obj.__args__[0]:
        return obj.__args__[0]
    return obj.__args__[1]
