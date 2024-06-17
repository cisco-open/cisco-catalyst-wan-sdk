# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv6Address
from typing import List, Literal, Union
from uuid import UUID

from pydantic import ConfigDict, Field

from catalystwan.models.common import AcceptRejectActionType, SequenceIpType
from catalystwan.models.policy.policy_definition import (
    ActionSet,
    AddressEntry,
    AdvancedCommunityEntry,
    AdvancedCommunityMatchFlag,
    AggregatorActionEntry,
    AggregatorActionEntryValue,
    AsPathActionEntry,
    AsPathActionEntryValue,
    AsPathListMatchEntry,
    AtomicAggregateActionEntry,
    CommunityAdditiveEntry,
    CommunityEntry,
    DefinitionWithSequencesCommonBase,
    ExpandedCommunityInLineEntry,
    ExpandedCommunityListEntry,
    ExtendedCommunityEntry,
    LocalPreferenceEntry,
    Match,
    MetricEntry,
    MetricType,
    MetricTypeEntry,
    NextHopActionEntry,
    NextHopMatchEntry,
    OMPTagEntry,
    OriginatorEntry,
    OriginEntry,
    OspfTagEntry,
    PeerEntry,
    PolicyAcceptRejectAction,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    WeightEntry,
)


class RoutePolicyRuleSequence(PolicyDefinitionSequenceBase):
    model_config = ConfigDict(populate_by_name=True)
    sequence_type: Literal["vedgeRoute"] = Field(
        default="vedgeRoute", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: AcceptRejectActionType = Field(
        default="reject", serialization_alias="baseAction", validation_alias="baseAction"
    )

    match: Match = Match(entries=[])
    actions: List[ActionSet] = []

    def match_address(self, address_ref: UUID):
        self._insert_match(AddressEntry(ref=address_ref))

    def match_path_list(self, path_list_ref: UUID):
        self._insert_match(AsPathListMatchEntry(ref=path_list_ref))

    def match_bgp_local_preference(self, value: int):
        self._insert_match(LocalPreferenceEntry(value=value))

    def match_metric(self, value: int):
        self._insert_match(MetricEntry(value=value))

    def match_next_hop(self, next_hop_ref: UUID):
        self._insert_match(NextHopMatchEntry(ref=next_hop_ref))

    def match_omp_tag(self, value: int):
        self._insert_match(OMPTagEntry(value=value))

    def match_origin(self, origin: Literal["egp", "igp", "incomplete"]):
        self._insert_match(OriginEntry(value=origin))

    def match_ospf_tag(self, tag: int):
        self._insert_match(OspfTagEntry(value=tag))

    def match_peer(self, address: Union[IPv4Address, IPv6Address]):
        self._insert_match(PeerEntry(value=address))

    def match_community_list(self):
        pass

    def match_standard_community_list(self, match_flag: AdvancedCommunityMatchFlag, community_lists: List[UUID]):
        ace = AdvancedCommunityEntry(
            match_flag=match_flag,
            refs=community_lists,
        )
        self._insert_match(ace)

    def match_expanded_community_list(self, expanded_community_list_ref: UUID):
        self._insert_match(ExpandedCommunityListEntry(ref=expanded_community_list_ref))

    def match_expanded_inline_community_list(self, variable_name: str):
        self._insert_match(ExpandedCommunityInLineEntry(vip_variable_name=variable_name))

    def match_extended_community_list(self, extended_community_ref: UUID):
        self._insert_match(ExtendedCommunityEntry(ref=extended_community_ref))

    def associate_aggregator_action(self, aggregator_value: int, ip_address: Union[IPv4Address, IPv6Address]):
        self._insert_action_in_set(
            AggregatorActionEntry(value=AggregatorActionEntryValue(aggregator=aggregator_value, ip_address=ip_address))
        )

    def associate_as_path_action(self, prepend_action: List[int], exclude_action: List[int]):
        self._insert_action_in_set(
            AsPathActionEntry(value=AsPathActionEntryValue(prepend=prepend_action, exclude=exclude_action))
        )

    def associate_atomic_aggregate_action(self):
        self._insert_action_in_set(AtomicAggregateActionEntry())

    def associate_origin_action(self, origin: Literal["egp", "igp", "incomplete"]):
        self._insert_action_in_set(OriginEntry(value=origin))

    def associate_originator_action(self, originator: IPv4Address):
        self._insert_action_in_set(OriginatorEntry(value=originator))

    def associate_community_by_value_action(self, community_entry: str, community_additive: bool = False):
        self._insert_action_in_set(CommunityEntry(value=community_entry))

        if community_additive:
            self._insert_action_in_set(CommunityAdditiveEntry())

    def associate_community_by_variable_action(self, variable: str, community_additive: bool = False):
        self._insert_action_in_set(CommunityEntry(vip_variable_name=variable))

        if community_additive:
            self._insert_action_in_set(CommunityAdditiveEntry())

    def associate_local_preference_action(self, value: int):
        self._insert_action_in_set(LocalPreferenceEntry(value=value))

    def associate_metric_action(self, value: int):
        self._insert_action_in_set(MetricEntry(value=value))

    def associate_nexthop_action(self, nexthop: Union[IPv4Address, IPv6Address]):
        self._insert_action_in_set(NextHopActionEntry(value=nexthop))

    def associate_metric_type_action(self, metric_type: MetricType):
        self._insert_action_in_set(MetricTypeEntry(value=metric_type))

    def associate_omp_tag_action(self, omp_tag: int):
        self._insert_action_in_set(OMPTagEntry(value=omp_tag))

    def associate_ospf_tag_action(self, ospf_tag: int):
        self._insert_action_in_set(OspfTagEntry(value=ospf_tag))

    def associate_weight_action(self, weight: int):
        self._insert_action_in_set(WeightEntry(value=weight))


class RoutePolicy(PolicyDefinitionBase, DefinitionWithSequencesCommonBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["vedgeRoute"] = "vedgeRoute"
    sequences: List[RoutePolicyRuleSequence] = []
    default_action: PolicyAcceptRejectAction = Field(
        default=PolicyAcceptRejectAction(type="reject"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )

    def add_sequence(
        self, id_: int, name: str, base_action: AcceptRejectActionType, ip_type: SequenceIpType
    ) -> RoutePolicyRuleSequence:
        sequence = RoutePolicyRuleSequence(
            sequence_id=id_,
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type=ip_type,
        )
        self.sequences.append(sequence)
        return sequence


class RoutePolicyEditPayload(RoutePolicy, PolicyDefinitionId):
    pass


class RoutePolicyGetResponse(RoutePolicy, PolicyDefinitionGetResponse):
    pass
