# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.models.common import TLOCColor

VpnId = Literal["0", "512"]
Role = Literal["primary", "secondary"]

Speed = Literal["10", "100", "1000"]
Duplex = Literal["full", "half"]
Carrier = Literal[
    "default", "carrier1", "carrier2", "carrier3", "carrier4", "carrier5", "carrier6", "carrier7", "carrier8"
]
FlowControl = Literal["ingress", "egress", "autoneg", "both", "none"]


class Ip(FeatureTemplateValidator):
    addr: ipaddress.IPv4Address = Field(..., description="IPv4 address for the interface.")
    mac: str = Field(..., description="MAC address associated with the IPv4 address.")


class VpnVsmartInterfaceModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "vSmart VPN Interface Feature Template configuration"

    if_name: str = Field(
        default=None, description="The name of the interface.", json_schema_extra={"vmanage_key": "if-name"}
    )
    interface_description: Optional[str] = Field(
        default=None, description="A description for the interface.", json_schema_extra={"vmanage_key": "description"}
    )
    ipv4_address: Optional[str] = Field(
        default=None,
        description="The primary IPv4 address assigned to the interface.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "address"},
    )
    dhcp_ipv4_client: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Whether DHCP client is enabled on the interface for IPv4 addressing. True if enabled, False otherwise."
        ),
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "dhcp-client"},
    )
    dhcp_distance: Optional[int] = Field(
        default=None,
        description="Administrative distance for DHCP routes on the interface.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "dhcp-distance"},
    )
    ipv6_address: Optional[ipaddress.IPv6Interface] = Field(
        default=None,
        description="The primary IPv6 address assigned to the interface.",
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "address"},
    )
    dhcp_ipv6_client: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Whether DHCP client is enabled on the interface for IPv6 addressing. True if enabled, False otherwise."
        ),
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "dhcp-client"},
    )
    dhcp_ipv6_distance: Optional[int] = Field(
        default=None,
        description="Administrative distance for DHCP routes on the interface.",
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "dhcp-distance"},
    )
    dhcp_rapid_commit: Optional[BoolStr] = Field(
        default=None,
        description=("Enable DHCPv6 rapid commit"),
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "dhcp-rapid-commit"},
    )
    group: Optional[List[int]] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface"]},
        description="Identifies the group or groups the interface belongs to.",
    )
    value: Optional[TLOCColor] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "color"]},
        description=(
            "The value field often corresponds to a specific attribute or setting, such as color in this context."
        ),
    )
    carrier: Optional[Carrier] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface"]},
        description="Specifies the carrier information for the tunnel interface.",
    )
    nat_refresh_interval: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "nat-refresh-interval", "data_path": ["tunnel-interface"]},
        description="Interval in seconds to refresh NAT (Network Address Translation) mappings.",
    )
    hello_interval: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "hello-interval", "data_path": ["tunnel-interface"]},
        description="Time interval in seconds between successive hello packets sent over the tunnel interface.",
    )
    hello_tolerance: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "hello-tolerance", "data_path": ["tunnel-interface"]},
        description="Time in seconds to wait before declaring a neighbor down due to missing hello packets.",
    )
    all: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Permits or denies all services through the tunnel interface.",
    )
    dhcp: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Enables or disables Dynamic Host Configuration Protocol (DHCP) on the tunnel interface.",
    )
    dns: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Allows or disallows Domain Name System (DNS) queries through the tunnel interface.",
    )
    icmp: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description=(
            "Enables or disables Internet Control Message Protocol (ICMP) "
            "for ping and traceroute through the tunnel interface."
        ),
    )
    sshd: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Allows or disallows Secure Shell (SSH) daemon access through the tunnel interface.",
    )
    netconf: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Enables or disables NETCONF protocol support on the tunnel interface.",
    )
    ntp: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Allows or disallows Network Time Protocol (NTP) synchronization through the tunnel interface.",
    )
    stun: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Enables or disables Session Traversal Utilities for NAT (STUN) on the tunnel interface.",
    )
    flow_control: Optional[FlowControl] = Field(default=None, description="Enable flow control.")
    clear_dont_fragment: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "clear-dont-fragment"},
        description="Enables Clear don't fragment bit",
    )
    autonegotiate: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "autonegotiate"},
        description="Link autonegotiation",
    )
    pmtu: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "pmtu"},
        description="Enables Path MTU Discovery",
    )
    mtu: Optional[int] = Field(
        default=1500,
        json_schema_extra={"vmanage_key": "mtu"},
        description="Interface MTU <576..2000>",
    )
    tcp_mss_adjust: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tcp-mss-adjust"},
        description="TCP MSS on SYN packets, in bytes",
    )
    mac_address: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "mac-address"},
        description="Specifies the MAC address for the interface.",
    )
    speed: Optional[Speed] = Field(
        default=None, description="Defines the speed of the interface, such as 10Mbps, 100Mbps, or 1Gbps."
    )
    duplex: Optional[Duplex] = Field(
        default=None, description="Sets the duplex mode for the interface, such as full or half duplex."
    )
    shutdown: Optional[BoolStr] = Field(default=False, description="Enables or disables (shuts down) the interface.")
    ip: Optional[List[Ip]] = Field(
        default=None,
        json_schema_extra={"data_path": ["arp"]},
        description="A list of IP configurations for Address Resolution Protocol (ARP) settings.",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "vpn-vsmart-interface"
