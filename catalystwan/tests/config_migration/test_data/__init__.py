# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List

from .device_template import create_device_template
from .feature_templates.dhcp import dhcp_server
from .feature_templates.interface import interface_ethernet, interface_gre, interface_ipsec, interface_multilink
from .feature_templates.ospfv3 import ospfv3
from .feature_templates.vpn import vpn_management, vpn_service, vpn_transport
from .localized_policies.localized_policy import create_localized_policy_info
from .policy_definitions.qos_map import create_qos_map_policy

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
    "create_qos_map_policy",
    "create_localized_policy_info",
    "create_device_template",
]


def __dir__() -> "List[str]":
    return list(__all__)
