# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from copy import deepcopy
from typing import Dict, List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_default, as_global
from catalystwan.models.common import CarrierType, EncapType, EthernetDuplexMode, EthernetNatType, Speed
from catalystwan.models.configuration.feature_profile.common import (
    AclQos,
    AllowService,
    Arp,
    DynamicDhcpDistance,
    DynamicIPv6Dhcp,
    Encapsulation,
    EthernetNatAttributesIpv4,
    EthernetNatPool,
    InterfaceDynamicIPv4Address,
    InterfaceDynamicIPv6Address,
    InterfaceStaticIPv4Address,
    StaticIPv4Address,
    StaticIPv4AddressConfig,
    StaticIPv6Address,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    Advanced,
    InterfaceEthernetParcel,
    InterfaceStaticIPv6Address,
    Static,
    TlocExtensionGreFrom,
    Tunnel,
)
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none
from catalystwan.utils.config_migration.converters.utils import parse_interface_name
from catalystwan.utils.config_migration.steps.constants import WAN_VPN_ETHERNET

logger = logging.getLogger(__name__)


class WanInterfaceEthernetConverter(FTConverter):
    supported_template_types = (WAN_VPN_ETHERNET,)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceEthernetParcel:
        data = deepcopy(template_values)

        encapsulation = self.parse_encapsulations(data.get("tunnel_interface", {}).get("encapsulation", []))
        interface_name = parse_interface_name(self, data)
        interface_description = data.get(
            "description", as_global(description)
        )  # Edge case where model doesn't have description but its required
        interface_ip_address = self.parse_interface_ip_address(data)
        tunnel_interface = self.parse_tunnel_interface(data)
        shutdown = data.get("shutdown")
        nat = self.parse_nat(data)
        nat_attributes_ipv4 = self.configure_network_address_translation(data)
        acl_qos = self.parse_acl_qos(data)
        advanced = self.parse_advanced(data)
        allow_service = self.parse_allow_service(data.get("allow_service", {}))
        arp = self.parse_arp(data)
        auto_detect_bandwidth = data.get("auto_detect_bandwidth")
        bandwidth_downstream = data.get("bandwidth_downstream")
        bandwidth_upstream = data.get("bandwidth_upstream")
        ipref_server = data.get("ipref_server")
        intf_ip_v6_address = self.parse_ipv6_address(data)
        block_non_source_ip = data.get("block_non_source_ip")
        service_provider = data.get("service_provider")
        dhcp_helper = data.get("dhcp_helper")
        tunnel = self.parse_tunnel(data)

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            encapsulation=encapsulation,
            interface_name=interface_name,
            interface_description=interface_description,
            interface_ip_address=interface_ip_address,
            tunnel_interface=tunnel_interface,
            shutdown=shutdown,
            nat=nat,
            nat_attributes_ipv4=nat_attributes_ipv4,
            acl_qos=acl_qos,
            advanced=advanced,
            allow_service=allow_service,
            arp=arp,
            auto_detect_bandwidth=auto_detect_bandwidth,
            bandwidth_downstream=bandwidth_downstream,
            bandwidth_upstream=bandwidth_upstream,
            intf_ip_v6_address=intf_ip_v6_address,
            ipref_server=ipref_server,
            block_non_source_ip=block_non_source_ip,
            service_provider=service_provider,
            dhcp_helper=dhcp_helper,
            tunnel=tunnel,
        )

        return InterfaceEthernetParcel(**payload)

    def parse_encapsulations(self, encapsulation: List[Dict]) -> List[Encapsulation]:
        return [self.create_encapsulation(encap) for encap in encapsulation]

    def create_encapsulation(self, encapsulation: Dict) -> Encapsulation:
        if encap := encapsulation.get("encap"):
            encap = as_global(encap.value, EncapType)
        return Encapsulation(
            preference=encapsulation.get("preference"),
            weight=encapsulation.get("weight"),
            encap=encap,
        )

    def parse_tunnel_interface(self, data: Dict) -> Optional[Global[bool]]:
        if data.get("tunnel_interface"):
            return as_global(True)
        return None

    def parse_interface_ip_address(self, data: Dict) -> Union[InterfaceDynamicIPv4Address, InterfaceStaticIPv4Address]:
        ip_address = data.get("ip", {})

        if "address" in ip_address and ip_address["address"].value != "":
            return InterfaceStaticIPv4Address(
                static=StaticIPv4AddressConfig(
                    primary_ip_address=self.get_static_ipv4_address(ip_address),
                    secondary_ip_address=self.get_secondary_static_ipv4_address(ip_address),
                )
            )

        elif "dhcp_client" in ip_address:
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

    def parse_nat(self, data: dict) -> Optional[Global[bool]]:
        if nat := data.get("nat"):
            if isinstance(nat, dict):
                return as_global(True)
        return None

    def configure_network_address_translation(self, values: dict) -> Optional[EthernetNatAttributesIpv4]:
        nat = values.get("nat", {})
        if not nat or isinstance(nat, Global):
            # Nat can be straight up Global[bool] or a dict with more values
            return None

        nat_pool = self.get_nat_pool(nat)
        nat_type = nat.get("nat_choice")
        if not nat_type:
            if nat_pool:
                nat_type = Global[EthernetNatType](value="pool")
            else:
                nat_type = Global[EthernetNatType](value="loopback")

        nat_type = as_global(nat_type.value, EthernetNatType)

        payload = create_dict_without_none(
            nat_type=nat_type,
            nat_pool=nat_pool,
            udp_timeout=nat.get("udp_timeout"),
            tcp_timeout=nat.get("tcp_timeout"),
            new_static_nat=nat.get("static"),
        )

        return EthernetNatAttributesIpv4(**payload)

    def get_nat_pool(self, values: dict) -> Optional[EthernetNatPool]:
        if nat_pool := values.get("natpool"):
            return EthernetNatPool(**nat_pool)
        return None

    def parse_acl_qos(self, data: Dict) -> Optional[AclQos]:
        if shaping_rate := data.get("shaping_rate"):
            return AclQos(shaping_rate=shaping_rate)
        return None

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
            tloc_extension=data.get("tloc_extension"),
            tloc_extension_gre_from=self.parse_tloc_extension_gre_from(data),
            tracker=self.parse_tracker(data),
        )

        if not payload:
            return None

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

    def parse_tloc_extension_gre_from(self, data: Dict) -> Optional[TlocExtensionGreFrom]:
        if tloc_extension_gre_from := data.get("tloc_extension_gre_from"):
            return TlocExtensionGreFrom(
                source_ip=tloc_extension_gre_from.get("src_ip"),
                xconnect=tloc_extension_gre_from.get("xconnect"),
            )
        return None

    def parse_allow_service(self, allow_service: Dict) -> AllowService:
        return AllowService(**allow_service)

    def parse_arp(self, data: dict) -> Optional[List[Arp]]:
        arps = data.get("arp", {}).get("ip", [])
        if not arps:
            return None
        return [Arp(ip_address=arp.get("addr", Default[None](value=None)), mac_address=arp.get("mac")) for arp in arps]

    def parse_ipv6_address(
        self, data: dict
    ) -> Optional[Union[InterfaceDynamicIPv6Address, InterfaceStaticIPv6Address]]:
        if ipv6_address_configuration := data.get("ipv6"):
            if "address" in ipv6_address_configuration:
                return InterfaceStaticIPv6Address(
                    static=Static(
                        primary_ip_v6_address=self.get_static_ipv6_address(ipv6_address_configuration),
                        secondary_ip_v6_address=self.get_secondary_static_ipv6_address(ipv6_address_configuration),
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

    def parse_tunnel(self, data: Dict) -> Optional[Tunnel]:
        ti = data.get("tunnel_interface", {})

        return Tunnel(
            bandwidth_percent=ti.get("bandwidth_percent"),
            bind=ti.get("bind"),
            border=ti.get("border"),
            carrier=self.parse_carrier(ti),
            clear_dont_fragment=data.get("clear_dont_fragment"),
            color=ti.get("color", {}).get("value"),
            cts_sgt_propagation=ti.get("cts_sgt_propagation"),
            exclude_controller_group_list=ti.get("exclude_controller_group_list"),
            group=self.parse_group(ti),
            hello_interval=ti.get("hello_interval"),
            hello_tolerance=ti.get("hello_tolerance"),
            last_resort_circuit=ti.get("last_resort_circuit"),
            low_bandwidth_link=ti.get("low_bandwidth_link"),
            max_control_connections=ti.get("max_control_connections"),
            mode=ti.get("mode"),
            nat_refresh_interval=ti.get("nat_refresh_interval"),
            network_broadcast=ti.get("network_broadcast"),
            per_tunnel_qos=ti.get("per_tunnel_qos"),
            port_hop=ti.get("port_hop"),
            restrict=ti.get("color", {}).get("restrict"),
            tloc_extension_gre_to=ti.get("tloc_extension_gre_to", {}).get("dst_ip"),
            tunnel_tcp_mss=ti.get("tunnel_tcp_mss"),
            v_bond_as_stun_server=ti.get("vbond_as_stun_server"),
            v_manage_connection_preference=ti.get("v_manage_connection_preference"),
        )

    def parse_carrier(self, data: Dict) -> Optional[Global[CarrierType]]:
        if carrier := data.get("carrier"):
            return as_global(carrier.value, CarrierType)
        return None

    def parse_group(self, data: Dict) -> Optional[Global[int]]:
        if group := data.get("group"):
            return as_global(group.value[0])
        return None
