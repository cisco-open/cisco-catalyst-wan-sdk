# Copyright 2024 Cisco Systems, Inc. and its affiliates
from copy import deepcopy
from ipaddress import IPv4Address
from typing import Dict, List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_default, as_global
from catalystwan.models.common import EthernetDuplexMode, EthernetNatType
from catalystwan.models.configuration.feature_profile.common import (
    Arp,
    DynamicIPv6Dhcp,
    EthernetNatPool,
    StaticIPv4Address,
    StaticIPv6Address,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import (
    AclQos,
    AdvancedEthernetAttributes,
    DynamicDhcpDistance,
    EthernetNatAttributesIpv4,
    InterfaceDynamicIPv4Address,
    InterfaceDynamicIPv6Address,
    InterfaceEthernetParcel,
    InterfaceStaticIPv4Address,
    InterfaceStaticIPv6Address,
    NatAttributesIPv6,
    StaticIPv4AddressConfig,
    StaticIPv6AddressConfig,
    Trustsec,
    VrrpIPv4,
    VrrpIPv6,
)
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.steps.constants import LAN_VPN_ETHERNET


class LanInterfaceEthernetConverter(FTConverter):
    supported_template_types = (LAN_VPN_ETHERNET,)

    delete_keys = (
        "if_name",
        "ip",
        "infru_mtu",
        "description",
        "arp",
        "duplex",
        "mac_address",
        "mtu",
        "ipv6_vrrp",
        "tcp_mss_adjust",
        "arp_timeout",
        "autonegotiate",
        "media_type",
        "load_interval",
        "icmp_redirect_disable",
        "tloc_extension_gre_from",
        "ip_directed_broadcast",
        "tracker",
        "trustsec",
        "intrf_mtu",
        "speed",
        "qos_map",
        "shaping_rate",
        "bandwidth_upstream",
        "bandwidth_downstream",
        "rewrite_rule",
        "block_non_source_ip",
        "tloc_extension",
        "iperf_server",
        "auto_bandwidth_detect",
        "service_provider",
        "ipv6",
        "clear_dont_fragment",
        "access_list",
        "qos_adaptive",
        "poe",
        "pmtu",
        "static_ingress_qos",
        "flow_control",
        "address",
        "tunnel_interface",  # Not sure if this is correct. There is some data in UX1 that is not transferable to UX2
        "nat66",  # Not sure if this is correct. There is some data in UX1 that is not transferable to UX2
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceEthernetParcel:
        data = deepcopy(template_values)
        nat_attributes_ipv4 = self.configure_network_address_translation(data)
        nat = as_global(True) if nat_attributes_ipv4 else as_global(False)
        nat_attributes_ipv6 = self.configure_network_address_translation_ipv6(data)
        nat_ipv6 = as_global(True) if nat_attributes_ipv6 else as_global(False)
        return InterfaceEthernetParcel(
            parcel_name=name,
            parcel_description=description,
            shutdown=data.get("shutdown", as_default(True)),
            interface_name=self.parse_interface_name(data),
            ethernet_description=data.get("description"),
            interface_ip_address=self.configure_ipv4_address(data),
            dhcp_helper=data.get("dhcp_helper"),
            interface_ipv6_address=self.configure_ipv6_address(data),
            nat=nat,
            nat_attributes_ipv4=nat_attributes_ipv4,
            nat_ipv6=nat_ipv6,
            nat_attributes_ipv6=nat_attributes_ipv6,
            acl_qos=self.configure_acl_qos(data),
            vrrp_ipv6=self.configure_virtual_router_redundancy_protocol_ipv6(data),
            vrrp=self.configure_virtual_router_redundancy_protocol_ipv4(data),
            arp=self.configure_arp(data),
            trustsec=self.configure_trustsec(data),
            advanced=self.configure_advanced_attributes(data),
        )

    def configure_ipv4_address(self, values: dict) -> Union[InterfaceStaticIPv4Address, InterfaceDynamicIPv4Address]:
        if ipv4_address_configuration := values.get("ip"):
            if "address" in ipv4_address_configuration and ipv4_address_configuration["address"].value != "":
                return InterfaceStaticIPv4Address(
                    static=StaticIPv4AddressConfig(
                        primary_ip_address=self.get_static_ipv4_address(ipv4_address_configuration),
                        secondary_ip_address=self.get_secondary_static_ipv4_address(ipv4_address_configuration),
                    )
                )
            elif "dhcp_client" in ipv4_address_configuration:
                return InterfaceDynamicIPv4Address(
                    dynamic=DynamicDhcpDistance(
                        dynamic_dhcp_distance=ipv4_address_configuration.get("dhcp_distance", as_global(1))
                    )
                )
        if "address" in values:
            return InterfaceStaticIPv4Address(
                static=StaticIPv4AddressConfig(
                    primary_ip_address=self.get_static_ipv4_address(values),
                )
            )
        return InterfaceStaticIPv4Address()

    def get_static_ipv4_address(self, address_configuration: dict) -> StaticIPv4Address:
        address = address_configuration["address"]

        if isinstance(address, Variable):
            return StaticIPv4Address(
                ip_address=address,
                subnet_mask=address,
            )

        static_network = address.value
        return StaticIPv4Address(
            ip_address=as_global(value=static_network.ip),
            subnet_mask=as_global(value=str(static_network.netmask)),
        )

    def get_secondary_static_ipv4_address(self, address_configuration: dict) -> Optional[List[StaticIPv4Address]]:
        secondary_address = []
        for address in address_configuration.get("secondary_address", []):
            secondary_address.append(self.get_static_ipv4_address(address))
        return secondary_address if secondary_address else None

    def configure_ipv6_address(
        self, values: dict
    ) -> Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]]:
        ipv6_address_configuration = values.get("ipv6")
        if not ipv6_address_configuration:
            return None
        if "address" in ipv6_address_configuration:
            return InterfaceStaticIPv6Address(
                static=StaticIPv6AddressConfig(
                    primary_ip_address=self.get_static_ipv6_address(ipv6_address_configuration),
                    secondary_ip_address=self.get_secondary_static_ipv6_address(ipv6_address_configuration),
                    dhcp_helper_v6=ipv6_address_configuration.get("dhcp_helper"),
                )
            )
        elif "dhcp_client" in ipv6_address_configuration:
            return InterfaceDynamicIPv6Address(
                dynamic=DynamicIPv6Dhcp(
                    dhcp_client=ipv6_address_configuration.get("dhcp_client"),
                    secondary_ipv6_address=ipv6_address_configuration.get("secondary_address"),
                )
            )
        return None

    def get_static_ipv6_address(self, address_configuration: dict) -> StaticIPv6Address:
        return StaticIPv6Address(address=address_configuration["address"])

    def get_secondary_static_ipv6_address(self, address_configuration: dict) -> Optional[List[StaticIPv6Address]]:
        secondary_address = []
        for address in address_configuration.get("secondary_address", []):
            secondary_address.append(self.get_static_ipv6_address(address))
        return secondary_address if secondary_address else None

    def configure_arp(self, values: dict) -> List[Arp]:
        arps = values.get("arp", {}).get("ip", [])
        arp_list = []
        for arp in arps:
            arp_list.append(Arp(ip_address=arp.get("addr", Default[None](value=None)), mac_address=arp.get("mac")))
        return arp_list

    def configure_advanced_attributes(self, values: dict) -> AdvancedEthernetAttributes:
        return AdvancedEthernetAttributes(
            duplex=self.parse_duplex(values),
            mac_address=values.get("mac_address"),
            speed=values.get("speed"),
            ip_mtu=values.get("mtu", as_default(value=1500)),
            interface_mtu=values.get("intrf_mtu", as_default(value=1500)),
            tcp_mss=values.get("tcp_mss_adjust"),
            arp_timeout=values.get("arp_timeout", as_default(value=1200)),
            autonegotiate=values.get("autonegotiate"),
            media_type=values.get("media_type"),
            load_interval=values.get("load_interval", as_default(value=30)),
            tracker=self.get_tracker_value(values),
            icmp_redirect_disable=values.get("icmp_redirect_disable", as_default(True)),
            xconnect=values.get("tloc_extension_gre_from", {}).get("xconnect"),
            ip_directed_broadcast=values.get("ip_directed_broadcast", as_default(False)),
        )

    def parse_duplex(self, data: Dict) -> Optional[Global[EthernetDuplexMode]]:
        if duplex := data.get("duplex"):
            return as_global(duplex.value, EthernetDuplexMode)
        return None

    def get_tracker_value(self, values: dict) -> Optional[Global[str]]:
        if tracker := values.get("tracker"):
            return as_global(",".join(tracker.value))
        return None

    def configure_trustsec(self, values: dict) -> Trustsec:
        return Trustsec(
            enable_sgt_propagation=values.get("propagate", {}).get("sgt", as_default(False)),
            security_group_tag=values.get("static", {}).get("sgt"),
            propagate=values.get("enable", as_default(False)),
            enable_enforced_propagation=values.get("enforced", {}).get("enable", Default[None](value=None)),
            enforced_security_group_tag=values.get("enforced", {}).get("sgt", Default[None](value=None)),
        )

    def configure_virtual_router_redundancy_protocol_ipv4(self, values: dict) -> List[VrrpIPv4]:
        vrrps = values.get("vrrp", [])
        vrrp_list = []
        for vrrp in vrrps:
            ip_address: Union[Global[str], Global[IPv4Address], Variable]
            address_ipv4 = vrrp.get("ipv4", {}).get("address")
            address = vrrp.get("address")
            if isinstance(address_ipv4, Global):
                ip_address = address_ipv4
            elif isinstance(address, Variable):
                ip_address = address
            if address_ipv4 is None and address is None:
                self._convert_result.update_status(
                    "partial",
                    "VRRP IPv4 address is required in UX2,"
                    "but in UX1 can be as default with empty value. VRRP group will not be created.",
                )
                continue
            vrrp_list.append(
                VrrpIPv4(
                    group_id=vrrp.get("grp_id", Default[int](value=1)),
                    priority=vrrp.get("priority", Default[int](value=100)),
                    timer=vrrp.get("timer", Default[int](value=1000)),
                    track_omp=vrrp.get("track_omp", Default[bool](value=False)),
                    ip_address=ip_address,
                    ip_address_secondary=self.get_vrrp_ipv4_secondary_addresses(vrrp),
                )
            )
        return vrrp_list

    def get_vrrp_ipv4_secondary_addresses(self, vrrp: dict) -> Optional[List[StaticIPv4Address]]:
        secondary_addresses = []
        for address in vrrp.get("ipv4", {}).get("ipv4_secondary", []):
            secondary_addresses.append(StaticIPv4Address(ip_address=address.get("address")))
        return secondary_addresses if secondary_addresses else None

    def configure_virtual_router_redundancy_protocol_ipv6(self, values: dict) -> List[VrrpIPv6]:
        vrrps_ipv6 = values.get("ipv6_vrrp", [])
        items = []
        for vrrp_ipv6 in vrrps_ipv6:
            vrrp_ipv6["group_id"] = vrrp_ipv6.pop("grp_id")
            items.append(VrrpIPv6(**vrrp_ipv6))
        return items

    def configure_network_address_translation(self, values: dict) -> Optional[EthernetNatAttributesIpv4]:
        nat = values.get("nat", {})
        if not nat or isinstance(nat, Global):
            return None
        # Nat can be straight up Global[bool] or a dict with more values
        nat_type = nat.get("nat_choice")
        if nat_type is None:
            nat_type = as_global("loopback", EthernetNatType)
        elif not isinstance(nat_type, Variable):
            nat_type = as_global(nat_type.value, EthernetNatType)
        return EthernetNatAttributesIpv4(
            nat_type=nat_type,
            nat_pool=self.get_nat_pool(nat),
            udp_timeout=nat.get("udp_timeout", as_default(1)),
            tcp_timeout=nat.get("tcp_timeout", as_default(60)),
            new_static_nat=nat.get("static"),
        )

    def get_nat_pool(self, values: dict) -> Optional[EthernetNatPool]:
        if nat_pool := values.get("natpool"):
            return EthernetNatPool(**nat_pool)
        return None

    def configure_acl_qos(self, values: dict) -> Optional[AclQos]:
        if shaping_rate := values.get("shaping_rate"):
            return AclQos(shaping_rate=shaping_rate)
        return None

    def configure_network_address_translation_ipv6(self, data: dict) -> Optional[NatAttributesIPv6]:
        if "nat66" in data:
            self._convert_result.update_status(
                "partial", "NAT66 is not supported in UX2. NAT66 configuration will not be migrated."
            )
            return None
        nat = data.get("nat64", Default[bool](value=False))
        if nat.value is False:
            return None
        return NatAttributesIPv6(nat64=nat)

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
