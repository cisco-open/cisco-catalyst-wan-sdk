from ipaddress import IPv4Address, IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.models.common import CarrierType, EthernetDuplexMode, MediaType, Speed, TLOCColor, TunnelMode
from catalystwan.models.configuration.feature_profile.common import (
    AclQos,
    AllowService,
    Arp,
    Encapsulation,
    EthernetNatAttributesIpv4,
    InterfaceDynamicIPv4Address,
    InterfaceDynamicIPv6Address,
    InterfaceStaticIPv4Address,
    MultiRegionFabric,
    StaticIPv6Address,
)


class Static(BaseModel):
    primary_ip_v6_address: Optional[StaticIPv6Address] = Field(
        default=None,
        validation_alias="primaryIpV6Address",
        serialization_alias="primaryIpV6Address",
        description="Static IpV6Address Primary",
    )
    secondary_ip_v6_address: Optional[List[StaticIPv6Address]] = Field(
        default=None,
        validation_alias="secondaryIpV6Address",
        serialization_alias="secondaryIpV6Address",
        description="Static secondary IPv6 addresses",
    )


class InterfaceStaticIPv6Address(BaseModel):
    static: Static = Field()


class Tunnel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    bandwidth_percent: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="bandwidthPercent", serialization_alias="bandwidthPercent"
    )
    bind: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    border: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    carrier: Optional[Union[Variable, Default[Literal["default"]], Global[CarrierType]]] = Field(default=None)
    clear_dont_fragment: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="clearDontFragment", serialization_alias="clearDontFragment"
    )
    color: Optional[Union[Global[TLOCColor], Default[Literal["mpls"]], Variable]] = Field(default=None)
    cts_sgt_propagation: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="ctsSgtPropagation", serialization_alias="ctsSgtPropagation"
    )
    exclude_controller_group_list: Optional[Union[Variable, Default[None], Global[List[int]]]] = Field(
        default=None, validation_alias="excludeControllerGroupList", serialization_alias="excludeControllerGroupList"
    )
    group: Optional[Union[Variable, Global[int], Default[None]]] = Field(default=None)
    hello_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="helloInterval", serialization_alias="helloInterval"
    )
    hello_tolerance: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="helloTolerance", serialization_alias="helloTolerance"
    )
    last_resort_circuit: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="lastResortCircuit", serialization_alias="lastResortCircuit"
    )
    low_bandwidth_link: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="lowBandwidthLink", serialization_alias="lowBandwidthLink"
    )
    max_control_connections: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="maxControlConnections", serialization_alias="maxControlConnections"
    )
    mode: Optional[Union[Variable, Global[TunnelMode]]] = Field(default=None)
    nat_refresh_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="natRefreshInterval", serialization_alias="natRefreshInterval"
    )
    network_broadcast: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="networkBroadcast", serialization_alias="networkBroadcast"
    )
    per_tunnel_qos: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="perTunnelQos", serialization_alias="perTunnelQos"
    )
    port_hop: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="portHop", serialization_alias="portHop"
    )
    restrict: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    tloc_extension_gre_to: Optional[Union[Variable, Global[str], Global[IPv4Address], Default[None]]] = Field(
        default=None, validation_alias="tlocExtensionGreTo", serialization_alias="tlocExtensionGreTo"
    )
    tunnel_tcp_mss: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="tunnelTcpMss", serialization_alias="tunnelTcpMss"
    )
    v_bond_as_stun_server: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="vBondAsStunServer", serialization_alias="vBondAsStunServer"
    )
    v_manage_connection_preference: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="vManageConnectionPreference", serialization_alias="vManageConnectionPreference"
    )


NatType = Literal[
    "interface",
    "loopback",
    "pool",
]


StaticNatDirection = Literal[
    "inside",
    "outside",
]


class StaticNat66(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    source_prefix: Union[Variable, Global[str], Global[IPv6Interface]] = Field(
        validation_alias="sourcePrefix", serialization_alias="sourcePrefix"
    )
    source_vpn_id: Union[Variable, Global[int], Default[None]] = Field(
        validation_alias="sourceVpnId", serialization_alias="sourceVpnId"
    )
    egress_interface: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="egressInterface", serialization_alias="egressInterface"
    )
    translated_source_prefix: Optional[Union[Variable, Global[str], Default[None], Global[IPv6Interface]]] = Field(
        default=None, validation_alias="translatedSourcePrefix", serialization_alias="translatedSourcePrefix"
    )


class NatAttributesIpv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    nat64: Optional[Union[Global[bool], Default[bool]]] = Field(default=None)
    nat66: Optional[Union[Global[bool], Default[bool]]] = Field(default=None)
    static_nat66: Optional[List[StaticNat66]] = Field(
        default=None, validation_alias="staticNat66", serialization_alias="staticNat66", description="static NAT66"
    )


class TlocExtensionGreFrom(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    source_ip: Optional[Union[Variable, Global[str], Global[IPv4Address], Default[None]]] = Field(
        default=None, validation_alias="sourceIp", serialization_alias="sourceIp"
    )
    xconnect: Optional[Union[Variable, Global[str], Global[IPv4Address], Default[None]]] = Field(default=None)


class Advanced(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    arp_timeout: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="arpTimeout", serialization_alias="arpTimeout"
    )
    autonegotiate: Optional[Union[Variable, Global[bool], Default[None]]] = Field(default=None)
    duplex: Optional[Union[Variable, Default[None], Global[EthernetDuplexMode]]] = Field(default=None)
    icmp_redirect_disable: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="icmpRedirectDisable", serialization_alias="icmpRedirectDisable"
    )
    intrf_mtu: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="intrfMtu", serialization_alias="intrfMtu"
    )
    ip_directed_broadcast: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="ipDirectedBroadcast", serialization_alias="ipDirectedBroadcast"
    )
    ip_mtu: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="ipMtu", serialization_alias="ipMtu"
    )
    load_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="loadInterval", serialization_alias="loadInterval"
    )
    mac_address: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias="macAddress", serialization_alias="macAddress"
    )
    media_type: Optional[Union[Variable, Global[MediaType], Default[None]]] = Field(
        default=None, validation_alias="mediaType", serialization_alias="mediaType"
    )
    speed: Optional[Union[Variable, Global[Speed], Default[None]]] = Field(default=None)
    tcp_mss: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="tcpMss", serialization_alias="tcpMss"
    )
    tloc_extension: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias="tlocExtension", serialization_alias="tlocExtension"
    )
    tloc_extension_gre_from: Optional[TlocExtensionGreFrom] = Field(
        default=None,
        validation_alias="tlocExtensionGreFrom",
        serialization_alias="tlocExtensionGreFrom",
        description="Extend remote TLOC over a GRE tunnel to a local WAN interface",
    )
    tracker: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)


class InterfaceEthernetParcel(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    type_: Literal["wan/vpn/interface/ethernet"] = Field(default="wan/vpn/interface/ethernet", exclude=True)
    encapsulation: List[Encapsulation] = Field(
        validation_alias=AliasPath("data", "encapsulation"), description="Encapsulation for TLOC"
    )
    interface_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "interfaceName"))
    interface_ip_address: Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address] = Field(
        validation_alias=AliasPath("data", "intfIpAddress"), default_factory=InterfaceStaticIPv4Address
    )
    interface_description: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "description")
    )
    nat: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "nat")
    )
    shutdown: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(True), validation_alias=AliasPath("data", "shutdown")
    )
    tunnel_interface: Union[Global[bool], Default[bool]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "tunnelInterface")
    )
    acl_qos: Optional[AclQos] = Field(default=None, validation_alias=AliasPath("data", "aclQos"), description="ACL/QOS")
    advanced: Optional[Advanced] = Field(
        default=None, validation_alias=AliasPath("data", "advanced"), description="Advanced Attributes"
    )
    allow_service: Optional[AllowService] = Field(
        default=None, validation_alias=AliasPath("data", "allowService"), description="Tunnel Interface Attributes"
    )
    arp: Optional[List[Arp]] = Field(
        default=None, validation_alias=AliasPath("data", "arp"), description="Configure ARP entries"
    )
    auto_detect_bandwidth: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "autoDetectBandwidth")
    )
    bandwidth_downstream: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthDownstream")
    )
    bandwidth_upstream: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthUpstream")
    )
    block_non_source_ip: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "blockNonSourceIp")
    )
    dhcp_helper: Optional[Union[Variable, Default[None], Global[List[str]]]] = Field(
        default=None, validation_alias=AliasPath("data", "dhcpHelper")
    )
    intf_ip_v6_address: Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]] = Field(
        default=None, validation_alias=AliasPath("data", "intfIpV6Address")
    )
    iperf_server: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "iperfServer")
    )
    multi_region_fabric: Optional[MultiRegionFabric] = Field(
        default=None, validation_alias=AliasPath("data", "multiRegionFabric"), description="Multi-Region Fabric"
    )
    nat_attributes_ipv4: Optional[EthernetNatAttributesIpv4] = Field(
        default=None, validation_alias=AliasPath("data", "natAttributesIpv4"), description="NAT Attributes IpV4"
    )
    nat_attributes_ipv6: Optional[NatAttributesIpv6] = Field(
        default=None, validation_alias=AliasPath("data", "natAttributesIpv6"), description="NAT Attributes Ipv6"
    )
    nat_ipv6: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "natIpv6")
    )
    service_provider: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "serviceProvider")
    )
    tunnel: Optional[Tunnel] = Field(
        default=None, validation_alias=AliasPath("data", "tunnel"), description="Tunnel Interface Attributes"
    )
