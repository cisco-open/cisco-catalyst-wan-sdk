from ipaddress import IPv4Address, IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import CarrierType, SubnetMask, TLOCColor
from catalystwan.models.configuration.feature_profile.common import (
    MultilinkAuthenticationType,
    MultilinkControllerTxExList,
    MultilinkControllerType,
    MultilinkMethod,
    MultilinkNimList,
    MultiRegionFabric,
    RefIdItem,
)


class InterfaceMultilinkParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["wan/vpn/interface/multilink"] = Field(
        default="wan/vpn/interface/multilink", frozen=True, exclude=True
    )

    group_number: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "groupNumber"))
    if_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "ifName"))
    method: Union[Global[MultilinkMethod], Default[None]] = Field(validation_alias=AliasPath("data", "method"))
    address_ipv4: Optional[Union[Variable, Global[IPv4Address], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "addressIpv4")
    )
    address_ipv6: Optional[Union[Variable, Global[IPv6Interface], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "addressIpv6")
    )
    all: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "all")
    )
    authentication_type: Union[
        Variable, Global[MultilinkAuthenticationType], Default[MultilinkAuthenticationType]
    ] = Field(
        default=Default[MultilinkAuthenticationType](value="unidirectional"),
        validation_alias=AliasPath("data", "authenticationType"),
    )
    bandwidth_upstream: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "bandwidthUpstream")
    )
    bgp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "bgp")
    )
    bind: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "bind")
    )
    border: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "border")
    )
    carrier: Optional[Union[Variable, Default[CarrierType], Global[CarrierType]]] = Field(
        default=None, validation_alias=AliasPath("data", "carrier")
    )
    clear_dont_fragment_sdwan_tunnel: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "clearDontFragmentSdwanTunnel")
    )
    control_connections: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "controlConnections")
    )
    controller_tx_ex_list: List[MultilinkControllerTxExList] = Field(
        default=[], validation_alias=AliasPath("data", "controllerTxExList")
    )
    controller_type: Global[MultilinkControllerType] = Field(
        default=Global[MultilinkControllerType](value="T1/E1"), validation_alias=AliasPath("data", "controllerType")
    )
    delay_value: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "delayValue")
    )
    dhcp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "dhcp")
    )
    disable: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Default[bool](value=False), validation_alias=AliasPath("data", "disable")
    )
    dns: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "dns")
    )
    exclude_controller_group_list: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "excludeControllerGroupList")
    )
    gre_encap: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "greEncap")
    )
    gre_preference: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "grePreference")
    )
    gre_weight: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "greWeight")
    )
    groups: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "groups")
    )
    hello_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "helloInterval")
    )
    hello_tolerance: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "helloTolerance")
    )
    hostname: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "hostname")
    )
    https: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "https")
    )
    icmp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "icmp")
    )
    interleave: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Default[bool](value=False), validation_alias=AliasPath("data", "interleave")
    )
    ip_directed_broadcast: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "ipDirectedBroadcast")
    )
    ipsec_encap: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "ipsecEncap")
    )
    ipsec_preference: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "ipsecPreference")
    )
    ipsec_weight: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "ipsecWeight")
    )
    ipv4_acl_egress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv4AclEgress"))
    ipv4_acl_ingress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv4AclIngress"))
    ipv6_acl_egress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv6AclEgress"))
    ipv6_acl_ingress: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "ipv6AclIngress"))
    last_resort_circuit: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "lastResortCircuit")
    )
    low_bandwidth_link: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "lowBandwidthLink")
    )
    mask_ipv4: Optional[Union[Variable, Global[SubnetMask], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "maskIpv4")
    )
    max_control_connections: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "maxControlConnections")
    )
    mtu: Union[Variable, Default[int], Global[int]] = Field(
        default=Default[int](value=1500), validation_alias=AliasPath("data", "mtu")
    )
    multi_region_fabric: Optional[MultiRegionFabric] = Field(
        default=None, validation_alias=AliasPath("data", "multiRegionFabric")
    )
    nat_refresh_interval: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "natRefreshInterval")
    )
    netconf: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "netconf")
    )
    network_broadcast: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "networkBroadcast")
    )
    nim_list: Optional[List[MultilinkNimList]] = Field(default=None, validation_alias=AliasPath("data", "nimList"))
    ntp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "ntp")
    )
    ospf: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "ospf")
    )
    password: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "password")
    )
    port_hop: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "portHop")
    )
    ppp_auth_password: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "pppAuthPassword")
    )
    restrict: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "restrict")
    )
    shaping_rate: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "shapingRate")
    )
    shutdown: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Default[bool](value=False), validation_alias=AliasPath("data", "shutdown")
    )
    snmp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "snmp")
    )
    sshd: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "sshd")
    )
    stun: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "stun")
    )
    tcp_mss_adjust: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tcpMssAdjust")
    )
    tloc_extension: Optional[Union[Variable, Global[str], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tlocExtension")
    )
    tunnel_interface: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelInterface")
    )
    tunnel_tcp_mss_adjust: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "tunnelTcpMssAdjust")
    )
    username_string: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "usernameString")
    )
    value: Optional[Union[Variable, Default[TLOCColor], Global[TLOCColor]]] = Field(
        default=None, validation_alias=AliasPath("data", "value")
    )
    vbond_as_stun_server: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "vbondAsStunServer")
    )
    vmanage_connection_preference: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "vmanageConnectionPreference")
    )
