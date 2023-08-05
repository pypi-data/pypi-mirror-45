import inspect
from functools import wraps
from typing import Callable, cast, Dict, Union, Awaitable, Type

from .compat import call_async
from .request import Request
from .response import Response
from .routing import HTTPRoute
from .views import Handler, get_handlers, View

HookFunction = Callable[[Request, Response, dict], Awaitable[None]]
HookCollection = Dict[HTTPRoute, HookFunction]

BEFORE = "before"
AFTER = "after"


class Hooks:
    """Hooks manager."""

    def before(self, hook: HookFunction, *args, **kwargs):
        """Register a before hook on a handler.

        # Parameters
        hook (callable): a hook function.
        """
        return self._hook_decorator(BEFORE, hook, *args, **kwargs)

    def after(self, hook: HookFunction, *args, **kwargs):
        """Register an after hook on a handler.

        # Parameters
        hook (callable): a hook function.
        """
        return self._hook_decorator(AFTER, hook, *args, **kwargs)

    def _hook_decorator(
        self, hook_type: str, hook: HookFunction, *args, **kwargs
    ):
        # Enclose args and kwargs
        async def hook_func(req: Request, res: Response, params: dict):
            await call_async(  # type: ignore
                hook, req, res, params, *args, **kwargs
            )

        def decorator(handler: Union[Type[View], Handler]):
            """Attach the hook to the given handler."""
            if not inspect.isclass(handler):
                return _with_hook(hook_type, hook_func, cast(Handler, handler))

            view_cls = cast(View, handler)

            # Recursively apply hook to all handlers.
            for method, _handler in get_handlers(view_cls).items():
                setattr(view_cls, method, decorator(_handler))

            return view_cls

        return decorator


def _with_hook(hook_type: str, func: HookFunction, handler: Handler):
    async def call_hook(args, kw):
        if len(args) == 2:
            req, res = args
        else:
            # method that has `self` as a first parameter
            req, res = args[1:3]
        assert isinstance(req, Request)
        assert isinstance(res, Response)
        await call_async(func, req, res, kw)

    if hook_type == BEFORE:

        @wraps(handler)
        async def with_before_hook(*args, **kwargs):
            await call_hook(args, kwargs)
            await call_async(handler, *args, **kwargs)

        return with_before_hook

    assert hook_type == AFTER

    @wraps(handler)
    async def with_after_hook(*args, **kwargs):
        await call_async(handler, *args, **kwargs)
        await call_hook(args, kwargs)

    return with_after_hook


# Pre-bind to module
hooks = Hooks()
before = hooks.before
after = hooks.after
