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
from catalystwan.models.common import AcceptRejectActionType

Community = Literal["internet", "local-AS", "no-advertise", "no-export"]
Criteria = Literal["OR", "AND", "EXACT"]
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
    base_action: Union[Global[AcceptRejectActionType], Default[AcceptRejectActionType]] = Field(
        default=as_default("reject", AcceptRejectActionType),
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

    @property
    def _action(self) -> Union[AcceptActions, RejectActions]:
        if self.actions is None:
            if self.base_action is None:
                self.base_action = Global[AcceptRejectActionType](value="accept")
            if self.base_action.value == "accept":
                self.actions = [(AcceptActions(accept=Accept()))]
            else:
                self.actions = [(RejectActions(reject=as_default(True)))]
        return self.actions[0]

    @property
    def _accept_action(self) -> Accept:
        action = self._action
        assert isinstance(action, AcceptActions), "Sequence action must be set to accept"
        return action.accept

    @property
    def _entry(self) -> MatchEntry:
        if self.match_entries is None:
            self.match_entries = [MatchEntry()]
        return self.match_entries[0]

    def match_as_path_list(self, as_path_list: UUID) -> None:
        self._entry.as_path_list = ReferenceId.from_uuid(as_path_list)

    def match_community_list(
        self,
        expanded_community_list: Optional[UUID] = None,
        standard_community_list: Optional[List[UUID]] = None,
        criteria: Criteria = "OR",
    ) -> None:
        if expanded_community_list and standard_community_list:
            raise ValueError("Only one community list should be set")

        if expanded_community_list:
            self._entry.community_list = ExpandedCommunityList.create(expanded_community_list)

        if standard_community_list:
            self._entry.community_list = StandardCommunityList.create(standard_community_list, criteria)

    def match_ext_community_list(self, ext_community_list: UUID) -> None:
        self._entry.ext_community_list = ReferenceId.from_uuid(ext_community_list)

    def match_bgp_local_preference(self, bgp_local_preference: int) -> None:
        self._entry.bgp_local_preference = as_global(bgp_local_preference)

    def match_metric(self, metric: int) -> None:
        self._entry.metric = as_global(metric)

    def match_omp_tag(self, omp_tag: int) -> None:
        self._entry.omp_tag = as_global(omp_tag)

    def match_ospf_tag(self, ospf_tag: int) -> None:
        self._entry.ospf_tag = as_global(ospf_tag)

    def match_ipv4_address(self, ipv4_address: UUID) -> None:
        self._entry.ipv4_address = ReferenceId.from_uuid(ipv4_address)

    def match_ipv4_next_hop(self, ipv4_next_hop: UUID) -> None:
        self._entry.ipv4_next_hop = ReferenceId.from_uuid(ipv4_next_hop)

    def match_ipv6_address(self, ipv6_address: UUID) -> None:
        self._entry.ipv6_address = ReferenceId.from_uuid(ipv6_address)

    def match_ipv6_next_hop(self, ipv6_next_hop: UUID) -> None:
        self._entry.ipv6_next_hop = ReferenceId.from_uuid(ipv6_next_hop)

    def associate_reject_action(self) -> None:
        self.actions = [(RejectActions(reject=as_default(True)))]

    def associate_as_path_action(self, prepend: List[int]) -> None:
        self._accept_action.as_path = SetAsPath.from_list(prepend)

    def associate_community_action(self, additive: bool, community: str) -> None:
        set_community = SetCommunity(additive=as_global(additive), community=as_global(community))
        self._accept_action.community = set_community

    def associate_community_variable_action(self, additive: bool, community: str) -> None:
        set_community = SetCommunity(additive=as_global(additive), community=as_variable(community))
        self._accept_action.community = set_community

    def associate_local_preference_action(self, preference: int) -> None:
        self._accept_action.local_preference = as_global(preference)

    def associate_metric_action(self, set_metric: int) -> None:
        self._accept_action.metric = as_global(set_metric)

    def associate_metric_type_action(self, set_metric_type: MetricType) -> None:
        self._accept_action.metric_type = as_global(set_metric_type, MetricType)

    def associate_omp_tag_action(self, set_omp_tag: int) -> None:
        self._accept_action.omp_tag = as_global(set_omp_tag)

    def associate_origin_action(self, set_origin: Origin) -> None:
        self._accept_action.origin = as_global(set_origin, Origin)

    def associate_ospf_tag_action(self, set_ospf_tag: int) -> None:
        self._accept_action.ospf_tag = as_global(set_ospf_tag)

    def associate_weight_action(self, set_weight: int) -> None:
        self._accept_action.weight = as_global(set_weight)

    def associate_ipv4_next_hop_action(self, set_ipv4_next_hop: IPv4Address) -> None:
        self._accept_action.ipv4_next_hop = as_global(set_ipv4_next_hop)

    def associate_ipv6_next_hop_action(self, set_ipv6_next_hop: IPv6Address) -> None:
        self._accept_action.ipv6_next_hop = as_global(set_ipv6_next_hop)

    @classmethod
    def create(
        cls,
        sequence_id: int,
        sequence_name: str,
        base_action: AcceptRejectActionType = "reject",
        protocol: Protocol = "IPV4",
        match_entries: Optional[List[MatchEntry]] = None,
        actions: Optional[List[Union[AcceptActions, RejectActions]]] = None,
    ) -> RoutePolicySequence:
        return cls(
            sequence_id=as_global(sequence_id),
            sequence_name=as_global(sequence_name),
            base_action=as_global(base_action, AcceptRejectActionType),
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
    default_action: Union[Global[AcceptRejectActionType], Default[AcceptRejectActionType]] = Field(
        default=as_default("reject", AcceptRejectActionType),
        validation_alias=AliasPath("data", "defaultAction"),
        description="Default Action",
    )
    sequences: List[RoutePolicySequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Route Policy List"
    )

    def set_default_action(self, default_action: AcceptRejectActionType):
        self.default_action = Global[AcceptRejectActionType](value=default_action)

    def add_sequence(
        self, id_: int, name: str, base_action: AcceptRejectActionType, protocol: Protocol
    ) -> RoutePolicySequence:
        sequence = RoutePolicySequence(
            sequence_id=as_global(id_),
            sequence_name=as_global(name),
            base_action=as_global(base_action, AcceptRejectActionType),
            protocol=as_global(protocol, Protocol),
        )
        self.sequences.append(sequence)
        return sequence
