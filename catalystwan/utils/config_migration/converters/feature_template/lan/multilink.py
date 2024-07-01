from typing import List, Optional

from catalystwan.api.configuration_groups.parcel import Default, Global
from catalystwan.models.configuration.feature_profile.common import (
    ChannelGroup,
    MultilinkAuthenticationType,
    MultilinkControllerTxExList,
    MultilinkMethod,
    MultilinkNimList,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.multilink import InterfaceMultilinkParcel
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter
from catalystwan.utils.config_migration.converters.feature_template.model_definition_normalizer import (
    flatten_datapaths,
    normalize_to_model_definition,
)
from catalystwan.utils.config_migration.steps.constants import LAN_VPN_MULTILINK


class LanMultilinkConverter(FTConverter):
    supported_template_types = (LAN_VPN_MULTILINK,)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceMultilinkParcel:
        addresses = self.parse_address(template_values)
        tunnel = self.get_tunnel(template_values)
        passwords = self.get_passwords(template_values)

        flattened_values = flatten_datapaths(template_values)
        authentication_type = self.get_authentication_type(flattened_values)
        method = self.get_method(flattened_values)
        normalized_values = normalize_to_model_definition(flattened_values, InterfaceMultilinkParcel.model_fields)

        controller_tx_ex_list = self.parse_controller_tx_ex_list(normalized_values.get("controller_tx_ex_list"))
        nim_list = self.parse_nim_list(normalized_values.get("nim_list"))
        return InterfaceMultilinkParcel(
            parcel_name=name,
            parcel_description=description,
            group_number=self.get_group_number(template_values),  # type: ignore
            if_name=normalized_values.get("if_name"),  # type: ignore
            method=method,  # type: ignore
            address_ipv4=addresses.get("address_ipv4"),
            address_ipv6=addresses.get("address_ipv6"),
            authentication_type=authentication_type,  # type: ignore
            bandwidth_upstream=normalized_values.get("bandwidth_upstream"),
            clear_dont_fragment_sdwan_tunnel=tunnel.get("clear_dont_fragment_sdwan_tunnel"),
            control_connections=normalized_values.get("control_connections"),
            controller_tx_ex_list=controller_tx_ex_list,  # type: ignore
            delay_value=normalized_values.get("delay_value"),
            disable=normalized_values.get("disable", Default[bool](value=False)),
            hostname=normalized_values.get("hostname"),
            interleave=normalized_values.get("interleave", Default[bool](value=False)),
            ip_directed_broadcast=normalized_values.get("ip_directed_brodcast"),
            mask_ipv4=addresses.get("mask_ipv4"),
            mtu=normalized_values.get("mtu", Default[int](value=1500)),
            nim_list=nim_list,
            password=passwords.get("password"),
            ppp_auth_password=passwords.get("ppp_auth_password"),
            shaping_rate=normalized_values.get("shaping_rate"),
            shutdown=normalized_values.get("shutdown", Default[bool](value=False)),
            tcp_mss_adjust=normalized_values.get("tcp_mss_adjust"),
            tloc_extension=normalized_values.get("tloc_extension"),
            username_string=normalized_values.get("username_string"),
        )

    def parse_controller_tx_ex_list(
        self, tx_ex_values: Optional[List[dict]]
    ) -> Optional[List[MultilinkControllerTxExList]]:
        if not tx_ex_values:
            return []

        controller_tx_ex_list = []
        for tx_ex_value in tx_ex_values:
            tx_ex_value = flatten_datapaths(tx_ex_value)

            framing = tx_ex_value.pop("framing", None)
            linecode = tx_ex_value.pop("linecode", None)
            channel_group = self.parse_channel_group(tx_ex_value.get("channel"))  # type: ignore

            tx_ex_value["clock_source"] = "internal" if tx_ex_value.get("internal") is not None else None

            tx_ex_value = normalize_to_model_definition(tx_ex_value, MultilinkControllerTxExList.model_fields)
            name = tx_ex_value["name"]

            controller_tx_ex_list.append(
                MultilinkControllerTxExList(
                    channel_group=channel_group,  # type: ignore
                    number=tx_ex_value.get("number"),  # type: ignore
                    clock_source=tx_ex_value.get("clock_source"),
                    description=tx_ex_value.get("description"),
                    e1_framing=framing if name == "E1" else None,
                    e1_linecode=linecode if name == "E1" else None,
                    t1_framing=framing if name == "T1" else None,
                    t1_linecode=linecode if name == "T1" else None,
                    line_mode=tx_ex_value.get("line_mode"),
                    long=tx_ex_value.get("long"),
                    name=name,
                )
            )

        return controller_tx_ex_list

    def parse_channel_group(self, channel_groups: dict) -> List[ChannelGroup]:
        if not channel_groups:
            return []
        channel_group_list = []
        for channel_group in channel_groups:
            normalized_group = normalize_to_model_definition(channel_group, ChannelGroup.model_fields)
            channel_group_list.append(
                ChannelGroup(
                    number=normalized_group.get("number"),  # type: ignore
                    timeslots=normalized_group.get("timeslots"),  # type: ignore
                )
            )
        return channel_group_list

    def parse_nim_list(self, nim_values: Optional[List[dict]]) -> Optional[List[MultilinkNimList]]:
        if not nim_values:
            return None
        nim_list = []
        for nim_value in nim_values:
            flattened_value = flatten_datapaths(nim_value)
            if_name = flattened_value.get("if_name")
            if if_name is not None:
                flattened_value["if_name"] = if_name.value.title()
            normalized_value = normalize_to_model_definition(flattened_value, MultilinkNimList.model_fields)
            nim_list.append(
                MultilinkNimList(  # type: ignore
                    if_name=normalized_value.get("if_name"),  # type: ignore
                    bandwidth=normalized_value.get("bandwidth"),
                    clock_rate=normalized_value.get("clock_rate"),
                    description=normalized_value.get("description"),
                )
            )

        return nim_list

    def parse_address(self, template_values: dict) -> dict:
        interface_ipv4 = template_values.get("ip", {}).get("address")
        address_ipv6 = template_values.get("ipv6", {}).get("address")

        addresses = {
            "address_ipv4": str(interface_ipv4.value.ip) if interface_ipv4 is not None else None,
            "mask_ipv4": str(interface_ipv4.value.network.netmask) if interface_ipv4 is not None else None,
            "address_ipv6": str(address_ipv6.value) if address_ipv6 is not None else None,
        }
        return normalize_to_model_definition(addresses, InterfaceMultilinkParcel.model_fields)

    def get_group_number(self, template_values: dict) -> dict:
        return template_values.get("ppp", {}).get("multilink", {}).get("group")

    def get_tunnel(self, template_values: dict) -> dict:
        tunnel_interface: dict = template_values.get("tunnel_interface", {})
        tunnel = {
            "clear_dont_fragment_sdwan_tunnel": tunnel_interface.get("clear_dont_fragment"),
        }
        return normalize_to_model_definition(tunnel, InterfaceMultilinkParcel.model_fields)

    def get_authentication_type(self, flattened_values: dict) -> Optional[Global[MultilinkAuthenticationType]]:
        callin: Optional[Global[str]] = flattened_values.get("callin")
        if callin is None:
            return None
        if callin.value is False:
            return Global[MultilinkAuthenticationType](value="bidirectional")
        elif callin.value == "callin":
            return Global[MultilinkAuthenticationType](value="unidirectional")
        else:
            return None

    def get_method(self, flattened_values: dict) -> Optional[Global[MultilinkMethod]]:
        method: Optional[Global[bool]] = flattened_values.get("method")
        pap: Optional[Global[bool]] = flattened_values.get("pap")
        if method is None:
            return None
        if method.value == "pap":
            return Global[MultilinkMethod](value="PAP")
        elif method.value == "chap":
            if pap:
                return Global[MultilinkMethod](value="PAP and CHAP")
            else:
                return Global[MultilinkMethod](value="CHAP")
        return None

    def get_passwords(self, template_values: dict) -> dict:
        chap_password = template_values.get("ppp", {}).get("chap", {}).get("password", {}).get("ppp_auth_password")
        pap_password = (
            template_values.get("ppp", {})
            .get("pap", {})
            .get("sent-username", {})
            .get("username", {})
            .get("ppp_auth_password")
        )

        return normalize_to_model_definition(
            {
                "password": pap_password,
                "ppp_auth_password": chap_password,
            },
            InterfaceMultilinkParcel.model_fields,
        )
