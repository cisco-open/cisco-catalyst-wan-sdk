# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv4Address
from typing import cast
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.policy.definition.route_policy import RoutePolicy, RoutePolicyRuleSequence
from catalystwan.models.policy.policy_definition import AdvancedCommunityEntry, PolicyAcceptRejectAction
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestRoutePolicyConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_route_conversion(self):
        # Arrange
        address_ref = uuid4()
        path_list_ref = uuid4()
        next_hop_ref = uuid4()
        standard_community_list_ref = [uuid4(), uuid4()]
        expanded_community_list_ref = uuid4()
        extended_community_list_ref = uuid4()
        rule_sequence = RoutePolicyRuleSequence(
            sequence_id=1,
            sequence_name="test_sequence",
        )
        rule_sequence.match_address(
            address_ref=address_ref,
        )
        rule_sequence.match_path_list(
            path_list_ref=path_list_ref,
        )
        rule_sequence.match_bgp_local_preference(
            value=100,
        )
        rule_sequence.match_metric(
            value=100,
        )
        rule_sequence.match_next_hop(
            next_hop_ref=next_hop_ref,
        )
        rule_sequence.match_omp_tag(
            value=100,
        )
        rule_sequence.match_origin(
            origin="igp",
        )
        rule_sequence.match_ospf_tag(
            tag=100,
        )
        rule_sequence.match_peer(
            address=IPv4Address("10.2.3.4"),
        )
        rule_sequence.match_community_list()
        rule_sequence.match_standard_community_list(
            community_list_entry=AdvancedCommunityEntry(
                match_flag="and",
                refs=standard_community_list_ref,
            )
        )
        rule_sequence.match_expanded_community_list(
            expanded_community_list_ref=expanded_community_list_ref,
        )
        rule_sequence.match_expanded_inline_community_list(variable_name="expanded_community_list")
        rule_sequence.match_extended_community_list(
            extended_community_ref=extended_community_list_ref,
        )
        rule_sequence.add_aggregator_action(
            aggregator_value=100,
            ip_address=IPv4Address("10.2.3.2"),
        )
        rule_sequence.add_as_path_action(
            prepend_action=[100, 200],
            exclude_action=[300, 400],
        )
        rule_sequence.add_atomic_aggregate_action()
        rule_sequence.add_origin_action(
            origin="igp",
        )
        rule_sequence.add_originator_action(
            originator=IPv4Address("9.9.9.9"),
        )
        rule_sequence.add_community_by_value_action(
            community_additive=True,
            community_entry="test_community",
        )
        rule_sequence.add_community_by_variable_action(
            variable="test_community_variable",
            community_additive=True,
        )
        rule_sequence.add_local_preference_action(
            value=100,
        )
        rule_sequence.add_metric_action(
            value=100,
        )
        rule_sequence.add_nexthop_action(
            nexthop=IPv4Address("8.8.8.7"),
        )
        rule_sequence.add_metric_type_action(
            metric_type="type1",
        )
        rule_sequence.add_omp_tag_action(
            omp_tag=100,
        )
        rule_sequence.add_ospf_tag_action(
            ospf_tag=100,
        )
        rule_sequence.add_weight_action(
            weight=100,
        )
        route_policy = RoutePolicy(
            name="test_route_policy",
            description="description",
            default_action=PolicyAcceptRejectAction(type="accept"),
            sequences=[rule_sequence],
        )
        uuid = uuid4()
        # Act
        parcel = cast(RoutePolicyParcel, convert(route_policy, uuid, context=self.context))
        # Assert
        assert parcel.parcel_name == "test_route_policy"
        assert parcel.parcel_description == "description"
        assert parcel.default_action.value == "accept"

        assert len(parcel.sequences) == 1
        sequence = parcel.sequences[0]

        assert sequence.sequence_id.value == 1
        assert sequence.sequence_name.value == "test_sequence"
        assert len(sequence.match_entries) == 1
        match_entries = sequence.match_entries[0]
