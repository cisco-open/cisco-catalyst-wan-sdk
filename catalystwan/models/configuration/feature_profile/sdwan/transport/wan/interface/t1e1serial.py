# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import CarrierType, ClockRate, TLOCColor
from catalystwan.models.configuration.feature_profile.common import (
    AddressWithMask,
    AllowService,
    Encapsulation,
    MultiRegionFabric,
    RefIdItem,
)

EncapsulationSerial = Literal[
    "frame-relay",
    "hdlc",
    "ppp",
]


class Tunnel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bind: Optional[Union[Global[str], Variable, Default[None]]] = Field(default=None)
    border: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(default=None)
    carrier: Optional[Union[Global[CarrierType], Variable, Default[Literal["default"]]]] = Field(default=None)
    clear_dont_fragment: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="clearDontFragment", serialization_alias="clearDontFragment"
    )
    color: Optional[Union[Global[TLOCColor], Variable, Default[Literal["default"]]]] = Field(default=None)
    exclude_controller_group_list: Optional[Union[Global[List[int]], Variable, Default[None]]] = Field(
        default=None, validation_alias="excludeControllerGroupList", serialization_alias="excludeControllerGroupList"
    )
    group: Optional[Union[Global[int], Variable, Default[None]]] = Field(default=None)
    hello_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, validation_alias="helloInterval", serialization_alias="helloInterval"
    )
    hello_tolerance: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, validation_alias="helloTolerance", serialization_alias="helloTolerance"
    )
    last_resort_circuit: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="lastResortCircuit", serialization_alias="lastResortCircuit"
    )
    low_bandwidth_link: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="lowBandwidthLink", serialization_alias="lowBandwidthLink"
    )
    max_control_connections: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None, validation_alias="maxControlConnections", serialization_alias="maxControlConnections"
    )
    mode: Optional[Union[Global[Literal["spoke"]], Variable]] = Field(default=None)
    nat_refresh_interval: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, validation_alias="natRefreshInterval", serialization_alias="natRefreshInterval"
    )
    network_broadcast: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="networkBroadcast", serialization_alias="networkBroadcast"
    )
    per_tunnel_qos: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="perTunnelQos", serialization_alias="perTunnelQos"
    )
    per_tunnel_qos_aggregator: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="perTunnelQosAggregator", serialization_alias="perTunnelQosAggregator"
    )
    port_hop: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="portHop", serialization_alias="portHop"
    )
    restrict: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(default=None)
    tunnel_tcp_mss_adjust: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None, validation_alias="tunnelTcpMssAdjust", serialization_alias="tunnelTcpMssAdjust"
    )
    vbond_as_stun_server: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias="vbondAsStunServer", serialization_alias="vbondAsStunServer"
    )
    vmanage_connection_preference: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, validation_alias="vmanageConnectionPreference", serialization_alias="vmanageConnectionPreference"
    )


class AclQos(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ipv4_acl_egress: Optional[RefIdItem] = Field(
        default=None, validation_alias="ipv4AclEgress", serialization_alias="ipv4AclEgress"
    )
    ipv4_acl_ingress: Optional[RefIdItem] = Field(
        default=None, validation_alias="ipv4AclIngress", serialization_alias="ipv4AclIngress"
    )
    ipv6_acl_egress: Optional[RefIdItem] = Field(
        default=None, validation_alias="ipv6AclEgress", serialization_alias="ipv6AclEgress"
    )
    ipv6_acl_ingress: Optional[RefIdItem] = Field(
        default=None, validation_alias="ipv6AclIngress", serialization_alias="ipv6AclIngress"
    )
    shaping_rate: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None, validation_alias="shapingRate", serialization_alias="shapingRate"
    )


class Advanced(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ip_mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, validation_alias="ipMtu", serialization_alias="ipMtu", description="Value cannot be less than 576"
    )
    mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(default=None)
    tcp_mss_adjust: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        validation_alias="tcpMssAdjust",
        serialization_alias="tcpMssAdjust",
        description="Value must cannot be greater then 1460",
    )
    tloc_extension: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=None, validation_alias="tlocExtension", serialization_alias="tlocExtension"
    )


class T1E1SerialParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["interface/serial"] = Field(default="interface/serial", exclude=True)
    interface_name: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "interfaceName"))
    acl_qos: Optional[AclQos] = Field(
        default=None,
        validation_alias=AliasPath("data", "aclQos"),
        description="ACL part",
    )
    address_v4: Optional[AddressWithMask] = Field(
        default=None,
        validation_alias=AliasPath("data", "addressV4"),
        description="Assign IPv4 address",
    )
    address_v6: Optional[Union[Global[IPv6Interface], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "addressV6"),
    )
    advanced: Optional[Advanced] = Field(
        default=None,
        validation_alias=AliasPath("data", "advanced"),
        description="advanced part",
    )
    allow_service: Optional[AllowService] = Field(
        default=None,
        validation_alias=AliasPath("data", "allowService"),
        description="Tunnel Interface Attributes",
    )
    bandwidth: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "bandwidth"),
    )
    bandwidth_downstream: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "bandwidthDownstream"),
    )
    clock_rate: Optional[Union[Global[ClockRate], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "clockRate"),
    )
    encapsulation: Optional[List[Encapsulation]] = Field(
        default=None,
        validation_alias=AliasPath("data", "encapsulation"),
        description="Encapsulation for TLOC",
    )
    encapsulation_serial: Optional[Union[Global[EncapsulationSerial], Variable, Default[None]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "encapsulationSerial"),
    )
    multi_region_fabric: Optional[MultiRegionFabric] = Field(
        default=None,
        validation_alias=AliasPath("data", "multiRegionFabric"),
        description="Multi-Region Fabric",
    )
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "shutdown")
    )
    tunnel: Optional[Tunnel] = Field(
        default=None,
        validation_alias=AliasPath("data", "tunnel"),
        description="Tunnel Interface Attributes",
    )
    tunnel_interface: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None,
        validation_alias=AliasPath("data", "tunnelInterface"),
    )
