# Copyright 2023 Cisco Systems, Inc. and its affiliates
from copy import deepcopy
from ipaddress import IPv4Address, IPv4Interface, IPv6Address

from catalystwan.api.configuration_groups.parcel import Default, Variable, as_default, as_global, as_variable
from catalystwan.models.common import IkeGroup
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, TunnelApplication
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecParcel
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.steps.constants import LAN_VPN_IPSEC


class LanInterfaceIpsecConverter(FTConverter):
    supported_template_types = (LAN_VPN_IPSEC,)

    # Default Values
    pre_shared_secret = "{{vpn_if_pre_shared_secret}}"

    delete_keys = (
        "dead_peer_detection",
        "if_name",
        "description",
        "ike",
        "authentication_type",
        "multiplexing",
        "ipsec",
        "ipv6",
        "ip",
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceIpsecParcel:
        values = deepcopy(template_values)
        self.configure_interface_name(values)
        self.configure_description(values)
        self.configure_dead_peer_detection(values)
        self.configure_ike(values)
        self.configure_ipsec(values)
        self.configure_tunnel_destination(values)
        self.configure_tunnel_source(values)
        self.configure_ipv6_address(values)
        self.configure_address(values)
        self.configure_tracker(values)
        self.configure_application(values)
        self.configure_pre_shared_secret(values)
        self.cleanup_keys(values)
        return InterfaceIpsecParcel(parcel_name=name, parcel_description=description, **values)

    def configure_interface_name(self, values: dict) -> None:
        values["interface_name"] = values.get("if_name")

    def configure_description(self, values: dict) -> None:
        values["ipsec_description"] = values.get("description", Default[None](value=None))

    def configure_dead_peer_detection(self, values: dict) -> None:
        values["dpd_interval"] = values.get("dead_peer_detection", {}).get("dpd_interval", as_default(10))
        values["dpd_retries"] = values.get("dead_peer_detection", {}).get("dpd_retries", as_default(3))

    def configure_ipv6_address(self, values: dict) -> None:
        values["ipv6_address"] = values.get("ipv6", {}).get("address")

    def configure_address(self, values: dict) -> None:
        address = values.get("ip", {}).get("address", {})
        if not address:
            raise CatalystwanConverterCantConvertException(
                "Ipsec Address is required in UX2 parcel but in a Feature Template can be optional."
            )
        values["address"] = AddressWithMask(
            address=as_global(str(address.value.network.network_address)),
            mask=as_global(str(address.value.network.netmask)),
        )

    def configure_ike(self, values: dict) -> None:
        ike = values.get("ike", {})
        if ike:
            if ike_group := ike.get("ike_group"):
                ike["ike_group"] = as_global(ike_group.value, IkeGroup)
            ike.update(ike.get("authentication_type", {}).get("pre_shared_key", {}))
        values.update(ike)

    def configure_ipsec(self, values: dict) -> None:
        values.update(values.get("ipsec", {}))

    def configure_tunnel_destination(self, values: dict) -> None:
        if tunnel_destination := values.get("tunnel_destination"):
            if isinstance(tunnel_destination.value, IPv4Interface):
                values["tunnel_destination"] = AddressWithMask(
                    address=as_global(str(tunnel_destination.value.network.network_address)),
                    mask=as_global(str(tunnel_destination.value.network.netmask)),
                )
            elif isinstance(tunnel_destination.value, IPv4Address):
                values["tunnel_destination"] = AddressWithMask(
                    address=tunnel_destination,
                    mask=as_global("0.0.0.0"),
                )
            elif isinstance(tunnel_destination, Variable):
                values["tunnel_destination"] = AddressWithMask(
                    address=tunnel_destination,
                    mask=as_global("0.0.0.0"),
                )

            elif isinstance(tunnel_destination.value, IPv6Address):
                # 20.12, 20.13 dont have tunnel_destination_v6
                # TODO: pass version to converter
                values["tunnel_destination"] = AddressWithMask(
                    address=as_variable(value="ipsec_tunnelDestination_addr"),
                    mask=as_global("0.0.0.0"),
                )

                # values.pop("tunnel_destination")
                # values["tunnel_destination_v6"] = tunnel_destination

    def configure_tunnel_source(self, values: dict) -> None:
        if tunnel_source := values.get("tunnel_source"):
            values["tunnel_source"] = AddressWithMask(
                address=as_global(str(tunnel_source.value)),
                mask=as_global("0.0.0.0"),
            )

    def configure_tracker(self, values: dict) -> None:
        tracker = values.get("tracker")
        if tracker:
            tracker = as_global("".join(tracker.value))
        values["tracker"] = tracker

    def configure_application(self, values: dict) -> None:
        if application := values.get("application"):
            values["application"] = as_global(application.value, TunnelApplication)

    def configure_pre_shared_secret(self, values: dict) -> None:
        values["pre_shared_secret"] = values.get("pre_shared_secret", as_variable(self.pre_shared_secret))

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)
