# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

MetricType = Literal["type1", "type2"]
Protocol = Literal["bgp", "connected", "eigrp", "isis", "lisp", "nat-route", "omp", "static"]
AdType = Literal["on-startup"]
Translate = Literal["always"]
Network = Literal["broadcast", "point-to-point", "non-broadcast", "point-to-multipoint"]
Type = Literal["md5", "sha1"]


class Redistribute(FeatureTemplateValidator):
    protocol: Protocol = Field(description="The routing protocol for redistribution")
    route_policy: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "route-policy"},
        description="The route policy to filter routes for redistribution",
    )
    dia: Optional[BoolStr] = Field(
        default=True, description="Whether to include Direct Internet Access (DIA) routes in redistribution"
    )
    model_config = ConfigDict(populate_by_name=True)


class RouterLsa(FeatureTemplateValidator):
    ad_type: AdType = Field(
        json_schema_extra={"vmanage_key": "ad-type"}, description="Advertisement type for the router LSA"
    )
    time: int = Field(description="Time configuration for the router LSA advertisement")
    model_config = ConfigDict(populate_by_name=True)


class Interface(FeatureTemplateValidator):
    name: str = Field(description="The name of the interface")
    hello_interval: Optional[int] = Field(
        default=10,
        json_schema_extra={"vmanage_key": "hello-interval"},
        description="The interval between HELLO packets in seconds",
    )
    dead_interval: Optional[int] = Field(
        default=40,
        json_schema_extra={"vmanage_key": "dead-interval"},
        description="The interval after which a neighbor is declared down if no HELLO packets are received",
    )
    retransmit_interval: Optional[int] = Field(
        default=5,
        json_schema_extra={"vmanage_key": "retransmit-interval"},
        description="The interval between LSA retransmissions",
    )
    cost: Optional[int] = Field(description="The cost metric for the interface")
    network: Optional[Network] = Field(default="broadcast", description="The network type for the OSPF interface")
    passive_interface: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "passive-interface"},
        description="Whether the interface is passive (not sending OSPF packets)",
    )
    type: Type = Field(
        json_schema_extra={"data_path": ["authentication"]},
        description="The type of authentication for OSPF (MD5 or SHA1)",
    )
    authentication_key: str = Field(
        json_schema_extra={"vmanage_key": "authentication-key", "data_path": ["authentication"]},
        description="The authentication key for OSPF",
    )
    spi: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["authentication", "ipsec"]},
        description="The Security Parameter Index for IPsec authentication",
    )
    model_config = ConfigDict(populate_by_name=True)


class Range(FeatureTemplateValidator):
    address: ipaddress.IPv4Interface = Field(..., description="The IPv4 interface address and subnet")
    cost: Optional[int] = Field(default=None, description="The cost metric for the address range")
    no_advertise: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "no-advertise"},
        description="Whether to advertise this range or not",
    )
    model_config = ConfigDict(populate_by_name=True)


class Area(FeatureTemplateValidator):
    a_num: int = Field(json_schema_extra={"vmanage_key": "a-num"}, description="The area number for OSPF configuration")
    stub: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]},
        description="Configuration for the stub area type with the option to suppress summary LSA",
    )
    nssa: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]},
        description="Configuration for the NSSA area type with the option to suppress summary LSA",
    )
    translate: Optional[Translate] = Field(
        default=None,
        json_schema_extra={"data_path": ["nssa"]},
        description="Control for translating type 7 LSAs to type 5 LSAs in NSSA",
    )
    normal: Optional[BoolStr] = Field(description="Whether the area is a normal OSPF area")
    interface: Optional[List[Interface]] = Field(
        default=None, description="List of OSPF interface configurations for the area"
    )
    range: Optional[List[Range]] = Field(default=None, description="List of address ranges for the area")
    model_config = ConfigDict(populate_by_name=True)


class RedistributeV6(FeatureTemplateValidator):
    protocol: Protocol = Field(description="The IPv6 routing protocol for redistribution")
    route_policy: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "route-policy"},
        description="The route policy to filter IPv6 routes for redistribution",
    )
    model_config = ConfigDict(populate_by_name=True)


class InterfaceV6(FeatureTemplateValidator):
    name: str = Field(description="The name of the IPv6 interface")
    hello_interval: Optional[int] = Field(
        default=10,
        json_schema_extra={"vmanage_key": "hello-interval"},
        description="The interval between HELLO packets in seconds for IPv6",
    )
    dead_interval: Optional[int] = Field(
        default=40,
        json_schema_extra={"vmanage_key": "dead-interval"},
        description="The interval after which a neighbor is declared down if no HELLO packets are received for IPv6",
    )
    retransmit_interval: Optional[int] = Field(
        default=5,
        json_schema_extra={"vmanage_key": "retransmit-interval"},
        description="The interval between LSA retransmissions for IPv6",
    )
    cost: Optional[int] = Field(description="The cost metric for the IPv6 interface")
    network: Optional[Network] = Field(default="broadcast", description="The network type for the OSPFv3 interface")
    passive_interface: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "passive-interface"},
        description="Whether the IPv6 interface is passive (not sending OSPF packets)",
    )
    type: Type = Field(
        json_schema_extra={"data_path": ["authentication"]},
        description="The type of authentication for OSPFv3 (MD5 or SHA1)",
    )
    authentication_key: str = Field(
        json_schema_extra={"vmanage_key": "authentication-key", "data_path": ["authentication"]},
        description="The authentication key for OSPFv3",
    )
    spi: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["authentication", "ipsec"]},
    )
    model_config = ConfigDict(populate_by_name=True)


class RangeV6(FeatureTemplateValidator):
    address: ipaddress.IPv6Interface = Field(..., description="The IPv6 interface address and subnet")
    cost: Optional[int] = Field(default=None, description="The cost metric for the IPv6 address range")
    no_advertise: Optional[bool] = Field(
        default=False,
        json_schema_extra={"vmanage_key": "no-advertise"},
        description="Whether to advertise this IPv6 range or not",
    )
    model_config = ConfigDict(populate_by_name=True)


class AreaV6(FeatureTemplateValidator):
    a_num: int = Field(
        json_schema_extra={"vmanage_key": "a-num"}, description="The IPv6 area number for OSPFv3 configuration"
    )
    stub: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]},
        description="Configuration for the IPv6 stub area type with the option to suppress summary LSA",
    )
    nssa: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]},
        description="Configuration for the IPv6 NSSA area type with the option to suppress summary LSA",
    )
    translate: Optional[Translate] = Field(
        default=None,
        json_schema_extra={"data_path": ["nssa"]},
        description="Control for translating type 7 LSAs to type 5 LSAs in NSSA for IPv6",
    )
    normal: Optional[BoolStr] = Field(description="Whether the IPv6 area is a normal OSPFv3 area")
    interface: Optional[List[InterfaceV6]] = Field(
        default=None, description="List of OSPFv3 interface configurations for the IPv6 area"
    )
    range: Optional[List[RangeV6]] = Field(default=None, description="List of IPv6 address ranges for the OSPFv3 area")
    model_config = ConfigDict(populate_by_name=True)


class CiscoOspfv3Model(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco OSPFv3  (Open Shortest Path First v3) configuration"

    router_id_v4: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospfv3", "address-family", "ipv4"]},
        description="IPv4 address to be used as the router ID for the OSPFv3 process",
    )
    reference_bandwidth_v4: Optional[int] = Field(
        100,
        json_schema_extra={
            "vmanage_key": "reference-bandwidth",
            "data_path": ["ospfv3", "address-family", "ipv4", "auto-cost"],
        },
        description="Reference bandwidth in Mbps for calculating the OSPFv3 cost on IPv4 interfaces",
    )
    rfc1583_v4: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "rfc1583", "data_path": ["ospfv3", "address-family", "ipv4", "compatible"]},
        description="Compatibility flag for RFC 1583 to influence OSPFv3 route selection and preferences on IPv4",
    )
    originate_v4: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "originate",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information"],
        },
        description="Flag to control the origination of default information/routes into the OSPFv3 domain for IPv4",
    )
    always_v4: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "always",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information", "originate"],
        },
        description=(
            "Flag indicating if the default route should always be advertised in OSPFv3 for IPv4, "
            "irrespective of its presence in the routing table"
        ),
    )
    metric_v4: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information", "originate"],
        },
        description="The OSPFv3 metric value to use for the default route advertisement in IPv4",
    )
    metric_type_v4: Optional[MetricType] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric-type",
            "data_path": ["ospfv3", "address-family", "ipv4", "default-information", "originate"],
        },
        description="The OSPFv3 metric type (E1 or E2) for the default route advertisement in IPv4",
    )
    external_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "external",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
        },
        description="Administrative distance for OSPFv3 external routes in IPv4",
    )
    inter_area_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "inter-area",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4", "ospf"],
        },
        description="Administrative distance for OSPFv3 inter-area routes in IPv4",
    )
    delay_v4: Optional[int] = Field(
        200,
        json_schema_extra={
            "vmanage_key": "delay",
            "data_path": ["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
        },
        description=(
            "Initial delay time in milliseconds before the OSPFv3 SPF algorithm starts "
            "after a topology change for IPv4"
        ),
    )
    initial_hold_v4: Optional[int] = Field(
        1000,
        json_schema_extra={
            "vmanage_key": "initial-hold",
            "data_path": ["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
        },
        description=(
            "Initial hold time in milliseconds for the OSPFv3 SPF algorithm to wait "
            "between two successive SPF calculations for IPv4"
        ),
    )
    max_hold_v4: Optional[int] = Field(
        10000,
        json_schema_extra={
            "vmanage_key": "max-hold",
            "data_path": ["ospfv3", "address-family", "ipv4", "timers", "throttle", "spf"],
        },
        description=(
            "Maximum hold time in milliseconds for the OSPFv3 SPF algorithm to wait "
            "between two successive SPF calculations for IPv4"
        ),
    )
    distance_v4: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "distance",
            "data_path": ["ospfv3", "address-family", "ipv4", "distance-ipv4"],
        },
        description="Administrative distance for OSPFv3 routes in IPv4",
    )
    name_v4: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "name", "data_path": ["ospfv3", "address-family", "ipv4", "table-map"]},
        description="Name of the route map used for OSPFv3 IPv4 route redistribution",
    )
    filter_v4: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "filter", "data_path": ["ospfv3", "address-family", "ipv4", "table-map"]},
        description="Flag indicating whether filtering is applied to OSPFv3 IPv4 routes using the specified route map",
    )
    redistribute_v4: Optional[List[Redistribute]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospfv3", "address-family", "ipv4"]},
        description="List of redistribution configurations for OSPFv3 IPv4 address family",
    )
    router_lsa_v4: Optional[List[RouterLsa]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "router-lsa",
            "data_path": ["ospfv3", "address-family", "ipv4", "max-metric"],
        },
        description=(
            "List of configurations to set the maximum metric for router LSAs in the OSPFv3 IPv4 address family"
        ),
    )
    area_v4: Optional[List[Area]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "area", "data_path": ["ospfv3", "address-family", "ipv4"]},
        description="List of OSPFv3 area configurations for the IPv4 address family",
    )
    router_id_v6: Optional[ipaddress.IPv4Address] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospfv3", "address-family", "ipv6"]},
        description="IPv4 address to be used as the router ID for the OSPFv3 process for IPv6",
    )
    reference_bandwidth_v6: Optional[int] = Field(
        100,
        json_schema_extra={
            "vmanage_key": "reference-bandwidth",
            "data_path": ["ospfv3", "address-family", "ipv6", "auto-cost"],
        },
        description="Reference bandwidth in Mbps for calculating the OSPFv3 cost on IPv6 interfaces",
    )
    rfc1583_v6: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "rfc1583", "data_path": ["ospfv3", "address-family", "ipv6", "compatible"]},
        description="Compatibility flag for RFC 1583 to influence OSPFv3 route selection and preferences on IPv6",
    )
    originate_v6: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "originate",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information"],
        },
        description="Flag to control the origination of default information/routes into the OSPFv3 domain for IPv6",
    )
    always_v6: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "always",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information", "originate"],
        },
        description=(
            "Flag indicating if the default route should always be advertised in OSPFv3 for IPv6, "
            "irrespective of its presence in the routing table"
        ),
    )
    metric_v6: Optional[int] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information", "originate"],
        },
        description="The OSPFv3 metric value to use for the default route advertisement in IPv6",
    )
    metric_type_v6: Optional[MetricType] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "metric-type",
            "data_path": ["ospfv3", "address-family", "ipv6", "default-information", "originate"],
        },
        description="The OSPFv3 metric type (E1 or E2) for the default route advertisement in IPv6",
    )
    external_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "external",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
        },
        description="Administrative distance for OSPFv3 external routes in IPv6",
    )
    inter_area_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "inter-area",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
        },
        description="Administrative distance for OSPFv3 inter-area routes in IPv6",
    )
    intra_area_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "intra-area",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6", "ospf"],
        },
        description="Administrative distance for OSPFv3 intra-area routes in IPv6",
    )
    delay_v6: Optional[int] = Field(
        200,
        json_schema_extra={
            "vmanage_key": "delay",
            "data_path": ["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
        },
        description=(
            "Initial delay time in milliseconds before the OSPFv3 SPF algorithm starts "
            "after a topology change for IPv6"
        ),
    )
    initial_hold_v6: Optional[int] = Field(
        1000,
        json_schema_extra={
            "vmanage_key": "initial-hold",
            "data_path": ["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
        },
        description=(
            "Initial hold time in milliseconds for the OSPFv3 SPF algorithm to "
            "wait between two successive SPF calculations for IPv6"
        ),
    )
    max_hold_v6: Optional[int] = Field(
        10000,
        json_schema_extra={
            "vmanage_key": "max-hold",
            "data_path": ["ospfv3", "address-family", "ipv6", "timers", "throttle", "spf"],
        },
        description=(
            "Maximum hold time in milliseconds for the OSPFv3 SPF algorithm "
            "to wait between two successive SPF calculations for IPv6"
        ),
    )
    distance_v6: Optional[int] = Field(
        110,
        json_schema_extra={
            "vmanage_key": "distance",
            "data_path": ["ospfv3", "address-family", "ipv6", "distance-ipv6"],
        },
        description="Administrative distance for OSPFv3 routes in IPv6",
    )
    name_v6: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "name", "data_path": ["ospfv3", "address-family", "ipv6", "table-map"]},
        description="Name of the route map used for OSPFv3 IPv6 route redistribution",
    )
    filter_v6: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "filter", "data_path": ["ospfv3", "address-family", "ipv6", "table-map"]},
        description="Flag indicating whether filtering is applied to OSPFv3 IPv6 routes using the specified route map",
    )
    redistribute_v6: Optional[List[RedistributeV6]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospfv3", "address-family", "ipv6"]},
        description="List of redistribution configurations for OSPFv3 IPv6 address family",
    )
    router_lsa_v6: Optional[List[RouterLsa]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "router-lsa",
            "data_path": ["ospfv3", "address-family", "ipv6", "max-metric"],
        },
        description=(
            "List of configurations to set the maximum metric for router LSAs in the OSPFv3 IPv6 address family"
        ),
    )
    area_v6: Optional[List[AreaV6]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "area", "data_path": ["ospfv3", "address-family", "ipv6"]},
        description="List of OSPFv3 area configurations for the IPv6 address family",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospfv3"
