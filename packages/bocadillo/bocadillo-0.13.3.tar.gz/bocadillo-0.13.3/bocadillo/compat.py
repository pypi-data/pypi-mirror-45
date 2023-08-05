import asyncio
import re
from typing import (
    Callable,
    cast,
    List,
    TypeVar,
    Union,
    Optional,
    Any,
    Awaitable,
)

try:
    # >= 3.7
    from contextlib import nullcontext  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    from contextlib import contextmanager

    @contextmanager
    def nullcontext(enter_result: Any = None):
        yield enter_result


from starlette.concurrency import run_in_threadpool

_CAMEL_REGEX = re.compile(r"(.)([A-Z][a-z]+)")
_SNAKE_REGEX = re.compile(r"([a-z0-9])([A-Z])")

_V = TypeVar("_V")


class asyncnullcontext:
    def __init__(self, enter_result: Any = None):
        self._result = enter_result

    async def __aenter__(self):
        return self._result

    async def __aexit__(self, *args):
        pass


async def call_async(
    func: Union[Callable[..., _V], Callable[..., Awaitable[_V]]],
    *args: Any,
    sync: Optional[bool] = None,
    **kwargs: Any
) -> _V:
    """Call a function in an async manner.

    # Parameters
    func:
        a callable that is either awaited (if a coroutine function)
        or run in the thread pool (if a regular function).
    sync (bool):
        a hint as to whether `func` is synchronous. If not given, it is
        inferred as `asyncio.iscoroutinefunction(func)`.

    # See Also
    - [Executing code in thread or process pools](https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools)
    """
    if sync or (sync is None and not asyncio.iscoroutinefunction(func)):
        return await run_in_threadpool(func, *args, **kwargs)

    async_func = cast(Callable[..., Awaitable[_V]], func)
    return await async_func(*args, **kwargs)


def camel_to_snake(name: str) -> str:
    """Convert a `CamelCase` name to its `snake_case` version."""
    s1 = _CAMEL_REGEX.sub(r"\1_\2", name)
    return _SNAKE_REGEX.sub(r"\1_\2", s1).lower()


# WSGI

Environ = dict
StartResponse = Callable[[str, List[str]], None]
WSGIApp = Callable[[Environ, StartResponse], List[bytes]]


def empty_wsgi_app() -> WSGIApp:
    """Return a WSGI app that always returns `404 Not Found`."""

    def wsgi(environ, start_response):
        status = "404 Not Found"
        body = b"Not Found"
        headers = [("Content-Type", "text/plain")]
        start_response(status, headers)
        return [body]

    return wsgi
