# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import (
    Default,
    Global,
    Variable,
    _ParcelBase,
    as_default,
    as_global,
    as_variable,
)

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

    @classmethod
    def from_uuid(cls, uuid: UUID) -> ReferenceId:
        return cls(ref_id=uuid)


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

    @classmethod
    def create(cls, standard_community_list: List[UUID], criteria: Criteria = "OR") -> StandardCommunityList:
        return cls(
            standard_community_list=[ReferenceId.from_uuid(i) for i in standard_community_list],
            criteria=as_global(criteria, Criteria),
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

    @classmethod
    def create(cls, expanded_community_list: UUID) -> ExpandedCommunityList:
        return cls(expanded_community_list=ReferenceId.from_uuid(expanded_community_list))


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

    def set_as_path_list(self, as_path_list: UUID) -> None:
        self.as_path_list = ReferenceId.from_uuid(as_path_list)

    def set_community_list(
        self,
        expanded_community_list: Optional[UUID] = None,
        standard_community_list: Optional[List[UUID]] = None,
        criteria: Criteria = "OR",
    ) -> None:
        if expanded_community_list and standard_community_list:
            raise ValueError("Only one community list should be set")

        if expanded_community_list:
            self.community_list = ExpandedCommunityList.create(expanded_community_list)

        if standard_community_list:
            self.community_list = StandardCommunityList.create(standard_community_list, criteria)

    def set_ext_community_list(self, ext_community_list: UUID) -> None:
        self.ext_community_list = ReferenceId.from_uuid(ext_community_list)

    def set_bgp_local_preference(self, bgp_local_preference: int) -> None:
        self.bgp_local_preference = as_global(bgp_local_preference)

    def set_metric(self, metric: int) -> None:
        self.metric = as_global(metric)

    def set_omp_tag(self, omp_tag: int) -> None:
        self.omp_tag = as_global(omp_tag)

    def set_ospf_tag(self, ospf_tag: int) -> None:
        self.ospf_tag = as_global(ospf_tag)

    def set_ipv4_address(self, ipv4_address: UUID) -> None:
        self.ipv4_address = ReferenceId.from_uuid(ipv4_address)

    def set_ipv4_next_hop(self, ipv4_next_hop: UUID) -> None:
        self.ipv4_next_hop = ReferenceId.from_uuid(ipv4_next_hop)

    def set_ipv6_address(self, ipv6_address: UUID) -> None:
        self.ipv6_address = ReferenceId.from_uuid(ipv6_address)

    def set_ipv6_next_hop(self, ipv6_next_hop: UUID) -> None:
        self.ipv6_next_hop = ReferenceId.from_uuid(ipv6_next_hop)


class SetAsPath(BaseModel):
    """
    Set AS Path
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    prepend: Optional[List[Global[int]]] = None

    @classmethod
    def from_list(cls, prepend: List[int]) -> SetAsPath:
        return cls(prepend=[as_global(i) for i in prepend])


class SetCommunity(BaseModel):
    """
    Set Community
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    additive: Union[Global[bool], Default[bool]] = as_default(False)
    community: Optional[Union[Global[str], Global[Community], Variable]] = None

    def set_community_as_variable(self, variable_name: str) -> None:
        self.community = as_variable(value=variable_name)

    def set_community_as_global(self, community: str) -> None:
        self.community = as_global(community)


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
    as_path: Optional[SetAsPath] = Field(
        default=None, serialization_alias="setAsPath", validation_alias="setAsPath", description="Set AS Path"
    )
    community: Optional[SetCommunity] = Field(
        default=None, serialization_alias="setCommunity", validation_alias="setCommunity", description="Set Community"
    )
    local_preference: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="setLocalPreference",
        validation_alias="setLocalPreference",
        description="Set Local Preference",
    )
    metric: Optional[Global[int]] = Field(
        default=None, serialization_alias="setMetric", validation_alias="setMetric", description="Set Metric"
    )
    metric_type: Optional[Global[MetricType]] = Field(
        default=None,
        serialization_alias="setMetricType",
        validation_alias="setMetricType",
        description="Set Metric Type",
    )
    omp_tag: Optional[Global[int]] = Field(
        default=None, serialization_alias="setOmpTag", validation_alias="setOmpTag", description="Set OMP Tag"
    )
    origin: Optional[Global[Origin]] = Field(
        default=None, serialization_alias="setOrigin", validation_alias="setOrigin", description="Set Origin"
    )
    ospf_tag: Optional[Global[int]] = Field(
        default=None, serialization_alias="setOspfTag", validation_alias="setOspfTag", description="Set OSPF Tag"
    )
    weight: Optional[Global[int]] = Field(
        default=None, serialization_alias="setWeight", validation_alias="setWeight", description="Set Weight"
    )
    ipv4_next_hop: Optional[Global[IPv4Address]] = Field(
        default=None,
        serialization_alias="setIpv4NextHop",
        validation_alias="setIpv4NextHop",
        description="Set Ipv4 Next Hop",
    )
    ipv6_next_hop: Optional[Global[IPv6Address]] = Field(
        default=None,
        serialization_alias="setIpv6NextHop",
        validation_alias="setIpv6NextHop",
        description="Set Ipv6 Next Hop",
    )

    def set_as_path(self, prepend: List[int]) -> None:
        self.as_path = SetAsPath.from_list(prepend)

    def set_community_as_global(self, additive: bool, community: str) -> None:
        set_community = SetCommunity(additive=as_global(additive))
        set_community.set_community_as_global(community)
        self.community = set_community

    def set_community_as_variable(self, additive: bool, community: str) -> None:
        set_community = SetCommunity(additive=as_global(additive))
        set_community.set_community_as_variable(community)
        self.community = set_community

    def set_local_preference(self, preference: int) -> None:
        self.local_preference = as_global(preference)

    def set_metric(self, set_metric: int) -> None:
        self.metric = as_global(set_metric)

    def set_metric_type(self, set_metric_type: MetricType) -> None:
        self.metric_type = as_global(set_metric_type, MetricType)

    def set_omp_tag(self, set_omp_tag: int) -> None:
        self.omp_tag = as_global(set_omp_tag)

    def set_origin(self, set_origin: Origin) -> None:
        self.origin = as_global(set_origin, Origin)

    def set_ospf_tag(self, set_ospf_tag: int) -> None:
        self.ospf_tag = as_global(set_ospf_tag)

    def set_weight(self, set_weight: int) -> None:
        self.weight = as_global(set_weight)

    def set_ipv4_next_hop(self, set_ipv4_next_hop: IPv4Address) -> None:
        self.ipv4_next_hop = set_ipv4_next_hop

    def set_ipv6_next_hop(self, set_ipv6_next_hop: Optional[IPv6Address]) -> None:
        self.ipv6_next_hop = set_ipv6_next_hop


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
        default=as_default("reject", BaseAction),
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

    def set_protocol(self, protocol: Protocol):
        self.protocol = Global[Protocol](value=protocol)

    def add_accept_action(self, accept: Accept) -> None:
        self.actions = [AcceptActions(accept=accept)]

    def add_match_entry(self, match_entry: MatchEntry) -> None:
        self.match_entries = [match_entry]

    @classmethod
    def create(
        cls,
        sequence_id: int,
        sequence_name: str,
        base_action: BaseAction = "reject",
        protocol: Protocol = "IPV4",
        match_entries: Optional[List[MatchEntry]] = None,
        actions: Optional[List[Union[AcceptActions, RejectActions]]] = None,
    ) -> RoutePolicySequence:
        return cls(
            sequence_id=as_global(sequence_id),
            sequence_name=as_global(sequence_name),
            base_action=as_global(base_action, BaseAction),
            protocol=as_global(protocol, Protocol),
            match_entries=match_entries,
            actions=actions,
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

    def set_default_action(self, default_action: DefaultAction):
        self.default_action = Global[DefaultAction](value=default_action)

    def add_sequence(self, sequence: RoutePolicySequence) -> None:
        self.sequences.append(sequence)
