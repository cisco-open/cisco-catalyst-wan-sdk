from copy import deepcopy
from ipaddress import IPv4Address
from typing import Literal, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, OptionType, as_default, as_global
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.sdwan.service.wireless_lan import (
    SSID,
    CountryCode,
    MeIpConfig,
    MeStaticIpConfig,
    QosProfile,
    RadioType,
    SecurityConfig,
    WirelessLanParcel,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

from .base import FTConverter


class WirelessLanConverter(FTConverter):
    supported_template_types = ("cisco_wireless_lan",)

    delete_keys = ("radio", "mgmt")

    def create_parcel(self, name: str, description: str, template_values: dict) -> WirelessLanParcel:
        values = self.prepare_values(template_values)
        self.configure_enable_radio(values)
        self.configure_username_and_password(values)
        self.configure_ssid(values)
        self.configure_me_ip_address(values)
        self.cleanup_keys(values)
        return WirelessLanParcel(parcel_name=name, parcel_description=description, **values)

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values)

    def configure_enable_radio(self, values: dict) -> None:
        self._configure_enable(values, "shutdown_2.4ghz", "enable_2_4G")
        self._configure_enable(values, "shutdown_5ghz", "enable_5G")

    def _configure_enable(self, values: dict, feature_template_key: str, ux2_model_field: str) -> None:
        """Logic in the Feature Template is inverted, so we need to invert it here"""
        shutdown = values.get("radio", {}).get(feature_template_key, as_default(True))
        if shutdown.option_type == OptionType.GLOBAL:
            shutdown.value = not shutdown.value
        values[ux2_model_field] = shutdown

    def configure_username_and_password(self, values: dict) -> None:
        values["username"] = values.get("mgmt", {}).get("username")
        values["password"] = values.get("mgmt", {}).get("password")

    def configure_ssid(self, values: dict) -> None:
        ssid = values.get("ssid", [])
        ssid_list = []
        for entry in ssid:
            ssid_list.append(
                SSID(
                    name=entry.get("name"),
                    admin_state=entry.get("admin_state", as_default(True)),
                    broadcast_ssid=entry.get("broadcast_ssid", as_default(True)),
                    vlan_id=entry.get("vlan_id"),
                    radio_type=entry.get("radio_type", as_default("all", RadioType)),
                    security_config=self._prepare_security_config(entry),
                    qos_profile=self._get_qos_profile(entry),
                )
            )
        values["ssid"] = ssid_list

    def configure_me_ip_address(self, values: dict) -> None:
        address = values.get("mgmt", {}).get("address")
        netmask = values.get("mgmt", {}).get("netmask")
        default_gateway = values.get("mgmt", {}).get("default_gateway")
        if not address or not netmask or not default_gateway:
            values["me_ip_config"] = MeIpConfig(me_dynamic_ip_enabled=as_default(True))
        else:
            values["me_ip_config"] = MeIpConfig(
                me_dynamic_ip_enabled=as_global(False),
                me_static_ip_config=MeStaticIpConfig(
                    me_ipv4_address=address,
                    netmask=netmask,
                    default_gateway=default_gateway,
                ),
            )

    def _prepare_security_config(self, entry: dict) -> SecurityConfig:
        security_type = entry.get("security_type")
        if not security_type:
            # This field is required and model can't be created without it
            raise CatalystwanConverterCantConvertException("Security type is required for SSID configuration")
        return SecurityConfig(
            security_type=security_type,
            passphrase=entry.get("passphrase"),
            radius_server_ip=entry.get("radius_server_ip"),
            radius_server_port=entry.get("radius_server_port"),
            radius_server_secret=entry.get("radius_server_secret"),
        )

    def _get_qos_profile(self, values: dict) -> Union[Global[QosProfile], Default[QosProfile]]:
        qos_profile = values.get("qos_profile", as_default("silver", QosProfile))
        if qos_profile.option_type == OptionType.GLOBAL:
            qos_profile = as_global(qos_profile.value, QosProfile)
        return qos_profile

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)

    @staticmethod
    def get_example_payload() -> dict:
        payload = {
            "radio": {
                "shutdown_2.4ghz": Global[bool](value=True),
                "shutdown_5ghz": Global[bool](value=True),
            },
            "country": Global[CountryCode](value="BB"),
            "mgmt": {
                "username": Global[str](value="23452345"),
                "password": Global[str](value="42$qsSdas!321"),
                "address": Global[IPv4Address](value=IPv4Address("2.3.2.1")),
                "netmask": Global[SubnetMask](value="255.255.255.0"),
                "default_gateway": Global[IPv4Address](value=IPv4Address("10.0.0.1")),
            },
            "ssid": [
                {
                    "name": Global[str](value="5345"),
                    "admin_state": Global[bool](value=True),
                    "broadcast_ssid": Global[bool](value=True),
                    "vlan_id": Global[int](value=44),
                    "radio_type": Global[Literal["all", "24ghz", "5ghz"]](value="24ghz"),
                    "security_type": Global[Literal["open", "personal", "enterprise"]](value="enterprise"),
                    "radius_server_ip": Global[IPv4Address](value=IPv4Address("43.3.1.2")),
                    "radius_server_port": Global[int](value=333),
                    "radius_server_secret": Global[str](value="2323232323"),
                    "qos_profile": Global[Literal["platinum", "gold", "silver", "bronze"]](value="platinum"),
                },
                {
                    "name": Global[str](value="555"),
                    "admin_state": Global[bool](value=False),
                    "broadcast_ssid": Global[bool](value=False),
                    "vlan_id": Global[int](value=234),
                    "radio_type": Global[Literal["all", "24ghz", "5ghz"]](value="5ghz"),
                    "security_type": Global[Literal["open", "personal", "enterprise"]](value="personal"),
                    "passphrase": Global[str](value="33123123123"),
                    "qos_profile": Global[
                        Literal[
                            "default",
                            "mpls",
                            "metro-ethernet",
                            "biz-internet",
                            "public-internet",
                            "lte",
                            "3g",
                            "red",
                            "green",
                            "blue",
                            "gold",
                            "silver",
                            "bronze",
                            "custom1",
                            "custom2",
                            "custom3",
                            "private1",
                            "private2",
                            "private3",
                            "private4",
                            "private5",
                            "private6",
                        ]
                    ](value="gold"),
                },
                {
                    "name": Global[str](value="12312"),
                    "vlan_id": Global[int](value=123),
                    "security_type": Global[Literal["open", "personal", "enterprise"]](value="open"),
                },
            ],
        }
        return payload
