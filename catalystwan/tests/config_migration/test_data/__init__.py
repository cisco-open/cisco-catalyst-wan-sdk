# Copyright 2023 Cisco Systems, Inc. and its affiliates
from typing import List

from .feature_templates.dhcp import dhcp_server
from .feature_templates.interface import interface_ethernet, interface_gre, interface_ipsec, interface_multilink
from .feature_templates.ospfv3 import ospfv3
from .feature_templates.vpn import vpn_management, vpn_service, vpn_transport

__all__ = [
    "interface_ethernet",
    "interface_gre",
    "interface_ipsec",
    "vpn_transport",
    "vpn_management",
    "vpn_service",
    "ospfv3",
    "dhcp_server",
    "interface_multilink",
]


def __dir__() -> "List[str]":
    return list(__all__)
