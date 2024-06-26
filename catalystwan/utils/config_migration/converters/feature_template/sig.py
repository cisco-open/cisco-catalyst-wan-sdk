from ipaddress import IPv4Address, IPv4Interface
from typing import Any, List, Optional, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.configuration.feature_profile.sdwan.sig_security.sig_security import (
    Interface,
    InterfacePair,
    IpsecCiphersuite,
    Service,
    SIGParcel,
    SigProvider,
    Tracker,
)
from catalystwan.utils.config_migration.converters.feature_template.model_definition_normalizer import (
    flatten_datapaths,
    normalize_to_model_definition,
)

from .base import FTConverter


class SIGConverter(FTConverter):
    supported_template_types = ("secure-internet-gateway", "cisco_secure_internet_gateway")

    PROVIDER_MAP = {
        "secure-internet-gateway-umbrella": Global[SigProvider](value="Umbrella"),
        "secure-internet-gateway-zscaler": Global[SigProvider](value="Zscaler"),
        "secure-internet-gateway-other": Global[SigProvider](value="Generic"),
    }

    def create_parcel(self, name: str, description: str, template_values: dict) -> SIGParcel:
        return SIGParcel(
            parcel_name=name,
            parcel_description=description,
            sig_provider=self.get_sig_provider(template_values.get("interface", [])),  # type: ignore
            interface=self.parse_interface(template_values.get("interface", [])),
            service=self.parse_service(template_values.get("service")),  # type: ignore
            tracker_src_ip=self.get_tracker_src_ip(template_values),  # type: ignore
            tracker=self.parse_tracker(template_values.get("tracker", [])),
        )

    def parse_service(self, service: List[dict]) -> Optional[Service]:
        if not service:
            return None
        # Service is a list, either empty or of single element
        service_value = service[0]
        flattened_values = flatten_datapaths(service_value)
        normalized_values = normalize_to_model_definition(flattened_values, Service.model_fields)
        return Service(
            interface_pair=self.parse_interface_pair(normalized_values.get("interface_pair", [])),  # type: ignore
            auth_required=normalized_values.get("auth_required"),
            xff_forward_enabled=normalized_values.get("xff_forward_enabled"),
            ofw_enabled=normalized_values.get("ofw_enabled"),
            ips_control=normalized_values.get("ips_control"),
            caution_enabled=normalized_values.get("caution_enabled"),
            primary_data_center=normalized_values.get("primary_data_center"),
            secondary_data_center=normalized_values.get("secondary_data_center"),
            ip=normalized_values.get("ip"),
            idle_time=normalized_values.get("idle_time"),
            display_time_unit=normalized_values.get("display_time_unit"),
            ip_enforced_for_known_browsers=normalized_values.get("ip_enforced_for_known_browsers"),
            refresh_time=normalized_values.get("refresh_time"),
            refresh_time_unit=normalized_values.get("refresh_time_unit"),
            enabled=normalized_values.get("enabled"),
            block_internet_until_accepted=normalized_values.get("block_internet_until_accepted"),
            force_ssl_inspection=normalized_values.get("force_ssl_inspection"),
            timeout=normalized_values.get("timeout"),
            location_name=normalized_values.get("location_name"),
            data_center_primary=normalized_values.get("data_center_primary"),
            data_center_secondary=normalized_values.get("data_center_secondary"),
        )

    def parse_interface_pair(self, interface_pair_values: List[dict]) -> Optional[List[InterfacePair]]:
        if not interface_pair_values:
            return None
        interface_pair = []
        for interface_pair_value in interface_pair_values:
            interface_pair.append(
                InterfacePair(
                    active_interface=interface_pair_value.get("active_interface"),  # type: ignore
                    backup_interface=interface_pair_value.get("backup_interface"),  # type: ignore
                    active_interface_weight=interface_pair_value.get("active_interface_weight"),  # type: ignore
                    backup_interface_weight=interface_pair_value.get("backup_interface_weight"),  # type: ignore
                )
            )

        return interface_pair

    def parse_tracker(self, tracker_values: List[dict]) -> List[Tracker]:
        tracker_list = []
        for tracker_value in tracker_values:
            flattened_values = flatten_datapaths(tracker_value)
            normalized_values = normalize_to_model_definition(flattened_values, Tracker.model_fields)
            tracker_list.append(
                Tracker(
                    name=normalized_values.get("name"),  # type: ignore
                    endpoint_api_url=normalized_values.get("endpoint_api_url"),  # type: ignore
                    threshold=normalized_values.get("threshold", Default[int](value=300)),
                    interval=normalized_values.get("interval", Default[int](value=60)),
                    multiplier=normalized_values.get("multiplier", Default[int](value=3)),
                    tracker_type=normalized_values.get("tracker_type"),  # type: ignore
                )
            )

        return tracker_list

    def parse_interface(self, interface_values: List[dict]) -> List[Interface]:
        interface_list = []
        for interface_value in interface_values:
            flattened_values = flatten_datapaths(interface_value)
            normalized_values = normalize_to_model_definition(flattened_values, Interface.model_fields)
            interface_list.append(
                Interface(
                    if_name=normalized_values.get("if_name"),  # type: ignore
                    auto=normalized_values.get("auto"),
                    shutdown=normalized_values.get("shutdown"),  # type: ignore
                    description=normalized_values.get("description"),
                    unnumbered=normalized_values.get("unnumbered"),
                    address=normalized_values.get("address"),
                    tunnel_source=normalized_values.get("tunnel_source"),
                    tunnel_source_interface=normalized_values.get("tunnel_source_interface"),  # type: ignore
                    tunnel_route_via=normalized_values.get("tunnel_route_via"),
                    tunnel_destination=normalized_values.get("tunnel_destination"),
                    application=normalized_values.get("application"),
                    tunnel_set=normalized_values.get("tunnel_set"),
                    tunnel_dc_preference=normalized_values.get("tunnel_dc_preference"),
                    tcp_mss_adjust=normalized_values.get("tcp_mss_adjust"),
                    mtu=normalized_values.get("mtu"),  # type: ignore
                    dpd_interval=normalized_values.get("dpd_interval"),
                    dpd_retries=normalized_values.get("dpd_retries"),
                    ike_version=normalized_values.get("ike_version"),
                    pre_shared_secret=normalized_values.get("pre_shared_secret"),
                    ike_rekey_interval=normalized_values.get("ike_rekey_interval"),
                    ike_ciphersuite=normalized_values.get("ike_ciphersuite"),
                    ike_group=normalized_values.get("ike_group"),
                    pre_shared_key_dynamic=normalized_values.get("pre_shared_key_dynamic"),
                    ike_local_id=normalized_values.get("ike_local_id"),
                    ike_remote_id=normalized_values.get("ike_remote_id"),
                    ipsec_rekey_interval=normalized_values.get("ipsec_rekey_interval"),
                    ipsec_replay_window=normalized_values.get("ipsec_replay_window"),
                    ipsec_ciphersuite=self.get_ipsec_ciphersuite(normalized_values),
                    perfect_forward_secrecy=normalized_values.get("perfect_forward_secrecy"),
                    tracker=normalized_values.get("tracker"),
                    track_enable=normalized_values.get("track_enable"),
                    tunnel_public_ip=normalized_values.get("tunnel_public_ip"),
                )
            )
        return interface_list

    def get_sig_provider(self, interface_values: List[dict]) -> Optional[Global[SigProvider]]:
        if not interface_values:
            return None
        # All interface values should have the same sig provider value
        for interface_value in interface_values:
            sig_provider = interface_value.get("tunnel_set")
            if sig_provider is not None:
                return self.PROVIDER_MAP.get(sig_provider.value)

        return None

    def get_tracker_src_ip(self, template_values: dict) -> Optional[Global[IPv4Address]]:
        tracker_src_ip = template_values.get("tracker_src_ip")
        if tracker_src_ip is None:
            return None

        tracker_src_ip = tracker_src_ip.value
        if isinstance(tracker_src_ip, IPv4Interface):
            return Global[IPv4Address](value=tracker_src_ip.ip)
        if isinstance(tracker_src_ip, IPv4Address):
            return Global[IPv4Address](value=tracker_src_ip)
        elif isinstance(tracker_src_ip, str):
            try:
                return Global[IPv4Address](value=IPv4Address(tracker_src_ip))
            except ValueError:
                return None
        return None

    def get_ipsec_ciphersuite(
        self, interface_value: dict
    ) -> Optional[Union[Default[IpsecCiphersuite], Global[IpsecCiphersuite], Global[Any], Variable]]:
        """Map unused ipsec ciphersuite values into a default"""
        OBSOLETE_VALUES = ["null-sha1", "null-sha384", "null-sha256", "null-sha512"]
        ipsec_ciphersuite = interface_value.get("ipsec_ciphersuite")
        if ipsec_ciphersuite is None:
            return None
        elif isinstance(ipsec_ciphersuite, Variable):
            return ipsec_ciphersuite
        else:
            value = ipsec_ciphersuite.value
            if value in OBSOLETE_VALUES:
                return Default[IpsecCiphersuite](value="aes256-cbc-sha512")
            else:
                return ipsec_ciphersuite
