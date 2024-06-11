# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from .dns import DnsParcel, TargetVpns

AnyDnsSecurityParcel = DnsParcel

__all__ = ("AnyDnsSecurityParcel", "DnsParcel", "TargetVpns")


def __dir__() -> "List[str]":
    return list(__all__)
