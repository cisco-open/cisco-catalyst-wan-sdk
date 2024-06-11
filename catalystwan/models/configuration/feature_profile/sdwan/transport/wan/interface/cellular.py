# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.models.common import CarrierType, TLOCColor
from catalystwan.models.configuration.feature_profile.common import (
    AclQos,
    AllowService,
    Encapsulation,
    MultiRegionFabric,
)


class Tunnel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bind: Optional[Union[Global[str], Default[None], Variable]] = Field(default=None)
    border: Optional[Union[Default[bool], Global[bool], Variable]] = Field(default=None)
    carrier: Optional[Union[Default[CarrierType], Global[CarrierType], Variable]] = Field(default=None)
    clear_dont_fragment: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="clearDontFragment", serialization_alias="clearDontFragment"
    )
    color: Optional[Union[Default[TLOCColor], Global[TLOCColor], Variable]] = Field(default=None)
    exclude_controller_group_list: Optional[Union[Global[List[int]], Default[None], Variable]] = Field(
        default=None, validation_alias="excludeControllerGroupList", serialization_alias="excludeControllerGroupList"
    )
    group: Optional[Union[Global[int], Default[None], Variable]] = Field(default=None)
    hello_interval: Optional[Union[Global[int], Default[int], Variable]] = Field(
        default=None, validation_alias="helloInterval", serialization_alias="helloInterval"
    )
    hello_tolerance: Optional[Union[Global[int], Default[int], Variable]] = Field(
        default=None, validation_alias="helloTolerance", serialization_alias="helloTolerance"
    )
    last_resort_circuit: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="lastResortCircuit", serialization_alias="lastResortCircuit"
    )
    low_bandwidth_link: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="lowBandwidthLink", serialization_alias="lowBandwidthLink"
    )
    max_control_connections: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="maxControlConnections", serialization_alias="maxControlConnections"
    )
    mode: Optional[Union[Global[Literal["spoke"]], Variable]] = Field(default=None)
    nat_refresh_interval: Optional[Union[Global[int], Default[int], Variable]] = Field(
        default=None, validation_alias="natRefreshInterval", serialization_alias="natRefreshInterval"
    )
    network_broadcast: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="networkBroadcast", serialization_alias="networkBroadcast"
    )
    per_tunnel_qos: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="perTunnelQos", serialization_alias="perTunnelQos"
    )
    port_hop: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="portHop", serialization_alias="portHop"
    )
    restrict: Optional[Union[Default[bool], Global[bool], Variable]] = Field(default=None)
    tunnel_tcp_mss: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="tunnelTcpMss", serialization_alias="tunnelTcpMss"
    )
    vbond_as_stun_server: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="vBondAsStunServer", serialization_alias="vBondAsStunServer"
    )
    vmanage_connection_preference: Optional[Union[Global[int], Default[int], Variable]] = Field(
        default=None, validation_alias="vManageConnectionPreference", serialization_alias="vManageConnectionPreference"
    )


class NatAttributesIpv4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    tcp_timeout: Union[Global[int], Default[int], Variable] = Field(
        default=as_default(60), validation_alias="tcpTimeout", serialization_alias="tcpTimeout"
    )
    udp_timeout: Union[Global[int], Default[int], Variable] = Field(
        default=as_default(1), validation_alias="udpTimeout", serialization_alias="udpTimeout"
    )


class Arp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ip_address: Union[Global[str], Global[IPv4Address], Default[None], Variable] = Field(
        default=as_default(None), validation_alias="ipAddress", serialization_alias="ipAddress"
    )
    mac_address: Union[Global[str], Default[None], Variable] = Field(
        default=as_default(None), validation_alias="macAddress", serialization_alias="macAddress"
    )


class Advanced(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    intrf_mtu: Optional[Union[Global[int], Default[int], Variable]] = Field(
        default=None, validation_alias="intrfMtu", serialization_alias="intrfMtu"
    )
    ip_directed_broadcast: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias="ipDirectedBroadcast", serialization_alias="ipDirectedBroadcast"
    )
    ip_mtu: Optional[Union[Global[int], Default[int], Variable]] = Field(
        default=None, validation_alias="ipMtu", serialization_alias="ipMtu"
    )
    tcp_mss: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias="tcpMss", serialization_alias="tcpMss"
    )
    tloc_extension: Optional[Union[Global[str], Default[None], Variable]] = Field(
        default=None, validation_alias="tlocExtension", serialization_alias="tlocExtension"
    )
    tracker: Optional[Union[Global[str], Default[None], Variable]] = Field(default=None)


class InterfaceCellularParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["wan/vpn/interface/cellular"] = Field(
        default="wan/vpn/interface/cellular", frozen=True, exclude=True
    )
    encapsulation: List[Encapsulation] = Field(
        validation_alias=AliasPath("data", "encapsulation"), description="Encapsulation for TLOC"
    )
    interface_description: Optional[Union[Global[str], Default[None], Variable]] = Field(
        validation_alias=AliasPath("data", "description")
    )
    interface_name: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "interfaceName"))
    nat: Union[Default[bool], Global[bool], Variable] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "nat")
    )
    shutdown: Union[Default[bool], Global[bool], Variable] = Field(
        default=as_default(True), validation_alias=AliasPath("data", "shutdown")
    )
    tunnel_interface: Union[Global[bool], Default[bool]] = Field(validation_alias=AliasPath("data", "tunnelInterface"))
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
    bandwidth_downstream: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthDownstream")
    )
    bandwidth_upstream: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthUpstream")
    )
    dhcp_helper: Optional[Union[Global[List[str]], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "dhcpHelper")
    )
    enable_ipv6: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "enableIpv6")
    )
    multi_region_fabric: Optional[MultiRegionFabric] = Field(
        default=None, validation_alias=AliasPath("data", "multiRegionFabric"), description="Multi-Region Fabric"
    )
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = Field(
        default=None, validation_alias=AliasPath("data", "natAttributesIpv4"), description="NAT Attributes"
    )
    service_provider: Optional[Union[Global[str], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "serviceProvider")
    )
    tunnel: Optional[Tunnel] = Field(
        default=None, validation_alias=AliasPath("data", "tunnel"), description="Tunnel Interface Attributes"
    )
