from __future__ import annotations

from contextlib import AbstractContextManager
from threading import Semaphore


class RequestLimiter(AbstractContextManager):
    def __init__(self, max_requests: int = 49):
        self._max_requests: int = max_requests
        self._semaphore: Semaphore = Semaphore(value=self._max_requests)

    def __enter__(self) -> RequestLimiter:
        self._semaphore.acquire()
        return self

    def __exit__(self, *exc_info) -> None:
        self._semaphore.release()
        return
