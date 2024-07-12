# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

NeighborFamilyType = Literal["ipv4-unicast", "vpnv4-unicast", "vpnv6-unicast"]
Direction = Literal["in", "out"]
Protocol = Literal["static", "connected", "ospf", "ospfv3", "omp", "eigrp", "nat"]
AddressFamilyType = Literal["ipv4-unicast"]
IPv6NeighborFamilyType = Literal["ipv6-unicast"]


class Export(FeatureTemplateValidator):
    asn_ip: str = Field(
        description="The ASN or IP address to be used as the export route target.",
        json_schema_extra={"vmanage_key": "asn-ip"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Import(FeatureTemplateValidator):
    asn_ip: str = Field(
        description="The ASN or IP address to be used as the import route target.",
        json_schema_extra={"vmanage_key": "asn-ip"},
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv4(FeatureTemplateValidator):
    vpn_id: int = Field(
        description="VPN identifier associated with the IPv4 route target.", json_schema_extra={"vmanage_key": "vpn-id"}
    )
    export: List[Export] = Field(description="List of export route targets.")
    import_: List[Import] = Field(
        description="List of import route targets.", json_schema_extra={"vmanage_key": "import"}
    )
    model_config = ConfigDict(populate_by_name=True)


class RouteTargetIpv6(FeatureTemplateValidator):
    vpn_id: int = Field(
        description="VPN identifier associated with the IPv6 route target.", json_schema_extra={"vmanage_key": "vpn-id"}
    )
    export: List[Export] = Field(description="List of export route targets.")
    import_: List[Import] = Field(
        description="List of import route targets.", json_schema_extra={"vmanage_key": "import"}
    )
    model_config = ConfigDict(populate_by_name=True)


class MplsInterface(FeatureTemplateValidator):
    if_name: Optional[str] = Field(
        default=None, description="Name of the MPLS interface.", json_schema_extra={"vmanage_key": "if-name"}
    )
    model_config = ConfigDict(populate_by_name=True)


class AggregateAddress(FeatureTemplateValidator):
    prefix: str = Field(description="IP prefix to be aggregated.")
    as_set: Optional[BoolStr] = Field(
        default=None,
        description="Include AS_SET information in the aggregate route.",
        json_schema_extra={"vmanage_key": "as-set"},
    )
    summary_only: Optional[BoolStr] = Field(
        default=None,
        description="Advertise only the summary route, not more specific routes.",
        json_schema_extra={"vmanage_key": "summary-only"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6AggregateAddress(FeatureTemplateValidator):
    prefix: str = Field(description="IPv6 prefix to be aggregated.")
    as_set: Optional[bool] = Field(
        default=False,
        description="Include AS_SET information in the aggregate IPv6 route.",
        json_schema_extra={"vmanage_key": "as-set"},
    )
    summary_only: Optional[bool] = Field(
        default=False,
        description="Advertise only the summary IPv6 route, not more specific routes.",
        json_schema_extra={"vmanage_key": "summary-only"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Network(FeatureTemplateValidator):
    prefix: str = Field(description="IP network prefix to be advertised.")


class Ipv6Network(FeatureTemplateValidator):
    prefix: str = Field(description="IPv6 network prefix to be advertised.")


class Redistribute(FeatureTemplateValidator):
    protocol: Protocol = Field(description="Routing protocol from which routes are to be redistributed.")
    route_policy: Optional[str] = Field(
        default=None,
        description="Name of the route policy to be applied during redistribution.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class AddressFamily(FeatureTemplateValidator):
    family_type: AddressFamilyType = Field(
        description="Type of address family for BGP (e.g., IPv4 unicast).",
        json_schema_extra={"vmanage_key": "family-type"},
    )
    aggregate_address: Optional[List[AggregateAddress]] = Field(
        default=None,
        description="List of aggregate address configurations.",
        json_schema_extra={"vmanage_key": "aggregate-address"},
    )
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = Field(
        default=None,
        description="List of IPv6 aggregate address configurations.",
        json_schema_extra={"vmanage_key": "ipv6-aggregate-address"},
    )
    network: Optional[List[Network]] = Field(default=None, description="List of networks to be advertised by BGP.")
    ipv6_network: Optional[List[Ipv6Network]] = Field(
        default=None,
        description="List of IPv6 networks to be advertised by BGP.",
        json_schema_extra={"vmanage_key": "ipv6-network"},
    )
    paths: Optional[int] = Field(
        default=None,
        description="Maximum number of equal-cost paths for load sharing.",
        json_schema_extra={"data_path": ["maximum-paths"]},
    )
    originate: Optional[BoolStr] = Field(
        default=None,
        description="Whether to originate default route.",
        json_schema_extra={"data_path": ["default-information"]},
    )
    policy_name: Optional[str] = Field(
        default=None,
        description="Name of the policy to apply to the address family.",
        json_schema_extra={"data_path": ["table-map"], "vmanage_key": "name"},
    )
    filter: Optional[BoolStr] = Field(
        default=None,
        description="Whether to filter routes according to the policy.",
        json_schema_extra={"data_path": ["table-map"]},
    )
    redistribute: Optional[List[Redistribute]] = Field(
        default=None, description="List of routing protocols and their respective redistribution configurations."
    )
    model_config = ConfigDict(populate_by_name=True)


class RoutePolicy(FeatureTemplateValidator):
    direction: Direction = Field(
        description="Direction in which the route policy is to be applied (inbound or outbound)."
    )
    pol_name: str = Field(description="Name of the route policy.", json_schema_extra={"vmanage_key": "pol-name"})
    model_config = ConfigDict(populate_by_name=True)


class NeighborAddressFamily(FeatureTemplateValidator):
    """Configuration for a BGP neighbor's address family settings."""

    family_type: NeighborFamilyType = Field(
        description="The address family type associated with this neighbor (e.g., ipv4-unicast, vpnv4-unicast).",
        json_schema_extra={"vmanage_key": "family-type"},
    )
    prefix_num: Optional[int] = Field(
        default=None,
        description="The maximum number of prefixes that can be received from a neighbor before taking action.",
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "prefix-num"},
    )
    threshold: Optional[int] = Field(
        default=None,
        description=(
            "The threshold percentage of maximum prefixes "
            "after which a warning is issued or further action is taken."
        ),
        json_schema_extra={"data_path": ["maximum-prefixes"]},
    )
    restart: Optional[int] = Field(
        default=None,
        description=(
            "The time in minutes to wait before re-establishing BGP peering"
            "after a maximum prefix limit has been exceeded."
        ),
        json_schema_extra={"data_path": ["maximum-prefixes"]},
    )
    warning_only: Optional[bool] = Field(
        default=None,
        description=(
            "Indicates whether only a warning message should be issued when the maximum prefix limit is exceeded,"
            " without dropping the BGP session."
        ),
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "warning-only"},
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None,
        description="A list of route policies applied to incoming or outgoing routes for this address family.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Neighbor(FeatureTemplateValidator):
    address: str = Field(description="IP address of the BGP neighbor.")
    description: Optional[str] = Field(default=None, description="A textual description of the BGP neighbor.")
    shutdown: Optional[BoolStr] = Field(
        default=None, description="Indicates whether the BGP neighbor is administratively shut down."
    )
    remote_as: int = Field(
        description="The Autonomous System (AS) number of the BGP neighbor.",
        json_schema_extra={"vmanage_key": "remote-as"},
    )
    keepalive: Optional[int] = Field(
        default=None,
        description="Keepalive interval for the BGP neighbor in seconds.",
        json_schema_extra={"data_path": ["timers"]},
    )
    holdtime: Optional[int] = Field(
        default=None,
        description="Hold time interval for the BGP neighbor in seconds.",
        json_schema_extra={"data_path": ["timers"]},
    )
    if_name: Optional[str] = Field(
        default=None,
        description="Interface name to use as the source address for BGP packets.",
        json_schema_extra={"data_path": ["update-source"], "vmanage_key": "if-name"},
    )
    next_hop_self: Optional[BoolStr] = Field(
        default=None,
        description="Whether the BGP neighbor should use its own address as the next hop.",
        json_schema_extra={"vmanage_key": "next-hop-self"},
    )
    send_community: Optional[BoolStr] = Field(
        default=None,
        description="Whether to send standard community attributes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-community"},
    )
    send_ext_community: Optional[BoolStr] = Field(
        default=None,
        description="Whether to send extended community attributes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-ext-community"},
    )
    ebgp_multihop: Optional[int] = Field(
        default=None,
        description="The maximum number of hops allowed for eBGP sessions with this neighbor.",
        json_schema_extra={"vmanage_key": "ebgp-multihop"},
    )
    password: Optional[str] = Field(default=None, description="Password for BGP authentication with the neighbor.")
    send_label: Optional[BoolStr] = Field(
        default=None,
        description="Whether to send MPLS labels for routes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-label"},
    )
    send_label_explicit: Optional[BoolStr] = Field(
        default=None,
        description="Whether to send MPLS labels explicitly for routes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-label-explicit"},
    )
    as_override: Optional[BoolStr] = Field(
        default=None,
        description="Whether to override the AS number in the AS_PATH for routes to this neighbor.",
        json_schema_extra={"vmanage_key": "as-override"},
    )
    as_number: Optional[int] = Field(
        default=None,
        description="The number of occurrences of the local AS number allowed in the AS_PATH before it is ignored.",
        json_schema_extra={"data_path": ["allowas-in"], "vmanage_key": "as-number"},
    )
    address_family: Optional[List[NeighborAddressFamily]] = Field(
        default=None,
        description="List of address family configurations for the BGP neighbor.",
        json_schema_extra={"vmanage_key": "address-family"},
    )
    model_config = ConfigDict(populate_by_name=True)


class IPv6NeighborAddressFamily(FeatureTemplateValidator):
    family_type: IPv6NeighborFamilyType = Field(
        description="The IPv6 address family type associated with this neighbor (e.g., ipv6-unicast).",
        json_schema_extra={"vmanage_key": "family-type"},
    )
    prefix_num: Optional[int] = Field(
        default=0,
        description=("The maximum number of IPv6 prefixes that can be received from a neighbor before taking action."),
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "prefix-num"},
    )
    threshold: Optional[int] = Field(
        default=None,
        description=(
            "The threshold percentage of maximum IPv6 prefixes"
            " after which a warning is issued or further action is taken."
        ),
        json_schema_extra={"data_path": ["maximum-prefixes"]},
    )
    restart: Optional[int] = Field(
        default=None,
        description=(
            "The time in minutes to wait before re-establishing BGP peering "
            "after an IPv6 maximum prefix limit has been exceeded."
        ),
        json_schema_extra={"data_path": ["maximum-prefixes"]},
    )
    warning_only: Optional[bool] = Field(
        default=False,
        description=(
            "Indicates whether only a warning message should be issued "
            "when the IPv6 maximum prefix limit is exceeded, without dropping the BGP session."
        ),
        json_schema_extra={"data_path": ["maximum-prefixes"], "vmanage_key": "warning-only"},
    )
    route_policy: Optional[List[RoutePolicy]] = Field(
        default=None,
        description="A list of route policies applied to incoming or outgoing routes for this IPv6 address family.",
        json_schema_extra={"vmanage_key": "route-policy"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Neighbor(FeatureTemplateValidator):
    address: str = Field(description="IPv6 address of the BGP neighbor.")
    description: Optional[str] = Field(default=None, description="A textual description of the BGP neighbor.")
    shutdown: Optional[BoolStr] = Field(
        default=None, description="Indicates whether the BGP neighbor is administratively shut down."
    )
    remote_as: Optional[int] = Field(
        default=None,
        description="The Autonomous System (AS) number of the BGP neighbor.",
        json_schema_extra={"vmanage_key": "remote-as"},
    )
    keepalive: Optional[int] = Field(
        default=None,
        description="Keepalive interval for the BGP neighbor in seconds.",
        json_schema_extra={"data_path": ["timers"]},
    )
    holdtime: Optional[int] = Field(
        default=None,
        description="Hold time interval for the BGP neighbor in seconds.",
        json_schema_extra={"data_path": ["timers"]},
    )
    if_name: Optional[str] = Field(
        default=None,
        description="Interface name to use as the source address for BGP packets.",
        json_schema_extra={"data_path": ["update-source"], "vmanage_key": "if-name"},
    )
    next_hop_self: Optional[BoolStr] = Field(
        default=False,
        description="Whether the BGP neighbor should use its own address as the next hop.",
        json_schema_extra={"vmanage_key": "next-hop-self"},
    )
    send_community: Optional[BoolStr] = Field(
        default=True,
        description="Whether to send standard community attributes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-community"},
    )
    send_ext_community: Optional[BoolStr] = Field(
        default=True,
        description="Whether to send extended community attributes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-ext-community"},
    )
    ebgp_multihop: Optional[int] = Field(
        default=1,
        description="The maximum number of hops allowed for eBGP sessions with this neighbor.",
        json_schema_extra={"vmanage_key": "ebgp-multihop"},
    )
    password: Optional[str] = Field(default=None, description="Password for BGP authentication with the neighbor.")
    send_label: Optional[BoolStr] = Field(
        default=False,
        description="Whether to send MPLS labels for routes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-label"},
    )
    send_label_explicit: Optional[BoolStr] = Field(
        default=False,
        description="Whether to send MPLS labels explicitly for routes to this neighbor.",
        json_schema_extra={"vmanage_key": "send-label-explicit"},
    )
    as_override: Optional[BoolStr] = Field(
        default=False,
        description="Whether to override the AS number in the AS_PATH for routes to this neighbor.",
        json_schema_extra={"vmanage_key": "as-override"},
    )
    as_number: Optional[int] = Field(
        default=None,
        description="The number of occurrences of the local AS number allowed in the AS_PATH before it is ignored.",
        json_schema_extra={"data_path": ["allowas-in"], "vmanage_key": "as-number"},
    )
    address_family: Optional[List[IPv6NeighborAddressFamily]] = Field(
        default=None,
        description="List of IPv6 address family configurations for the BGP neighbor.",
        json_schema_extra={"vmanage_key": "address-family"},
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoBGPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco Border Gateway Protocol (BGP) configuration"

    as_num: Optional[str] = Field(
        default=None,
        description="Autonomous System number for the BGP process.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "as-num"},
    )
    shutdown: Optional[BoolStr] = Field(
        default=None,
        description="Indicates whether the BGP process is administratively shut down.",
        json_schema_extra={"data_path": ["bgp"]},
    )
    router_id: Optional[str] = Field(
        default=None,
        description="Router identifier for the BGP process.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "router-id"},
    )
    propagate_aspath: Optional[bool] = Field(
        default=None,
        description="Option to enable or disable AS path propagation.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "propagate-aspath"},
    )
    propagate_community: Optional[bool] = Field(
        default=None,
        description="Option to enable or disable community attribute propagation.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "propagate-community"},
    )
    route_target_ipv4: List[RouteTargetIpv4] = Field(
        default=[],
        description="List of IPv4 route targets for BGP VPNs.",
        json_schema_extra={"data_path": ["bgp", "target"], "vmanage_key": "route-target-ipv4"},
    )
    route_target_ipv6: List[RouteTargetIpv6] = Field(
        default=[],
        description="List of IPv6 route targets for BGP VPNs.",
        json_schema_extra={"data_path": ["bgp", "target"], "vmanage_key": "route-target-ipv6"},
    )
    mpls_interface: Optional[List[MplsInterface]] = Field(
        default=None,
        description="List of MPLS interfaces associated with the BGP process.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "mpls-interface"},
    )
    external: Optional[int] = Field(
        default=None,
        description="Administrative distance for external BGP routes.",
        json_schema_extra={"data_path": ["bgp", "distance"]},
    )
    internal: Optional[int] = Field(
        default=None,
        description="Administrative distance for internal BGP routes.",
        json_schema_extra={"data_path": ["bgp", "distance"]},
    )
    local: Optional[int] = Field(
        default=None,
        description="Administrative distance for local BGP routes.",
        json_schema_extra={"data_path": ["bgp", "distance"]},
    )
    keepalive: Optional[int] = Field(
        default=None,
        description="Keepalive interval for BGP sessions in seconds.",
        json_schema_extra={"data_path": ["bgp", "timers"]},
    )
    holdtime: Optional[int] = Field(
        default=None,
        description="Hold time interval for BGP sessions in seconds.",
        json_schema_extra={"data_path": ["bgp", "timers"]},
    )
    always_compare: Optional[bool] = Field(
        default=None,
        description="Always compare MED for paths from neighbors in different ASes.",
        json_schema_extra={"data_path": ["bgp", "best-path", "med"], "vmanage_key": "always-compare"},
    )
    deterministic: Optional[BoolStr] = Field(
        default=None,
        description="Deterministic comparison of MED for paths from different neighbors.",
        json_schema_extra={"data_path": ["bgp", "best-path", "med"]},
    )
    missing_as_worst: Optional[BoolStr] = Field(
        default=None,
        description="Treat missing AS as worst path.",
        json_schema_extra={"data_path": ["bgp", "best-path", "med"], "vmanage_key": "missing-as-worst"},
    )
    compare_router_id: Optional[BoolStr] = Field(
        default=None,
        description="Compare router ID for identical EBGP paths.",
        json_schema_extra={"data_path": ["bgp", "best-path"], "vmanage_key": "compare-router-id"},
    )
    multipath_relax: Optional[BoolStr] = Field(
        default=None,
        description="Option to enable or disable relaxation of the BGP multipath selection criteria.",
        json_schema_extra={"data_path": ["bgp", "best-path", "as-path"], "vmanage_key": "multipath-relax"},
    )
    address_family: Optional[List[AddressFamily]] = Field(
        default=None,
        description="List of address family configurations for the BGP process.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "address-family"},
    )
    neighbor: Optional[List[Neighbor]] = Field(
        default=None, description="List of IPv4 BGP neighbor configurations.", json_schema_extra={"data_path": ["bgp"]}
    )
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = Field(
        default=None,
        description="List of IPv6 BGP neighbor configurations.",
        json_schema_extra={"data_path": ["bgp"], "vmanage_key": "ipv6-neighbor"},
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_bgp"
