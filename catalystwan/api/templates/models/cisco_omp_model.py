# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

DEFAULT_OMP_HOLDTIME = 60
DEFAULT_OMP_EOR_TIMER = 300
DEFAULT_OMP_GRACEFUL_RESTART_TIMER = 43200
DEFAULT_OMP_ADVERTISEMENT_INTERVAL = 1
DEFAULT_OMP_SENDPATH_LIMIT = 4
DEFAULT_OMP_ECMP_LIMIT = 4


IPv4AdvertiseProtocol = Literal["bgp", "ospf", "ospfv3", "connected", "static", "eigrp", "lisp", "isis"]
IPv6AdvertiseProtocol = Literal["bgp", "ospf", "connected", "static", "eigrp", "lisp", "isis"]
TransportGateway = Literal["prefer", "ecmp-with-direct-path"]
SiteTypes = Literal["type-1", "type-2", "type-3", "cloud", "branch", "br", "spoke"]
Route = Literal["external"]


class IPv4Advertise(FeatureTemplateValidator):
    protocol: IPv4AdvertiseProtocol = Field(description="The IPv4 routing protocol whose routes are to be advertised.")
    route: Optional[Route] = Field(
        default=None,
        description="The type of IPv4 routes to be advertised. For example, 'external' for external routes.",
    )


class IPv6Advertise(FeatureTemplateValidator):
    protocol: IPv6AdvertiseProtocol = Field(description="The IPv6 routing protocol whose routes are to be advertised.")


class CiscoOMPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Configuration settings for the Cisco Overlay Management Protocol (OMP) feature template."

    graceful_restart: Optional[BoolStr] = Field(
        default=True,
        description="Enable or disable graceful restart for OMP.",
        json_schema_extra={"vmanage_key": "graceful-restart"},
    )
    overlay_as: Optional[int] = Field(
        default=None,
        description="The autonomous system number used for the overlay.",
        json_schema_extra={"vmanage_key": "overlay-as"},
    )
    send_path_limit: Optional[int] = Field(
        default=DEFAULT_OMP_SENDPATH_LIMIT,
        ge=1,
        le=32,
        description="The maximum number of paths that can be sent for each prefix.",
        json_schema_extra={"vmanage_key": "send-path-limit"},
    )
    ecmp_limit: Optional[int] = Field(
        default=DEFAULT_OMP_ECMP_LIMIT,
        description="The maximum number of equal-cost multi-path routes.",
        json_schema_extra={"vmanage_key": "ecmp-limit"},
    )
    shutdown: Optional[BoolStr] = Field(default=None, description="Enable or disable the shutdown of OMP.")
    omp_admin_distance_ipv4: Optional[int] = Field(
        default=None,
        description="The administrative distance for IPv4 routes learned via OMP.",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv4"},
    )
    omp_admin_distance_ipv6: Optional[int] = Field(
        default=None,
        description="The administrative distance for IPv6 routes learned via OMP.",
        json_schema_extra={"vmanage_key": "omp-admin-distance-ipv6"},
    )
    advertisement_interval: Optional[int] = Field(
        default=DEFAULT_OMP_ADVERTISEMENT_INTERVAL,
        description="The interval between sending unsolicited OMP route advertisements.",
        json_schema_extra={"vmanage_key": "advertisement-interval", "data_path": ["timers"]},
    )
    graceful_restart_timer: Optional[int] = Field(
        default=DEFAULT_OMP_GRACEFUL_RESTART_TIMER,
        description="The timer for graceful restart, specifying the period during which peerings are preserved.",
        json_schema_extra={"vmanage_key": "graceful-restart-timer", "data_path": ["timers"]},
    )
    eor_timer: Optional[int] = Field(
        default=DEFAULT_OMP_EOR_TIMER,
        description="End-of-RIB (EOR) timer which indicates stability of the route table.",
        json_schema_extra={"vmanage_key": "eor-timer", "data_path": ["timers"]},
    )
    holdtime: Optional[int] = Field(
        default=DEFAULT_OMP_HOLDTIME,
        description="The amount of time that the routes are preserved while the peer is unreachable.",
        json_schema_extra={"data_path": ["timers"]},
    )
    advertise: Optional[List[IPv4Advertise]] = Field(default=None, description="A list of IPv4 advertise rules.")
    ipv6_advertise: Optional[List[IPv6Advertise]] = Field(
        default=None, description="A list of IPv6 advertise rules.", json_schema_extra={"vmanage_key": "ipv6-advertise"}
    )
    ignore_region_path_length: Optional[BoolStr] = Field(
        default=False,
        description="Whether to ignore the region part of the path length for OMP routes.",
        json_schema_extra={"vmanage_key": "ignore-region-path-length"},
    )
    transport_gateway: Optional[TransportGateway] = Field(
        default=None,
        description="Specifies the preferred transport gateway selection strategy.",
        json_schema_extra={"vmanage_key": "transport-gateway"},
    )
    site_types: Optional[List[SiteTypes]] = Field(
        default=None,
        description="A list of site types that are allowed to participate in the overlay network.",
        json_schema_extra={"vmanage_key": "site-types"},
    )
    auto_translate: Optional[BoolStr] = Field(
        default=False,
        description="Enable or disable automatic translation of network settings.",
        json_schema_extra={"vmanage_key": "auto-translate"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_omp"
