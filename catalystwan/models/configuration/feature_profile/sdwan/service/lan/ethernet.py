# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import EthernetDuplexMode, MediaType
from catalystwan.models.configuration.feature_profile.common import (
    Arp,
    DynamicDhcpDistance,
    EthernetNatAttributesIpv4,
    InterfaceDynamicIPv4Address,
    InterfaceDynamicIPv6Address,
    InterfaceStaticIPv4Address,
    StaticIPv4Address,
    StaticIPv4AddressConfig,
    StaticIPv6Address,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.common import (
    VrrpIPv6Address,
    VrrpTrackingObject,
)


class Dhcpv6Helper(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ip_address: Union[Global[str], Variable] = Field(serialization_alias="ipAddress", validation_alias="ipAddress")
    vpn: Optional[Union[Global[int], Variable, Default[None]]] = None


class StaticIPv6AddressConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    primary_ip_address: StaticIPv6Address = Field(
        serialization_alias="staticIpV6AddressPrimary", validation_alias="staticIpV6AddressPrimary"
    )
    secondary_ip_address: Optional[List[StaticIPv6Address]] = Field(
        serialization_alias="staticIpV6AddressSecondary", validation_alias="staticIpV6AddressSecondary", default=None
    )
    dhcp_helper_v6: Optional[List[Dhcpv6Helper]] = Field(
        serialization_alias="dhcpHelperV6", validation_alias="dhcpHelperV6", default=None
    )


class InterfaceStaticIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    static: StaticIPv6AddressConfig


class NatAttributesIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    nat64: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=False)


class AclQos(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    shaping_rate: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="shapingRate", validation_alias="shapingRate", default=None
    )
    ipv4_acl_egress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv4AclEgress", validation_alias="ipv4AclEgress", default=None
    )
    ipv4_acl_ingress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv4AclIngress", validation_alias="ipv4AclIngress", default=None
    )
    ipv6_acl_egress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv6AclEgress", validation_alias="ipv6AclEgress", default=None
    )
    ipv6_acl_ingress: Optional[Global[UUID]] = Field(
        serialization_alias="ipv6AclIngress", validation_alias="ipv6AclIngress", default=None
    )


class VrrpIPv6(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_id: Union[Variable, Global[int]] = Field(serialization_alias="groupId", validation_alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="trackOmp", validation_alias="trackOmp", default=Default[bool](value=False)
    )
    ipv6: List[VrrpIPv6Address]


class VrrpIPv4(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    group_id: Union[Variable, Global[int]] = Field(serialization_alias="groupId", validation_alias="groupId")
    priority: Union[Variable, Global[int], Default[int]] = Default[int](value=100)
    timer: Union[Variable, Global[int], Default[int]] = Default[int](value=1000)
    track_omp: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="trackOmp", validation_alias="trackOmp", default=Default[bool](value=False)
    )
    ip_address: Union[Global[str], Global[IPv4Address], Variable] = Field(
        serialization_alias="ipAddress", validation_alias="ipAddress"
    )
    ip_address_secondary: Optional[List[StaticIPv4Address]] = Field(
        serialization_alias="ipAddressSecondary",
        validation_alias="ipAddressSecondary",
        default=None,
    )
    tloc_pref_change: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="tlocPrefChange", validation_alias="tlocPrefChange", default=Default[bool](value=False)
    )
    tloc_pref_change_value: Optional[Union[Global[int], Default[None]]] = Field(
        serialization_alias="tlocPrefChangeValue", validation_alias="tlocPrefChangeValue", default=None
    )
    tracking_object: Optional[List[VrrpTrackingObject]] = Field(
        serialization_alias="trackingObject", validation_alias="trackingObject", default=None
    )


class Trustsec(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    enable_sgt_propagation: Union[Global[bool], Default[bool]] = Field(
        serialization_alias="enableSGTPropagation",
        validation_alias="enableSGTPropagation",
        default=Default[bool](value=False),
    )
    propagate: Optional[Union[Global[bool], Default[bool]]] = Default[bool](value=True)
    security_group_tag: Optional[Union[Global[int], Variable, Default[None]]] = Field(
        serialization_alias="securityGroupTag", validation_alias="securityGroupTag", default=None
    )
    enable_enforced_propagation: Union[Global[bool], Default[None]] = Field(
        serialization_alias="enableEnforcedPropagation", validation_alias="enableEnforcedPropagation"
    )
    enforced_security_group_tag: Union[Global[int], Variable, Default[None]] = Field(
        serialization_alias="enforcedSecurityGroupTag", validation_alias="enforcedSecurityGroupTag"
    )


class AdvancedEthernetAttributes(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    duplex: Optional[Union[Global[EthernetDuplexMode], Variable, Default[None]]] = None
    mac_address: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="macAddress", validation_alias="macAddress", default=None
    )
    ip_mtu: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="ipMtu", validation_alias="ipMtu", default=Default[int](value=1500)
    )
    interface_mtu: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        default=None, serialization_alias="intrfMtu", validation_alias="intrfMtu"
    )
    tcp_mss: Optional[Union[Global[int], Variable, Default[int]]] = Field(
        serialization_alias="tcpMss", validation_alias="tcpMss", default=None
    )
    speed: Optional[Union[Global[str], Variable, Default[None]]] = None
    arp_timeout: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="arpTimeout", validation_alias="arpTimeout", default=Default[int](value=1200)
    )
    autonegotiate: Optional[Union[Global[bool], Variable, Default[bool]]] = None
    media_type: Optional[Union[Global[MediaType], Variable, Default[None]]] = Field(
        serialization_alias="mediaType", validation_alias="mediaType", default=None
    )
    load_interval: Union[Global[int], Variable, Default[int]] = Field(
        serialization_alias="loadInterval", validation_alias="loadInterval", default=Default[int](value=30)
    )
    tracker: Optional[Union[Global[str], Variable, Default[None]]] = None
    icmp_redirect_disable: Optional[Union[Global[bool], Variable, Default[bool]]] = Field(
        serialization_alias="icmpRedirectDisable",
        validation_alias="icmpRedirectDisable",
        default=Default[bool](value=True),
    )
    xconnect: Optional[Union[Global[str], Global[IPv4Address], Variable, Default[None]]] = None
    ip_directed_broadcast: Union[Global[bool], Variable, Default[bool]] = Field(
        serialization_alias="ipDirectedBroadcast",
        validation_alias="ipDirectedBroadcast",
        default=Default[bool](value=False),
    )


class InterfaceEthernetParcel(_ParcelBase):
    type_: Literal["lan/vpn/interface/ethernet"] = Field(default="lan/vpn/interface/ethernet", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    shutdown: Union[Global[bool], Variable, Default[bool]] = Field(
        default=Default[bool](value=True), validation_alias=AliasPath("data", "shutdown")
    )
    interface_name: Union[Global[str], Variable] = Field(validation_alias=AliasPath("data", "interfaceName"))
    ethernet_description: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        default=Default[None](value=None), validation_alias=AliasPath("data", "description")
    )
    interface_ip_address: Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address] = Field(
        validation_alias=AliasPath("data", "intfIpAddress"), default_factory=InterfaceStaticIPv4Address
    )
    dhcp_helper: Optional[Union[Variable, Global[List[str]], Default[None]]] = Field(
        validation_alias=AliasPath("data", "dhcpHelper"), default=None
    )
    interface_ipv6_address: Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]] = Field(
        validation_alias=AliasPath("data", "intfIpV6Address"), default=None
    )
    nat: Union[Global[bool], Default[bool]] = Field(
        validation_alias=AliasPath("data", "nat"), default=Default[bool](value=False)
    )
    nat_attributes_ipv4: Optional[EthernetNatAttributesIpv4] = Field(
        validation_alias=AliasPath("data", "natAttributesIpv4"), default=None
    )
    nat_ipv6: Optional[Union[Global[bool], Default[bool]]] = Field(
        validation_alias=AliasPath("data", "natIpv6"), default=Default[bool](value=False)
    )
    nat_attributes_ipv6: Optional[NatAttributesIPv6] = Field(
        validation_alias=AliasPath("data", "natAttributesIpv6"), default=None
    )
    acl_qos: Optional[AclQos] = Field(validation_alias=AliasPath("data", "aclQos"), default=None)
    vrrp_ipv6: Optional[List[VrrpIPv6]] = Field(validation_alias=AliasPath("data", "vrrpIpv6"), default=None)
    vrrp: Optional[List[VrrpIPv4]] = Field(validation_alias=AliasPath("data", "vrrp"), default=None)
    arp: Optional[List[Arp]] = Field(validation_alias=AliasPath("data", "arp"), default=None)
    trustsec: Optional[Trustsec] = Field(validation_alias=AliasPath("data", "trustsec"), default=None)
    advanced: AdvancedEthernetAttributes = Field(
        validation_alias=AliasPath("data", "advanced"), default_factory=AdvancedEthernetAttributes
    )

    def set_dynamic_interface_ip_address(self, dhcp_distance: Union[Global[int], Variable]) -> None:
        self.interface_ip_address = InterfaceDynamicIPv4Address(
            dynamic=DynamicDhcpDistance(dynamic_dhcp_distance=dhcp_distance)
        )

    def set_static_primary_interface_ip_address(
        self,
        ip_address: Union[Global[str], Global[IPv4Address], Variable],
        subnet_mask: Optional[Union[Global[str], Variable]] = None,
    ) -> None:
        if subnet_mask is None:
            primary_ip_address = StaticIPv4Address(ip_address=ip_address)
        else:
            primary_ip_address = StaticIPv4Address(ip_address=ip_address, subnet_mask=subnet_mask)
        self.interface_ip_address = InterfaceStaticIPv4Address(
            static=StaticIPv4AddressConfig(primary_ip_address=primary_ip_address)
        )

    def add_static_secondary_interface_ip_address(
        self, ip_address: Union[Global[str], Global[IPv4Address], Variable], subnet_mask: Union[Global[str], Variable]
    ) -> None:
        if self.interface_ip_address is None:
            raise ValueError("Missing static primary IP Address")
        if isinstance(self.interface_ip_address, InterfaceDynamicIPv4Address):
            raise ValueError("Interface IP Address is already dynamic")

        secondary_ip_address = StaticIPv4Address(ip_address=ip_address, subnet_mask=subnet_mask)
        if self.interface_ip_address.static.secondary_ip_address is None:
            self.interface_ip_address.static.secondary_ip_address = []
        self.interface_ip_address.static.secondary_ip_address.append(secondary_ip_address)
