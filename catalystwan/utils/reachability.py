# Copyright 2024 Cisco Systems, Inc. and its affiliates

from enum import Enum


class Reachability(str, Enum):
    REACHABLE = "reachable"
    UNREACHABLE = "unreachable"
    UNKNOWN = "unknown"

    @classmethod
    def _missing_(cls, value):
        # Value emitted by Manager ver. 20.10 can be None
        return cls.UNKNOWN
