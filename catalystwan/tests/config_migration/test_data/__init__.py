from typing import List

from .feature_templates.interface import interface_ethernet, interface_gre, interface_ipsec
from .feature_templates.malformed import malformed
from .feature_templates.vpn import vpn_management, vpn_service, vpn_transport

__all__ = [
    "interface_ethernet",
    "interface_gre",
    "interface_ipsec",
    "vpn_transport",
    "vpn_management",
    "vpn_service",
    "malformed",
]


def __dir__() -> "List[str]":
    return list(__all__)
