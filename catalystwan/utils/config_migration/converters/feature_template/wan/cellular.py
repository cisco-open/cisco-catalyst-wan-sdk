from copy import deepcopy
from typing import Dict, List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, as_default, as_global
from catalystwan.models.common import EncapType
from catalystwan.models.configuration.feature_profile.common import Encapsulation
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    Advanced,
    AllowService,
    Arp,
    InterfaceCellularParcel,
    NatAttributesIpv4,
    Tunnel,
)
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none


class InterfaceCellularConverter(FTConverter):
    supported_template_types = ("vpn-vedge-interface-cellular", "vpn-cedge-interface-cellular")

    def create_parcel(self, name: str, description: str, template_values: Dict) -> InterfaceCellularParcel:
        """
        Create a new InterfaceCellularParcel object.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (Dict): A Dictionary containing template values.

        Returns:
            InterfaceCellularParcel: The created InterfaceCellularParcel object.
        """
        data = deepcopy(template_values)

        tunnel_interface = data.get("tunnel_interface", {})
        nat = data.get("nat", {})

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            interface_name=data.get("if_name"),
            shutdown=data.get("shutdown"),
            dhcp_helper=data.get("dhcp_helper"),
            bandwidth_upstream=data.get("bandwidth_upstream"),
            bandwidth_downstream=data.get("bandwidth_downstream"),
            encapsulation=self.parse_encapsulation(tunnel_interface.get("encapsulation", [])),
            allow_service=self.parse_allow_service(tunnel_interface.get("allow_service", {})),
            service_provider=data.get("service_provider"),
            arp=self.parse_arp(data),
            nat_attributes_ipv4=self.parse_nat_attributes(nat),
            nat=self.parse_nat(nat),
            tunnel=self.parse_tunnel(data),
            tunnel_interface=self.parse_tunnel_interface(data),
            advanced=self.parse_advanced(data),
        )

        return InterfaceCellularParcel(interface_description=data.get("description"), **payload)

    def parse_encapsulation(self, encapsulations: List[Dict]) -> List[Encapsulation]:
        return [
            Encapsulation(
                encap=self.parse_encap(enc),
                preference=enc.get("preference"),
                weight=enc.get("weight"),
            )
            for enc in encapsulations
        ]

    def parse_encap(self, encap: Dict) -> Optional[Global[EncapType]]:
        if enc := encap.get("encap"):
            return as_global(enc.value, EncapType)
        return None

    def parse_allow_service(self, allow_service: Dict) -> AllowService:
        return AllowService(**allow_service)

    def parse_nat(self, nat: Dict) -> Union[Global[bool], Default[bool]]:
        if not nat:
            return as_default(False)
        return as_global(True)

    def parse_nat_attributes(self, nat: Dict) -> Optional[NatAttributesIpv4]:
        if not nat:
            return None

        payload = create_dict_without_none(udp_timeout=nat.get("udp_timeout"), tcp_timeout=nat.get("tcp_timeout"))

        return NatAttributesIpv4(**payload)

    def parse_tunnel(self, data: Dict) -> Optional[Tunnel]:
        tunnel_data = data.get("tunnel_interface")
        if not tunnel_data:
            return None

        return Tunnel(
            border=tunnel_data.get("border"),
            clear_dont_fragment=tunnel_data.get("clear_dont_fragment"),
            color=tunnel_data.get("color", {}).get("value"),
            low_bandwidth_link=tunnel_data.get("low_bandwidth_link"),
            max_control_connections=tunnel_data.get("max_control_connections"),
            mode=tunnel_data.get("mode"),
            network_broadcast=tunnel_data.get("network_broadcast"),
            per_tunnel_qos=tunnel_data.get("per_tunnel_qos"),
            port_hop=tunnel_data.get("port_hop"),
            restrict=tunnel_data.get("color", {}).get("restrict"),
            tunnel_tcp_mss=tunnel_data.get("tunnel_tcp_mss_adjust"),
            vbond_as_stun_server=tunnel_data.get("vbond_as_stun_server"),
            vmanage_connection_preference=tunnel_data.get("vmanage_connection_preference"),
        )

    def parse_tunnel_interface(self, data: Dict) -> Union[Global[bool], Default[bool]]:
        if not data.get("tunnel_interface"):
            return as_default(False)
        return as_global(True)

    def parse_arp(self, data: Dict) -> Optional[List[Arp]]:
        arp = data.get("arp", {}).get("ip", [])
        if not arp:
            return None

        return [Arp(ip_address=entry.get("addr"), mac_address=entry.get("mac")) for entry in arp]

    def parse_advanced(self, data: Dict) -> Optional[Advanced]:
        intrf_mtu = data.get("mtu")
        ip_directed_broadcast = data.get("ip_directed_broadcast")
        tloc_extension = data.get("tloc_extension")
        tcp_mss = data.get("tcp_mss_adjust")
        tracker = data.get("tracker")
        if tracker:
            tracker = as_global(",".join(tracker.value))

        if intrf_mtu or ip_directed_broadcast or tloc_extension or tracker or tcp_mss:
            return Advanced(
                intrf_mtu=intrf_mtu,
                ip_directed_broadcast=ip_directed_broadcast,
                tloc_extension=tloc_extension,
                tracker=tracker,
                tcp_mss=tcp_mss,
            )
        return None
