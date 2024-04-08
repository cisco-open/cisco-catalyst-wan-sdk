from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

BaseAction = Literal["reject", "accept"]
Community = Literal["internet", "local-AS", "no-advertise", "no-export"]
Criteria = Literal["OR", "AND", "EXACT"]
DefaultAction = Literal["reject", "accept"]
Protocol = Literal["IPV4", "IPV6", "BOTH"]
MetricType = Literal["type1", "type2"]
Origin = Literal["EGP", "IGP", "Incomplete"]


class ReferenceId(BaseModel):
    """
    Don't repeat yourself. Use RefereneceId for all policies
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ref_id: UUID = Field(..., serialization_alias="refId", validation_alias="refId")


class StandardCommunityList(BaseModel):
    """
    Community List
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    criteria: Union[Global[Criteria], Default[Criteria]] = Field(
        default=as_default("OR", Criteria), description="Select a condition such as OR, AND or EXACT"
    )
    standard_community_list: List[ReferenceId] = Field(
        ...,
        serialization_alias="standardCommunityList",
        validation_alias="standardCommunityList",
        description="Select a standard community list",
        min_length=1,
    )


class ExpandedCommunityList(BaseModel):
    """
    Community List
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    expanded_community_list: ReferenceId = Field(
        ...,
        serialization_alias="expandedCommunityList",
        validation_alias="expandedCommunityList",
        description="Select a expanded community list",
    )


class MatchEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    as_path_list: Optional[ReferenceId] = Field(
        default=None, serialization_alias="asPathList", validation_alias="asPathList", description="As Path List"
    )
    community_list: Optional[Union[StandardCommunityList, ExpandedCommunityList]] = Field(
        default=None,
        serialization_alias="communityList",
        validation_alias="communityList",
        description="Community List",
    )
    ext_community_list: Optional[ReferenceId] = Field(
        default=None,
        serialization_alias="extCommunityList",
        validation_alias="extCommunityList",
        description="Extended Community List",
    )
    bgp_local_preference: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="bgpLocalPreference",
        validation_alias="bgpLocalPreference",
        description="BGP Local Preference",
    )
    metric: Optional[Global[int]] = Field(default=None, description="Select Metric")
    omp_tag: Optional[Global[int]] = Field(
        default=None, serialization_alias="ompTag", validation_alias="ompTag", description="Select OMP Tag"
    )
    ospf_tag: Optional[Global[int]] = Field(
        default=None, serialization_alias="ospfTag", validation_alias="ospfTag", description="Select OSPF Tag"
    )
    ipv4_address: Optional[ReferenceId] = Field(
        default=None, serialization_alias="ipv4Address", validation_alias="ipv4Address", description="Ipv4 Address"
    )
    ipv4_next_hop: Optional[ReferenceId] = Field(
        default=None, serialization_alias="ipv4NextHop", validation_alias="ipv4NextHop", description="Ipv4 Next Hop"
    )
    ipv6_address: Optional[ReferenceId] = Field(
        default=None, serialization_alias="ipv6Address", validation_alias="ipv6Address", description="Ipv6 Address"
    )
    ipv6_next_hop: Optional[ReferenceId] = Field(
        default=None, serialization_alias="ipv6NextHop", validation_alias="ipv6NextHop", description="Ipv6 Next Hop"
    )


class SetAsPath(BaseModel):
    """
    Set AS Path
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    prepend: Optional[List[Global[int]]] = None


class SetCommunity(BaseModel):
    """
    Set Community
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    additive: Union[Global[bool], Default[bool]] = as_default(False)
    community: Optional[Union[Global[str], Global[Community], Variable]] = None


class Accept(BaseModel):
    """
    Accept Action
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    enable_accept_action: Default[bool] = Field(
        default=as_default(True),
        serialization_alias="enableAcceptAction",
        validation_alias="enableAcceptAction",
        description="Enable Accept Action",
    )
    set_as_path: Optional[SetAsPath] = Field(
        default=None, serialization_alias="setAsPath", validation_alias="setAsPath", description="Set AS Path"
    )
    set_community: Optional[SetCommunity] = Field(
        default=None, serialization_alias="setCommunity", validation_alias="setCommunity", description="Set Community"
    )
    set_local_preference: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="setLocalPreference",
        validation_alias="setLocalPreference",
        description="Set Local Preference",
    )
    set_metric: Optional[Global[int]] = Field(
        default=None, serialization_alias="setMetric", validation_alias="setMetric", description="Set Metric"
    )
    set_metric_type: Optional[Global[MetricType]] = Field(
        default=None,
        serialization_alias="setMetricType",
        validation_alias="setMetricType",
        description="Set Metric Type",
    )
    set_omp_tag: Optional[Global[int]] = Field(
        default=None, serialization_alias="setOmpTag", validation_alias="setOmpTag", description="Set OMP Tag"
    )
    set_origin: Optional[Global[Origin]] = Field(
        default=None, serialization_alias="setOrigin", validation_alias="setOrigin", description="Set Origin"
    )
    set_ospf_tag: Optional[Global[int]] = Field(
        default=None, serialization_alias="setOspfTag", validation_alias="setOspfTag", description="Set OSPF Tag"
    )
    set_weight: Optional[Global[int]] = Field(
        default=None, serialization_alias="setWeight", validation_alias="setWeight", description="Set Weight"
    )
    set_ipv4_next_hop: Optional[Global[IPv4Address]] = Field(
        default=None,
        serialization_alias="setIpv4NextHop",
        validation_alias="setIpv4NextHop",
        description="Set Ipv4 Next Hop",
    )
    set_ipv6_next_hop: Optional[Global[IPv6Address]] = Field(
        default=None,
        serialization_alias="setIpv6NextHop",
        validation_alias="setIpv6NextHop",
        description="Set Ipv6 Next Hop",
    )


class AcceptActions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    accept: Accept = Field(..., description="Accept Action")


class RejectActions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    reject: Default[bool] = Field(as_default(True), description="Reject Action")


class RoutePolicySequence(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    sequence_id: Global[int] = Field(
        ..., serialization_alias="sequenceId", validation_alias="sequenceId", description="Sequence Id"
    )
    sequence_name: Global[str] = Field(
        ..., serialization_alias="sequenceName", validation_alias="sequenceName", description="Sequence Name"
    )
    base_action: Union[Global[BaseAction], Default[BaseAction]] = Field(
        default=as_default("Reject", BaseAction),
        serialization_alias="baseAction",
        validation_alias="baseAction",
        description="Base Action",
    )
    protocol: Union[Global[Protocol], Default[Protocol]] = Field(
        default=as_default("IPV4", Protocol), description="protocol such as IPV4, IPV6, or BOTH"
    )
    match_entries: Optional[List[MatchEntry]] = Field(
        default=None,
        serialization_alias="matchEntries",
        validation_alias="matchEntries",
        description="Define match conditions",
        max_length=1,
        min_length=1,
    )
    actions: Optional[List[Union[AcceptActions, RejectActions]]] = Field(
        default=None, description="Define list of actions", max_length=1, min_length=1
    )


class RoutePolicyParcel(_ParcelBase):
    type_: Literal["route-policy"] = Field(default="route-policy", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    default_action: Union[Global[DefaultAction], Default[DefaultAction]] = Field(
        default=as_default("reject", DefaultAction),
        validation_alias=AliasPath("data", "defaultAction"),
        description="Default Action",
    )
    sequences: List[RoutePolicySequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Route Policy List"
    )
