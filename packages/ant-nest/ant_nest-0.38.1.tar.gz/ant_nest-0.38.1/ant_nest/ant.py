import typing
import asyncio
import abc
import itertools
import logging
import time
import random
from collections import defaultdict
from asyncio.queues import Queue, QueueEmpty
from itertools import islice

import aiohttp
from aiohttp import ClientSession
from yarl import URL
from tenacity import retry
from tenacity.retry import retry_if_result, retry_if_exception_type
from tenacity.wait import wait_fixed
from tenacity.stop import stop_after_attempt

from .pipelines import Pipeline
from .things import Request, Response, Item
from .exceptions import ThingDropped
from .utils import run_cor_func

__all__ = ["Ant", "CliAnt"]


class Ant(abc.ABC):
    response_pipelines: typing.List[Pipeline] = []
    request_pipelines: typing.List[Pipeline] = []
    item_pipelines: typing.List[Pipeline] = []
    request_cls = Request
    response_cls = Response
    request_timeout = 60
    request_retries = 3
    request_retry_delay = 5
    request_proxies: typing.List[typing.Union[str, URL]] = []
    request_max_redirects = 10
    request_allow_redirects = True
    response_in_stream = False
    connection_limit = 10  # see "TCPConnector" in "aiohttp"
    connection_limit_per_host = 0
    concurrent_limit = 100

    def __init__(self, loop: typing.Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session: typing.Optional[aiohttp.ClientSession] = None
        # coroutine`s concurrency support
        self._queue: Queue = Queue(loop=self.loop)
        self._done_queue: Queue = Queue(loop=self.loop)
        self._running_count = 0
        self._is_closed = False
        # report var
        self._reports: typing.DefaultDict[str, typing.List[int]] = defaultdict(
            lambda: [0, 0]
        )
        self._drop_reports: typing.DefaultDict[str, typing.List[int]] = defaultdict(
            lambda: [0, 0]
        )
        self._start_time = time.time()
        self._last_time = self._start_time
        self._report_slot = 60  # report once after one minute by default

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def is_running(self) -> bool:
        return self._running_count > 0

    async def request(
        self,
        url: typing.Union[str, URL],
        method: str = aiohttp.hdrs.METH_GET,
        params: typing.Optional[dict] = None,
        headers: typing.Optional[dict] = None,
        cookies: typing.Optional[dict] = None,
        data: typing.Optional[
            typing.Union[typing.AnyStr, typing.Dict, typing.IO]
        ] = None,
        proxy: typing.Optional[typing.Union[str, URL]] = None,
        timeout: typing.Optional[float] = None,
        retries: typing.Optional[int] = None,
        response_in_stream: typing.Optional[bool] = None,
    ) -> Response:
        if not isinstance(url, URL):
            url = URL(url)
        if proxy and not isinstance(proxy, URL):
            proxy = URL(proxy)
        elif proxy is None:
            proxy = self.get_proxy()
        if timeout is None:
            timeout = self.request_timeout
        if retries is None:
            retries = self.request_retries
        if response_in_stream is None:
            response_in_stream = self.response_in_stream

        req: Request = await self._handle_thing_with_pipelines(
            self.request_cls(
                method,
                url,
                timeout=timeout,
                params=params,
                headers=headers,
                cookies=cookies,
                data=data,
                proxy=proxy,
                response_in_stream=response_in_stream,
            ),
            self.request_pipelines,
        )
        self.report(req)

        if retries > 0:
            res = await self.make_retry_decorator(retries, self.request_retry_delay)(
                self._request
            )(req)
        else:
            res = await self._request(req)

        res = await self._handle_thing_with_pipelines(res, self.response_pipelines)
        self.report(res)
        return res

    async def collect(self, item: Item) -> None:
        self.logger.debug("Collect item: " + str(item))
        await self._handle_thing_with_pipelines(item, self.item_pipelines)
        self.report(item)

    async def open(self) -> None:
        self.logger.info("Opening")
        for pipeline in itertools.chain(
            self.item_pipelines, self.response_pipelines, self.request_pipelines
        ):
            await run_cor_func(pipeline.on_spider_open)

    async def close(self) -> None:
        await self.wait_scheduled_tasks()

        for pipeline in itertools.chain(
            self.item_pipelines, self.response_pipelines, self.request_pipelines
        ):
            await run_cor_func(pipeline.on_spider_close)

        if self.session:
            await self.session.close()

        self._is_closed = True
        self.logger.info("Closed")

    @abc.abstractmethod
    async def run(self) -> None:
        """App custom entrance"""

    async def main(self) -> None:
        try:
            await self.open()
            await self.run()
        except Exception as e:
            self.logger.exception("Run ant with " + e.__class__.__name__)
        try:
            await self.close()
        except Exception as e:
            self.logger.exception("Close ant with " + e.__class__.__name__)
        # total report
        for name, counts in self._reports.items():
            self.logger.info("Get {:d} {:s} in total".format(counts[1], name))
        for name, counts in self._drop_reports.items():
            self.logger.info("Drop {:d} {:s} in total".format(counts[1], name))
        self.logger.info(
            "Run {:s} in {:f} seconds".format(
                self.__class__.__name__, time.time() - self._start_time
            )
        )

    @staticmethod
    def make_retry_decorator(
        retries: int, delay: float
    ) -> typing.Callable[[typing.Callable], typing.Callable]:
        return retry(
            wait=wait_fixed(delay),
            retry=(
                retry_if_result(lambda res: res.status >= 500)
                | retry_if_exception_type(exception_types=aiohttp.ClientError)
            ),
            stop=stop_after_attempt(retries + 1),
        )

    def get_proxy(self) -> typing.Optional[URL]:
        """Chose a proxy, default by random"""
        try:
            return URL(random.choice(self.request_proxies))
        except IndexError:
            return None

    def schedule_task(self, coroutine: typing.Awaitable) -> None:
        """Like "asyncio.ensure_future", with concurrent count limit

        Call "self.wait_scheduled_tasks" make sure all task has been
        done.
        """

        def _done_callback(f):
            self._running_count -= 1
            self._done_queue.put_nowait(f)
            try:
                if (
                    self.concurrent_limit == -1
                    or self._running_count < self.concurrent_limit
                ):
                    next_coroutine = self._queue.get_nowait()
                    self._running_count += 1
                    asyncio.ensure_future(
                        next_coroutine, loop=self.loop
                    ).add_done_callback(_done_callback)
            except QueueEmpty:
                pass

        if self._is_closed:
            self.logger.warning("This ant has be closed!")
            return

        if self.concurrent_limit == -1 or self._running_count < self.concurrent_limit:
            self._running_count += 1
            asyncio.ensure_future(coroutine, loop=self.loop).add_done_callback(
                _done_callback
            )
        else:
            self._queue.put_nowait(coroutine)

    def schedule_tasks(self, coros: typing.Iterable[typing.Awaitable]) -> None:
        """A short way to schedule many tasks.
        """
        for coro in coros:
            self.schedule_task(coro)

    async def wait_scheduled_tasks(self):
        """Wait scheduled tasks to be done"""
        while self._running_count > 0 or self._done_queue.qsize() > 0:
            await self._done_queue.get()

    def as_completed(
        self,
        coros: typing.Iterable[typing.Awaitable],
        limit: typing.Optional[int] = None,
    ) -> typing.Generator[typing.Awaitable, None, None]:
        """Like "asyncio.as_completed",
        run and iter coros out of pool.

        :param limit: set to "self.concurrent_limit" by default,
        this "limit" is not shared with pool`s limit
        """
        limit = self.concurrent_limit if limit is None else limit

        coros = iter(coros)
        queue: Queue = Queue(loop=self.loop)
        todo: typing.List[asyncio.Future] = []

        def _done_callback(f):
            queue.put_nowait(f)
            todo.remove(f)
            try:
                nf = asyncio.ensure_future(next(coros))
                nf.add_done_callback(_done_callback)
                todo.append(nf)
            except StopIteration:
                pass

        async def _wait_for_one():
            return (await queue.get()).result()

        if limit <= 0:
            fs = {asyncio.ensure_future(cor, loop=self.loop) for cor in coros}
        else:
            fs = {
                asyncio.ensure_future(cor, loop=self.loop)
                for cor in islice(coros, 0, limit)
            }
        for f in fs:
            f.add_done_callback(_done_callback)
            todo.append(f)

        while len(todo) > 0 or queue.qsize() > 0:
            yield _wait_for_one()

    async def as_completed_with_async(
        self,
        coros: typing.Iterable[typing.Awaitable],
        limit: typing.Optional[int] = None,
        raise_exception: bool = True,
    ) -> typing.AsyncGenerator[typing.Any, None]:
        """as_completed`s async version, can catch and log exception inside.
        """
        for coro in self.as_completed(coros, limit=limit):
            try:
                yield await coro
            except Exception as e:
                if raise_exception:
                    raise e
                else:
                    self.logger.exception(
                        "Get exception {:s} in "
                        '"as_completed_with_async"'.format(str(e))
                    )

    def report(self, thing: typing.Any, dropped: bool = False) -> None:
        now_time = time.time()
        if now_time - self._last_time > self._report_slot:
            self._last_time = now_time
            for name, counts in self._reports.items():
                count = counts[1] - counts[0]
                counts[0] = counts[1]
                self.logger.info(
                    "Get {:d} {:s} in total with {:d}/{:d}s rate".format(
                        counts[1], name, count, self._report_slot
                    )
                )
            for name, counts in self._drop_reports.items():
                count = counts[1] - counts[0]
                counts[0] = counts[1]
                self.logger.info(
                    "Drop {:d} {:s} in total with {:d}/{:d} rate".format(
                        counts[1], name, count, self._report_slot
                    )
                )
        report_type = thing.__class__.__name__
        if dropped:
            reports = self._drop_reports
        else:
            reports = self._reports
        counts = reports[report_type]
        counts[1] += 1

    async def _handle_thing_with_pipelines(
        self, thing: typing.Any, pipelines: typing.List[Pipeline]
    ) -> typing.Any:
        """Process thing one by one, break the process chain when get
        exception.
        """
        self.logger.debug("Process thing: " + str(thing))
        raw_thing = thing
        for pipeline in pipelines:
            try:
                thing = await run_cor_func(pipeline.process, thing)
            except Exception as e:
                if isinstance(e, ThingDropped):
                    self.report(raw_thing, dropped=True)
                raise e
        return thing

    async def _request(self, req: Request) -> Response:
        if self.session is None:
            self.session = ClientSession(
                response_class=self.response_cls,
                connector=aiohttp.TCPConnector(
                    limit=self.connection_limit,
                    enable_cleanup_closed=True,
                    limit_per_host=self.connection_limit_per_host,
                ),
            )

        if req.proxy is not None:
            # proxy auth not work in one session with many requests,
            # add auth header to fix it
            auth = aiohttp.BasicAuth.from_url(req.proxy)
            if req.proxy.scheme == "http" and auth is not None:
                req.headers[aiohttp.hdrs.PROXY_AUTHORIZATION] = auth.encode()

        # cookies in headers, params in url
        response: typing.Any = await self.session._request(
            req.method,
            req.url,
            headers=req.headers,
            data=req.data,
            timeout=req.timeout,
            proxy=req.proxy,
            max_redirects=self.request_max_redirects,
            allow_redirects=self.request_allow_redirects,
        )

        if not req.response_in_stream:
            await response.read()
            response.close()
            await response.wait_for_close()
        return response


class CliAnt(Ant):
    """As a http client"""

    async def run(self):
        pass
