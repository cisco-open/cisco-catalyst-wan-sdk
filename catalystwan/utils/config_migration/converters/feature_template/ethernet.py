# Copyright 2024 Cisco Systems, Inc. and its affiliates
from copy import deepcopy
from ipaddress import IPv6Interface
from typing import Dict, List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_default, as_global
from catalystwan.models.common import EthernetDuplexMode, Speed
from catalystwan.models.configuration.feature_profile.common import (
    Arp,
    DynamicDhcpDistance,
    InterfaceDynamicIPv4Address,
    InterfaceStaticIPv4Address,
    StaticIPv4Address,
    StaticIPv4AddressConfig,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.management.ethernet import (
    Advanced,
    DhcpClient,
    InterfaceDynamicIPv6Address,
    InterfaceEthernetParcel,
    InterfaceStaticIPv6Address,
    StaticIPv6Address,
    StaticIPv6AddressConfig,
)
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none
from catalystwan.utils.config_migration.converters.utils import parse_interface_name
from catalystwan.utils.config_migration.steps.constants import MANAGEMENT_VPN_ETHERNET

from .base import FTConverter


class ManagementInterfaceEthernetConverter(FTConverter):
    supported_template_types = (MANAGEMENT_VPN_ETHERNET,)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceEthernetParcel:
        data = deepcopy(template_values)

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            advanced=self.parse_advanced(data),
            interface_name=parse_interface_name(self, data),
            interface_description=data.get("description", Default[None](value=None)),
            intf_ip_address=self.parse_ipv4_address(data),
            shutdown=data.get("shutdown"),
            arp=self.parse_arp(data),
            auto_detect_bandwidth=data.get("auto_bandwidth_detect"),
            dhcp_helper=data.get("dhcp_helper"),
            intf_ip_v6_address=self.parse_ipv6_address(data),
            iperf_server=data.get("iperf_server"),
        )

        return InterfaceEthernetParcel(**payload)

    def parse_ipv4_address(
        self, data: Dict
    ) -> Optional[Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address]]:
        ip_address = data.get("ip", {})

        if "address" in ip_address and ip_address["address"].value != "":
            return InterfaceStaticIPv4Address(
                static=StaticIPv4AddressConfig(
                    primary_ip_address=self.get_static_ipv4_address(ip_address),
                    secondary_ip_address=self.get_secondary_static_ipv4_address(ip_address),
                )
            )

        if "dhcp_client" in ip_address:
            return InterfaceDynamicIPv4Address(
                dynamic=DynamicDhcpDistance(dynamic_dhcp_distance=ip_address.get("dhcp_distance", as_default(1)))
            )

        return InterfaceDynamicIPv4Address(dynamic=DynamicDhcpDistance())

    def get_static_ipv4_address(self, address_configuration: dict) -> StaticIPv4Address:
        address = address_configuration["address"]

        if isinstance(address, Variable):
            return StaticIPv4Address(
                ip_address=address,
                subnet_mask=address,
            )

        static_network = address.value.network
        return StaticIPv4Address(
            ip_address=as_global(value=static_network.network_address),
            subnet_mask=as_global(value=str(static_network.netmask)),
        )

    def get_secondary_static_ipv4_address(self, address_configuration: dict) -> Optional[List[StaticIPv4Address]]:
        secondary_address = []
        for address in address_configuration.get("secondary_address", []):
            secondary_address.append(self.get_static_ipv4_address(address))
        return secondary_address if secondary_address else None

    def parse_ipv6_address(
        self, data: dict
    ) -> Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]]:
        ip_address = data.get("ipv6", {})

        if "address" in ip_address:
            return InterfaceStaticIPv6Address(
                static=StaticIPv6AddressConfig(
                    primary_ip_v6_address=self.get_static_ipv6_address(ip_address),
                )
            )

        if "dhcp_client" in ip_address:
            return InterfaceDynamicIPv6Address(dynamic=DhcpClient(dhcp_client=ip_address.get("dhcp_client")))

        return None

    def get_static_ipv6_address(self, address_configuration: dict) -> StaticIPv6Address:
        address = address_configuration["address"]

        if isinstance(address, Variable):
            return StaticIPv6Address(address=address)

        return StaticIPv6Address(address=Global[IPv6Interface](value=address.value))

    def parse_advanced(self, data: Dict) -> Optional[Advanced]:
        payload = create_dict_without_none(
            arp_timeout=data.get("arp_timeout"),
            autonegotiate=data.get("autonegotiate"),
            duplex=self.parse_duplex(data),
            icmp_redirect_disable=data.get("icmp_redirect_disable"),
            intrf_mtu=data.get("intrf_mtu"),
            ip_directed_broadcast=data.get("ip_directed_broadcast"),
            ip_mtu=data.get("ip_mtu"),
            load_interval=data.get("load_interval"),
            mac_address=data.get("mac_address"),
            media_type=data.get("media_type"),
            speed=self.parse_speed(data),
            tcp_mss=data.get("tcp_mss"),
        )

        return Advanced(**payload)

    def parse_tracker(self, data: Dict) -> Optional[Global[str]]:
        if tracker := data.get("tracker"):
            return as_global(",".join(tracker.value))
        return None

    def parse_duplex(self, data: Dict) -> Optional[Global[EthernetDuplexMode]]:
        if duplex := data.get("duplex"):
            return as_global(duplex.value, EthernetDuplexMode)
        return None

    def parse_speed(self, data: Dict) -> Optional[Global[Speed]]:
        if speed := data.get("speed"):
            return as_global(speed.value, Speed)
        return None

    def parse_arp(self, data: dict) -> Optional[List[Arp]]:
        arps = data.get("arp", {}).get("ip", [])
        if not arps:
            return None
        return [Arp(ip_address=arp.get("addr", Default[None](value=None)), mac_address=arp.get("mac")) for arp in arps]
