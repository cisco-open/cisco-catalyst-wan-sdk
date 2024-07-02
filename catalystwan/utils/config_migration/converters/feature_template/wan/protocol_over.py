from copy import deepcopy
from dataclasses import dataclass
from ipaddress import IPv4Interface
from typing import Dict, List, Optional, Tuple, Union

from catalystwan.api.configuration_groups.parcel import Default, Global, OptionType, as_global
from catalystwan.models.common import CarrierType
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, AllowService
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    Advanced,
    AtmEncapsulation,
    AtmInterface,
    Callin,
    Chap,
    Dynamic,
    DynamicIntfIpAddress,
    Ethernet,
    InterfaceDslIPoEParcel,
    InterfaceDslPPPoAParcel,
    InterfaceDslPPPoEParcel,
    InterfaceEthPPPoEParcel,
    IPoEEthernet,
    Method,
    NatProp,
    Pap,
    Ppp,
    Static,
    StaticIntfIpAddress,
    Tunnel,
    TunnelAdvancedOption,
    VbrNrtConfig,
    VbrRtConfig,
    Vdsl,
    VdslMode,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter


@dataclass
class EncapsulationOption:
    encap: Optional[Global[bool]] = None
    preference: Optional[Global[int]] = None
    weight: Optional[Global[int]] = None


class InterfaceBaseConverter(FTConverter):
    def parse_tunnel_advanced_option(self, data: dict) -> Optional[TunnelAdvancedOption]:
        tunnel = data.get("tunnel_interface", {})
        if not tunnel:
            return None

        carrier = tunnel.get("carrier")
        if carrier:
            carrier = as_global(carrier.value, CarrierType)

        gre_option, ipsec_option = self.parse_encapsulation_options(tunnel.get("encapsulation", []))

        return TunnelAdvancedOption(
            bind=tunnel.get("bind"),
            carrier=carrier,
            gre_encap=gre_option.encap,
            gre_preference=gre_option.preference,
            gre_weight=gre_option.weight,
            hello_interval=tunnel.get("hello_interval"),
            hello_tolerance=tunnel.get("hello_tolerance"),
            ipsec_encap=ipsec_option.encap,
            ipsec_preference=ipsec_option.preference,
            ipsec_weight=ipsec_option.weight,
            last_resort_circuit=tunnel.get("last_resort_circuit"),
            nat_refresh_interval=tunnel.get("nat_refresh_interval"),
        )

    def parse_encapsulation_options(
        self, encapsulations: List[Dict]
    ) -> Tuple[EncapsulationOption, EncapsulationOption]:
        gre_option = EncapsulationOption()
        ipsec_option = EncapsulationOption()

        for encap in encapsulations:
            encap_type = encap.get("encap", {}).value
            preference = encap.get("preference")
            weight = encap.get("weight")

            if encap_type == "gre":
                gre_option = EncapsulationOption(encap=as_global(True), preference=preference, weight=weight)
            elif encap_type == "ipsec":
                ipsec_option = EncapsulationOption(encap=as_global(True), preference=preference, weight=weight)

        return gre_option, ipsec_option

    def parse_tunnel(self, data: dict) -> Optional[Tunnel]:
        tunnel_data = data.get("tunnel_interface")
        if not tunnel_data:
            return None

        exclude_controller_group_list = self.parse_list(tunnel_data.get("exclude_controller_group_list"))
        group = self.parse_list(tunnel_data.get("group"))

        return Tunnel(
            bandwidth_percent=tunnel_data.get("bandwidth_percent"),
            border=tunnel_data.get("border"),
            clear_dont_fragment=tunnel_data.get("clear_dont_fragment"),
            color=tunnel_data.get("color", {}).get("value"),
            group=group,
            exclude_controller_group_list=exclude_controller_group_list,
            low_bandwidth_link=tunnel_data.get("low_bandwidth_link"),
            max_control_connections=tunnel_data.get("max_control_connections"),
            mode=tunnel_data.get("mode"),
            network_broadcast=tunnel_data.get("network_broadcast"),
            per_tunnel_qos=tunnel_data.get("per_tunnel_qos"),
            port_hop=tunnel_data.get("port_hop"),
            restrict=tunnel_data.get("color", {}).get("restrict"),
            tunnel_interface=as_global(True),
            tunnel_tcp_mss_adjust=tunnel_data.get("tunnel_tcp_mss_adjust"),
            vbond_as_stun_server=tunnel_data.get("vbond_as_stun_server"),
            vmanage_connection_preference=tunnel_data.get("vmanage_connection_preference"),
        )

    def parse_list(self, value: Global[List[int]]) -> Optional[Global[str]]:
        if value:
            return as_global(",".join(list(map(str, value.value))))
        return None

    def parse_shutdown(self, data: dict) -> Optional[Global[bool]]:
        return data.get("shutdown")

    def parse_service_provider(self, data: dict) -> Optional[Global[str]]:
        return data.get("service_provider")

    def parse_bandwidth_downstream(self, data: dict) -> Optional[Global[int]]:
        return data.get("bandwidth_downstream")

    def parse_bandwidth_upstream(self, data: dict) -> Optional[Global[int]]:
        return data.get("bandwidth_upstream")

    def parse_advanced(self, data: dict) -> Advanced:
        return Advanced(
            ip_directed_broadcast=data.get("ip_directed_broadcast"),
            ip_mtu=data.get("dialer_ip_mtu"),
            tcp_mss=data.get("dialer_tcp_mss_adjust"),
            tloc_extension=data.get("tloc_extension"),
        )

    def parse_ethernet(self, data: dict) -> Ethernet:
        if_name = data.get("if_name")
        if not if_name:
            raise CatalystwanConverterCantConvertException("Interface name is required")

        return Ethernet(
            if_name=if_name,
            description=data.get("description"),
            vlan_id=data.get("vlan_id"),
        )

    def parse_nat_prop(self, data: dict) -> Optional[NatProp]:
        nat_prop = data.get("nat")
        if not nat_prop:
            return None
        return NatProp(
            nat=as_global(True),
            tcp_timeout=nat_prop.get("tcp_timeout"),
            udp_timeout=nat_prop.get("udp_timeout"),
        )

    def parse_tunnel_allow_service(self, data: dict) -> Optional[AllowService]:
        allow_service = data.get("tunnel_interface", {}).get("allow_service")
        if not allow_service:
            return None
        return AllowService(**allow_service)

    def parse_ppp(self, data: Dict) -> Optional[Ppp]:
        pppoe_client_data = data.get("pppoe_client")
        if not pppoe_client_data:
            return None

        ppp_data = data.get("ppp", {})
        chap = self.parse_chap(ppp_data.get("chap"))
        pap = self.parse_pap(ppp_data.get("pap", {}))
        callin = self.parse_callin(ppp_data.get("authentication", {}))
        method = self.parse_method(ppp_data.get("authentication", {}))

        return Ppp(
            dial_pool_number=pppoe_client_data["dial_pool_number"],
            ppp_max_payload=pppoe_client_data.get("ppp_max_payload"),
            method=method,
            callin=callin,
            chap=chap,
            pap=pap,
        )

    def parse_chap(self, chap_data: Optional[Dict]) -> Optional[Chap]:
        if not chap_data:
            return None

        hostname = chap_data["hostname"]
        ppp_auth_password = chap_data["password"]["ppp_auth_password"]
        return Chap(hostname=hostname, ppp_auth_password=ppp_auth_password)

    def parse_pap(self, pap_data: Dict) -> Optional[Pap]:
        sent_username = pap_data.get("sent_username", {}).get("username")
        if not sent_username:
            return None

        ppp_auth_password = sent_username.get("ppp_auth_password")
        username = sent_username.get("username_string")
        return Pap(ppp_auth_password=ppp_auth_password, username=username)

    def parse_callin(self, auth_data: Dict) -> Optional[Global[Callin]]:
        callin = auth_data.get("callin")
        if callin and callin.value != "callin":
            return as_global(callin, Callin)
        return None

    def parse_method(self, auth_data: Dict) -> Union[Global[Method], Default[None]]:
        method = auth_data.get("method", {})
        if method and method.option_type == OptionType.GLOBAL:
            return as_global(method.value, Method)
        return Default[None](value=None)

    def parse_vdsl(self, data: dict) -> Optional[Vdsl]:
        controller = data.get("controller", {}).get("vdsl", [])

        if not controller:
            return None

        controller_data = controller[0]
        sra = controller_data.get("sra", {})
        slot = controller_data.get("name", {})

        operating_mode = controller_data.get("operating", {}).get("mode", {})
        mode = self.parse_mode(operating_mode)

        return Vdsl(sra=sra, slot=slot, mode=mode)

    def parse_mode(self, mode: dict) -> Optional[Global[VdslMode]]:
        if "auto" in mode:
            return None

        mode_key = next(iter(mode.keys()), None)
        if mode_key:
            return as_global(mode_key.upper(), VdslMode)

        return None


class InterfaceEthernetPppoeConverter(InterfaceBaseConverter):
    supported_template_types = ("vpn-interface-ethpppoe",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceEthPPPoEParcel:
        data = deepcopy(template_values)
        tunnel_allow_service = self.parse_tunnel_allow_service(data)
        ppp = self.parse_ppp(data)
        nat_prop = self.parse_nat_prop(data)
        ethernet = self.parse_ethernet(data)
        advanced = self.parse_advanced(data)
        bandwidth_downstream = self.parse_bandwidth_downstream(data)
        bandwidth_upstream = self.parse_bandwidth_upstream(data)
        service_provider = self.parse_service_provider(data)
        shutdown = self.parse_shutdown(data)
        tunnel = self.parse_tunnel(data)
        tunnel_advanced_option = self.parse_tunnel_advanced_option(data)
        return InterfaceEthPPPoEParcel(
            parcel_name=name,
            parcel_description=description,
            ethernet=ethernet,
            ppp=ppp,
            tunnel=tunnel,
            bandwidth_downstream=bandwidth_downstream,
            bandwidth_upstream=bandwidth_upstream,
            advanced=advanced,
            shutdown=shutdown,
            nat_prop=nat_prop,
            tunnel_advanced_option=tunnel_advanced_option,
            service_provider=service_provider,
            tunnel_allow_service=tunnel_allow_service,
        )


class InterfaceDslPppoeConverter(InterfaceBaseConverter):
    supported_template_types = ("vpn-interface-pppoe",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceDslPPPoEParcel:
        data = deepcopy(template_values)
        tunnel_allow_service = self.parse_tunnel_allow_service(data)
        ppp = self.parse_ppp(data)
        nat_prop = self.parse_nat_prop(data)
        ethernet = self.parse_ethernet(data)
        advanced = self.parse_advanced(data)
        bandwidth_downstream = self.parse_bandwidth_downstream(data)
        bandwidth_upstream = self.parse_bandwidth_upstream(data)
        service_provider = self.parse_service_provider(data)
        shutdown = self.parse_shutdown(data)
        tunnel = self.parse_tunnel(data)
        tunnel_advanced_option = self.parse_tunnel_advanced_option(data)
        vdsl = self.parse_vdsl(data)
        return InterfaceDslPPPoEParcel(
            parcel_name=name,
            parcel_description=description,
            ethernet=ethernet,
            ppp=ppp,
            tunnel=tunnel,
            bandwidth_downstream=bandwidth_downstream,
            bandwidth_upstream=bandwidth_upstream,
            advanced=advanced,
            shutdown=shutdown,
            nat_prop=nat_prop,
            tunnel_advanced_option=tunnel_advanced_option,
            service_provider=service_provider,
            tunnel_allow_service=tunnel_allow_service,
            vdsl=vdsl,
        )


class InterfaceDslPppoaConverter(InterfaceBaseConverter):
    supported_template_types = ("vpn-interface-pppoa",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceDslPPPoAParcel:
        data = deepcopy(template_values)
        tunnel_allow_service = self.parse_tunnel_allow_service(data)
        ppp = self.parse_ppp(data)
        nat_prop = self.parse_nat_prop(data)
        advanced = self.parse_advanced(data)
        bandwidth_downstream = self.parse_bandwidth_downstream(data)
        bandwidth_upstream = self.parse_bandwidth_upstream(data)
        service_provider = self.parse_service_provider(data)
        shutdown = self.parse_shutdown(data)
        tunnel = self.parse_tunnel(data)
        tunnel_advanced_option = self.parse_tunnel_advanced_option(data)
        vdsl = self.parse_vdsl(data)
        atm_interface = self.parse_atm_interface(data)
        return InterfaceDslPPPoAParcel(
            parcel_name=name,
            parcel_description=description,
            ppp=ppp,
            tunnel=tunnel,
            bandwidth_downstream=bandwidth_downstream,
            bandwidth_upstream=bandwidth_upstream,
            advanced=advanced,
            shutdown=shutdown,
            nat_prop=nat_prop,
            tunnel_advanced_option=tunnel_advanced_option,
            service_provider=service_provider,
            tunnel_allow_service=tunnel_allow_service,
            vdsl=vdsl,
            atm_interface=atm_interface,
        )

    def parse_atm_interface(self, data: Dict) -> Optional[AtmInterface]:
        pvc = next(iter(data.get("pvc", [])), None)
        if not pvc:
            return None

        if_name = data.get("if_name")
        if not if_name:
            raise CatalystwanConverterCantConvertException("Interface name is required")

        encapsulation = self.parse_encapsulation(pvc.get("encapsulation", {}))
        vbr_nrt_config = self.parse_vbr_nrt_config(pvc.get("vbr_nrt", {}))
        vbr_rt_config = self.parse_vbr_rt_config(pvc.get("vbr_rt", {}))

        return AtmInterface(
            if_name=if_name,
            local_vpi_vci=pvc.get("local_vpi_vci"),
            encapsulation=encapsulation,
            vbr_rt_config=vbr_rt_config,
            vbr_nrt_config=vbr_nrt_config,
        )

    def parse_encapsulation(self, encapsulation: Dict) -> Optional[Global[AtmEncapsulation]]:
        atm_encapsulation = next(iter(encapsulation.keys()), None)
        if not atm_encapsulation:
            return None
        return as_global(atm_encapsulation.upper(), AtmEncapsulation)

    def parse_vbr_nrt_config(self, vbr_nrt: Dict) -> Optional[VbrNrtConfig]:
        if not vbr_nrt:
            return None
        return VbrNrtConfig(
            p_c_r=vbr_nrt["PCR"],
            s_c_r=vbr_nrt["SCR"],
            burst_cell_size=vbr_nrt["MCR"],
        )

    def parse_vbr_rt_config(self, vbr_rt: Dict) -> Optional[VbrRtConfig]:
        if not vbr_rt:
            return None
        return VbrRtConfig(
            a_c_r=vbr_rt["ACR"],
            p_c_r=vbr_rt["PCR"],
            burst_cell_size=vbr_rt["Burst_cell_size"],
        )


class InterfaceDslIPoEConverter(InterfaceBaseConverter):
    supported_template_types = ("vpn-interface-ipoe",)

    def create_parcel(self, name: str, description: str, template_values: dict) -> InterfaceDslIPoEParcel:
        data = deepcopy(template_values)
        tunnel_allow_service = self.parse_tunnel_allow_service(data)
        ppp = self.parse_ppp(data)
        nat_prop = self.parse_nat_prop(data)
        advanced = self.parse_advanced(data)
        bandwidth_downstream = self.parse_bandwidth_downstream(data)
        bandwidth_upstream = self.parse_bandwidth_upstream(data)
        service_provider = self.parse_service_provider(data)
        shutdown = self.parse_shutdown(data)
        tunnel = self.parse_tunnel(data)
        tunnel_advanced_option = self.parse_tunnel_advanced_option(data)
        vdsl = self.parse_vdsl(data)
        ethernet = self.parse_ethernet(data)
        return InterfaceDslIPoEParcel(
            parcel_name=name,
            parcel_description=description,
            ppp=ppp,
            tunnel=tunnel,
            bandwidth_downstream=bandwidth_downstream,
            bandwidth_upstream=bandwidth_upstream,
            advanced=advanced,
            shutdown=shutdown,
            nat_prop=nat_prop,
            tunnel_advanced_option=tunnel_advanced_option,
            service_provider=service_provider,
            tunnel_allow_service=tunnel_allow_service,
            vdsl=vdsl,
            ethernet=ethernet,
        )

    def parse_ethernet(self, data: dict) -> IPoEEthernet:
        if_name = data.get("if_name")
        if not if_name:
            raise CatalystwanConverterCantConvertException("Interface name is required")

        intf_ip_address = self.parse_intf_ip_address(data)
        return IPoEEthernet(
            if_name=if_name,
            description=data.get("description"),
            vlan_id=data.get("vlan_id"),
            intf_ip_address=intf_ip_address,
        )

    def parse_intf_ip_address(self, data: dict) -> Union[DynamicIntfIpAddress, StaticIntfIpAddress]:
        if static_ip_address := data.get("ip", {}).get("address"):
            return self.parse_static_ip_address(static_ip_address.value)
        return self.parse_dynamic_ip_address(data)

    def parse_static_ip_address(self, interface: IPv4Interface) -> StaticIntfIpAddress:
        return StaticIntfIpAddress(
            static=Static(
                static_ip_v4=AddressWithMask(
                    address=as_global(interface.network.network_address),
                    mask=as_global(str(interface.netmask)),
                )
            )
        )

    def parse_dynamic_ip_address(self, data: dict) -> DynamicIntfIpAddress:
        if dhcp_helper := data.get("dhcp_helper"):
            dhcp_helper = as_global(",".join(dhcp_helper.value))
        return DynamicIntfIpAddress(
            dynamic=Dynamic(dhcp_helper=dhcp_helper, dynamic_dhcp_distance=data.get("ip", {}).get("dhcp_distance"))
        )
