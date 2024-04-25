# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

Gateway = Literal["nextHop", "dhcp", "null0"]
Nat = Literal["NAT64", "NAT66"]
SubnetMask = Literal[
    "255.255.255.255",
    "255.255.255.254",
    "255.255.255.252",
    "255.255.255.248",
    "255.255.255.240",
    "255.255.255.224",
    "255.255.255.192",
    "255.255.255.128",
    "255.255.255.0",
    "255.255.254.0",
    "255.255.252.0",
    "255.255.248.0",
    "255.255.240.0",
    "255.255.224.0",
    "255.255.192.0",
    "255.255.128.0",
    "255.255.0.0",
    "255.254.0.0",
    "255.252.0.0",
    "255.240.0.0",
    "255.224.0.0",
    "255.192.0.0",
    "255.128.0.0",
    "255.0.0.0",
    "254.0.0.0",
    "252.0.0.0",
    "248.0.0.0",
    "240.0.0.0",
    "224.0.0.0",
    "192.0.0.0",
    "128.0.0.0",
    "0.0.0.0",
]


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
    list_of_ip: Union[Variable, Global[list]] = Field(
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
    gateway: Union[Global[Gateway], Default[Gateway]] = Field(as_default("nextHop", Gateway), description="Gateway")
    next_hop: Optional[List[NextHopItem]] = Field(
        default=None,
        serialization_alias="nextHop",
        validation_alias="nextHop",
        description="IPv4 Route Gateway Next Hop",
    )
    distance: Optional[Union[Variable, Global[int], Default[int]]] = Field(
        default=None, description="Administrative distance"
    )


class NextHopItem1(BaseModel):
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
    next_hop: Optional[List[NextHopItem1]] = Field(
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
    prefix: Union[Variable, Global[str]] = Field(..., description="Prefix")
    one_of_ip_route: Union[OneOfIpRouteNextHopContainer, OneOfIpRouteNull0, OneOfIpRouteNat] = Field(
        ..., serialization_alias="oneOfIpRoute", validation_alias="oneOfIpRoute"
    )


class ManagementVpn(_ParcelBase):
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
