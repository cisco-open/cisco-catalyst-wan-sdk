from dataclasses import dataclass
from typing import Callable

from catalystwan.models.configuration.config_migration import PushContext, UX2Config, UX2ConfigPushResult
from catalystwan.session import ManagerSession


@dataclass
class PusherConfig:
    ux2_config: UX2Config
    session: ManagerSession
    push_result: UX2ConfigPushResult
    push_context: PushContext
    progress: Callable[[str, int, int], None]


class Pusher:
    def load_config(self, config: PusherConfig) -> None:
        self._ux2_config = config.ux2_config
        self._session = config.session
        self._push_result = config.push_result
        self._push_context = config.push_context
        self._progress: Callable[[str, int, int], None] = config.progress
