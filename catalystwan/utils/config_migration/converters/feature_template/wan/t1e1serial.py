from copy import deepcopy

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.common import CarrierType, ClockRate, EncapType
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, AllowService, Encapsulation
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.t1e1serial import (
    Advanced,
    EncapsulationSerial,
    T1E1SerialParcel,
    Tunnel,
)
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter


class T1E1SerialConverter(FTConverter):
    supported_template_types = ("vpn-interface-t1-e1",)
    delete_keys = (
        "description",
        "if_name",
        "ip",
        "ipv6",
        "clear_dont_fragment",
        "tloc_extension",
        "rewrite_rule",
        "autonegotiate",
        "pmtu",
        "mtu",
        "static_ingress_qos",
        "tcp_mss_adjust",
    )

    def create_parcel(self, name: str, description: str, template_values: dict) -> T1E1SerialParcel:
        self.values = deepcopy(template_values)
        self.set_clock_rate()
        self.set_interface_name()
        self.set_address_ipv4()
        self.set_address_ipv6()
        self.set_bandwidth()
        self.set_allow_service()
        self.set_encapsulation()
        self.set_encapsulation_serial()
        self.set_tunnel_interface()
        self.set_advanced()
        self.cleanup_keys()
        return T1E1SerialParcel(parcel_name=name, parcel_description=description, **self.values)

    def set_clock_rate(self) -> None:
        if clock_rate := self.values.get("clock_rate"):
            self.values["clock_rate"] = as_global(clock_rate.value, ClockRate)

    def set_interface_name(self) -> None:
        self.values["interface_name"] = self.values.get("if_name")

    def set_address_ipv4(self) -> None:
        address = self.values.get("ip", {}).get("address")
        if not address:
            return
        self.values["address_v4"] = AddressWithMask(
            address=as_global(address.value.ip),
            mask=as_global(str(address.value.netmask)),
        )

    def set_address_ipv6(self) -> None:
        address = self.values.get("ipv6", {}).get("address")
        if not address:
            return
        self.values["address_v6"] = address

    def set_bandwidth(self) -> None:
        if bandwidth := self.values.get("bandwidth"):
            self.values["bandwidth"] = as_global(int(bandwidth.value))

    def set_encapsulation_serial(self) -> None:
        if encapsulation_serial := self.values.get("encapsulation_serial"):
            self.values["encapsulation_serial"] = as_global(encapsulation_serial.value, EncapsulationSerial)

    def set_tunnel_interface(self) -> None:
        """There are many values that map 1 to 1."""
        if tunnel_interface := self.values.get("tunnel_interface"):
            tunnel_interface.pop("allow_service", None)
            tunnel_interface.pop("encapsulation", None)
            self._process_color(tunnel_interface)
            self._process_carrier(tunnel_interface)
            self._process_group(tunnel_interface)
            self.values["tunnel"] = Tunnel(**tunnel_interface)
            self.values["tunnel_interface"] = as_global(True)

    def _process_color(self, tunnel_interface: dict) -> None:
        color = tunnel_interface.get("color", {})
        if color:
            tunnel_interface["color"] = color.get("value")
            tunnel_interface["restrict"] = color.get("restrict")

    def _process_carrier(self, tunnel_interface: dict) -> None:
        carrier = tunnel_interface.get("carrier")
        if carrier:
            tunnel_interface["carrier"] = as_global(carrier.value, CarrierType)

    def _process_group(self, tunnel_interface: dict) -> None:
        group = tunnel_interface.get("group")
        if group:
            # This value is passed as a list in UX1, but it is integer in UX2.
            if len(group.value) == 1:
                tunnel_interface["group"] = as_global(group.value[0])

    def set_allow_service(self) -> None:
        """This needs to be called before set_tunnel_interface, because it needs values from original dict."""
        if allow_service := self.values.get("tunnel_interface", {}).get("allow_service"):
            self.values["allow_service"] = AllowService(**allow_service)

    def set_encapsulation(self) -> None:
        """This needs to be called before set_tunnel_interface, because it needs values from original dict."""
        if encapsulation := self.values.get("tunnel_interface", {}).get("encapsulation"):
            self.values["encapsulation"] = [self.create_encapsulation(entry) for entry in encapsulation]

    def create_encapsulation(self, encapsulation: dict) -> Encapsulation:
        if encap := encapsulation.get("encap"):
            encap = as_global(encap.value, EncapType)
        return Encapsulation(
            preference=encapsulation.get("preference"),
            weight=encapsulation.get("weight"),
            encap=encap,
        )

    def set_advanced(self) -> None:
        self.values["advanced"] = Advanced(
            ip_mtu=self.values.get("mtu"),
            tcp_mss_adjust=self.values.get("tcp_mss_adjust"),
            tloc_extension=self.values.get("tloc_extension"),
        )

    def cleanup_keys(self) -> None:
        for key in self.delete_keys:
            self.values.pop(key, None)
