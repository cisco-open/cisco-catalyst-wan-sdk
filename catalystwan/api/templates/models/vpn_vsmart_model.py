# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

VpnId = Literal["0", "512"]
Role = Literal["primary", "secondary"]


class Dns(FeatureTemplateValidator):
    dns_addr: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "dns-addr"}, description="The IP address of the DNS server."
    )
    role: Role = Field(description="The role of the DNS server, either 'PRIMARY' or 'SECONDARY'.")
    model_config = ConfigDict(populate_by_name=True)


class Host(FeatureTemplateValidator):
    hostname: str = Field(..., description="The hostname of the device.")
    ip: List[str] = Field(..., description="A list of IP addresses associated with the hostname.")


class NextHop(FeatureTemplateValidator):
    address: Optional[str] = Field(default=None, description="The IP address of the next hop for the route.")
    distance: Optional[int] = Field(default=1, description="The administrative distance of the next hop.")


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
    distance: Optional[int] = Field(default=1, description="The administrative distance for the static route.")
    vpn: Optional[int] = Field(default=0, description="The VPN instance identifier associated with the static route.")
    model_config = ConfigDict(populate_by_name=True)


class VpnVsmartModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "vSmart VPN Feature Template configuration."

    vpn_id: VpnId = Field(
        description="The unique identifier for the VPN, only 0 and 512 are allowed on vsmart",
        json_schema_extra={"vmanage_key": "vpn-id"},
    )
    name: Optional[str] = Field(
        default=None, description="The name of the VPN.", json_schema_extra={"vmanage_key": "name"}
    )
    dns: Optional[List[Dns]] = Field(
        default=None,
        description="A list of DNS configurations for the VPN instance.",
    )
    host: Optional[List[Host]] = Field(
        default=None,
        description="Static DNS mapping",
        json_schema_extra={"priority_order": ["hostname", "ip"]},
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

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "vpn-vsmart"
