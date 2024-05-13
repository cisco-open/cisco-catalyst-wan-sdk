# Copyright 2023 Cisco Systems, Inc. and its affiliates

from datetime import datetime
from ipaddress import IPv4Address, IPv4Interface
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_global
from catalystwan.models.common import CoreRegion, SecondaryRegion, SubnetMask, check_fields_exclusive
from catalystwan.models.configuration.common import Solution

IPV4Address = str
IPv6Address = str

ProfileType = Literal[
    "transport",
    "system",
    "cli",
    "service",
    "application-priority",
    "policy-object",
    "embedded-security",
    "other",
]

SchemaType = Literal[
    "post",
    "put",
]


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
    associated_profile_parcels: List[str] = Field(alias="associatedProfileParcels")
    rid: int = Field(alias="@rid")
    profile_parcel_count: int = Field(alias="profileParcelCount")
    cached_profile: Optional[str] = Field(alias="cachedProfile")


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


class GetFeatureProfilesPayload(BaseModel):
    limit: Optional[int]
    offset: Optional[int]


class DNSIPv4(BaseModel):
    primary_dns_address_ipv4: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="primaryDnsAddressIpv4"
    )
    secondary_dns_address_ipv4: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="secondaryDnsAddressIpv4"
    )


class DNSIPv6(BaseModel):
    primary_dns_address_ipv6: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="primaryDnsAddressIpv6"
    )
    secondary_dns_address_ipv6: Union[Default[None], Global[str], Variable] = Field(
        default=Default[None](value=None), alias="secondaryDnsAddressIpv6"
    )


class HostMapping(BaseModel):
    host_name: Union[Global[str], Variable] = Field(alias="hostName")
    list_of_ips: Union[Global[List[str]], Variable] = Field(alias="listOfIp")


class NextHop(BaseModel):
    address: Union[Global[str], Variable] = Field()
    distance: Union[Default[int], Global[int], Default[int]] = Field(default=Default[int](value=1))


class IPv4Prefix(BaseModel):
    ip_address: Union[Global[IPV4Address], Variable] = Field()
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


class RefIdList(BaseModel):
    ref_id: Global[List[str]] = Field(..., serialization_alias="refId", validation_alias="refId")


class MultiRegionFabric(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    core_region: Optional[Union[Global[CoreRegion], Default[Literal["core-shared"]]]] = Field(
        default=None, validation_alias="coreRegion", serialization_alias="coreRegion"
    )
    enable_core_region: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="enableCoreRegion", serialization_alias="enableCoreRegion"
    )
    enable_secondary_region: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="enableSecondaryRegion", serialization_alias="enableSecondaryRegion"
    )
    secondary_region: Optional[Union[Global[SecondaryRegion], Default[Literal["secondary-shared"]]]] = Field(
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
