# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default
from catalystwan.models.common import SubnetMask

Gateway = Literal["nextHop", "dhcp", "null0"]
Nat = Literal["NAT64", "NAT66"]
ServiceType = Literal["TE"]


class DnsIpv4(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    primary_dns_address_ipv4: Optional[Union[Variable, Global[IPv4Address], Default[None]]] = Field(
        default=None,
        serialization_alias="primaryDnsAddressIpv4",
        validation_alias="primaryDnsAddressIpv4",
        description="Primary DNS Address (IPv4)",
    )
    secondary_dns_address_ipv4: Optional[Union[Variable, Global[IPv4Address], Default[None]]] = Field(
        default=None,
        serialization_alias="secondaryDnsAddressIpv4",
        validation_alias="secondaryDnsAddressIpv4",
        description="Secondary DNS Address (IPv4)",
    )


class DnsIpv6(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    primary_dns_address_ipv6: Optional[Union[Variable, Global[IPv6Address], Default[None]]] = Field(
        default=None,
        serialization_alias="primaryDnsAddressIpv6",
        validation_alias="primaryDnsAddressIpv6",
        description="Primary DNS Address (IPv6)",
    )
    secondary_dns_address_ipv6: Optional[Union[Variable, Global[IPv6Address], Default[None]]] = Field(
        default=None,
        serialization_alias="secondaryDnsAddressIpv6",
        validation_alias="secondaryDnsAddressIpv6",
        description="Secondary DNS Address (IPv6)",
    )


class NewHostMappingItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    host_name: Union[Variable, Global[str]] = Field(
        ..., serialization_alias="hostName", validation_alias="hostName", description="Hostname"
    )
    list_of_ip: Union[Variable, Global[List[str]]] = Field(
        ..., serialization_alias="listOfIp", validation_alias="listOfIp", description="List of IP"
    )


class Prefix(BaseModel):
    """
    Prefix
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ip_address: Union[Variable, Global[IPv4Address]] = Field(
        ..., serialization_alias="ipAddress", validation_alias="ipAddress", description="IP Address"
    )
    subnet_mask: Union[Variable, Global[SubnetMask]] = Field(
        ..., serialization_alias="subnetMask", validation_alias="subnetMask", description="Subnet Mask"
    )


class NextHopItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Variable, Global[IPv4Address], Global[str]] = Field(..., description="Variable")
    distance: Union[Variable, Global[int], Default[int]] = Field(as_default(1), description="Administrative distance")


class Ipv4RouteItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    prefix: Prefix = Field(..., description="Prefix")
    gateway: Union[Global[Gateway], Default[Gateway]] = Field(
        default=as_default("nextHop", Gateway), description="Gateway"
    )
    next_hop: Optional[List[NextHopItem]] = Field(
        default=None,
        serialization_alias="nextHop",
        validation_alias="nextHop",
        description="IPv4 Route Gateway Next Hop",
    )
    distance: Optional[Union[Variable, Global[int], Default[int]]] = Field(
        default=None, description="Administrative distance"
    )


class NextHopItemIpv6(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: Union[Variable, Global[IPv6Address]] = Field(..., description="Variable")
    distance: Union[Variable, Global[int], Default[int]] = Field(..., description="Administrative distance")


class NextHopContainer(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    next_hop: Optional[List[NextHopItemIpv6]] = Field(
        default=None,
        serialization_alias="nextHop",
        validation_alias="nextHop",
        description="IPv6 Route Gateway Next Hop",
    )


class OneOfIpRouteNextHopContainer(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    next_hop_container: NextHopContainer = Field(
        ..., serialization_alias="nextHopContainer", validation_alias="nextHopContainer"
    )


class OneOfIpRouteNull0(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    null0: Union[Global[bool], Default[bool]] = Field(
        default=as_default(True), description="IPv6 Route Gateway Next Hop"
    )


class OneOfIpRouteNat(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    nat: Union[Variable, Global[Nat]] = Field(..., description="IPv6 Variable")


class Ipv6RouteItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    prefix: Union[Variable, Global[IPv6Interface]] = Field(..., description="Prefix")
    one_of_ip_route: Union[OneOfIpRouteNextHopContainer, OneOfIpRouteNull0, OneOfIpRouteNat] = Field(
        ..., serialization_alias="oneOfIpRoute", validation_alias="oneOfIpRoute"
    )


class ServiceItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    service_type: Global[ServiceType] = Field(
        ..., serialization_alias="serviceType", validation_alias="serviceType", description="Service Type"
    )


class Address64V4PoolItem(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    name: Union[Variable, Global[str]] = Field(
        ..., serialization_alias="nat64V4PoolName", validation_alias="nat64V4PoolName", description="NAT64 v4 Pool Name"
    )
    range_start: Union[Variable, Global[IPv4Address]] = Field(
        ...,
        serialization_alias="nat64V4PoolRangeStart",
        validation_alias="nat64V4PoolRangeStart",
        description="NAT64 Pool Range Start",
    )
    range_end: Union[Variable, Global[IPv4Address]] = Field(
        ...,
        serialization_alias="nat64V4PoolRangeEnd",
        validation_alias="nat64V4PoolRangeEnd",
        description="NAT64 Pool Range End",
    )
    overload: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        serialization_alias="nat64V4PoolOverload",
        validation_alias="nat64V4PoolOverload",
        description="NAT64 Overload",
    )


class ManagementVpnParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    type_: Literal["management/vpn"] = Field(default="management/vpn", exclude=True)
    vpn_id: Default[int] = Field(
        default=as_default(512),
        validation_alias=AliasPath("data", "vpnId"),
        frozen=True,
        description="Management VPN, which will always be 512",
    )
    dns_ipv4: Optional[DnsIpv4] = Field(default=None, validation_alias=AliasPath("data", "dnsIpv4"))
    dns_ipv6: Optional[DnsIpv6] = Field(default=None, validation_alias=AliasPath("data", "dnsIpv6"))
    new_host_mapping: Optional[List[NewHostMappingItem]] = Field(
        default=None, validation_alias=AliasPath("data", "newHostMapping")
    )
    ipv4_route: List[Ipv4RouteItem] = Field(
        default_factory=list, validation_alias=AliasPath("data", "ipv4Route"), description="IPv4 Static Route"
    )
    ipv6_route: List[Ipv6RouteItem] = Field(
        default_factory=list, validation_alias=AliasPath("data", "ipv6Route"), description="IPv6 Static Route"
    )


class TransportVpnParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["wan/vpn"] = Field(default="wan/vpn", exclude=True)
    vpn_id: Default[int] = Field(
        default=as_default(0),
        validation_alias=AliasPath("data", "vpnId"),
        frozen=True,
        description="Transport VPN, which will always be 0",
    )
    dns_ipv4: Optional[DnsIpv4] = Field(default=None, validation_alias=AliasPath("data", "dnsIpv4"))
    dns_ipv6: Optional[DnsIpv6] = Field(default=None, validation_alias=AliasPath("data", "dnsIpv6"))
    new_host_mapping: Optional[List[NewHostMappingItem]] = Field(
        default=None, validation_alias=AliasPath("data", "newHostMapping")
    )
    ipv4_route: List[Ipv4RouteItem] = Field(
        default_factory=list, validation_alias=AliasPath("data", "ipv4Route"), description="IPv4 Static Route"
    )
    ipv6_route: List[Ipv6RouteItem] = Field(
        default_factory=list, validation_alias=AliasPath("data", "ipv6Route"), description="IPv6 Static Route"
    )
    enhance_ecmp_keying: Union[Variable, Global[bool], Default[bool]] = Field(
        default=as_default(False),
        validation_alias=AliasPath("data", "enhanceEcmpKeying"),
        description="Enhance ECMP Keying",
    )
    service: Optional[List[ServiceItem]] = Field(
        default=None, validation_alias=AliasPath("data", "service"), description="Service"
    )
    nat64_v4_pool: Optional[List[Address64V4PoolItem]] = Field(
        default=None, validation_alias=AliasPath("data", "nat64V4Pool"), description="NAT64 V4 Pool"
    )
