from copy import deepcopy
from ipaddress import IPv4Address, IPv6Address
from typing import Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, as_global
from catalystwan.models.configuration.feature_profile.common import (
    AddressWithMask,
    SourceIp,
    SourceNotLoopback,
    TunnelApplication,
    TunnelSourceType,
)
from catalystwan.models.configuration.feature_profile.sdwan.service import InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import (
    AdvancedGre,
    BasicGre,
    GreSourceIPv6,
    TunnelSourceIPv6,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.steps.constants import LAN_VPN_GRE


class LanInterfaceGreConverter(FTConverter):
    supported_template_types = (LAN_VPN_GRE,)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceGreParcel:
        """
        Create a new InterfaceGreParcel object.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing template values.

        Returns:
            InterfaceGreParcel: The created InterfaceGreParcel object.
        """
        data = deepcopy(template_values)

        basic = self.parse_basic(data)
        advanced = self.parse_advanced(data)

        return InterfaceGreParcel(
            parcel_name=name,
            parcel_description=description,
            basic=basic,
            advanced=advanced,
        )

    def parse_basic(self, data: dict) -> BasicGre:
        interface_name = data.get("if_name")
        if not interface_name:
            raise CatalystwanConverterCantConvertException("Interface name is required")

        description = data.get("description", Default[None](value=None))
        address = self.parse_address(data)
        tunnel_destination = self.parse_tunnel_destination(data)
        ipv6_address = data.get("ipv6", {}).get("address")
        shutdown = data.get("shutdown")
        tunnel_protection = data.get("tunnel_protection")
        tunnel_source_type = self.parse_tunnel_source_type(data)
        mtu = data.get("mtu")
        tcp_mss_adjust = data.get("tcp_mss_adjust")
        clear_dont_fragment = data.get("clear_dont_fragment")
        dpd_interval = self.parse_dpd_internal(data)
        dpd_retries = self.parse_dpd_retries(data)

        return BasicGre(
            if_name=interface_name,
            description=description,
            address=address,
            tunnel_destination=tunnel_destination,
            ipv6_address=ipv6_address,
            shutdown=shutdown,
            tunnel_protection=tunnel_protection,
            tunnel_source_type=tunnel_source_type,
            mtu=mtu,
            tcp_mss_adjust=tcp_mss_adjust,
            clear_dont_fragment=clear_dont_fragment,
            dpd_interval=dpd_interval,
            dpd_retries=dpd_retries,
        )

    def parse_address(self, data: dict) -> Optional[AddressWithMask]:
        address = data.get("ip", {}).get("address", {})
        if not address:
            return None
        return AddressWithMask(
            address=as_global(address.value.network.network_address),
            mask=as_global(str(address.value.netmask)),
        )

    def parse_tunnel_destination(self, data: dict) -> Global[IPv4Address]:
        destination = data.get("tunnel_destination")
        if not destination:
            raise CatalystwanConverterCantConvertException("Tunnel destination is required")
        return destination

    def parse_tunnel_source_type(self, data: dict) -> Union[TunnelSourceType, GreSourceIPv6]:
        tunnel_source = data.get("tunnel_source")
        tunnel_source_interface = data.get("tunnel_source_interface")
        tunnel_source_ipv6: Optional[Global[IPv6Address]] = data.get("tunnel_source_v6")

        if tunnel_source and (tunnel_source_interface or tunnel_source_ipv6):
            raise CatalystwanConverterCantConvertException(
                "Tunnel source and tunnel source interface/IPv6 are mutually exclusive"
            )

        if tunnel_source:
            return TunnelSourceType(
                source_ip=SourceIp(
                    tunnel_source=tunnel_source,
                )
            )

        if tunnel_source_interface:
            # UI is sending SourceNotLoopback
            return TunnelSourceType(
                source_not_loopback=SourceNotLoopback(
                    tunnel_source_interface=tunnel_source_interface,
                )
            )

        if tunnel_source_ipv6:
            return GreSourceIPv6(
                source_ipv6=TunnelSourceIPv6(
                    tunnel_source_v6=tunnel_source_ipv6,
                    tunnel_route_via=data.get("tunnel_route_via"),
                )
            )

        raise CatalystwanConverterCantConvertException("Tunnel source is required")

    def parse_dpd_internal(self, data: dict) -> Optional[Global[int]]:
        return data.get("dead_peer_detection", {}).get("dpd_interval")

    def parse_dpd_retries(self, data: dict) -> Optional[Global[int]]:
        return data.get("dead_peer_detection", {}).get("dpd_retries")

    def parse_advanced(self, data: dict) -> Optional[AdvancedGre]:
        application = data.get("application")
        if not application:
            return None
        return AdvancedGre(
            application=as_global(application.value, TunnelApplication),
        )
