# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from copy import deepcopy
from ipaddress import IPv4Interface, IPv6Interface
from typing import Callable, Dict, List, Literal, Optional, Tuple, Type, Union

from pydantic import BaseModel

from catalystwan.api.configuration_groups.parcel import Default, Global, OptionType, Variable, as_default, as_global
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, DNSIPv4, DNSIPv6, HostMapping
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import (
    DHCP,
    Direction,
    InterfaceIPv6Container,
    InterfaceRouteIPv6Container,
    IPv4Prefix,
    IPv4RouteGatewayNextHop,
    IPv4RouteGatewayNextHopWithTracker,
    IPv6Prefix,
    IPv6StaticRouteInterface,
    LanVpnParcel,
    Nat64v4Pool,
    NatPool,
    NatPortForward,
    NATPortForwardProtocol,
    NextHopContainer,
    NextHopRouteContainer,
    OmpAdvertiseIPv4,
    OmpAdvertiseIPv6,
    ProtocolIPv4,
    ProtocolIPv6,
    RedistributeToService,
    RedistributeToServiceProtocol,
    Region,
    RouteLeakBetweenServices,
    RouteLeakFromGlobal,
    RouteLeakFromService,
    RouteLeakFromServiceProtocol,
    RoutePrefix,
    Service,
    ServiceRoute,
    ServiceType,
    StaticGreRouteIPv4,
    StaticIpsecRouteIPv4,
    StaticNat,
    StaticRouteIPv4,
    StaticRouteIPv6,
    StaticRouteVPN,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import (
    Gateway,
    Ipv4RouteItem,
    Ipv6RouteItem,
    ManagementVpnParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import (
    NextHopContainer as TransportNextHopContainer,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import (
    NextHopItem,
    NextHopItemIpv6,
    OneOfIpRouteNextHopContainer,
    OneOfIpRouteNull0,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import Prefix as TransportPrefix
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import ServiceItem
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import ServiceType as TransportServiceType
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import TransportVpnParcel
from catalystwan.utils.config_migration.converters.feature_template.helpers import create_dict_without_none

from .base import FTConverter

logger = logging.getLogger(__name__)


class RouteLeakMappingItem(BaseModel):
    ux2_model: Type[Union[RouteLeakFromGlobal, RouteLeakFromService, RouteLeakBetweenServices]]
    ux2_field: Literal["route_leak_from_global", "route_leak_from_service", "route_leak_between_services"]


class RouteMappingItem(BaseModel):
    ux2_model: Type[Union[StaticGreRouteIPv4, StaticIpsecRouteIPv4, ServiceRoute]]
    ux2_field: Literal["route_gre", "route_service", "ipsec_route"]


class OmpMappingItem(BaseModel):
    ux2_model_omp: Type[Union[OmpAdvertiseIPv4, OmpAdvertiseIPv6]]
    ux2_model_prefix: Type[Union[IPv4Prefix, IPv6Prefix]]
    ux2_field: Literal["omp_advertise_ipv4", "omp_advertise_ipv6"]


class BaseTransportAndManagementConverter(FTConverter):
    supported_template_types = ("cisco_vpn", "vpn-vedge", "vpn-vsmart")

    def parse_host_mapping(self, values: dict) -> Optional[List[HostMapping]]:
        hosts = values.get("host", [])
        if not hosts:
            return None

        hosts_cleared = [h for h in hosts if self.is_host_mapping_parsable(h)]

        return [
            HostMapping(
                host_name=host["hostname"],
                list_of_ips=self.parse_list_of_ip(host),
            )
            for host in hosts_cleared
        ]

    def parse_list_of_ip(self, host: Dict) -> Union[Variable, Global[List[str]]]:
        list_of_ips = host["ip"]
        if isinstance(list_of_ips, Variable):
            return list_of_ips

        # ["34.199.1.194"," 34.204.213.179], extra space before the ip is a bug in the feature template
        return Global[List[str]](value=[ip.strip() for ip in list_of_ips.value])

    def is_host_mapping_parsable(self, host: Dict) -> bool:
        return "ip" in host and "hostname" in host

    def parse_dns(self, values: dict) -> Tuple[DNSIPv4, DNSIPv6]:
        dns = values.get("dns", [])
        dns_ipv4 = DNSIPv4()
        dns_ipv6 = DNSIPv6()
        for dns_entry in dns:
            dns_address = dns_entry.get("dns_addr", Default[None](value=None))
            if dns_entry["role"].value == "primary":
                dns_ipv4.primary_dns_address_ipv4 = dns_address
            elif dns_entry["role"].value == "secondary":
                dns_ipv4.secondary_dns_address_ipv4 = dns_address
            elif dns_entry["role"].value == "primaryv6":
                dns_ipv6.primary_dns_address_ipv6 = dns_address
            elif dns_entry["role"].value == "secondaryv6":
                dns_ipv6.secondary_dns_address_ipv6 = dns_address
        return dns_ipv4, dns_ipv6

    def parse_route_ipv4(self, values: dict) -> Optional[List[Ipv4RouteItem]]:
        routes = values.get("ip", {}).get("route", [])
        if not routes:
            return None
        static_routes = []
        for route in routes:
            prefix = route.get("prefix")
            if not prefix:
                continue

            if prefix.option_type == OptionType.GLOBAL:
                ipv4route_item = Ipv4RouteItem(
                    prefix=TransportPrefix(
                        ip_address=as_global(prefix.value.network.network_address),
                        subnet_mask=as_global(str(prefix.value.netmask), SubnetMask),
                    )
                )
            elif prefix.option_type == OptionType.VARIABLE:
                ipv4route_item = Ipv4RouteItem(
                    prefix=TransportPrefix(ip_address=prefix, subnet_mask=as_global("0.0.0.0", SubnetMask))
                )
            if "next_hop" in route:
                ipv4route_item.gateway = as_global("nextHop", Gateway)
                for next_hop in route["next_hop"]:
                    address = next_hop.get("address")
                    if not address:
                        continue
                    ipv4route_item.next_hop = [
                        NextHopItem(
                            address=next_hop.get("address"),
                            distance=next_hop.get("distance", as_default(1)),
                        )
                    ]
            elif "dhcp" in route:
                ipv4route_item.gateway = as_global("dhcp", Gateway)
            static_routes.append(ipv4route_item)
        return static_routes

    def parse_route_ipv6(self, values: dict) -> Optional[List[Ipv6RouteItem]]:
        routes = values.get("ipv6", {}).get("route", [])
        if not routes:
            return None
        static_routes = []
        for route in routes:
            one_of_ip_route: Union[OneOfIpRouteNull0, OneOfIpRouteNextHopContainer] = OneOfIpRouteNull0()
            if "null0" in route:
                one_of_ip_route = OneOfIpRouteNull0(null0=route.get("null0"))
            elif "next_hop" in route:
                one_of_ip_route = OneOfIpRouteNextHopContainer(
                    next_hop_container=TransportNextHopContainer(
                        next_hop=[
                            NextHopItemIpv6(
                                address=next_hop.get("address"),
                                distance=next_hop.get("distance", as_default(1)),
                            )
                            for next_hop in route["next_hop"]
                        ]
                    )
                )
            else:
                one_of_ip_route = OneOfIpRouteNull0()
            ipv6route_item = Ipv6RouteItem(prefix=route.get("prefix"), one_of_ip_route=one_of_ip_route)
            static_routes.append(ipv6route_item)
        return static_routes


class ManagementVpnConverter(BaseTransportAndManagementConverter):
    def create_parcel(self, name: str, description: str, template_values: dict) -> ManagementVpnParcel:
        """
        Creates a ManagementVpnParcel parcel.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            VPN: The created ManagementVpnParcel.
        """
        data = deepcopy(template_values)

        dns_ipv4, dns_ipv6 = self.parse_dns(data)
        ipv4_route = self.parse_route_ipv4(data)
        ipv6_route = self.parse_route_ipv6(data)
        new_host_mapping = self.parse_host_mapping(data)
        dns_ipv4, dns_ipv6 = self.parse_dns(data)

        payload = create_dict_without_none(
            dns_ipv4=dns_ipv4,
            dns_ipv6=dns_ipv6,
            new_host_mapping=new_host_mapping,
            ipv6_route=ipv6_route,
            ipv4_route=ipv4_route,
        )

        return ManagementVpnParcel(parcel_name=name, parcel_description=description, **payload)


class TransportVpnConverter(BaseTransportAndManagementConverter):
    def create_parcel(self, name: str, description: str, template_values: dict) -> TransportVpnParcel:
        """
        Creates a TransportVpnParcel parcel.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            VPN: The created TransportVpnParcel.
        """
        data = deepcopy(template_values)

        ipv4_route = self.parse_route_ipv4(data)
        ipv6_route = self.parse_route_ipv6(data)
        new_host_mapping = self.parse_host_mapping(data)
        dns_ipv4, dns_ipv6 = self.parse_dns(data)
        service = self.parse_service(data.get("service", []))
        enhance_ecmp_keying = data.get("enhance_ecmp_keying", {}).get("layer4")

        payload = create_dict_without_none(
            service=service,
            enhance_ecmp_keying=enhance_ecmp_keying,
            dns_ipv4=dns_ipv4,
            dns_ipv6=dns_ipv6,
            new_host_mapping=new_host_mapping,
            ipv6_route=ipv6_route,
            ipv4_route=ipv4_route,
        )

        return TransportVpnParcel(parcel_name=name, parcel_description=description, **payload)

    def parse_service(self, services: List[Dict]) -> Optional[List[ServiceItem]]:
        if not services:
            return None
        return [
            ServiceItem(
                service_type=as_global(service["svc_type"].value, TransportServiceType),
            )
            for service in services
        ]


class ServiceVpnConverter(FTConverter):
    """
    A class for converting template values into a LanVpnParcel object.
    """

    supported_template_types = ("cisco_vpn", "vpn-vedge", "vpn-vsmart")

    route_leaks_mapping = {
        "route_import": RouteLeakMappingItem(ux2_model=RouteLeakFromGlobal, ux2_field="route_leak_from_global"),
        "route_export": RouteLeakMappingItem(ux2_model=RouteLeakFromService, ux2_field="route_leak_from_service"),
        "route_import_from": RouteLeakMappingItem(
            ux2_model=RouteLeakBetweenServices, ux2_field="route_leak_between_services"
        ),
    }

    routes_mapping = {
        "route_gre": RouteMappingItem(ux2_model=StaticGreRouteIPv4, ux2_field="route_gre"),
        "route_service": RouteMappingItem(ux2_model=ServiceRoute, ux2_field="route_service"),
        "ipsec_route": RouteMappingItem(ux2_model=StaticIpsecRouteIPv4, ux2_field="ipsec_route"),
    }

    omp_mapping = {
        "advertise": OmpMappingItem(
            ux2_model_omp=OmpAdvertiseIPv4,
            ux2_model_prefix=IPv4Prefix,
            ux2_field="omp_advertise_ipv4",
        ),
        "ipv6_advertise": OmpMappingItem(
            ux2_model_omp=OmpAdvertiseIPv6, ux2_model_prefix=IPv6Prefix, ux2_field="omp_advertise_ipv6"
        ),
    }

    def create_parcel(self, name: str, description: str, template_values: dict) -> LanVpnParcel:
        """
        Creates a parcel from VPN family object based on the provided parameters.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            VPN: The created VPN object.
        """
        data = deepcopy(template_values)

        vpn_name = data.get("name")
        vpn_id = data.get("vpn_id")
        omp_admin_distance_ipv4 = data.get("omp_admin_distance_ipv4")
        omp_admin_distance_ipv6 = data.get("omp_admin_distance_ipv6")
        dns_ipv4, dns_ipv6 = self.parse_dns(data.get("dns", []))
        new_host_mapping = self.parse_host_mapping(data.get("host", []))
        net_port_forwarding = self.parse_port_forwarding(data.get("nat", {}).get("port_forward", []))
        nat_pool = self.parse_natpool(data.get("nat", {}).get("natpool", []))
        static_nat = self.parse_static_nat(data.get("nat", {}).get("static", []))
        nat_64_v4_pool = self.parse_nat64_v4_pool(data.get("nat64", {}).get("v4", {}).get("pool", []))
        service = self.parse_service(data.get("service", []))

        self.parse_omp(data)
        self.parse_ipv4_route(data)
        self.parse_ipv6_route(data)
        self.parse_routes(data)
        self.parse_route_leaks(data)

        omp_advertise_ipv4 = data.get("omp_advertise_ipv4")
        omp_advertise_ipv6 = data.get("omp_advertise_ipv6")
        route_gre = data.get("route_gre")
        route_service = data.get("route_service")
        ipsec_route = data.get("ipsec_route")
        route_leak_from_global = data.get("route_leak_from_global")
        route_leak_from_service = data.get("route_leak_from_service")
        route_leak_between_services = data.get("route_leak_between_services")
        mpls_vpn_ipv4_route_target = data.get("mpls_vpn_ipv4_route_target")
        mpls_vpn_ipv6_route_target = data.get("mpls_vpn_ipv6_route_target")
        enable_sdra = data.get("enable_sdra")
        ipv6_route = data.get("ipv6_route")
        ipv4_route = data.get("ipv4_route")

        payload = create_dict_without_none(
            parcel_name=name,
            parcel_description=description,
            vpn_name=vpn_name,
            vpn_id=vpn_id,
            omp_admin_distance_ipv4=omp_admin_distance_ipv4,
            omp_admin_distance_ipv6=omp_admin_distance_ipv6,
            dns_ipv4=dns_ipv4,
            dns_ipv6=dns_ipv6,
            new_host_mapping=new_host_mapping,
            net_port_forwarding=net_port_forwarding,
            nat_pool=nat_pool,
            static_nat=static_nat,
            nat_64_v4_pool=nat_64_v4_pool,
            service=service,
            omp_advertise_ipv4=omp_advertise_ipv4,
            omp_advertise_ipv6=omp_advertise_ipv6,
            route_gre=route_gre,
            route_service=route_service,
            ipsec_route=ipsec_route,
            route_leak_from_global=route_leak_from_global,
            route_leak_from_service=route_leak_from_service,
            route_leak_between_services=route_leak_between_services,
            mpls_vpn_ipv4_route_target=mpls_vpn_ipv4_route_target,
            mpls_vpn_ipv6_route_target=mpls_vpn_ipv6_route_target,
            enable_sdra=enable_sdra,
            ipv6_route=ipv6_route,
            ipv4_route=ipv4_route,
        )

        return LanVpnParcel(**payload)

    def parse_dns(self, dns: dict) -> Tuple[DNSIPv4, DNSIPv6]:
        dns_ipv4 = DNSIPv4()
        dns_ipv6 = DNSIPv6()
        for dns_entry in dns:
            dns_address = dns_entry.get("dns_addr", Default[None](value=None))
            if dns_entry["role"].value == "primary":
                dns_ipv4.primary_dns_address_ipv4 = dns_address
            elif dns_entry["role"].value == "secondary":
                dns_ipv4.secondary_dns_address_ipv4 = dns_address
            elif dns_entry["role"].value == "primaryv6":
                dns_ipv6.primary_dns_address_ipv6 = dns_address
            elif dns_entry["role"].value == "secondaryv6":
                dns_ipv6.secondary_dns_address_ipv6 = dns_address
        return dns_ipv4, dns_ipv6

    def parse_host_mapping(self, hosts: List[Dict]) -> Optional[List[HostMapping]]:
        if not hosts:
            return None

        hosts_cleared = [h for h in hosts if self.is_host_mapping_parsable(h)]

        return [
            HostMapping(
                host_name=host["hostname"],
                list_of_ips=self.parse_list_of_ip(host),
            )
            for host in hosts_cleared
        ]

    def parse_list_of_ip(self, host: Dict) -> Union[Variable, Global[List[str]]]:
        list_of_ips = host["ip"]
        if isinstance(list_of_ips, Variable):
            return list_of_ips

        # ["34.199.1.194"," 34.204.213.179], extra space before the ip is a bug in the feature template
        return Global[List[str]](value=[ip.strip() for ip in list_of_ips.value])

    def is_host_mapping_parsable(self, host: Dict) -> bool:
        return "ip" in host and "hostname" in host

    def parse_service(self, service: List[Dict]) -> Optional[List[Service]]:
        if not service:
            return None
        service_items = []
        for entry in service:
            service_type = entry.get("svc_type")
            if isinstance(service_type, Global):
                service_type = as_global(service_type.value, ServiceType)
            service_item = Service(
                service_type=service_type,
                ipv4_addresses=entry.get("address"),  # type: ignore
                tracking=entry.get("track_enable", as_default(True)),
            )
            service_items.append(service_item)
        return service_items

    def parse_natpool(self, natpool: List[Dict]) -> Optional[List[NatPool]]:
        if not natpool:
            return None
        nat_items = []
        for entry in natpool:
            direction = entry.get("direction")
            nat_pool_name = entry.get("name")
            prefix_length = entry.get("prefix_length")
            range_start = entry.get("range_start")
            range_end = entry.get("range_end")
            overload = entry.get("overload", as_default(True))

            if (
                nat_pool_name is None
                or prefix_length is None
                or range_start is None
                or range_end is None
                or direction is None
            ):
                continue

            if isinstance(direction, Global):
                direction = as_global(str(direction.value), Direction)

            nat_items.append(
                NatPool(
                    nat_pool_name=nat_pool_name,
                    prefix_length=prefix_length,
                    range_start=range_start,
                    range_end=range_end,
                    overload=overload,
                    direction=direction,
                )
            )
        return nat_items

    def parse_port_forwarding(self, port_forward: List[Dict]) -> Optional[List[NatPortForward]]:
        if not port_forward:
            return None
        nat_port_forwarding_items = []
        for entry in port_forward:
            protocol = entry.get("proto")
            if isinstance(protocol, Global):
                protocol = as_global(protocol.value.upper(), NATPortForwardProtocol)
            nat_port_forwarding_items.append(
                NatPortForward(
                    **create_dict_without_none(
                        nat_pool_name=entry.get("pool_name"),
                        source_port=entry.get("source_port"),
                        translate_port=entry.get(
                            "translate_port",
                        ),
                        source_ip=entry.get("source_ip"),
                        translated_source_ip=entry.get(
                            "translate_ip",
                        ),
                        protocol=protocol,
                    )
                )
            )
        return nat_port_forwarding_items

    def parse_static_nat(self, static_nat: List[Dict]) -> Optional[List[StaticNat]]:
        if not static_nat:
            return None
        static_nat_items = []
        for entry in static_nat:
            static_nat_direction = entry.get("static_nat_direction")
            nat_pool_name = entry.get("pool_name")
            source_ip = entry.get("source_ip")
            translated_source_ip = entry.get("translate_ip")

            if (
                static_nat_direction is None
                or nat_pool_name is None
                or source_ip is None
                or translated_source_ip is None
            ):
                continue

            if isinstance(static_nat_direction, Global):
                static_nat_direction = as_global(static_nat_direction.value, Direction)

            static_nat_items.append(
                StaticNat(
                    nat_pool_name=nat_pool_name,
                    source_ip=source_ip,
                    translated_source_ip=translated_source_ip,
                    static_nat_direction=static_nat_direction,
                )  # type: ignore
            )
        return static_nat_items

    def parse_nat64_v4_pool(self, nat64pool: List[Dict]) -> Optional[List[Nat64v4Pool]]:
        if not nat64pool:
            return None
        return [
            Nat64v4Pool(
                **create_dict_without_none(
                    nat64_v4_pool_name=entry.get("name"),
                    nat64_v4_pool_range_start=entry.get("start_address"),
                    nat64_v4_pool_range_end=entry.get("end_address"),
                    nat64_v4_pool_overload=entry.get("overload", as_default(False)),
                )
            )
            for entry in nat64pool  # type: ignore
        ]

    def parse_ipv4_route(self, values: dict) -> None:
        ipv4_route = values.get("ip", {}).get("route", [])
        if not ipv4_route:
            return
        if len(ipv4_route) == 1 and ipv4_route[0] == {}:
            # Sometimes it parses as a list with an empty dictionary
            return

        ipv4_route_items = []
        for route in ipv4_route:
            prefix: Union[Global, Variable] = route.pop("prefix", None)
            if prefix.option_type == OptionType.GLOBAL:
                interface = IPv4Interface(prefix.value)
                route_prefix = RoutePrefix(
                    ip_address=as_global(interface.network.network_address),
                    subnet_mask=as_global(str(interface.netmask)),
                )

            elif prefix.option_type == OptionType.VARIABLE:
                route_prefix = RoutePrefix(
                    ip_address=prefix,
                    subnet_mask=as_global("0.0.0.0"),
                )
            ip_route_item = None
            if "next_hop" in route:
                next_hop_items = []
                for next_hop in route.pop("next_hop", []):
                    address = next_hop.pop("address", None)
                    distance = next_hop.pop("distance", as_default(1))
                    if address is None:
                        continue

                    next_hop_items.append(
                        IPv4RouteGatewayNextHop(
                            address=address,
                            distance=distance,
                        )
                    )
                ip_route_item = NextHopRouteContainer(next_hop_container=NextHopContainer(next_hop=next_hop_items))
            elif "next_hop_with_track" in route:
                next_hop_with_track_items = []
                for next_hop_with_track in route.pop("next_hop_with_track", []):
                    tracker = next_hop_with_track.pop("tracker")
                    if tracker:
                        logger.warning(
                            f"Tracker can be any value in UX1.0, but must be UUID in UX2.0. Current value {tracker}"
                        )

                    address = next_hop_with_track.pop("address", None)
                    distance = next_hop_with_track.pop("distance", as_default(1))
                    if address is None:
                        continue

                    next_hop_with_track_items.append(
                        IPv4RouteGatewayNextHopWithTracker(address=address, distance=distance)
                    )

                ip_route_item = NextHopRouteContainer(
                    next_hop_container=NextHopContainer(next_hop_with_tracker=next_hop_with_track_items)
                )
            elif "vpn" in route:
                ip_route_item = StaticRouteVPN(  # type: ignore
                    vpn=as_global(True),
                )
            elif "dhcp" in route:
                ip_route_item = DHCP(  # type: ignore
                    dhcp=as_global(True),
                )
            else:
                # Let's assume it's a static route with enabled VPN
                ip_route_item = StaticRouteVPN(  # type: ignore
                    vpn=as_global(True),
                )
            ipv4_route_items.append(StaticRouteIPv4(prefix=route_prefix, one_of_ip_route=ip_route_item))  # type: ignore
        values["ipv4_route"] = ipv4_route_items

    def parse_ipv6_route(self, values: dict) -> None:
        if ipv6_route := values.get("ipv6", {}).get("route", []):
            ipv6_route_items = []
            for route in ipv6_route:
                ipv6_interface = IPv6Interface(route.get("prefix").value)
                route_prefix = RoutePrefix(
                    ip_address=as_global(ipv6_interface.network.network_address),
                    subnet_mask=as_global(str(ipv6_interface.netmask)),
                )
                if route_interface := route.pop("route_interface", []):
                    static_route_interfaces = [IPv6StaticRouteInterface(**entry) for entry in route_interface]
                    ipv6_route_item = InterfaceRouteIPv6Container(
                        interface_container=InterfaceIPv6Container(ipv6_static_route_interface=static_route_interfaces)
                    )
                ipv6_route_items.append(StaticRouteIPv6(prefix=route_prefix, one_of_ip_route=ipv6_route_item))
            values["ipv6_route"] = ipv6_route_items

    def parse_omp(self, values: dict) -> None:
        for omp in self.omp_mapping.keys():
            if omp_advertises := values.get("omp", {}).get(omp, []):
                pydantic_model_omp = self.omp_mapping[omp].ux2_model_omp
                pydantic_model_prefix = self.omp_mapping[omp].ux2_model_prefix
                pydantic_field = self.omp_mapping[omp].ux2_field
                self._parse_omp(values, omp_advertises, pydantic_model_omp, pydantic_model_prefix, pydantic_field)

    def _parse_omp(
        self, values: dict, omp_advertises: list, pydantic_model_omp, pydantic_model_prefix, pydantic_field
    ) -> None:
        omp_advertise_items = []
        for entry in omp_advertises:
            prefix_list_items = []
            for prefix_entry in entry.get("prefix_list", []):
                prefix_list_items.append(
                    pydantic_model_prefix(
                        prefix=prefix_entry["prefix_entry"],
                        aggregate_only=prefix_entry["aggregate_only"],
                        region=as_global(prefix_entry["region"].value, Region),
                    )
                )
            if pydantic_model_omp == OmpAdvertiseIPv4:
                pydantic_model_protocol = ProtocolIPv4
            else:
                pydantic_model_protocol = ProtocolIPv6
            omp_advertise_items.append(
                pydantic_model_omp(
                    omp_protocol=as_global(entry["protocol"].value, pydantic_model_protocol),
                    prefix_list=prefix_list_items if prefix_list_items else None,
                )
            )
        values[pydantic_field] = omp_advertise_items

    def parse_routes(self, values: dict) -> None:
        for route in self.routes_mapping.keys():
            if routes := values.get("ip", {}).get(route, []):
                pydantic_model = self.routes_mapping[route].ux2_model
                pydantic_field = self.routes_mapping[route].ux2_field
                self._parse_route(values, routes, pydantic_model, pydantic_field)

    def _parse_route(self, values: dict, routes: list, pydantic_model, pydantic_field) -> None:
        items = []
        for route in routes:
            ipv4_interface = IPv4Interface(route.get("prefix").value)
            service_prefix = AddressWithMask(
                address=as_global(ipv4_interface.network.network_address),
                mask=as_global(str(ipv4_interface.netmask)),
            )
            items.append(pydantic_model(prefix=service_prefix, vpn=route.get("vpn")))
        values[pydantic_field] = items

    def parse_route_leaks(self, values: dict) -> None:
        for leak in self.route_leaks_mapping.keys():
            if route_leaks := values.get(leak, []):
                pydantic_model = self.route_leaks_mapping[leak].ux2_model
                pydantic_field = self.route_leaks_mapping[leak].ux2_field
                self._parse_leak(values, route_leaks, pydantic_model, pydantic_field)

    def _parse_leak(self, values: dict, route_leaks: list, pydantic_model, pydantic_field) -> None:
        items = []
        for rl in route_leaks:
            redistribute_items = []
            for redistribute_item in rl.get("redistribute_to", []):
                redistribute_items.append(
                    RedistributeToService(
                        protocol=as_global(redistribute_item["protocol"].value, RedistributeToServiceProtocol),
                    )
                )
            configuration = {
                "route_protocol": as_global(rl["protocol"].value, RouteLeakFromServiceProtocol),
                "redistribute_to_protocol": redistribute_items if redistribute_items else None,
            }
            if pydantic_model == RouteLeakBetweenServices:
                configuration["source_vpn"] = rl["source_vpn"]
            items.append(pydantic_model(**configuration))
        values[pydantic_field] = items


class VpnConverter(FTConverter):
    supported_template_types = ("cisco_vpn", "vpn-vedge", "vpn-vsmart")

    def create_parcel(
        self, name: str, description: str, template_values: dict
    ) -> Union[LanVpnParcel, TransportVpnParcel, ManagementVpnParcel]:
        """
        Creates a parcel from VPN family object based on the provided parameters.

        Args:
            name (str): The name of the parcel.
            description (str): The description of the parcel.
            template_values (dict): A dictionary containing the template values.

        Returns:
            VPN: The created VPN object.
        """

        vpn_converters: Dict[
            int, Callable[..., Union[TransportVpnConverter, ManagementVpnConverter, ServiceVpnConverter]]
        ] = {
            0: TransportVpnConverter,
            512: ManagementVpnConverter,
        }
        vpn_id = self.get_vpn_id(template_values)
        converter = vpn_converters.get(vpn_id, ServiceVpnConverter)()
        parcel = converter.create_parcel(name, description, template_values)
        self._convert_result.info = converter._convert_result.info
        self._convert_result.status = converter._convert_result.status
        return parcel

    def get_vpn_id(self, values: dict) -> int:
        return int(values["vpn_id"].value)
