# Copyright 2024 Cisco Systems, Inc. and its affiliates
# Copyright 2023 Cisco Systems, Inc. and its affiliates

from datetime import datetime
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_default, as_global
from catalystwan.models.common import (
    CableLengthLongValue,
    CableLengthShortValue,
    ClockRate,
    CoreRegion,
    E1Framing,
    E1Linecode,
    EncapType,
    EthernetDirection,
    EthernetNatType,
    LineMode,
    SecondaryRegion,
    SubnetMask,
    T1Framing,
    T1Linecode,
    check_fields_exclusive,
)
from catalystwan.models.configuration.common import Solution

ProfileType = Literal[
    "transport",
    "system",
    "cli",
    "service",
    "application-priority",
    "policy-object",  # automatically created default policy object feature profile
    "embedded-security",
    "other",
    "uc-voice",
    "global",  # automatically created global cellulargateway feature profile
    "sig-security",
    "topology",
    "dns-security",
]

SchemaType = Literal[
    "post",
    "put",
]


class ParcelBasic(BaseModel):
    parcel_id: str = Field(alias="parcelId")
    description: Optional[str] = None


class FeatureProfileInfo(BaseModel):
    profile_id: UUID = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")
    reference_count: Optional[int] = Field(default=None, alias="referenceCount")


class FeatureProfileDetail(BaseModel):
    profile_id: str = Field(alias="profileId")
    profile_name: str = Field(alias="profileName")
    solution: Solution
    profile_type: ProfileType = Field(alias="profileType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    description: str
    created_on: datetime = Field(alias="createdOn")
    last_updated_on: datetime = Field(alias="lastUpdatedOn")
    associated_profile_parcels: Optional[Union[List[str], List[ParcelBasic]]] = Field(alias="associatedProfileParcels")
    rid: int = Field(alias="@rid")
    profile_parcel_count: Optional[int] = Field(default=None, alias="profileParcelCount")
    cached_profile: Optional[str] = Field(default=None, alias="cachedProfile")


class FromFeatureProfile(BaseModel):
    copy_: UUID = Field(alias="copy")


class FeatureProfileCreationPayload(BaseModel):
    name: str
    description: str
    from_feature_profile: Optional[FromFeatureProfile] = Field(alias="fromFeatureProfile", default=None)


class FeatureProfileEditPayload(BaseModel):
    name: str
    description: str


class FeatureProfileCreationResponse(BaseModel):
    id: UUID


class AddressWithMask(BaseModel):
    address: Union[Variable, Global[str], Global[IPv4Address], Global[IPv6Address]]
    mask: Union[Variable, Global[str], Global[SubnetMask]]


class SchemaTypeQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_type: SchemaType = Field(alias="schemaType")


class GetFeatureProfilesParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None


class GetReferenceCountFeatureProfilesPayload(GetFeatureProfilesParams):
    model_config = ConfigDict(populate_by_name=True)

    reference_count: Optional[bool] = Field(serialization_alias="referenceCount", validation_alias="referenceCount")


class DNSIPv4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    primary_dns_address_ipv4: Union[Default[None], Global[str], Global[IPv4Address], Variable] = Field(
        default=Default[None](value=None),
        serialization_alias="primaryDnsAddressIpv4",
        validation_alias="primaryDnsAddressIpv4",
    )
    secondary_dns_address_ipv4: Optional[Union[Default[None], Global[str], Global[IPv4Address], Variable]] = Field(
        default=None,
        serialization_alias="secondaryDnsAddressIpv4",
        validation_alias="secondaryDnsAddressIpv4",
    )


class DNSIPv6(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    primary_dns_address_ipv6: Union[Default[None], Global[str], Global[IPv6Address], Variable] = Field(
        default=Default[None](value=None),
        serialization_alias="primaryDnsAddressIpv6",
        validation_alias="primaryDnsAddressIpv6",
    )
    secondary_dns_address_ipv6: Optional[Union[Default[None], Global[str], Global[IPv6Address], Variable]] = Field(
        default=None,
        serialization_alias="secondaryDnsAddressIpv6",
        validation_alias="secondaryDnsAddressIpv6",
    )


class HostMapping(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    host_name: Union[Global[str], Variable] = Field(serialization_alias="hostName", validation_alias="hostName")
    list_of_ips: Union[Global[List[str]], Variable] = Field(serialization_alias="listOfIp", validation_alias="listOfIp")


class NextHop(BaseModel):
    address: Union[Global[str], Variable] = Field()
    distance: Union[Default[int], Global[int], Default[int]] = Field(default=Default[int](value=1))


class IPv4Prefix(BaseModel):
    ip_address: Union[Global[IPv4Address], Variable] = Field()
    subnet_mask: Union[Global[str], Variable] = Field()


class WANIPv4StaticRoute(BaseModel):
    prefix: IPv4Prefix = Field()
    gateway: Global[Literal["nextHop", "null0", "dhcp"]] = Field(default=Global(value="nextHop"), alias="gateway")
    next_hops: Optional[List[NextHop]] = Field(default_factory=list, alias="nextHop")
    distance: Optional[Global[int]] = Field(default=None, alias="distance")

    def set_to_next_hop(
        self,
        prefix: Optional[Global[str]] = None,
        next_hops: Optional[List[NextHop]] = None,
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        self.gateway = Global[Literal["nextHop", "null0", "dhcp"]](value="nextHop")
        self.next_hops = next_hops or []
        self.distance = None

    def set_to_null0(
        self,
        prefix: Optional[IPv4Prefix] = None,
        distance: Union[Global[int], int] = 1,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global(value="null0")
        self.next_hops = None
        if isinstance(distance, int):
            self.distance = Global(value=distance)
        else:
            self.distance = distance

    def set_to_dhcp(
        self,
        prefix: Optional[IPv4Prefix] = None,
    ):
        if prefix is not None:
            self.prefix = prefix
        self.gateway = Global(value="dhcp")
        self.next_hops = None
        self.distance = None


class NextHopContainer(BaseModel):
    next_hop: List[NextHop] = Field(default=[], alias="nextHop")


class Ipv6StaticRouteNull0(BaseModel):
    null0: Union[Default[bool], Global[bool]] = Field(default=Default[bool](value=True))


class IPv6StaticRouteNextHop(BaseModel):
    next_hop_container: Optional[NextHopContainer] = Field(default=None)


class IPv6StaticRouteNAT(BaseModel):
    nat: Union[Variable, Global[Literal["NAT64", "NAT66"]]] = Field()


class WANIPv6StaticRoute(BaseModel):
    prefix: Global[IPv6Address] = Field()
    gateway: Union[Ipv6StaticRouteNull0, IPv6StaticRouteNextHop, IPv6StaticRouteNAT] = Field(alias="oneOfIpRoute")

    def set_to_next_hop(
        self,
        prefix: Optional[IPv6Address] = None,
        next_hops: Optional[List[NextHop]] = None,
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        if next_hops:
            self.gateway = IPv6StaticRouteNextHop(next_hop_container=NextHopContainer(nextHop=next_hops))

    def set_to_null0(
        self,
        prefix: Optional[IPv6Address] = None,
        enabled: Union[Default[bool], Global[bool], None] = None,
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        if enabled is None:
            enabled = Default[bool](value=True)
        self.gateway = Ipv6StaticRouteNull0(null0=enabled)

    def set_to_nat(
        self,
        prefix: Optional[IPv6Address],
        nat: Union[Variable, Global[Literal["NAT64", "NAT66"]]],
    ):
        if prefix is not None:
            self.prefix = as_global(prefix)
        self.gateway = IPv6StaticRouteNAT(nat=nat)


class WANService(BaseModel):
    service_type: Global[Literal["TE"]] = Field(alias="serviceType")


class RefIdItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ref_id: Global[str] = Field(..., serialization_alias="refId", validation_alias="refId")

    @classmethod
    def from_uuid(cls, ref_id: UUID):
        return cls(ref_id=as_global(str(ref_id)))


class RefIdList(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )

    ref_id: Global[List[str]] = Field(..., serialization_alias="refId", validation_alias="refId")

    @classmethod
    def from_uuids(cls, uuids: List[UUID]) -> Self:
        return cls(ref_id=as_global([str(uuid) for uuid in uuids]))


class MultiRegionFabric(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    core_region: Optional[Union[Global[CoreRegion], Default[CoreRegion]]] = Field(
        default=None, validation_alias="coreRegion", serialization_alias="coreRegion"
    )
    enable_core_region: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="enableCoreRegion", serialization_alias="enableCoreRegion"
    )
    enable_secondary_region: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="enableSecondaryRegion", serialization_alias="enableSecondaryRegion"
    )
    secondary_region: Optional[Union[Global[SecondaryRegion], Default[SecondaryRegion]]] = Field(
        default=None, validation_alias="secondaryRegion", serialization_alias="secondaryRegion"
    )


class SourceIp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    tunnel_source: Union[Variable, Global[str], Global[IPv4Address]] = Field(
        validation_alias="tunnelSource", serialization_alias="tunnelSource"
    )


class SourceNotLoopback(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    tunnel_source_interface: Union[Variable, Global[str], Global[IPv4Interface]] = Field(
        validation_alias="tunnelSourceInterface", serialization_alias="tunnelSourceInterface"
    )


class SourceLoopback(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    tunnel_route_via: Union[Variable, Global[str]] = Field(
        validation_alias="tunnelRouteVia", serialization_alias="tunnelRouteVia"
    )
    tunnel_source_interface: Union[Variable, Global[str]] = Field(
        validation_alias="tunnelSourceInterface", serialization_alias="tunnelSourceInterface"
    )


class TunnelSourceType(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    source_loopback: Optional[SourceLoopback] = Field(
        default=None, validation_alias="sourceLoopback", serialization_alias="sourceLoopback"
    )
    source_ip: Optional[SourceIp] = Field(default=None, validation_alias="sourceIp", serialization_alias="sourceIp")
    source_not_loopback: Optional[SourceNotLoopback] = Field(
        default=None, validation_alias="sourceNotLoopback", serialization_alias="sourceNotLoopback"
    )

    @model_validator(mode="after")
    def check_country_xor_continent(self):
        check_fields_exclusive(self.__dict__, {"source_loopback", "source_ip", "source_not_loopback"}, True)
        return self


TunnelApplication = Literal[
    "none",
    "sig",
]


class AdvancedGre(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    application: Optional[Union[Global[TunnelApplication], Variable]] = None


class ShapingRateUpstreamConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    default_shaping_rate_upstream: Union[Variable, Global[int]] = Field(
        validation_alias="defaultShapingRateUpstream", serialization_alias="defaultShapingRateUpstream"
    )
    max_shaping_rate_upstream: Union[Variable, Global[int]] = Field(
        validation_alias="maxShapingRateUpstream", serialization_alias="maxShapingRateUpstream"
    )
    min_shaping_rate_upstream: Union[Variable, Global[int]] = Field(
        validation_alias="minShapingRateUpstream", serialization_alias="minShapingRateUpstream"
    )


class ShapingRateDownstreamConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    default_shaping_rate_downstream: Union[Variable, Global[int]] = Field(
        validation_alias="defaultShapingRateDownstream", serialization_alias="defaultShapingRateDownstream"
    )
    max_shaping_rate_downstream: Union[Variable, Global[int]] = Field(
        validation_alias="maxShapingRateDownstream", serialization_alias="maxShapingRateDownstream"
    )
    min_shaping_rate_downstream: Union[Variable, Global[int]] = Field(
        validation_alias="minShapingRateDownstream", serialization_alias="minShapingRateDownstream"
    )


class AclQos(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    adapt_period: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias="adaptPeriod", serialization_alias="adaptPeriod"
    )
    adaptive_qos: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="adaptiveQoS", serialization_alias="adaptiveQoS"
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
    shaping_rate: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="shapingRate", serialization_alias="shapingRate"
    )
    shaping_rate_downstream: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="shapingRateDownstream", serialization_alias="shapingRateDownstream"
    )
    shaping_rate_downstream_config: Optional[ShapingRateDownstreamConfig] = Field(
        default=None,
        validation_alias="shapingRateDownstreamConfig",
        serialization_alias="shapingRateDownstreamConfig",
        description="adaptiveQoS Shaping Rate Downstream config",
    )
    shaping_rate_upstream: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="shapingRateUpstream", serialization_alias="shapingRateUpstream"
    )
    shaping_rate_upstream_config: Optional[ShapingRateUpstreamConfig] = Field(
        default=None,
        validation_alias="shapingRateUpstreamConfig",
        serialization_alias="shapingRateUpstreamConfig",
        description="adaptiveQoS Shaping Rate Upstream config",
    )


class Encapsulation(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    encap: Optional[Global[EncapType]] = Field(default=None)
    preference: Optional[Union[Global[int], Variable, Default[None]]] = Field(default=None)
    weight: Optional[Union[Global[int], Variable, Default[int]]] = Field(default=None)


class AllowService(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    bfd: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, description="Field not available for InterfaceCellularParcel"
    )
    all: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    bgp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    dhcp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    dns: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    https: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, description="Field not available for InterfaceDslPPPoEParcel"
    )
    icmp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    netconf: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    ntp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    ospf: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    snmp: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    sshd: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    stun: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    ssh: Optional[Union[Default[bool], Global[bool], Variable]] = Field(
        default=None, description="Field available only for InterfaceCellularParcel"
    )


class Arp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="ipAddress", validation_alias="ipAddress", default=Default[None](value=None)
    )
    mac_address: Union[Global[str], Variable] = Field(serialization_alias="macAddress", validation_alias="macAddress")


class EthernetNatPool(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    range_start: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="rangeStart", validation_alias="rangeStart"
    )
    range_end: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="rangeEnd", validation_alias="rangeEnd"
    )
    prefix_length: Union[Variable, Global[int], Default[None]] = Field(
        default=as_default(None), serialization_alias="prefixLength", validation_alias="prefixLength"
    )
    overload: Union[Variable, Global[bool], Default[bool]] = Default[bool](value=True)


class StaticNat(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    source_ip: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="sourceIp", validation_alias="sourceIp"
    )

    translate_ip: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="translateIp", validation_alias="translateIp"
    )
    static_nat_direction: Union[Global[EthernetDirection], Default[EthernetDirection]] = Field(
        serialization_alias="staticNatDirection",
        validation_alias="staticNatDirection",
        default=Default[EthernetDirection](value="inside"),
    )
    source_vpn: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="sourceVpn", validation_alias="sourceVpn", default=Default[int](value=0)
    )


class EthernetNatAttributesIpv4(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    nat_type: Union[Global[EthernetNatType], Variable] = Field(
        serialization_alias="natType", validation_alias="natType"
    )
    nat_pool: Optional[EthernetNatPool] = Field(serialization_alias="natPool", validation_alias="natPool", default=None)
    nat_loopback: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="natLoopback", validation_alias="natLoopback", default=None
    )
    udp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="udpTimeout", validation_alias="udpTimeout", default=Default[int](value=1)
    )
    tcp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="tcpTimeout", validation_alias="tcpTimeout", default=Default[int](value=60)
    )
    new_static_nat: Optional[List[StaticNat]] = Field(
        serialization_alias="newStaticNat", validation_alias="newStaticNat", default=None
    )


class StaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Union[Variable, Global[str], Global[IPv4Address], Default[None]] = Field(
        serialization_alias="ipAddress", validation_alias="ipAddress", default=Default[None](value=None)
    )
    subnet_mask: Union[Variable, Global[str], Default[None]] = Field(
        serialization_alias="subnetMask", validation_alias="subnetMask", default=Default[None](value=None)
    )


class StaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Global[str], Global[IPv6Interface], Variable]


class DynamicDhcpDistance(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic_dhcp_distance: Union[Variable, Global[int], Default[int]] = Field(
        default=Default[int](value=1), serialization_alias="dynamicDhcpDistance", validation_alias="dynamicDhcpDistance"
    )


class InterfaceDynamicIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic: DynamicDhcpDistance


class StaticIPv4AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    primary_ip_address: StaticIPv4Address = Field(
        serialization_alias="staticIpV4AddressPrimary",
        validation_alias="staticIpV4AddressPrimary",
        default_factory=StaticIPv4Address,
    )
    secondary_ip_address: Optional[List[StaticIPv4Address]] = Field(
        serialization_alias="staticIpV4AddressSecondary", validation_alias="staticIpV4AddressSecondary", default=None
    )


class InterfaceStaticIPv4Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    static: StaticIPv4AddressConfig = Field(default_factory=StaticIPv4AddressConfig)


class DynamicIPv6Dhcp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dhcp_client: Union[Global[dict], Global[bool]] = Field(
        serialization_alias="dhcpClient", validation_alias="dhcpClient", default=Global[dict](value={})
    )
    secondary_ipv6_address: Optional[List[StaticIPv6Address]] = Field(
        serialization_alias="secondaryIpV6Address", validation_alias="secondaryIpV6Address", default=None
    )


class InterfaceDynamicIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic: DynamicIPv6Dhcp


class ChannelGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    number: Union[Global[int], Variable] = Field()
    timeslots: Union[Global[str], Variable] = Field()


MultilinkControllerType = Literal[
    "A/S Serial",
    "T1/E1",
]


MultilinkAuthenticationType = Literal[
    "bidirectional",
    "unidirectional",
]

MultilinkMethod = Literal[
    "CHAP",
    "PAP",
    "PAP and CHAP",
]

MultilinkTxExName = Literal[
    "E1",
    "T1",
]

MultilinkClockSource = Literal[
    "internal",
    "line",
    "loop-timed",
]


class MultilinkControllerTxExList(BaseModel):
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
    clock_source: Optional[Union[Global[MultilinkClockSource], Default[None]]] = Field(
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
    long: Optional[Union[Variable, Global[CableLengthLongValue], Default[None]]] = Field(default=None)
    name: Optional[Global[MultilinkTxExName]] = Field(default=None)
    short: Optional[Union[Variable, Global[CableLengthShortValue], Default[None]]] = Field(default=None)
    t1_framing: Optional[Union[Variable, Global[T1Framing], Default[None]]] = Field(
        default=None, validation_alias="t1Framing", serialization_alias="t1Framing"
    )
    t1_linecode: Optional[Union[Variable, Default[None], Global[T1Linecode]]] = Field(
        default=None, validation_alias="t1Linecode", serialization_alias="t1Linecode"
    )


class MultilinkNimList(BaseModel):
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


IcmpMsg = Literal[
    "administratively-prohibited",
    "dod-host-prohibited",
    "dod-net-prohibited",
    "echo",
    "echo-reply",
    "echo-reply-no-error",
    "extended-echo",
    "extended-echo-reply",
    "general-parameter-problem",
    "host-isolated",
    "host-precedence-unreachable",
    "host-redirect",
    "host-tos-redirect",
    "host-tos-unreachable",
    "host-unknown",
    "host-unreachable",
    "interface-error",
    "malformed-query",
    "multiple-interface-match",
    "net-redirect",
    "net-tos-redirect",
    "net-tos-unreachable",
    "net-unreachable",
    "network-unknown",
    "no-room-for-option",
    "option-missing",
    "packet-too-big",
    "parameter-problem",
    "photuris",
    "port-unreachable",
    "precedence-unreachable",
    "protocol-unreachable",
    "reassembly-timeout",
    "redirect",
    "router-advertisement",
    "router-solicitation",
    "source-route-failed",
    "table-entry-error",
    "time-exceeded",
    "timestamp-reply",
    "timestamp-request",
    "ttl-exceeded",
    "unreachable",
]

Icmp6Msg = Literal[
    "beyond-scope",
    "cp-advertisement",
    "cp-solicitation",
    "destination-unreachable",
    "dhaad-reply",
    "dhaad-request",
    "echo-reply",
    "echo-request",
    "header",
    "hop-limit",
    "ind-advertisement",
    "ind-solicitation",
    "mld-query",
    "mld-reduction",
    "mld-report",
    "mldv2-report",
    "mpd-advertisement",
    "mpd-solicitation",
    "mr-advertisement",
    "mr-solicitation",
    "mr-termination",
    "nd-na",
    "nd-ns",
    "next-header-type",
    "ni-query",
    "ni-query-name",
    "ni-query-v4-address",
    "ni-query-v6-address",
    "ni-response",
    "ni-response-qtype-unknown",
    "ni-response-refuse",
    "ni-response-success",
    "no-admin",
    "no-route",
    "packet-too-big",
    "parameter-option",
    "parameter-problem",
    "port-unreachable",
    "reassembly-timeout",
    "redirect",
    "reject-route",
    "renum-command",
    "renum-result",
    "renum-seq-number",
    "router-advertisement",
    "router-renumbering",
    "router-solicitation",
    "rpl-control",
    "source-policy",
    "source-route-header",
    "time-exceeded",
    "unreachable",
]
