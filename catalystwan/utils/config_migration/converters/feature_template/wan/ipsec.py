# Copyright 2024 Cisco Systems, Inc. and its affiliates
from copy import deepcopy
from ipaddress import IPv6Address
from typing import Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, as_default, as_global
from catalystwan.models.common import IkeGroup, IpsecCiphersuite
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, TunnelApplication
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ipsec import (
    InterfaceIpsecParcel,
    PerfectForwardSecrecy,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none
from catalystwan.utils.config_migration.steps.constants import WAN_VPN_IPSEC


class WanInterfaceIpsecConverter(FTConverter):
    supported_template_types = (WAN_VPN_IPSEC,)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceIpsecParcel:
        data = deepcopy(template_values)

        if_name = data.get("if_name")
        if_description = data.get("description")
        application = self.parse_application(data)
        address = self.parse_address(data)
        tunnel_source = self.parse_tunnel_source(data)
        tunnel_destination = self.parse_tunnel_destination(data)
        mtu = data.get("mtu")
        tcp_mss_adjust = data.get("tcp_mss_adjust")
        dpd_interval = data.get("dead_peer_detection", {}).get("dpd_interval")
        dpd_retries = data.get("dead_peer_detection", {}).get("dpd_retires")
        ike = data.get("ike", {})
        ike_version = ike.get("ike_version")
        ike_rekey_interval = ike.get("ike_rekey_interval")
        ike_ciphersuite = ike.get("ike_ciphersuite")
        ike_group = self.parse_ike_group(data)
        authentication_type = ike.get("authentication_type", {})
        pre_shared_key = authentication_type.get("pre_shared_key", {})
        ike_local_id = pre_shared_key.get("ike_local_id")
        ike_remote_id = pre_shared_key.get("ike_remote_id")
        pre_shared_secret = self.parse_pre_shared_secret(data)
        ipsec_rekey_interval = data.get("ipsec", {}).get("ipsec_rekey_interval")
        ipsec_replay_window = data.get("ipsec", {}).get("ipsec_replay_window")
        ipsec_ciphersuite = self.parse_ipsec_cyphersuite(data)
        perfect_forward_secrecy = self.parse_perfect_forward_secrecy(data)
        clear_dont_fragment = data.get("clear_dont_fragment")
        tracker = self.parse_tracker(data)
        tunnel_source_interface = data.get("tunnel_source_interface")

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            if_name=if_name,
            if_description=if_description,
            application=application,
            address=address,
            tunnel_source=tunnel_source,
            tunnel_destination=tunnel_destination,
            mtu=mtu,
            tcp_mss_adjust=tcp_mss_adjust,
            dpd_interval=dpd_interval,
            dpd_retries=dpd_retries,
            ike_version=ike_version,
            ike_rekey_interval=ike_rekey_interval,
            ike_ciphersuite=ike_ciphersuite,
            ike_group=ike_group,
            ike_local_id=ike_local_id,
            ike_remote_id=ike_remote_id,
            pre_shared_secret=pre_shared_secret,
            ipsec_rekey_interval=ipsec_rekey_interval,
            ipsec_replay_window=ipsec_replay_window,
            ipsec_ciphersuite=ipsec_ciphersuite,
            perfect_forward_secrecy=perfect_forward_secrecy,
            clear_dont_fragment=clear_dont_fragment,
            tracker=tracker,
            tunnel_source_interface=tunnel_source_interface,
        )

        return InterfaceIpsecParcel(**payload)

    def parse_address(self, data: dict) -> AddressWithMask:
        address = data.get("ip", {}).get("address", {})
        if not address:
            raise CatalystwanConverterCantConvertException("Interface address is required")
        return AddressWithMask(
            address=as_global(address.value.network.network_address),
            mask=as_global(str(address.value.netmask)),
        )

    def parse_tunnel_source(self, data: dict) -> AddressWithMask:
        tunnel_source = data.get("tunnel_source")
        if not tunnel_source:
            raise CatalystwanConverterCantConvertException("Tunnel source is required")
        return AddressWithMask(
            address=tunnel_source,
            mask=as_global("0.0.0.0"),  # UI sends this
        )

    def parse_tunnel_destination(self, data: dict) -> AddressWithMask:
        tunnel_destination = data.get("tunnel_destination")
        if not tunnel_destination:
            raise CatalystwanConverterCantConvertException("Tunnel destination is required")
        if isinstance(tunnel_destination.value, IPv6Address):
            raise CatalystwanConverterCantConvertException("IPv6 is not supported for tunnel destination")
        return AddressWithMask(
            address=tunnel_destination,
            mask=as_global("0.0.0.0"),  # UI sends this
        )

    def parse_pre_shared_secret(self, data: dict) -> Global[str]:
        pre_shared_secret = (
            data.get("ike", {}).get("authentication_type", {}).get("pre_shared_key", {}).get("pre_shared_secret")
        )
        if pre_shared_secret:
            return pre_shared_secret
        raise CatalystwanConverterCantConvertException("Pre-shared key is required")

    def parse_application(self, data: dict) -> Global[TunnelApplication]:
        application = data.get("application")
        if application:
            return as_global(application.value, TunnelApplication)
        raise CatalystwanConverterCantConvertException("Application is required")

    def parse_ipsec_cyphersuite(self, data: dict) -> Union[Global[IpsecCiphersuite], Default[IpsecCiphersuite]]:
        if ipsec_cyphersuite := data.get("ipsec", {}).get("ipsec_cyphersuite"):
            return as_global(ipsec_cyphersuite.value, IpsecCiphersuite)
        return as_default("aes256-gcm", IpsecCiphersuite)

    def parse_perfect_forward_secrecy(
        self, data: dict
    ) -> Union[Global[PerfectForwardSecrecy], Default[PerfectForwardSecrecy]]:
        if perfect_forward_secrecy := data.get("ipsec", {}).get("perfect_forward_secrecy"):
            return as_global(perfect_forward_secrecy.value, PerfectForwardSecrecy)
        return as_default("group-16", PerfectForwardSecrecy)

    def parse_ike_group(self, data: dict) -> Optional[Global[str]]:
        if ike_group := data.get("ike", {}).get("ike_group"):
            return as_global(ike_group.value, IkeGroup)
        return None

    def parse_tracker(self, data: dict) -> Default[None]:
        # TODO: Implement tracker
        self._convert_result.update_status(
            "partial", "Tracker is set as default value. It should be implemented in the future."
        )
        return Default[None](value=None)
