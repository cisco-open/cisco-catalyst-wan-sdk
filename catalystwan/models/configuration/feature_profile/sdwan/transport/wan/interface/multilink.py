from ipaddress import IPv4Address, IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import ChannelGroup, MultiRegionFabric, RefIdItem

MaskIpv4 = Literal[
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]

Method = Literal[
    "CHAP",
    "PAP",
    "PAP and CHAP",
]

AuthenticationType = Literal[
    "bidirectional",
    "unidirectional",
]


Value = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]


Carrier = Literal[
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
    "default",
]

ControllerType = Literal[
    "A/S Serial",
    "T1/E1",
]

Name = Literal[
    "E1",
    "T1",
]

T1Framing = Literal[
    "esf",
    "sf",
]

E1Framing = Literal[
    "crc4",
    "no-crc4",
]

LineMode = Literal[
    "primary",
    "secondary",
]

ClockSource = Literal[
    "internal",
    "line",
    "loop-timed",
]

T1Linecode = Literal[
    "ami",
    "b8zs",
]

E1Linecode = Literal[
    "ami",
    "hdb3",
]

Long = Literal[
    "-15db",
    "-22.5db",
    "-7.5db",
    "0db",
]

Short = Literal[
    "110ft",
    "220ft",
    "330ft",
    "440ft",
    "550ft",
    "660ft",
]


class ControllerTxExList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    channel_group: List[ChannelGroup] = Field(
        default=[],
        validation_alias="channelGroup",
        serialization_alias="channelGroup",
        description="Channel Group List",
    )
    number: Union[Variable, Global[str]] = Field()
    clock_source: Optional[Union[Global[ClockSource], Default[None]]] = Field(
        default=None, validation_alias="clockSource", serialization_alias="clockSource"
    )
    description: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    e1_framing: Optional[Union[Variable, Global[E1Framing], Default[None]]] = Field(
        default=None, validation_alias="e1Framing", serialization_alias="e1Framing"
    )
    e1_linecode: Optional[Union[Variable, Global[E1Linecode], Default[None]]] = Field(
        default=None, validation_alias="e1Linecode", serialization_alias="e1Linecode"
    )
    line_mode: Optional[Union[Variable, Default[None], Global[LineMode]]] = Field(
        default=None, validation_alias="lineMode", serialization_alias="lineMode"
    )
    long: Optional[Union[Variable, Global[Long], Default[None]]] = Field(default=None)
    name: Optional[Global[Name]] = Field(default=None)
    short: Optional[Union[Variable, Global[Short], Default[None]]] = Field(default=None)
    t1_framing: Optional[Union[Variable, Global[T1Framing], Default[None]]] = Field(
        default=None, validation_alias="t1Framing", serialization_alias="t1Framing"
    )
    t1_linecode: Optional[Union[Variable, Default[None], Global[T1Linecode]]] = Field(
        default=None, validation_alias="t1Linecode", serialization_alias="t1Linecode"
    )


ClockRate = Literal[
    "1000000",
    "115200",
    "1200",
    "125000",
    "14400",
    "148000",
    "19200",
    "192000",
    "2000000",
    "2400",
    "250000",
    "256000",
    "28800",
    "32000",
    "38400",
    "384000",
    "4000000",
    "4800",
    "48000",
    "500000",
    "512000",
    "5300000",
    "56000",
    "57600",
    "64000",
    "72000",
    "768000",
    "800000",
    "8000000",
    "9600",
]


class NimList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    if_name: Union[Variable, Global[str]] = Field(validation_alias="ifName", serialization_alias="ifName")
    bandwidth: Optional[Union[Variable, Global[int], Default[None]]] = Field(default=None)
    clock_rate: Optional[Union[Variable, Global[ClockRate], Default[None]]] = Field(
        default=None, validation_alias="clockRate", serialization_alias="clockRate"
    )
    description: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)


CoreRegion = Literal[
    "core",
    "core-shared",
]


SecondaryRegion = Literal[
    "secondary-only",
    "secondary-shared",
]


class MultilinkParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["interface/multilink"] = Field(default="interface/multilink", frozen=True, exclude=True)

    group_number: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "groupNumber"))
    if_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "ifName"))
    method: Union[Global[Method], Default[None]] = Field(validation_alias=AliasPath("data", "method"))
    address_ipv4: Optional[Union[Variable, Global[IPv4Address], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "addressIpv4")
    )
    address_ipv6: Optional[Union[Variable, Global[IPv6Interface], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "addressIpv6")
    )
    all: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "all")
    )
    authentication_type: Union[Variable, Global[AuthenticationType], Default[AuthenticationType]] = Field(
        default=Default[AuthenticationType](value="unidirectional"),
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
    carrier: Optional[Union[Variable, Default[Literal["default"]], Global[Carrier]]] = Field(
        default=None, validation_alias=AliasPath("data", "carrier")
    )
    clear_dont_fragment_sdwan_tunnel: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "clearDontFragmentSdwanTunnel")
    )
    control_connections: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "controlConnections")
    )
    controller_tx_ex_list: List[ControllerTxExList] = Field(
        default=[], validation_alias=AliasPath("data", "controllerTxExList")
    )
    controller_type: Global[ControllerType] = Field(
        default=Global[ControllerType](value="T1/E1"), validation_alias=AliasPath("data", "controllerType")
    )
    delay_value: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "delayValue")
    )
    dhcp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "dhcp")
    )
    disable: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "disable")
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
    interleave: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "interleave")
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
    mask_ipv4: Optional[Union[Variable, Global[MaskIpv4], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "maskIpv4")
    )
    max_control_connections: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "maxControlConnections")
    )
    mtu: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "mtu")
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
    nim_list: Optional[List[NimList]] = Field(default=None, validation_alias=AliasPath("data", "nimList"))
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
    shutdown: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "shutdown")
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
    value: Optional[Union[Variable, Default[Literal["default"]], Global[Value]]] = Field(
        default=None, validation_alias=AliasPath("data", "value")
    )
    vbond_as_stun_server: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "vbondAsStunServer")
    )
    vmanage_connection_preference: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "vmanageConnectionPreference")
    )
