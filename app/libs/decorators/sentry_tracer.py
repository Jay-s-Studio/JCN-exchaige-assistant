"""
telemetry tracer
"""
import inspect
from functools import wraps
from typing import Callable

import sentry_sdk
from sentry_sdk.consts import SPANDATA
from sentry_sdk.tracing import Span


def distributed_trace(
    *,
    op: str = None,
    description: str = None,
    inject_span: bool = False
) -> Callable:
    """
    A decorator to instrument a class or function with an open telemetry tracing span.
    Usage Example::
        class Foo:

            @distributed_trace()
            def sync_func(self, *args, **kwargs):
                ...

            @distributed_trace()
            async def async_func(self, *args, **kwargs):
                ...

            @distributed_trace(inject_span=True)
            def func_with_inject_span(self, xxx, _span: Span):
                # _span.set_data()
                ...

    :param op:
    :param description:
    :param inject_span:
    :return:
    """

    def decorator(func):
        """

        :param func:
        :return:
        """
        operation = op or func.__name__.replace("_", " ").title()
        name = description or func.__qualname__

        def _set_semantic_attributes(span: Span, raw_func: Callable):
            """

            :param span:
            :param raw_func:
            :return:
            """
            span.set_data(SPANDATA.CODE_FILEPATH, str(raw_func.__code__.co_filename))  # noqa
            span.set_data(SPANDATA.CODE_LINENO, str(raw_func.__code__.co_firstlineno))  # noqa
            span.set_data(SPANDATA.CODE_FUNCTION, str(raw_func.__qualname__))  # noqa
            span.set_data(SPANDATA.CODE_NAMESPACE, str(raw_func.__module__))  # noqa

        def _check_func_args_has_span(raw_func: Callable):
            """

            :param raw_func:
            :return:
            """
            return "_span" in inspect.signature(raw_func).parameters

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            with sentry_sdk.start_span(
                op=operation,
                description=name
            ) as span:  # type: Span
                _set_semantic_attributes(span=span, raw_func=func)
                try:
                    if inject_span and _check_func_args_has_span(func):
                        result = func(*args, **kwargs, _span=span)
                    else:
                        result = func(*args, **kwargs)
                except Exception as exc:
                    span.set_data("Exception", str(exc))
                    raise exc
            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            with sentry_sdk.start_span(
                op=operation,
                description=name
            ) as span:  # type: Span
                _set_semantic_attributes(span=span, raw_func=func)
                try:
                    if inject_span and _check_func_args_has_span(func):
                        result = await func(*args, **kwargs, _span=span)
                    else:
                        result = await func(*args, **kwargs)
                except Exception as exc:
                    span.set_data("Exception", str(exc))
                    raise exc
            return result

        wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
        return wrapper

    return decorator
