from copy import deepcopy
from typing import Literal, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, OptionType
from catalystwan.models.configuration.feature_profile.sdwan.service.switchport import (
    Duplex,
    Speed,
    StaticMacAddress,
    SwitchportInterface,
    SwitchportParcel,
)

from .base import FTConverter


class SwitchportConverter(FTConverter):
    supported_template_types = ("switchport",)

    delete_keys = ("slot", "module", "subslot")

    def create_parcel(self, name: str, description: str, template_values: dict) -> SwitchportParcel:
        values = self.prepare_values(template_values)
        self.configure_static_mac_address(values)
        self.configure_interface(values)
        self.cleanup_keys(values)
        return SwitchportParcel(parcel_name=name, parcel_description=description, **values)

    def prepare_values(self, template_values: dict) -> dict:
        return deepcopy(template_values)

    def configure_interface(self, values: dict) -> None:
        interface = values.get("interface", [])
        if not interface:
            return
        interface_list = []
        for entry in interface:
            interface_list.append(
                SwitchportInterface(
                    interface_name=entry.get("if_name"),
                    shutdown=entry.get("shutdown", Default[bool](value=True)),
                    mode=entry.get("switchport", {}).get("mode", Default[str](value="access")),
                    switchport_access_vlan=self._set_switchport_access_vlan(entry),
                    switchport_trunk_allowed_vlans=self._set_switchport_trunk_allowed_vlans(entry),
                    switchport_trunk_native_vlan=self._set_switchport_trunk_native_vlan(entry),
                    speed=self._set_speed(entry),
                    duplex=self._set_duplex(entry),
                    **self.prepare_interface_values(entry),
                )
            )
        values["interface"] = interface_list

    def _set_speed(self, entry: dict) -> Union[Global[Speed], Default[None]]:
        """Set the speed value. The value is not casted in normalizer, beacuase it's to generic."""
        speed = entry.get("speed", Default[None](value=None))
        if speed.option_type == OptionType.DEFAULT:
            return speed
        return Global[Speed](value=speed.value)

    def _set_duplex(self, entry: dict) -> Union[Global[Duplex], Default[None]]:
        """Set the duplex value. The value is not casted in normalizer, beacuase it's to generic."""
        duplex = entry.get("duplex", Default[None](value=None))
        if duplex.option_type == OptionType.DEFAULT:
            return duplex
        return Global[Duplex](value=duplex.value)

    def _set_switchport_access_vlan(self, entry: dict) -> Union[Global[int], Default[None]]:
        switchport_access_vlan = (
            entry.get("switchport", {}).get("access", {}).get("vlan", {}).get("vlan", Default[None](value=None))
        )
        return switchport_access_vlan

    def _set_switchport_trunk_allowed_vlans(self, entry: dict) -> Union[Global[str], Default[None]]:
        switchport_trunk_allowed_vlans = (
            entry.get("switchport", {})
            .get("trunk", {})
            .get("allowed", {})
            .get("vlan", {})
            .get("vlans", Default[None](value=None))
        )
        return switchport_trunk_allowed_vlans

    def _set_switchport_trunk_native_vlan(self, entry: dict) -> Union[Global[int], Default[None]]:
        switchport_trunk_native_vlan = (
            entry.get("switchport", {}).get("trunk", {}).get("native", {}).get("vlan", Default[None](value=None))
        )
        return switchport_trunk_native_vlan

    def prepare_interface_values(self, entry: dict) -> dict:
        """This function flattens the dotx1 dictionary and gives the rest of SwitchportInterface values."""
        values = entry.get("dot1x", {})
        values.pop("dot1x_enable", None)  # This is not defined in the UX2 model
        authentication = values.pop("authentication", {})
        if authentication:
            periodic_reauthentication = authentication.pop("periodic_reauthentication", {})
            event = authentication.pop("event", {})
            authentication = {
                "control_direction": authentication.pop("control_direction", None),
                "host_mode": authentication.pop("host_mode", None),
                "enable_periodic_reauth": authentication.pop("enable_periodic_reauth", None),
                **periodic_reauthentication,
                **event,
            }
        return {
            **values,
            **authentication,
        }

    def configure_static_mac_address(self, values: dict) -> None:
        static_mac_address = values.get("static_mac_address", [])
        if not static_mac_address:
            return
        static_mac_address_list = []
        for entry in static_mac_address:
            static_mac_address_list.append(
                StaticMacAddress(
                    mac_address=entry.get("macaddr"),
                    vlan=entry.get("vlan"),
                    interface_name=entry.get("if_name"),
                )
            )
        values["static_mac_address"] = static_mac_address_list

    def cleanup_keys(self, values: dict) -> None:
        for key in self.delete_keys:
            values.pop(key, None)

    def get_example_payloads(self) -> dict:
        payload = {
            "slot": Global[int](value=0),
            "module": Global[str](value="22"),
            "subslot": Global[int](value=0),
            "interface": [
                {
                    "if_name": Global[str](value="GigabitEthernet0/0/3"),
                    "switchport": {
                        "mode": Global[Literal["access", "trunk"]](value="trunk"),
                        "trunk": {
                            "allowed": {"vlan": {"vlans": Global[str](value="123")}},
                            "native": {"vlan": Global[int](value=33)},
                        },
                    },
                    "shutdown": Global[bool](value=False),
                    "speed": Global[str](value="1000"),
                    "duplex": Global[Literal["full", "half"]](value="half"),
                    "dot1x": {
                        "dot1x_enable": Global[bool](value=True),
                        "port_control": Global[Literal["auto", "force-unauthorized", "force-authorized"]](
                            value="force-unauthorized"
                        ),
                        "voice_vlan": Global[int](value=2323),
                        "pae_enable": Global[bool](value=True),
                        "mac_authentication_bypass": Global[bool](value=True),
                        "authentication": {
                            "host_mode": Global[
                                Literal[
                                    "single-host",
                                    "multi-auth",
                                    "multi-host",
                                    "multi-domain",
                                ]
                            ](value="multi-host"),
                            "enable_periodic_reauth": Global[bool](value=True),
                            "periodic_reauthentication": {
                                "inactivity": Global[int](value=333),
                                "reauthentication": Global[int](value=222),
                            },
                            "control_direction": Global[Literal["both", "in"]](value="both"),
                            "event": {
                                "restricted_vlan": Global[int](value=213),
                                "guest_vlan": Global[int](value=33),
                                "critical_vlan": Global[int](value=323),
                                "enable_voice": Global[bool](value=True),
                            },
                        },
                    },
                },
                {
                    "if_name": Global[str](value="FastEthernet0/0/1"),
                    "switchport": {
                        "access": {"vlan": {"vlan": Global[int](value=322)}},
                        "mode": Global[Literal["access", "trunk"]](value="access"),
                    },
                    "speed": Global[str](value="10000"),
                    "duplex": Global[Literal["full", "half"]](value="full"),
                    "dot1x": {
                        "dot1x_enable": Global[bool](value=False),
                        "voice_vlan": Global[int](value=3),
                        "pae_enable": Global[bool](value=False),
                    },
                },
            ],
            "static_mac_address": [
                {
                    "macaddr": Global[str](value="B0B8.78A8.7722"),
                    "if_name": Global[str](value="GigabitEthernet0/0/3"),
                    "vlan": Global[int](value=22),
                }
            ],
        }
        return payload
