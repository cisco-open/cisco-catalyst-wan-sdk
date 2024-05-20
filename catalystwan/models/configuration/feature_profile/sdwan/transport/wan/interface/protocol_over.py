# Copyright 2024 Cisco Systems, Inc. and its affiliates

# This file is named PPPoX, because it contains different Point-To-Point Protocol Interfaces.

from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import CarrierType, TLOCColor, TunnelMode
from catalystwan.models.configuration.feature_profile.common import (
    AclQos,
    AddressWithMask,
    AllowService,
    MultiRegionFabric,
)


class NatProp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    nat: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    tcp_timeout: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="tcpTimeout", serialization_alias="tcpTimeout"
    )
    udp_timeout: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="udpTimeout", serialization_alias="udpTimeout"
    )


class Ethernet(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    if_name: Union[Variable, Global[str]] = Field(validation_alias="ifName", serialization_alias="ifName")
    description: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    vlan_id: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="vlanId", serialization_alias="vlanId"
    )


Method = Literal[
    "chap",
    "pap",
    "papandchap",
]


class Chap(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    hostname: Union[Variable, Global[str]] = Field()
    ppp_auth_password: Union[Variable, Global[str]] = Field(
        validation_alias="pppAuthPassword", serialization_alias="pppAuthPassword"
    )


class Pap(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ppp_auth_password: Union[Variable, Global[str]] = Field(
        validation_alias="pppAuthPassword", serialization_alias="pppAuthPassword"
    )
    username: Union[Variable, Global[str]] = Field()


Callin = Literal[
    "Bidirectional",
    "Unidirectional",
]


class Ppp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    dial_pool_number: Union[Variable, Global[int]] = Field(
        validation_alias="dialPoolNumber", serialization_alias="dialPoolNumber"
    )
    method: Union[Global[Method], Default[None]] = Field()
    callin: Optional[Union[Variable, Global[Callin], Default[None]]] = Field(default=None)
    chap: Optional[Chap] = Field(default=None, description="CHAP Attributes")
    pap: Optional[Pap] = Field(default=None, description="PAP Attributes")
    ppp_max_payload: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="pppMaxPayload", serialization_alias="pppMaxPayload"
    )


class Tunnel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bandwidth_percent: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="bandwidthPercent", serialization_alias="bandwidthPercent"
    )
    border: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    clear_dont_fragment: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="clearDontFragment", serialization_alias="clearDontFragment"
    )
    color: Optional[Union[Global[TLOCColor], Default[Literal["default"]], Variable]] = Field(default=None)
    exclude_controller_group_list: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias="excludeControllerGroupList", serialization_alias="excludeControllerGroupList"
    )
    group: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    low_bandwidth_link: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="lowBandwidthLink", serialization_alias="lowBandwidthLink"
    )
    max_control_connections: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="maxControlConnections", serialization_alias="maxControlConnections"
    )
    mode: Optional[Union[Variable, Global[TunnelMode]]] = Field(default=None)
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
    tunnel_interface: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="tunnelInterface", serialization_alias="tunnelInterface"
    )
    tunnel_tcp_mss_adjust: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="tunnelTcpMssAdjust", serialization_alias="tunnelTcpMssAdjust"
    )
    vbond_as_stun_server: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="vbondAsStunServer", serialization_alias="vbondAsStunServer"
    )
    vmanage_connection_preference: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="vmanageConnectionPreference", serialization_alias="vmanageConnectionPreference"
    )


class TunnelAdvancedOption(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bind: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    carrier: Optional[Union[Variable, Default[Literal["default"]], Global[CarrierType]]] = Field(default=None)
    gre_encap: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="greEncap", serialization_alias="greEncap"
    )
    gre_preference: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="grePreference", serialization_alias="grePreference"
    )
    gre_weight: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="greWeight", serialization_alias="greWeight"
    )
    hello_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="helloInterval", serialization_alias="helloInterval"
    )
    hello_tolerance: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="helloTolerance", serialization_alias="helloTolerance"
    )
    ipsec_encap: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="ipsecEncap", serialization_alias="ipsecEncap"
    )
    ipsec_preference: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="ipsecPreference", serialization_alias="ipsecPreference"
    )
    ipsec_weight: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="ipsecWeight", serialization_alias="ipsecWeight"
    )
    last_resort_circuit: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="lastResortCircuit", serialization_alias="lastResortCircuit"
    )
    nat_refresh_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="natRefreshInterval", serialization_alias="natRefreshInterval"
    )


class Advanced(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ip_directed_broadcast: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="ipDirectedBroadcast", serialization_alias="ipDirectedBroadcast"
    )
    ip_mtu: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="ipMtu", serialization_alias="ipMtu"
    )
    tcp_mss: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="tcpMss", serialization_alias="tcpMss"
    )
    tloc_extension: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias="tlocExtension", serialization_alias="tlocExtension"
    )


VdslMode = Literal[
    "ADSL1",
    "ADSL2",
    "ADSL2+",
    "ANSI",
    "VDSL2",
]


class Vdsl(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    slot: Union[Variable, Global[str]] = Field()
    mode: Optional[Union[Variable, Global[VdslMode], Default[Literal["auto"]]]] = Field(default=None)
    sra: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)


AtmEncapsulation = Literal[
    "AAL5MUX",
    "AAL5NLPID",
    "AAL5SNAP",
]


class VbrNrtConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    burst_cell_size: Union[Variable, Global[int]] = Field(
        validation_alias="burstCellSize", serialization_alias="burstCellSize"
    )
    p_c_r: Union[Variable, Global[int]] = Field(validation_alias="pCR", serialization_alias="pCR")
    s_c_r: Union[Variable, Global[int]] = Field(validation_alias="sCR", serialization_alias="sCR")


class VbrRtConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    a_c_r: Union[Variable, Global[int]] = Field(validation_alias="aCR", serialization_alias="aCR")
    burst_cell_size: Union[Variable, Global[int]] = Field(
        validation_alias="burstCellSize", serialization_alias="burstCellSize"
    )
    p_c_r: Union[Variable, Global[int]] = Field(validation_alias="pCR", serialization_alias="pCR")


class AtmInterface(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    if_name: Union[Variable, Global[str]] = Field(validation_alias="ifName", serialization_alias="ifName")
    local_vpi_vci: Union[Variable, Global[str]] = Field(
        validation_alias="localVpiVci", serialization_alias="localVpiVci"
    )
    description: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    encapsulation: Optional[Union[Default[Literal["AAL5MUX"]], Global[AtmEncapsulation]]] = Field(default=None)
    vbr_nrt_config: Optional[VbrNrtConfig] = Field(
        default=None, validation_alias="vbrNrtConfig", serialization_alias="vbrNrtConfig", description="VBR-NRT config"
    )
    vbr_rt_config: Optional[VbrRtConfig] = Field(
        default=None, validation_alias="vbrRtConfig", serialization_alias="vbrRtConfig", description="VBR-NRT config"
    )


class Dynamic(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    dhcp_helper: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias="dhcpHelper", serialization_alias="dhcpHelper"
    )
    dynamic_dhcp_distance: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="dynamicDhcpDistance", serialization_alias="dynamicDhcpDistance"
    )


class Static(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    static_ip_v4: Optional[AddressWithMask] = Field(
        default=None,
        validation_alias="staticIpV4AddressPrimary",
        serialization_alias="staticIpV4AddressPrimary",
        description="Static IpV4Address Primary",
    )


class DynamicIntfIpAddress(BaseModel):
    dynamic: Dynamic = Field()


class StaticIntfIpAddress(BaseModel):
    static: Static = Field()


class IPoEEthernet(Ethernet):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    intf_ip_address: Union[DynamicIntfIpAddress, StaticIntfIpAddress] = Field(
        validation_alias="intfIpAddress", serialization_alias="intfIpAddress"
    )


class InterfaceBase(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    acl_qos: Optional[AclQos] = Field(default=None, validation_alias=AliasPath("data", "aclQos"), description="ACL/QOS")
    advanced: Optional[Advanced] = Field(
        default=None, validation_alias=AliasPath("data", "advanced"), description="Advanced Attributes"
    )
    bandwidth_downstream: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthDownstream")
    )
    bandwidth_upstream: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthUpstream")
    )
    multi_region_fabric: Optional[MultiRegionFabric] = Field(
        default=None, validation_alias=AliasPath("data", "multiRegionFabric"), description="Multi-Region Fabric"
    )
    nat_prop: Optional[NatProp] = Field(
        default=None, validation_alias=AliasPath("data", "natProp"), description="NAT Attributes"
    )
    ppp: Optional[Ppp] = Field(default=None, validation_alias=AliasPath("data", "ppp"), description="PPP Attributes")
    service_provider: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "serviceProvider")
    )
    shutdown: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "shutdown")
    )
    tunnel: Optional[Tunnel] = Field(
        default=None, validation_alias=AliasPath("data", "tunnel"), description="Tunnel Interface Attributes"
    )
    tunnel_advanced_option: Optional[TunnelAdvancedOption] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelAdvancedOption")
    )
    tunnel_allow_service: Optional[AllowService] = Field(
        default=None,
        validation_alias=AliasPath("data", "tunnelAllowService"),
        description="Tunnel Interface Attributes",
    )


class InterfaceEthPPPoEParcel(InterfaceBase):
    type_: Literal["wan/vpn/interface/ethpppoe"] = Field(
        default="wan/vpn/interface/ethpppoe", frozen=True, exclude=True
    )
    ethernet: Optional[Ethernet] = Field(
        default=None,
        validation_alias=AliasPath("data", "ethernet"),
        description="Ethernet Interface Attributes applicable for both ethppoe/ipoe",
    )


class InterfaceDslPPPoEParcel(InterfaceBase):
    type_: Literal["wan/vpn/interface/dsl-pppoe"] = Field(
        default="wan/vpn/interface/dsl-pppoe", frozen=True, exclude=True
    )
    vdsl: Optional[Vdsl] = Field(default=None, validation_alias=AliasPath("data", "vdsl"), description="vdsl")
    ethernet: Optional[Ethernet] = Field(
        default=None,
        validation_alias=AliasPath("data", "ethernet"),
        description="Ethernet Interface Attributes applicable for both ethppoe/ipoe",
    )


class InterfaceDslPPPoAParcel(InterfaceBase):
    type_: Literal["wan/vpn/interface/dsl-pppoa"] = Field(
        default="wan/vpn/interface/dsl-pppoa", frozen=True, exclude=True
    )
    atm_interface: Optional[AtmInterface] = Field(
        default=None, validation_alias=AliasPath("data", "atmInterface"), description="ATM Interface attributes"
    )
    vdsl: Optional[Vdsl] = Field(default=None, validation_alias=AliasPath("data", "vdsl"), description="vdsl")


class InterfaceDslIPoEParcel(InterfaceBase):
    type_: Literal["wan/vpn/interface/dsl-ipoe"] = Field(
        default="wan/vpn/interface/dsl-ipoe", frozen=True, exclude=True
    )
    ethernet: Optional[IPoEEthernet] = Field(
        default=None,
        validation_alias=AliasPath("data", "ethernet"),
        description="Ethernet Interface Attributes for ipoe",
    )
    vdsl: Optional[Vdsl] = Field(
        default=None,
        validation_alias=AliasPath("data", "vdsl"),
        description="vdsl",
    )
