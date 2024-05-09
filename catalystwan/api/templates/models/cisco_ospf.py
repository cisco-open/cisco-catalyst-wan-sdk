# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress
from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

DEFAULT_OSPF_HELLO_INTERVAL = 10
DEFAULT_OSPF_DEAD_INTERVAL = 40
DEFAULT_OSPF_RETRANSMIT_INTERVAL = 5
DEFAULT_OSPF_INTERFACE_PRIORITY = 1
DEFAULT_OSPF_REFERENCE_BANDWIDTH = 100
DEFAULT_OSPF_EXTERNAL = 110
DEFAULT_OSPF_INTER_AREA = 110
DEFAULT_OSPF_INTRA_AREA = 110
DEFAULT_OSPF_DELAY = 200
DEFAULT_OSPF_INITIAL_HOLD = 1000
DEFAULT_OSPF_MAX_HOLD = 10000


Protocol = Literal["static", "connected", "bgp", "omp", "nat", "eigrp"]

AdType = Literal["administrative", "on-startup"]

Direction = Literal["in"]

Network = Literal["broadcast", "point-to-point", "non-broadcast", "point-to-multipoint"]

Type = Literal["simple", "message-digest", "null"]

MetricType = Literal["type1", "type2"]


class Redistribute(FeatureTemplateValidator):
    protocol: Protocol = Field(description="The routing protocol from which routes are to be redistributed into OSPF.")
    route_policy: Optional[str] = Field(
        default=None,
        description="Name of the route policy to control the redistribution.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    dia: Optional[BoolStr] = Field(
        default=True, description="Default information originate, which controls the advertisement of default route."
    )
    model_config = ConfigDict(populate_by_name=True)


class RouterLsa(FeatureTemplateValidator):
    ad_type: AdType = Field(
        description="Type of advertisement for the router LSA.", json_schema_extra={"vmanage_key": "ad-type"}
    )
    time: int = Field(description="Time in seconds for advertisement.")
    model_config = ConfigDict(populate_by_name=True)


class RoutePolicy(FeatureTemplateValidator):
    direction: Direction = Field(description="Direction of the route policy (e.g., 'in' for incoming).")
    pol_name: str = Field(description="Name of the route policy.", json_schema_extra={"vmanage_key": "pol-name"})

    model_config = ConfigDict(populate_by_name=True)


class Interface(FeatureTemplateValidator):
    name: str = Field(description="The name of the OSPF interface.")
    hello_interval: Optional[int] = Field(
        DEFAULT_OSPF_HELLO_INTERVAL,
        description="The interval between the OSPF Hello packets that the router sends on the interface.",
        json_schema_extra={"vmanage_key": "hello-interval"},
    )
    dead_interval: Optional[int] = Field(
        DEFAULT_OSPF_DEAD_INTERVAL,
        description=(
            "The time interval an OSPF router waits for a Hello packet before declaring the sending router down."
        ),
        json_schema_extra={"vmanage_key": "dead-interval"},
    )
    retransmit_interval: Optional[int] = Field(
        DEFAULT_OSPF_RETRANSMIT_INTERVAL,
        description="The interval between LSA retransmissions for adjacencies belonging to the interface.",
        json_schema_extra={"vmanage_key": "retransmit-interval"},
    )
    cost: Optional[int] = Field(default=None, description="The OSPF cost (metric) for this interface.")
    priority: Optional[int] = Field(
        default=DEFAULT_OSPF_INTERFACE_PRIORITY, description="The OSPF priority of the interface."
    )
    network: Optional[Network] = Field(default="broadcast", description="The OSPF network type for the interface.")
    passive_interface: Optional[BoolStr] = Field(
        default=False,
        description="Whether the interface is a passive OSPF interface.",
        json_schema_extra={"vmanage_key": "passive-interface"},
    )
    type: Optional[Type] = Field(
        default=None,
        description="The OSPF authentication type for the interface.",
        json_schema_extra={"data_path": ["authentication"]},
    )
    message_digest_key: Optional[int] = Field(
        default=None,
        description="The message-digest key ID for OSPF authentication.",
        json_schema_extra={"vmanage_key": "message-digest-key", "data_path": ["authentication", "message-digest"]},
    )
    md5: Optional[str] = Field(
        default=None,
        description="The MD5 string for OSPF message-digest authentication.",
        json_schema_extra={"data_path": ["authentication", "message-digest"]},
    )
    model_config = ConfigDict(populate_by_name=True)


class Range(FeatureTemplateValidator):
    address: ipaddress.IPv4Interface = Field(description="The IPv4 network address to be advertised as an OSPF range.")
    cost: Optional[int] = Field(default=None, description="The OSPF cost (metric) for this range.")
    no_advertise: Optional[BoolStr] = Field(
        default=False,
        description="Whether to suppress advertising this range.",
        json_schema_extra={"vmanage_key": "no-advertise"},
    )

    model_config = ConfigDict(populate_by_name=True)


class Area(FeatureTemplateValidator):
    a_num: int = Field(description="The OSPF area number.", json_schema_extra={"vmanage_key": "a-num"})
    stub: Optional[BoolStr] = Field(
        default=None,
        description="Configuration for the OSPF area to be a stub area. If set, no-summary can be applied.",
        json_schema_extra={"vmanage_key": "no-summary", "data_path": ["stub"]},
    )
    nssa: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Configuration for the OSPF area to be a Not-So-Stubby Area (NSSA). If set, no-summary can be applied."
        ),
        json_schema_extra={"vmanage_key": "no-summary", "data_path": ["nssa"]},
    )
    interface: Optional[List[Interface]] = Field(
        default=None, description="A list of OSPF interface configurations associated with this area."
    )
    range: Optional[List[Range]] = Field(
        default=None, description="A list of OSPF range entries to be associated with this area."
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoOSPFModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco OSPF (Open Shortest Path First) configuration"

    router_id: Optional[str] = Field(
        default=None,
        description="The router ID of the OSPF process.",
        json_schema_extra={"vmanage_key": "router-id", "data_path": ["ospf"]},
    )
    reference_bandwidth: Optional[int] = Field(
        DEFAULT_OSPF_REFERENCE_BANDWIDTH,
        description="The reference bandwidth used by OSPF for cost calculation.",
        json_schema_extra={"data_path": ["ospf", "auto-cost"], "vmanage_key": "reference-bandwidth"},
    )
    rfc1583: Optional[BoolStr] = Field(
        default=True,
        description="Compatibility switch for RFC 1583.",
        json_schema_extra={"data_path": ["ospf", "compatible"]},
    )
    originate: Optional[BoolStr] = Field(
        default=None,
        description="Controls the origination of default information into the OSPF domain.",
        json_schema_extra={"data_path": ["ospf", "default-information"]},
    )
    always: Optional[BoolStr] = Field(
        default=None,
        description=(
            "Ensures that the default route is always advertised,"
            " regardless of the existence of a default route in the routing table."
        ),
        json_schema_extra={"data_path": ["ospf", "default-information", "originate"]},
    )
    metric: Optional[int] = Field(
        default=None,
        description="The metric value to be set for the default route advertised by OSPF.",
        json_schema_extra={"data_path": ["ospf", "default-information", "originate"]},
    )
    metric_type: Optional[MetricType] = Field(
        default=None,
        description="The metric type (Type 1 or Type 2) for OSPF external routes.",
        json_schema_extra={"vmanage_key": "metric-type", "data_path": ["ospf", "default-information", "originate"]},
    )
    external: Optional[int] = Field(
        DEFAULT_OSPF_EXTERNAL,
        description="The OSPF external route metric.",
        json_schema_extra={"data_path": ["ospf", "distance"]},
    )
    inter_area: Optional[int] = Field(
        DEFAULT_OSPF_INTER_AREA,
        description="The OSPF inter-area route metric.",
        json_schema_extra={"data_path": ["ospf", "distance"], "vmanage_key": "inter-area"},
    )
    intra_area: Optional[int] = Field(
        DEFAULT_OSPF_INTRA_AREA,
        description="The OSPF intra-area route metric.",
        json_schema_extra={"data_path": ["ospf", "distance"], "vmanage_key": "intra-area"},
    )
    delay: Optional[int] = Field(
        DEFAULT_OSPF_DELAY,
        description="The OSPF Shortest Path First (SPF) delay time.",
        json_schema_extra={"data_path": ["ospf", "timers", "spf"]},
    )
    initial_hold: Optional[int] = Field(
        DEFAULT_OSPF_INITIAL_HOLD,
        description="The initial hold time between consecutive SPF calculations.",
        json_schema_extra={"vmanage_key": "initial-hold", "data_path": ["ospf", "timers", "spf"]},
    )
    max_hold: Optional[int] = Field(
        DEFAULT_OSPF_MAX_HOLD,
        description="The maximum hold time between consecutive SPF calculations.",
        json_schema_extra={"vmanage_key": "max-hold", "data_path": ["ospf", "timers", "spf"]},
    )
    redistribute: Optional[List[Redistribute]] = Field(
        default=None,
        description="A list of OSPF redistribution configurations.",
        json_schema_extra={"vmanage_key": "redistribute", "data_path": ["ospf"]},
    )
    router_lsa: Optional[List[RouterLsa]] = Field(
        default=None,
        description="Configuration options for the Router LSA in OSPF.",
        json_schema_extra={"vmanage_key": "router-lsa", "data_path": ["ospf", "max-metric"]},
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None,
        description="A list of OSPF route policies.",
        json_schema_extra={"vmanage_key": "route-policy", "data_path": ["ospf"]},
    )
    area: Optional[List[Area]] = Field(
        default=None,
        description="A list of OSPF areas and their configurations.",
        json_schema_extra={"vmanage_key": "area", "data_path": ["ospf"]},
    )
    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ospf"
