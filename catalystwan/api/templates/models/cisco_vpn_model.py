# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field, field_validator

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.models.common import Protocol, StaticNatDirection

Role = Literal["primary", "secondary"]
SvcType = Literal["FW", "IDS", "IDP", "netsvc1", "netsvc2", "netsvc3", "netsvc4", "TE", "appqoe"]
ServiceRouteService = Literal["sig"]
Nat = Literal["NAT64", "NAT66"]
AdvertiseProtocol = Literal[
    "bgp", "ospf", "ospfv3", "connected", "static", "network", "aggregate", "eigrp", "lisp", "isis"
]
AdvertiseProtocolSubType = Literal["external"]
Region = Literal["core", "access"]
Ipv6AdvertiseProtocol = Literal["bgp", "ospf", "connected", "static", "network", "aggregate"]
Ipv6AdvertiseProtocolSubType = Literal["external"]
LeakFromGlobalProtocol = Literal["all", "static", "mobile", "connected", "rip", "odr"]
Overload = Literal["true", "false"]
RouteImportProtocol = Literal["static", "connected", "bgp", "ospf"]
RouteImportProtocolSubType = Literal["external"]
RouteImportRedistributeProtocol = Literal["bgp", "eigrp", "ospf"]
RouteImportFromProtocol = Literal["static", "connected", "bgp", "ospf", "eigrp"]
RouteImportFromProtocolSubType = Literal["external"]
RouteImportFromRedistributeProtocol = Literal["bgp", "eigrp", "ospf"]
RouteExportProtocol = Literal["static", "connected", "bgp", "eigrp", "ospf"]
RouteExportProtocolSubType = Literal["external"]
RouteExportRedistributeProtocol = Literal["bgp", "ospf"]


class Dns(FeatureTemplateValidator):
    dns_addr: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "dns-addr"}, description="The IP address of the DNS server."
    )
    role: Role = Field(default="primary", description="The role of the DNS server, either 'PRIMARY' or 'SECONDARY'.")
    model_config = ConfigDict(populate_by_name=True)


class DnsIpv6(FeatureTemplateValidator):
    dns_addr: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "dns-addr"}, description="The IPv6 address of the DNS server."
    )
    role: Optional[Role] = Field(
        default="primary",
        description="The role of the DNS server for IPv6, optionally either 'PRIMARY' or 'SECONDARY'.",
    )
    model_config = ConfigDict(populate_by_name=True)


class Host(FeatureTemplateValidator):
    hostname: str = Field(..., description="The hostname of the device.")
    ip: List[str] = Field(..., description="A list of IP addresses associated with the hostname.")


class Service(FeatureTemplateValidator):
    svc_type: SvcType = Field(
        description="The type of service to be configured.", json_schema_extra={"vmanage_key": "svc-type"}
    )
    address: Optional[List[str]] = Field(default=None, description="A list of IP addresses for the service.")
    interface: Optional[str] = Field(default=None, description="The interface associated with the service.")
    track_enable: BoolStr = Field(
        default=True,
        description="Indicates whether tracking is enabled for the service.",
        json_schema_extra={"vmanage_key": "track-enable"},
    )
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("track_enable")
    @classmethod
    def convert_to_string(cls, value):
        return str(value).lower()


class ServiceRoute(FeatureTemplateValidator):
    prefix: str = Field(description="The network prefix for the service route.")
    vpn: int = Field(description="The VPN identifier where the service route is to be applied.")
    service: ServiceRouteService = Field(default="sig", description="The service associated with the route.")


class NextHop(FeatureTemplateValidator):
    address: Optional[str] = Field(default=None, description="The IP address of the next hop for the route.")
    distance: Optional[int] = Field(default=1, description="The administrative distance of the next hop.")


class NextHopWithTrack(FeatureTemplateValidator):
    address: Optional[str] = Field(
        default=None, description="The IP address of the next hop for the route that requires tracking."
    )
    distance: Optional[int] = Field(
        default=1, description="The administrative distance of the next hop that requires tracking."
    )
    tracker: str = Field(description="The tracker associated with this next hop.")


class RouteInterface(FeatureTemplateValidator):
    interface_name: str = Field(
        description="The name of the interface used for routing.", json_schema_extra={"vmanage_key": "interface-name"}
    )
    interface_next_hop: Optional[List[NextHop]] = Field(
        default=None,
        description="A list of next hops associated with the interface for routing purposes.",
        json_schema_extra={"vmanage_key": "interface-next-hop", "priority_order": ["address", "distance"]},
    )
    model_config = ConfigDict(populate_by_name=True)


class Routev4(FeatureTemplateValidator):
    prefix: Optional[str] = Field(default=None, description="The IPv4 network prefix for the static route.")
    next_hop: Optional[List[NextHop]] = Field(
        default=None,
        description="A list of IPv4 next hops for the route.",
        json_schema_extra={"vmanage_key": "next-hop", "priority_order": ["address", "distance"]},
    )
    next_hop_with_track: Optional[List[NextHopWithTrack]] = Field(
        default=None,
        description="A list of IPv4 next hops with tracking for the route.",
        json_schema_extra={"vmanage_key": "next-hop-with-track"},
    )
    route_interface: Optional[RouteInterface] = Field(
        default=None,
        description="The interface configuration for the IPv4 static route.",
        json_schema_extra={"vmanage_key": "route-interface"},
    )
    null0: Optional[BoolStr] = Field(
        default=None, description="A flag indicating whether to route traffic to null0 for this static route."
    )
    distance: Optional[int] = Field(default=None, description="The administrative distance for the static route.")
    vpn: Optional[int] = Field(
        default=None, description="The VPN instance identifier associated with the static route."
    )
    dhcp: Optional[BoolStr] = Field(
        default=None, description="A flag indicating whether DHCP is used for this static route."
    )

    model_config = ConfigDict(populate_by_name=True)


class NextHopv6(FeatureTemplateValidator):
    address: str = Field(description="The IPv6 address of the next hop for the route.")
    distance: Optional[int] = Field(default=1, description="The administrative distance of the IPv6 next hop.")


class Routev6(FeatureTemplateValidator):
    prefix: str = Field(description="The IPv6 network prefix for the static route.")
    next_hop: Optional[List[NextHopv6]] = Field(
        default=None,
        description="A list of IPv6 next hops for the route.",
        json_schema_extra={"vmanage_key": "next-hop"},
    )
    null0: Optional[BoolStr] = Field(
        default=None, description="A flag indicating whether to route IPv6 traffic to null0 for this static route."
    )
    vpn: Optional[int] = Field(
        default=None, description="The VPN instance identifier associated with the IPv6 static route."
    )
    nat: Optional[Nat] = Field(
        default=None, description="The type of NAT to apply for the IPv6 static route, if applicable."
    )
    model_config = ConfigDict(populate_by_name=True)


class GreRoute(FeatureTemplateValidator):
    prefix: str = Field(description="The network prefix for the GRE (Generic Routing Encapsulation) route.")
    vpn: int = Field(description="The VPN identifier where the GRE route is to be applied.")
    interface: Optional[List[str]] = Field(
        default=None, description="A list of interfaces associated with the GRE route."
    )


class IpsecRoute(FeatureTemplateValidator):
    prefix: str = Field(description="The network prefix for the IPSec (Internet Protocol Security) route.")
    vpn: int = Field(description="The VPN identifier where the IPSec route is to be applied.")
    interface: Optional[List[str]] = Field(
        default=None, description="A list of interfaces associated with the IPSec route."
    )


class PrefixList(FeatureTemplateValidator):
    prefix_entry: str = Field(
        description="The network prefix entry for the prefix list.", json_schema_extra={"vmanage_key": "prefix-entry"}
    )
    aggregate_only: Optional[BoolStr] = Field(
        default=None,
        description="A flag indicating if only aggregate routes should be considered.",
        json_schema_extra={"vmanage_key": "aggregate-only"},
    )
    region: Optional[Region] = Field(default=None, description="The network region where the prefix list is applied.")
    model_config = ConfigDict(populate_by_name=True)


class Advertise(FeatureTemplateValidator):
    protocol: AdvertiseProtocol = Field(description="The protocol used for route advertisement.")
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy associated with advertisement.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    protocol_sub_type: Optional[List[AdvertiseProtocolSubType]] = Field(
        default=None,
        description="A list of subtypes for the advertisement protocol.",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    prefix_list: Optional[List[PrefixList]] = Field(
        default=None,
        description="A list of prefix lists associated with the advertisement settings.",
        json_schema_extra={"vmanage_key": "prefix-list"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Advertise(FeatureTemplateValidator):
    protocol: Ipv6AdvertiseProtocol = Field(description="The IPv6 protocol used for route advertisement.")
    route_policy: Optional[str] = Field(
        default=None,
        description="The IPv6 route policy associated with advertisement.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    protocol_sub_type: Optional[List[Ipv6AdvertiseProtocolSubType]] = Field(
        default=None,
        description="A list of subtypes for the IPv6 advertisement protocol.",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    prefix_list: Optional[List[PrefixList]] = Field(
        default=None,
        description="A list of IPv6 prefix lists associated with the advertisement settings.",
        json_schema_extra={"vmanage_key": "prefix-list"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Pool(FeatureTemplateValidator):
    name: str = Field(description="The name of the IP address pool.")
    start_address: str = Field(
        description="The starting IP address of the pool.", json_schema_extra={"vmanage_key": "start-address"}
    )
    end_address: str = Field(
        description="The ending IP address of the pool.", json_schema_extra={"vmanage_key": "end-address"}
    )
    overload: Optional[BoolStr] = Field(
        default=None, description="A flag indicating whether address overload is allowed."
    )
    leak_from_global: BoolStr = Field(description="A flag indicating whether leaking from the global table is enabled.")
    leak_from_global_protocol: LeakFromGlobalProtocol = Field(
        description="The protocol used for leaking from the global routing table."
    )
    leak_to_global: BoolStr = Field(description="A flag indicating whether leaking to the global table is enabled.")
    model_config = ConfigDict(populate_by_name=True)


class Natpool(FeatureTemplateValidator):
    name: int = Field(description="The identifier for the NAT pool.")
    prefix_length: Optional[int] = Field(
        default=None,
        description="The length of the network prefix for the NAT pool.",
        json_schema_extra={"vmanage_key": "prefix-length"},
    )
    range_start: str = Field(
        default=None,
        description="The starting IP address for the NAT pool range.",
        json_schema_extra={"vmanage_key": "range-start"},
    )
    range_end: Optional[str] = Field(
        default=None,
        description="The ending IP address for the NAT pool range.",
        json_schema_extra={"vmanage_key": "range-end"},
    )
    overload: Overload = Field(
        default="true", description="Flag indicating whether NAT overload (PAT) is enabled for the pool."
    )
    direction: StaticNatDirection = Field(description="The direction (inside or outside) associated with the NAT pool.")
    tracker_id: Optional[int] = Field(
        default=None,
        description="The tracker identifier associated with the NAT pool.",
        json_schema_extra={"vmanage_key": "tracker-id"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Static(FeatureTemplateValidator):
    pool_name: Optional[int] = Field(
        default=None,
        description="The identifier for the NAT pool associated with the static NAT rule.",
        json_schema_extra={"vmanage_key": "pool-name"},
    )
    source_ip: Optional[str] = Field(
        default=None,
        description="The original source IP address to be translated by static NAT.",
        json_schema_extra={"vmanage_key": "source-ip"},
    )
    translate_ip: Optional[str] = Field(
        default=None,
        description="The translated IP address used by static NAT.",
        json_schema_extra={"vmanage_key": "translate-ip"},
    )
    static_nat_direction: StaticNatDirection = Field(
        description="The direction (inside or outside) for the static NAT rule.",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
    )
    tracker_id: Optional[int] = Field(
        default=None,
        description="The tracker identifier associated with the static NAT rule.",
        json_schema_extra={"vmanage_key": "tracker-id"},
    )
    model_config = ConfigDict(populate_by_name=True)


class SubnetStatic(FeatureTemplateValidator):
    source_ip_subnet: str = Field(
        description="The original source IP subnet to be translated by static NAT.",
        json_schema_extra={"vmanage_key": "source-ip-subnet"},
    )
    translate_ip_subnet: str = Field(
        description="The translated IP subnet used by static NAT.",
        json_schema_extra={"vmanage_key": "translate-ip-subnet"},
    )
    prefix_length: int = Field(
        description="The prefix length for the translated IP subnet in static NAT.",
        json_schema_extra={"vmanage_key": "prefix-length"},
    )
    static_nat_direction: StaticNatDirection = Field(
        description="The direction (inside or outside) for the subnet static NAT rule.",
        json_schema_extra={"vmanage_key": "static-nat-direction"},
    )
    tracker_id: Optional[int] = Field(
        default=None,
        description="The tracker identifier associated with the subnet static NAT rule.",
        json_schema_extra={"vmanage_key": "tracker-id"},
    )
    model_config = ConfigDict(populate_by_name=True)


class PortForward(FeatureTemplateValidator):
    pool_name: Optional[int] = Field(
        default=None,
        description="The identifier for the NAT pool associated with the port forwarding rule.",
        json_schema_extra={"vmanage_key": "pool-name"},
    )
    source_port: int = Field(
        description="The source port number for the port forwarding rule.",
        json_schema_extra={"vmanage_key": "source-port"},
    )
    translate_port: int = Field(
        description="The destination port number to which the source port is translated.",
        json_schema_extra={"vmanage_key": "translate-port"},
    )
    source_ip: str = Field(
        description="The source IP address for the port forwarding rule.",
        json_schema_extra={"vmanage_key": "source-ip"},
    )
    translate_ip: str = Field(
        description="The destination IP address to which the source IP is translated.",
        json_schema_extra={"vmanage_key": "translate-ip"},
    )
    proto: Protocol = Field(description="The protocol used in the port forwarding rule (TCP/UDP).")
    model_config = ConfigDict(populate_by_name=True)


class RouteImportRedistribute(FeatureTemplateValidator):
    protocol: RouteImportRedistributeProtocol = Field(
        description="The protocol from which routes are to be redistributed."
    )
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy that specifies the conditions for route redistribution.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteImport(FeatureTemplateValidator):
    protocol: RouteImportProtocol = Field(description="The protocol from which routes are to be imported.")
    protocol_sub_type: List[RouteImportProtocolSubType] = Field(
        description="The list of subtypes for the import protocol.",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy that specifies the conditions for route import.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    redistribute: Optional[List[RouteImportRedistribute]] = Field(
        default=None,
        description="A list of redistribute configurations that define how routes from other protocols are imported.",
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteImportFromRedistribute(FeatureTemplateValidator):
    protocol: RouteImportFromRedistributeProtocol = Field(
        description="The protocol from which routes are to be redistributed into the local routing table."
    )
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy that defines the conditions for route redistribution.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteImportFrom(FeatureTemplateValidator):
    source_vpn: int = Field(
        description="The VPN instance (VRF) from which routes are to be imported.",
        json_schema_extra={"vmanage_key": "source-vpn"},
    )
    protocol: RouteImportFromProtocol = Field(description="The routing protocol from which routes are to be imported.")
    protocol_sub_type: List[RouteImportFromProtocolSubType] = Field(
        description="The list of protocol subtypes for route importation.",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy that specifies the criteria for route importation.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    redistribute: Optional[List[RouteImportFromRedistribute]] = Field(
        default=None,
        description=(
            "A list of route redistribution configurations specifying how routes from other protocols are imported."
        ),
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteExportRedistribute(FeatureTemplateValidator):
    protocol: RouteExportRedistributeProtocol = Field(
        description="The protocol from which routes are to be redistributed out of the local routing table."
    )
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy that defines the conditions for route redistribution.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteExport(FeatureTemplateValidator):
    protocol: RouteExportProtocol = Field(description="The routing protocol to which routes are to be exported.")
    protocol_sub_type: List[RouteExportProtocolSubType] = Field(
        description="The list of protocol subtypes for route exportation.",
        json_schema_extra={"vmanage_key": "protocol-sub-type"},
    )
    route_policy: Optional[str] = Field(
        default=None,
        description="The route policy that specifies the criteria for route exportation.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    redistribute: Optional[List[RouteExportRedistribute]] = Field(
        default=None,
        description=(
            "A list of route redistribution configurations specifying how routes from other protocols are exported."
        ),
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoVPNModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco VPN Feature Template configuration."

    vpn_id: int = Field(
        default=0,
        description="The unique identifier for the VPN instance (VRF).",
        json_schema_extra={"vmanage_key": "vpn-id"},
    )
    vpn_name: Optional[str] = Field(
        default=None, description="The name of the VPN instance.", json_schema_extra={"vmanage_key": "name"}
    )
    tenant_vpn_id: Optional[int] = Field(
        default=None,
        description="The tenant-specific identifier for the VPN instance, used in multi-tenant environments.",
        json_schema_extra={"vmanage_key": "tenant-vpn-id"},
    )
    org_name: Optional[str] = Field(
        default=None,
        description="The name of the organization to which the VPN instance belongs.",
        json_schema_extra={"vmanage_key": "org-name"},
    )
    omp_admin_distance_ipv4: Optional[int] = Field(
        default=None,
        description="The administrative distance for IPv4 routes received over the Overlay Management Protocol (OMP).",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv4"},
    )
    omp_admin_distance_ipv6: Optional[int] = Field(
        default=None,
        description="The administrative distance for IPv6 routes received over OMP.",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv6"},
    )
    dns: Optional[List[Dns]] = Field(
        default=None,
        description="A list of DNS configurations for the VPN instance.",
    )
    dns_ipv6: Optional[List[DnsIpv6]] = Field(
        default=None,
        description="A list of DNS configurations for IPv6 within the VPN instance.",
        json_schema_extra={"vmanage_key": "dns-ipv6"},
    )
    layer4: Optional[BoolStr] = Field(
        default=None,
        description="A flag indicating whether Layer 4 information is included in the ECMP hash key.",
        json_schema_extra={"data_path": ["ecmp-hash-key"]},
    )
    host: Optional[List[Host]] = Field(
        default=None,
        description="A list of host configurations within the VPN instance.",
        json_schema_extra={"priority_order": ["hostname", "ip"]},
    )
    service: Optional[List[Service]] = Field(
        default=None,
        description="A list of service configurations associated with the VPN instance.",
    )
    service_route: Optional[List[ServiceRoute]] = Field(
        default=None,
        description="A list of service route configurations for directing traffic to services within the VPN.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "service-route"},
    )
    route_v4: Optional[List[Routev4]] = Field(
        default=None,
        description="A list of IPv4 route configurations within the VPN instance.",
        json_schema_extra={
            "data_path": ["ip"],
            "vmanage_key": "route",
            "priority_order": ["prefix", "next-hop", "next-hop-with-track"],
        },
    )
    route_v6: Optional[List[Routev6]] = Field(
        default=None,
        description="A list of IPv6 route configurations within the VPN instance.",
        json_schema_extra={"data_path": ["ipv6"], "vmanage_key": "route"},
    )
    gre_route: Optional[List[GreRoute]] = Field(
        default=None,
        description="A list of GRE tunnel route configurations within the VPN instance.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "gre-route"},
    )
    ipsec_route: Optional[List[IpsecRoute]] = Field(
        default=None,
        description="A list of IPSec route configurations within the VPN instance.",
        json_schema_extra={"data_path": ["ip"], "vmanage_key": "ipsec-route"},
    )
    advertise: Optional[List[Advertise]] = Field(
        default=None,
        description="A list of configurations for advertising routes via OMP within the VPN instance.",
        json_schema_extra={"data_path": ["omp"]},
    )
    ipv6_advertise: Optional[List[Ipv6Advertise]] = Field(
        default=None,
        description="A list of configurations for advertising IPv6 routes via OMP within the VPN instance.",
        json_schema_extra={"data_path": ["omp"], "vmanage_key": "ipv6-advertise"},
    )
    pool: Optional[List[Pool]] = Field(
        default=None,
        description="A list of NAT64 pool configurations within the VPN instance.",
        json_schema_extra={"data_path": ["nat64", "v4"]},
    )
    natpool: Optional[List[Natpool]] = Field(
        default=None,
        description="A list of NAT pool configurations within the VPN instance.",
        json_schema_extra={"data_path": ["nat"]},
    )
    static: Optional[List[Static]] = Field(
        default=None,
        description="A list of static configurations within the VPN instance for NAT.",
        json_schema_extra={"data_path": ["nat"]},
    )
    subnet_static: Optional[List[SubnetStatic]] = Field(
        default=None,
        description="A list of subnet-specific static configurations within the VPN instance for NAT.",
        json_schema_extra={"data_path": ["nat"], "vmanage_key": "subnet-static"},
    )
    port_forward: Optional[List[PortForward]] = Field(
        default=None,
        description="A list of port forwarding configurations within the VPN instance.",
        json_schema_extra={"data_path": ["nat"], "vmanage_key": "port-forward"},
    )
    route_import: Optional[List[RouteImport]] = Field(
        default=None,
        description="A list of route import configurations within the VPN instance.",
        json_schema_extra={"vmanage_key": "route-import"},
    )
    route_import_from: Optional[List[RouteImportFrom]] = Field(
        default=None,
        description="A list of configurations specifying routes to import from other sources into the VPN instance.",
        json_schema_extra={"vmanage_key": "route-import-from"},
    )
    route_export: Optional[List[RouteExport]] = Field(
        default=None,
        description="A list of route export configurations within the VPN instance.",
        json_schema_extra={"vmanage_key": "route-export"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_vpn"

    def generate_vpn_id(self, session):
        if self.vpn_id not in [0, 512]:
            payload = {"resourcePoolDataType": "vpn", "tenantId": self.org_name, "tenantVpn": self.vpn_id}
            url = "/dataservice/resourcepool/resource/vpn"
            response = session.put(url=url, json=payload).json()
            self.vpn_id = response["deviceVpn"]
