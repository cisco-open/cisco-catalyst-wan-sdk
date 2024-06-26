from copy import deepcopy
from ipaddress import IPv4Address, IPv4Interface
from typing import Optional

from catalystwan.api.configuration_groups.parcel import Default, Global, as_global
from catalystwan.models.configuration.feature_profile.common import (
    AddressWithMask,
    AdvancedGre,
    SourceIp,
    SourceNotLoopback,
    TunnelApplication,
    TunnelSourceType,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.gre import Basic, InterfaceGreParcel
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.steps.constants import WAN_VPN_GRE


class WanInterfaceGreConverter(FTConverter):
    supported_template_types = (WAN_VPN_GRE,)

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

    def parse_basic(self, data: dict) -> Basic:
        interface_name = data.get("if_name")
        if not interface_name:
            raise CatalystwanConverterCantConvertException("Interface name is required")

        description = data.get("description", Default[None](value=None))
        address = self.parse_address(data)
        tunnel_destination = self.parse_tunnel_destination(data)
        shutdown = data.get("shutdown")
        tunnel_source_type = self.parse_tunnel_source_type(data)
        mtu = data.get("mtu")
        tcp_mss_adjust = data.get("tcp_mss_adjust")
        clear_dont_fragment = data.get("clear_dont_fragment")

        return Basic(
            if_name=interface_name,
            description=description,
            address=address,
            tunnel_destination=tunnel_destination,
            shutdown=shutdown,
            tunnel_source_type=tunnel_source_type,
            mtu=mtu,
            tcp_mss_adjust=tcp_mss_adjust,
            clear_dont_fragment=clear_dont_fragment,
        )

    def parse_address(self, data: dict) -> AddressWithMask:
        address = data.get("ip", {}).get("address", {})
        if not address:
            # TODO: Ask technitians if there can be default value for address
            raise CatalystwanConverterCantConvertException("Address is required")
        return AddressWithMask(
            address=as_global(address.value.network.network_address),
            mask=as_global(str(address.value.netmask)),
        )

    def parse_tunnel_destination(self, data: dict) -> Global[IPv4Address]:
        destination = data.get("tunnel_destination")
        if not destination:
            raise CatalystwanConverterCantConvertException("Tunnel destination is required")
        return destination

    def parse_tunnel_source_type(self, data: dict) -> TunnelSourceType:
        tunnel_source: Optional[Global[IPv4Address]] = data.get("tunnel_source")
        tunnel_source_interface: Optional[Global[IPv4Interface]] = data.get("tunnel_source_interface")

        if tunnel_source and tunnel_source_interface:
            raise CatalystwanConverterCantConvertException(
                "Tunnel source and tunnel source interface are mutually exclusive"
            )

        if tunnel_source:
            return TunnelSourceType(
                source_ip=SourceIp(
                    tunnel_source=tunnel_source,
                )
            )

        if tunnel_source_interface:
            return TunnelSourceType(
                source_not_loopback=SourceNotLoopback(
                    tunnel_source_interface=tunnel_source_interface,
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
