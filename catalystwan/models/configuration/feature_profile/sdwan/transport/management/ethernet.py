from ipaddress import IPv6Interface
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import EthernetDuplexMode, MediaType, Speed
from catalystwan.models.configuration.feature_profile.common import (
    Arp,
    InterfaceDynamicIPv4Address,
    InterfaceStaticIPv4Address,
)


class DhcpClient(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dhcp_client: Optional[Global[bool]] = Field(
        default=Global[bool](value=True), validation_alias="dhcpClient", serialization_alias="dhcpClient"
    )


class InterfaceDynamicIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    dynamic: DhcpClient


class StaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    address: Union[Variable, Global[IPv6Interface], Default[None]] = Field(default=Default[None](value=None))


class StaticIPv6AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    primary_ip_v6_address: Optional[StaticIPv6Address] = Field(
        default=None,
        validation_alias="primaryIpV6Address",
        serialization_alias="primaryIpV6Address",
        description="Static IpV6Address Primary",
    )


class InterfaceStaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    static: StaticIPv6AddressConfig


class Advanced(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    arp_timeout: Union[Variable, Default[int], Global[int]] = Field(
        default=Global[int](value=1200), validation_alias="arpTimeout", serialization_alias="arpTimeout"
    )
    ip_directed_broadcast: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Global[bool](value=False),
        validation_alias="ipDirectedBroadcast",
        serialization_alias="ipDirectedBroadcast",
    )
    ip_mtu: Union[Variable, Default[int], Global[int]] = Field(
        default=Global[int](value=1500), validation_alias="ipMtu", serialization_alias="ipMtu"
    )
    load_interval: Union[Variable, Default[int], Global[int]] = Field(
        default=Global[int](value=30), validation_alias="loadInterval", serialization_alias="loadInterval"
    )
    autonegotiate: Optional[Union[Variable, Global[bool], Default[None]]] = Field(default=None)
    duplex: Optional[Union[Variable, Default[None], Global[EthernetDuplexMode]]] = Field(default=None)
    icmp_redirect_disable: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="icmpRedirectDisable", serialization_alias="icmpRedirectDisable"
    )
    intrf_mtu: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="intrfMtu", serialization_alias="intrfMtu"
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


class InterfaceEthernetParcel(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    type_: Literal["management/vpn/interface/ethernet"] = Field(
        default="management/vpn/interface/ethernet", exclude=True
    )

    advanced: Advanced = Field(validation_alias=AliasPath("data", "advanced"), description="Advanced Attributes")
    interface_name: Union[Variable, Global[str]] = Field(validation_alias=AliasPath("data", "interfaceName"))
    interface_description: Union[Variable, Global[str], Default[None]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "description")
    )
    intf_ip_address: Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address] = Field(
        validation_alias=AliasPath("data", "intfIpAddress")
    )
    shutdown: Union[Variable, Global[bool], Default[bool]] = Field(
        default=Default[bool](value=True), validation_alias=AliasPath("data", "shutdown")
    )
    arp: Optional[List[Arp]] = Field(
        default=None, validation_alias=AliasPath("data", "arp"), description="Configure ARP entries"
    )
    auto_detect_bandwidth: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "autoDetectBandwidth")
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
