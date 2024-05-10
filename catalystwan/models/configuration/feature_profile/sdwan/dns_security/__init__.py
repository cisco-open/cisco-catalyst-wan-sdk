# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from .dns import DnsParcel

AnyDnsSecurityParcel = DnsParcel

__all__ = ("AnyDnsSecurityParcel", "DnsParcel")


def __dir__() -> "List[str]":
    return list(__all__)
