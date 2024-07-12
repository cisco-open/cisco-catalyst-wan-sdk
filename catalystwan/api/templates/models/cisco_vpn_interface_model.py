# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.models.common import Protocol, StaticNatDirection, TLOCColor

DEFAULT_STATIC_NAT64_SOURCE_VPN_ID = 0
DEFAULT_STATIC_NAT_SOURCE_VPN_ID = 0
DEFAULT_STATIC_PORT_FORWARD_SOURCE_PORT = 0
DEFAULT_STATIC_PORT_FORWARD_TRANSLATE_PORT = 0
DEFAULT_STATIC_PORT_FORWARD_SOURCE_VPN = 0
DEFAULT_ENCAPSULATION_WEIGHT = 1
DEFAULT_VRRP_PRIORITY = 100
DEFAULT_VRRP_TIMER = 1000
DEFAULT_IPV6_VRRP_PRIORITY = 100
DEFAULT_IPV6_VRRP_TIMER = 1000


Direction = Literal["in", "out"]
NatChoice = Literal["Interface", "Pool", "Loopback"]
CoreRegion = Literal["core", "core-shared"]
SecondaryRegion = Literal["off", "secondary-only", "secondary-shared"]
Encap = Literal["gre", "ipsec"]
Mode = Literal["hub", "spoke"]
Carrier = Literal[
    "default", "carrier1", "carrier2", "carrier3", "carrier4", "carrier5", "carrier6", "carrier7", "carrier8"
]
MediaType = Literal["auto-select", "rj45", "sfp"]
Speed = Literal["10", "100", "1000", "2500", "10000"]
Duplex = Literal["full", "half", "auto"]
TrackAction = Literal["Decrement", "Shutdown"]


class SecondaryIPv4Address(FeatureTemplateValidator):
    address: Optional[ipaddress.IPv4Interface] = Field(
        default=None, description="IPv4 address with CIDR notation for the secondary interface."
    )


class SecondaryIPv6Address(FeatureTemplateValidator):
    address: Optional[ipaddress.IPv6Interface] = Field(
        default=None, description="IPv6 address with CIDR notation for the secondary interface."
    )


class AccessList(FeatureTemplateValidator):
    direction: Direction = Field(..., description="Direction of the traffic flow for applying the ACL ('in' or 'out').")
    acl_name: str = Field(
        ..., json_schema_extra={"vmanage_key": "acl-name"}, description="Name of the access control list."
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class DhcpHelperV6(FeatureTemplateValidator):
    address: ipaddress.IPv6Address = Field(..., description="IPv6 address of the DHCP server or relay.")
    vpn: Optional[int] = Field(default=None, description="Optional VPN ID where the DHCP helper is configured.")


class StaticNat66(FeatureTemplateValidator):
    source_prefix: ipaddress.IPv6Interface = Field(
        ...,
        json_schema_extra={"vmanage_key": "source-prefix"},
        description="IPv6 network prefix that is to be translated.",
    )
    translated_source_prefix: str = Field(
        ...,
        json_schema_extra={"vmanage_key": "translated-source-prefix"},
        description="IPv6 network prefix to which the source prefix is translated.",
    )
    source_vpn_id: int = Field(
        default=DEFAULT_STATIC_NAT64_SOURCE_VPN_ID,
        json_schema_extra={"vmanage_key": "source-vpn-id"},
        description="VPN ID associated with the source network prefix.",
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class Static(FeatureTemplateValidator):
    source_ip: ipaddress.IPv4Address = Field(
        ..., json_schema_extra={"vmanage_key": "source-ip"}, description="IPv4 address of the source IP for static NAT."
    )
    translate_ip: ipaddress.IPv4Address = Field(
        ...,
        json_schema_extra={"vmanage_key": "translate-ip"},
        description="IPv4 address used for translation in static NAT.",
    )
    static_nat_direction: StaticNatDirection = Field(
        default="inside",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
        description="Direction of static NAT mapping ('inside' or 'outside').",
    )
    source_vpn: int = Field(
        default=DEFAULT_STATIC_NAT_SOURCE_VPN_ID,
        json_schema_extra={"vmanage_key": "source-vpn"},
        description="VPN ID associated with the source IP for static NAT.",
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class StaticPortForward(FeatureTemplateValidator):
    source_ip: ipaddress.IPv4Address = Field(
        ...,
        json_schema_extra={"vmanage_key": "source-ip"},
        description="IPv4 address of the source IP for port forwarding.",
    )
    translate_ip: ipaddress.IPv4Address = Field(
        ...,
        json_schema_extra={"vmanage_key": "translate-ip"},
        description="IPv4 address used for translation in port forwarding.",
    )
    static_nat_direction: StaticNatDirection = Field(
        default="inside",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
        description="Direction of port forwarding mapping ('inside' or 'outside').",
    )
    source_port: int = Field(
        default=DEFAULT_STATIC_PORT_FORWARD_SOURCE_PORT,
        json_schema_extra={"vmanage_key": "source-port"},
        description="Source port number for port forwarding.",
    )
    translate_port: int = Field(
        default=DEFAULT_STATIC_PORT_FORWARD_TRANSLATE_PORT,
        json_schema_extra={"vmanage_key": "translate-port"},
        description="Translated port number for port forwarding.",
    )
    proto: Protocol = Field(..., description="Protocol used for port forwarding (TCP/UDP).")
    source_vpn: int = Field(
        default=DEFAULT_STATIC_PORT_FORWARD_SOURCE_VPN,
        json_schema_extra={"vmanage_key": "source-vpn"},
        description="VPN ID associated with the source IP for port forwarding.",
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class Encapsulation(FeatureTemplateValidator):
    encap: Encap = Field(..., description="Type of encapsulation used for the VPN tunnel (GRE/IPsec).")
    preference: Optional[int] = Field(
        default=None, description="Preference value for the encapsulation type (lower values have higher priority)."
    )
    weight: int = Field(
        default=DEFAULT_ENCAPSULATION_WEIGHT,
        description="Weight for the encapsulation type used in load balancing decisions.",
    )


class Ip(FeatureTemplateValidator):
    addr: ipaddress.IPv4Address = Field(..., description="IPv4 address for the interface.")
    mac: str = Field(..., description="MAC address associated with the IPv4 address.")


class Ipv4Secondary(FeatureTemplateValidator):
    address: ipaddress.IPv4Address = Field(..., description="IPv4 address for the secondary interface.")


class TrackingObject(FeatureTemplateValidator):
    name: int = Field(..., description="Unique identifier for the tracking object.")
    track_action: TrackAction = Field(
        default="Decrement",
        json_schema_extra={"vmanage_key": "track-action"},
        description="Action to take when the tracked object state changes (e.g., decrement priority or shutdown).",
    )
    decrement: int = Field(
        ..., description="Value by which to decrement the VRRP priority when the tracked object is down."
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class Vrrp(FeatureTemplateValidator):
    grp_id: int = Field(..., json_schema_extra={"vmanage_key": "grp-id"}, description="VRRP group ID.")
    priority: int = Field(
        default=DEFAULT_VRRP_PRIORITY, description="Priority value for the VRRP group (higher values take precedence)."
    )
    timer: int = Field(default=DEFAULT_VRRP_TIMER, description="VRRP advertisement interval timer in milliseconds.")
    track_omp: BoolStr = Field(
        default=False,
        json_schema_extra={"vmanage_key": "track-omp"},
        description="Flag to track Overlay Management Protocol (OMP) session state.",
    )
    track_prefix_list: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "track-prefix-list"},
        description="Name of the prefix-list used for tracking specific routes.",
    )
    address: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"data_path": ["ipv4"], "vmanage_key": "address"},
        description="Virtual IP address used by the VRRP group.",
    )
    ipv4_secondary: Optional[List[Ipv4Secondary]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "ipv4-secondary"},
        description="List of secondary IPv4 addresses for the VRRP group.",
    )
    tloc_change_pref: BoolStr = Field(
        default=False,
        json_schema_extra={"vmanage_key": "tloc-change-pref"},
        description="Flag to change preference based on TLOC status.",
    )
    value: int = Field(..., description="VRRP value to determine the primary node for the VRRP group.")
    tracking_object: Optional[List[TrackingObject]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tracking-object"},
        description="List of tracking objects associated with the VRRP configuration.",
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)


class Ipv6(FeatureTemplateValidator):
    ipv6_link_local: ipaddress.IPv6Address = Field(
        ...,
        json_schema_extra={"vmanage_key": "ipv6-link-local"},
        description="IPv6 link-local address for the interface.",
    )
    prefix: Optional[ipaddress.IPv6Interface] = Field(
        default=None, description="Optional IPv6 prefix for the interface, with CIDR notation."
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Vrrp(FeatureTemplateValidator):
    grp_id: int = Field(..., json_schema_extra={"vmanage_key": "grp-id"}, description="IPv6 VRRP group ID.")
    priority: int = Field(
        default=DEFAULT_IPV6_VRRP_PRIORITY,
        description="Priority value for the IPv6 VRRP group (higher values take precedence).",
    )
    timer: int = Field(
        default=DEFAULT_IPV6_VRRP_TIMER, description="IPv6 VRRP advertisement interval timer in milliseconds."
    )
    track_omp: BoolStr = Field(
        default=False,
        json_schema_extra={"vmanage_key": "track-omp"},
        description="Flag to track Overlay Management Protocol (OMP) session state for IPv6.",
    )
    track_prefix_list: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "track-prefix-list"},
        description="Name of the IPv6 prefix-list used for tracking specific routes.",
    )
    ipv6: Optional[List[Ipv6]] = Field(
        default=None, description="List of IPv6 configurations associated with the VRRP group."
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoVpnInterfaceModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco VPN Interface Feature Template configuration"

    if_name: Optional[str] = Field(
        default=None, description="The name of the interface.", json_schema_extra={"vmanage_key": "if-name"}
    )
    interface_description: Optional[str] = Field(
        default=None, description="A description for the interface.", json_schema_extra={"vmanage_key": "description"}
    )
    poe: Optional[BoolStr] = Field(
        default=None,
        description="Power over Ethernet setting for the interface. True if enabled, False otherwise.",
    )
    ipv4_address: Optional[str] = Field(
        default=None,
        description="The primary IPv4 address assigned to the interface.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "address"},
    )
    secondary_ipv4_address: Optional[List[SecondaryIPv4Address]] = Field(
        default=None,
        description="A list of secondary IPv4 addresses assigned to the interface.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "secondary-address"},
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
        json_schema_extra={"vmanage_key": "dhcp-distance"},
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
    secondary_ipv6_address: Optional[List[SecondaryIPv6Address]] = Field(
        default=None,
        description="A list of secondary IPv6 addresses assigned to the interface.",
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "secondary-address"},
    )
    access_list_ipv4: Optional[List[AccessList]] = Field(
        default=None,
        description="A list of IPv4 access control lists (ACLs) applied to the interface.",
        json_schema_extra={"vmanage_key": "access-list"},
    )
    dhcp_helper: Optional[List[ipaddress.IPv4Address]] = Field(
        default=None,
        description="A list of DHCP helper addresses configured on the interface.",
        json_schema_extra={"vmanage_key": "dhcp-helper"},
    )
    dhcp_helper_v6: Optional[List[DhcpHelperV6]] = Field(
        default=None,
        description="A list of DHCPv6 helper configurations applied to the interface.",
        json_schema_extra={"vmanage_key": "dhcp-helper-v6"},
    )
    tracker: Optional[List[str]] = Field(
        default=None,
        description="A list of tracker identifiers associated with the interface.",
    )
    auto_bandwidth_detect: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Whether automatic bandwidth detection is enabled on the interface. True if enabled, False otherwise."
        ),
        json_schema_extra={"vmanage_key": "auto-bandwidth-detect"},
    )
    iperf_server: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        description="The IP address of the iPerf server used for performance testing from this interface.",
        json_schema_extra={"vmanage_key": "iperf-server"},
    )
    nat: Optional[BoolStr] = Field(
        default=None,
        description="Indicates whether Network Address Translation (NAT) is enabled on the interface.",
    )
    nat_choice: Optional[NatChoice] = Field(
        default=None,
        description="The type of NAT configured on the interface, if applicable.",
        json_schema_extra={"vmanage_key": "nat-choice"},
    )
    udp_timeout: Optional[int] = Field(
        default=None,
        description="The timeout value in seconds for UDP connections through the NAT on this interface.",
        json_schema_extra={"vmanage_key": "udp-timeout"},
    )
    tcp_timeout: Optional[int] = Field(
        default=None,
        description="The timeout value in seconds for TCP connections through the NAT on this interface.",
        json_schema_extra={"vmanage_key": "tcp-timeout"},
    )
    nat_range_start: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        description="The starting IP address in the range used for NAT on this interface.",
        json_schema_extra={"vmanage_key": "range-start"},
    )
    nat_range_end: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        description="The ending IP address in the range used for NAT on this interface.",
        json_schema_extra={"vmanage_key": "range-end"},
    )
    overload: Optional[BoolStr] = Field(
        default=None,
        description="Indicates if NAT overload (PAT - Port Address Translation) is enabled.",
    )
    loopback_interface: Optional[str] = Field(
        default=None,
        description="The associated loopback interface, if any, for the VPN interface.",
        json_schema_extra={"vmanage_key": "loopback-interface"},
    )
    prefix_length: Optional[int] = Field(
        default=None,
        description="The prefix length for the interface's IP address, indicating the size of the subnet.",
        json_schema_extra={"vmanage_key": "prefix-length"},
    )
    enable: Optional[BoolStr] = Field(
        default=None,
        description="Indicates whether the interface is enabled or disabled.",
    )
    nat64: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Indicates whether NAT64 is enabled on the interface, "
            "allowing IPv6 addresses to communicate with IPv4 services."
        ),
    )
    nat66: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Indicates whether NAT66 is enabled on the interface, translating IPv6 addresses into IPv6 addresses."
        ),
    )
    static_nat66: Optional[List[StaticNat66]] = Field(
        default=None,
        description="List of static NAT66 entries for translating IPv6 addresses into other IPv6 addresses.",
        json_schema_extra={"vmanage_key": "static-nat66"},
    )

    static: Optional[List[Static]] = Field(
        default=None,
        description="List of static NAT entries for configuring one-to-one address mappings.",
        json_schema_extra={"data_path": ["nat"], "vmanage_key": "static"},
    )
    static_port_forward: Optional[List[StaticPortForward]] = Field(
        default=None,
        description="List of static port forwarding entries for the interface.",
        json_schema_extra={"vmanage_key": "static-port-forward"},
    )
    enable_core_region: Optional[BoolStr] = Field(
        default=None,
        description="Indicates if the interface is part of the core network region for centralized services.",
        json_schema_extra={"vmanage_key": "enable-core-region"},
    )
    core_region: Optional[CoreRegion] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "core-region"},
        description="Configuration details for the core region.",
    )
    secondary_region: Optional[SecondaryRegion] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "secondary-region"},
        description="Configuration details for a secondary region.",
    )
    tloc_encapsulation: Optional[List[Encapsulation]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "encapsulation", "data_path": ["tunnel-interface"]},
        description="Transport Location (TLOC) encapsulation settings.",
    )
    border: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface"]},
        description="Defines if the interface is at the border of a network segment.",
    )
    per_tunnel_qos: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "per-tunnel-qos"},
        description="Enable or disable per-tunnel Quality of Service (QoS).",
    )
    per_tunnel_qos_aggregator: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "per-tunnel-qos-aggregator"},
        description="Enable or disable per-tunnel QoS aggregator.",
    )
    mode: Optional[Mode] = Field(default=None, description="Defines the operating mode for the interface.")
    tunnels_bandwidth: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tunnels-bandwidth"},
        description="Specifies the total bandwidth available across all tunnels.",
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
    max_control_connections: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "max-control-connections", "data_path": ["tunnel-interface"]},
        description="Maximum number of control connections that can be established on the interface.",
    )
    control_connections: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "control-connections", "data_path": ["tunnel-interface"]},
        description="Enables or disables control connections on the interface.",
    )
    vbond_as_stun_server: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "vbond-as-stun-server", "data_path": ["tunnel-interface"]},
        description="Configures the vBond orchestrator to act as a STUN server for the interface.",
    )
    exclude_controller_group_list: Optional[List[int]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "exclude-controller-group-list", "data_path": ["tunnel-interface"]},
        description="List of controller groups to exclude from connections.",
    )
    vmanage_connection_preference: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "vmanage-connection-preference", "data_path": ["tunnel-interface"]},
        description="Preference value for establishing vManage connections.",
    )
    port_hop: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "port-hop", "data_path": ["tunnel-interface"]},
        description="Enables or disables port hopping for the interface to evade port blocking.",
    )
    restrict: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "color"]},
        description="Indicates whether the interface color is restricted for use.",
    )
    dst_ip: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "dst-ip", "data_path": ["tunnel-interface", "tloc-extension-gre-to"]},
        description="Destination IP address for GRE (Generic Routing Encapsulation) tunnel extension.",
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
    bind: Optional[str] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface"]},
        description="Interface or IP address to which the tunnel interface is bound.",
    )
    last_resort_circuit: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "last-resort-circuit", "data_path": ["tunnel-interface"]},
        description="Marks the interface as a last resort circuit for traffic to fall back to.",
    )
    low_bandwidth_link: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "low-bandwidth-link", "data_path": ["tunnel-interface"]},
        description="Indicates if the link is considered a low bandwidth link.",
    )
    tunnel_tcp_mss_adjust: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tunnel-tcp-mss-adjust", "data_path": ["tunnel-interface"]},
        description="Adjusts the Maximum Segment Size (MSS) value for TCP connections over the tunnel.",
    )
    clear_dont_fragment: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "clear-dont-fragment", "data_path": ["tunnel-interface"]},
        description="Enables or disables the clearing of the 'Don't Fragment' (DF) bit in the IP header.",
    )
    propagate_sgt: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface"], "vmanage_key": "propagate-sgt"},
        description="Enables or disables the propagation of Security Group Tags (SGTs) across the tunnel interface.",
    )
    network_broadcast: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "network-broadcast", "data_path": ["tunnel-interface"]},
        description="Allows or disallows network broadcast traffic through the tunnel interface.",
    )
    all: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Permits or denies all services through the tunnel interface.",
    )
    bgp: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Allows or disallows Border Gateway Protocol (BGP) traffic through the tunnel interface.",
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
    ospf: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description=(
            "Permits or denies Open Shortest Path First (OSPF) routing protocol traffic through the tunnel interface."
        ),
    )
    stun: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Enables or disables Session Traversal Utilities for NAT (STUN) on the tunnel interface.",
    )
    snmp: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Allows or disallows Simple Network Management Protocol (SNMP) through the tunnel interface.",
    )
    https: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["tunnel-interface", "allow-service"]},
        description="Permits or denies HTTPS traffic through the tunnel interface.",
    )
    media_type: Optional[MediaType] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "media-type"},
        description="Specifies the media type used by the interface, such as copper or fiber.",
    )
    intrf_mtu: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "intrf-mtu"},
        description="Sets the Maximum Transmission Unit (MTU) size for the interface.",
    )
    mtu: Optional[int] = Field(default=None, description="Specifies the MTU size for the tunnel or logical interface.")
    tcp_mss_adjust: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tcp-mss-adjust"},
        description="Adjusts the TCP Maximum Segment Size (MSS) value for connections over the interface.",
    )
    tloc_extension: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tloc-extension"},
        description="Defines the Transport Location (TLOC) extension for the interface.",
    )
    load_interval: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "load-interval"},
        description="Sets the time interval in seconds for calculating interface load statistics.",
    )
    src_ip: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "src-ip", "data_path": ["tloc-extension-gre-from"]},
        description="Source IP address for GRE tunnel extension.",
    )
    xconnect: Optional[str] = Field(
        default=None,
        json_schema_extra={"data_path": ["tloc-extension-gre-from"]},
        description="Cross-connect identifier for the GRE tunnel extension.",
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
    arp_timeout: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "arp-timeout"},
        description="Time in seconds before an ARP cache entry is timed out.",
    )
    autonegotiate: Optional[BoolStr] = Field(
        default=None, description="Enables or disables autonegotiation of speed and duplex settings on the interface."
    )
    ip_directed_broadcast: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "ip-directed-broadcast"},
        description="Allows or disallows IP directed broadcasts on the interface.",
    )
    icmp_redirect_disable: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "icmp-redirect-disable"},
        description="Enables or disables ICMP redirect messages on the interface.",
    )
    qos_adaptive: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "qos-adaptive"},
        description="Activates or deactivates adaptive QoS on the interface.",
    )
    period: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive"]},
        description="Time period in seconds for measuring and adapting QoS settings.",
    )
    bandwidth_down: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "bandwidth-down", "data_path": ["qos-adaptive", "downstream"]},
        description="Specifies the downstream bandwidth in Kbps for adaptive QoS calculations.",
    )
    dmin: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive", "downstream", "range"]},
        description="Specifies the minimum downstream bandwidth in Kbps for adaptive QoS.",
    )
    dmax: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive", "downstream", "range"]},
        description="Specifies the maximum downstream bandwidth in Kbps for adaptive QoS.",
    )
    bandwidth_up: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "bandwidth-up", "data_path": ["qos-adaptive", "upstream"]},
        description="Specifies the upstream bandwidth in Kbps for adaptive QoS calculations.",
    )
    umin: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive", "upstream", "range"]},
        description="Specifies the minimum upstream bandwidth in Kbps for adaptive QoS.",
    )
    umax: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["qos-adaptive", "upstream", "range"]},
        description="Specifies the maximum upstream bandwidth in Kbps for adaptive QoS.",
    )
    shaping_rate: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "shaping-rate"},
        description="Defines the traffic shaping rate for the interface.",
    )
    qos_map: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "qos-map"},
        description="Associates a QoS map with the interface for traffic classification and prioritization.",
    )
    qos_map_vpn: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "qos-map-vpn"},
        description="Associates a QoS map with a VPN for traffic classification and prioritization within the VPN.",
    )
    service_provider: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "service-provider"},
        description="Identifies the service provider associated with the interface.",
    )
    bandwidth_upstream: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "bandwidth-upstream"},
        description="Specifies the upstream bandwidth in Kbps available on the interface.",
    )
    bandwidth_downstream: Optional[int] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "bandwidth-downstream"},
        description="Specifies the downstream bandwidth in Kbps available on the interface.",
    )
    block_non_source_ip: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "block-non-source-ip"},
        description="Enables or disables blocking of traffic with non-matching source IP addresses.",
    )
    rule_name: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "rule-name", "data_path": ["rewrite-rule"]},
        description="Specifies the name of the rewrite rule applied to the interface.",
    )
    access_list_ipv6: Optional[List[AccessList]] = Field(
        default=None,
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "access-list"},
        description="Defines a list of access control entries for IPv6 traffic filtering.",
    )
    ip: Optional[List[Ip]] = Field(
        default=None,
        json_schema_extra={"data_path": ["arp"]},
        description="A list of IP configurations for Address Resolution Protocol (ARP) settings.",
    )
    vrrp: Optional[List[Vrrp]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "vrrp"},
        description="A list of Virtual Router Redundancy Protocol (VRRP) configurations for IPv4.",
    )
    ipv6_vrrp: Optional[List[Ipv6Vrrp]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "ipv6-vrrp"},
        description="A list of Virtual Router Redundancy Protocol (VRRP) configurations for IPv6.",
    )
    enable_sgt_propagation: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["trustsec", "propagate"], "vmanage_key": "sgt"},
        description="Enables or disables Security Group Tag (SGT) propagation.",
    )
    security_group_tag: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["trustsec", "static"], "vmanage_key": "sgt"},
        description="Specifies a static Security Group Tag (SGT) for the interface.",
    )
    trusted: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["trustsec", "static"]},
        description="Marks the interface as trusted or untrusted for TrustSec.",
    )
    enable_sgt_authorization_and_forwarding: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["trustsec"], "vmanage_key": "enable"},
        description="Enables or disables Security Group Tag (SGT) authorization and forwarding.",
    )
    enable_sgt_enforcement: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"data_path": ["trustsec", "enforcement"], "vmanage_key": "enable"},
        description="Activates or deactivates Security Group Tag (SGT) enforcement.",
    )
    enforcement_sgt: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["trustsec", "enforcement"], "vmanage_key": "sgt"},
        description="Specifies the Security Group Tag (SGT) to be enforced on the interface.",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn_interface"
