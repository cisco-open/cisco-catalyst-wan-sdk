from threading import Semaphore
from typing import Callable

from catalystwan.response import ManagerResponse


class RequestLimiter:
    def __init__(self, max_requests: int = 60):
        self.max_requests: int = max_requests
        self._semaphore = Semaphore(value=self.max_requests)

    def send_request(self, delayed_request: Callable[[], ManagerResponse]) -> ManagerResponse:
        with self._semaphore:
            result = delayed_request()
            return result
