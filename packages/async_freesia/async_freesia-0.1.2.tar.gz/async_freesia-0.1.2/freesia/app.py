"""
This module implements the async app of the web framework.
"""
import asyncio
from inspect import iscoroutinefunction
from typing import Any, Callable, MutableMapping, Tuple, Union, Container, Sized, Iterable
from pprint import pprint

from aiohttp import web

from .route import Route, Router
from .utils import Response


class Freesia:
    """
    The main class of this framework.
    """
    #: Default route class.
    #: See more information in :class:`freesia.route.Route` and :class:`freesia.route.AbstractRoute`.
    route_cls = Route
    #: Default router class.
    #: See more information in :class:`freesia.route.Router` and :class:`freesia.route.AbstractRouter`.
    url_map_cls = Router
    #: collected routes
    rules = None
    #: collected groups
    groups = None

    def __init__(self):
        self.rules = []
        self.middleware = []
        self.groups = {}
        self.url_map = self.url_map_cls()

    def route(self, rule: str, **options: Any) -> Callable:
        """
        Register the new route to the framework.

        :param rule: url rule
        :param options: optional params
        :return: a decorator to collect the target function
        """
        options.setdefault("method", ("GET",))
        methods = options["method"]

        def decorator(func):
            self.add_route(rule, methods, func, options)
            return func

        return decorator

    def set_filter(self, name: str, url_filter: Tuple[str, Union[None, Callable], Union[None, Callable]]):
        """
        Add url filter.
        For more information see :attr:`route_cls`

        :param name: name of the url filter
        :param url_filter: A tuple that includ regex, in_filter and out_filter
        :return: None
        """
        self.route_cls.set_filter(name, url_filter)

    def add_route(self, rule: str, methods: Iterable[str] = None,
                  target: Callable = None,
                  options: MutableMapping = None,
                  view_func: Callable = None) -> None:
        """
        Internal method of :func:`route`.

        :param rule: url rule
        :param methods: the method that the target function should handles.
        :param target: target function
        :param options: optional prams
        :param view_func: the class based view. See :class:`freesia.view.View`.
        :return: None
        """
        if view_func:
            if hasattr(view_func, "methods"):
                methods = getattr(view_func, "methods")
            target = view_func

        if not callable(target):
            raise ValueError("Invalid target function {}.".format(target.__name__))

        r = self.route_cls(rule, methods or ["GET"], target, options or {})
        self.rules.append(r)
        self.url_map.add_route(r)

    async def cast(self, res: Any) -> Response:
        """
        Cast the res made by the user's handler to the normal response.

        :param res: route returned value
        :return: the instance of :class:`freesia.response.Response`
        """
        if iscoroutinefunction(res):
            return await self.cast(await res())

        if isinstance(res, Response): return res
        if isinstance(res, str) or isinstance(res, bytes):
            return Response(text=str(res))
        if isinstance(res, Container) and isinstance(res, Sized):
            if len(res) > 3:
                raise ValueError("Invalid response.")

            return Response(text=res[0],
                            status=res[1] if len(res) >= 1 else 200,
                            reason=res[2] if len(res) >= 2 else "ok",
                            )
        return Response(text=str(res))

    async def traverse_middleware(self, request: web.BaseRequest, user_handler: Callable) -> Any:
        """
        Call all registered middleware.
        """
        last_handler = user_handler
        for m in self.middleware:
            async def h(next_handler=m, last_handler=last_handler):
                return await next_handler(request, last_handler)

            last_handler = h
        return await last_handler()

    async def dispatch_request(self, request: web.BaseRequest) -> Response:
        """
        Dispatch request.

        :param request: the instance of :class:`aiohttp.web.BaseRequest`
        :return:
        """
        target, params = self.url_map.get(request.path, request.method)

        res = await target(request, *params)
        return res

    async def handler(self, request: web.BaseRequest) -> Response:
        """
        hands out a incoming request

        :param request: the instance of :class:`aiohttp.web.BaseRequest`
        :return: result
        """
        pprint(request.path)

        async def user_handler():
            return await self.dispatch_request(request)

        res = await self.cast(
            await self.traverse_middleware(request, user_handler)
        )
        return res

    async def serve(self, host: str, port: int):
        """
        Start to serve. Should be placed in a event loop.

        :param host: host
        :param port: port
        :return: None
        """
        server = web.Server(self.handler)
        runner = web.ServerRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

        print("""
 _______ .______       _______     _______.     _______. __       ___       __  
|   ____||   _  \     |   ____|   /       |    /       ||  |     /   \     |  | 
|  |__   |  |_)  |    |  |__     |   (----`   |   (----`|  |    /  ^  \    |  | 
|   __|  |      /     |   __|     \   \        \   \    |  |   /  /_\  \   |  | 
|  |     |  |\  \----.|  |____.----)   |   .----)   |   |  |  /  _____  \  |__| 
|__|     | _| `._____||_______|_______/    |_______/    |__| /__/     \__\ (__) 
            """)
        print("============ Servint on http://{}:{}/ ============".format(host, port))

        while True:
            await asyncio.sleep(1000 * 3600)

    def run(self, host="localhost", port=8080):
        """
        start a async serve
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.serve(host, port))
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    def register_group(self, group: Any) -> None:
        """
        Register :class:`freesia.groups.Group` to the app.

        :param group: The instance of :class:`freesia.groups.Group`.
        :return: None
        """
        if group.name in self.groups:
            raise ValueError("The group `{}` has been registered!".format(group.name))
        self.groups[group.name] = group
        group.register(self)

    def use(self, middleware: Iterable) -> None:
        """
        Register the middleware for this framework. See example::

            async def middleware(request, handler):
                print("enter middleware")
                return await handler()

            app = Freesia()
            app.use([middleware])

        :param middleware: A tuple of the middleware.
        :return: None
        """
        for m in middleware:
            if not iscoroutinefunction(m):
                raise ValueError("Middleware {} should be awaitable.".format(m.__name__))
            self.middleware.append(m)
