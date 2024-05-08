from copy import deepcopy
from typing import Optional

from catalystwan.api.configuration_groups.parcel import Default, Global, OptionType, as_global
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethpppoe import (
    Advanced,
    Callin,
    Chap,
    Ethernet,
    InterfaceEthPPPoEParcel,
    Method,
    NatProp,
    Pap,
    Ppp,
    Tunnel,
    TunnelAdvancedOption,
    TunnelAllowService,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


class InterfaceEthernetPppoeTemplateConverter:
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

    def parse_tunnel_advanced_option(self, data: dict) -> Optional[TunnelAdvancedOption]:
        """There is no data to parse from Feature Template. Return None."""
        return None
        # return TunnelAdvancedOption(
        #     bind=data.get("bind"),
        #     carrier=data.get("carrier"),
        #     gre_encap=data.get("gre_encap"),
        #     gre_preference=data.get("gre_preference"),
        #     gre_weight=data.get("gre_weight"),
        #     hello_interval=data.get("hello_interval"),
        #     hello_tolerance=data.get("hello_tolerance"),
        #     ipsec_encap=data.get("ipsec_encap"),
        #     ipsec_preference=data.get("ipsec_preference"),
        #     ipsec_weight=data.get("ipsec_weight"),
        #     last_resort_circuit=data.get("last_resort_circuit"),
        #     nat_refresh_interval=data.get("nat_refresh_interval"),
        # )

    def parse_tunnel(self, data: dict) -> Optional[Tunnel]:
        tunnel_data = data.get("tunnel_interface")
        if not tunnel_data:
            return None

        exclude_controller_group_list = tunnel_data.get("exclude_controller_group_list")
        if exclude_controller_group_list:
            exclude_controller_group_list = as_global(",".join(list(map(str, exclude_controller_group_list.value))))
        group = tunnel_data.get("group")
        if group:
            group = as_global(",".join(list(map(str, group.value))))

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
            restrict=tunnel_data.get("restrict"),
            tunnel_interface=tunnel_data.get("tunnel_interface"),
            tunnel_tcp_mss_adjust=tunnel_data.get("tunnel_tcp_mss_adjust"),
            vbond_as_stun_server=tunnel_data.get("vbond_as_stun_server"),
            vmanage_connection_preference=tunnel_data.get("vmanage_connection_preference"),
        )

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

    def parse_tunnel_allow_service(self, data: dict) -> Optional[TunnelAllowService]:
        allow_service = data.get("tunnel_interface", {}).get("allow_service")
        if not allow_service:
            return None
        return TunnelAllowService(**allow_service)

    def parse_ppp(self, data: dict) -> Optional[Ppp]:
        pppoe_client_data = data.get("pppoe_client")
        if not pppoe_client_data:
            return None

        ppp_data = data.get("ppp", {})

        if chap := ppp_data.get("chap"):
            chap = Chap(
                hostname=chap.get("hostname"),
                ppp_auth_password=chap.get("password", {}).get("ppp_auth_password"),
            )

        if pap := ppp_data.get("pap", {}).get("sent_username", {}).get("username"):
            pap = Pap(
                ppp_auth_password=pap.get("ppp_auth_password"),
                username=pap.get("username_string"),
            )

        if callin := ppp_data.get("authentication", {}).get("callin"):
            if callin.value == "callin":
                # There is only Bidirectional and Unidirectional in the UX2 model
                callin = None
            else:
                callin = as_global(callin.value, Callin)

        method = ppp_data.get("authentication", {}).get("method", Default[None](value=None))
        if method.option_type == OptionType.GLOBAL:
            method = as_global(method.value, Method)

        return Ppp(
            dial_pool_number=pppoe_client_data["dial_pool_number"],
            ppp_max_payload=pppoe_client_data.get("ppp_max_payload"),
            method=method,
            callin=callin,
            chap=chap,
            pap=pap,
        )
