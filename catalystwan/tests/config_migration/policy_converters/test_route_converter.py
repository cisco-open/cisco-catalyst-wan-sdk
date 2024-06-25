# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv4Address
from uuid import uuid4

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import ReferenceId, RoutePolicyParcel
from catalystwan.models.policy.definition.route_policy import RoutePolicy
from catalystwan.models.policy.policy_definition import PolicyAcceptRejectAction
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
        extended_community_list_ref = uuid4()
        uuid = uuid4()

        route_policy = RoutePolicy(
            name="test_route_policy",
            description="description",
            default_action=PolicyAcceptRejectAction(type="accept"),
        )
        rule_sequence = route_policy.add_sequence(id_=1, name="test_sequence", base_action="accept", ip_type="ipv4")
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
        rule_sequence.match_standard_community_list(match_flag="and", community_lists=standard_community_list_ref)
        rule_sequence.match_extended_community_list(
            extended_community_ref=extended_community_list_ref,
        )
        rule_sequence.associate_aggregator_action(
            aggregator_value=100,
            ip_address=IPv4Address("10.2.3.2"),
        )
        rule_sequence.associate_as_path_action(
            prepend_action=[100, 200],
            exclude_action=[300, 400],
        )
        rule_sequence.associate_atomic_aggregate_action()
        rule_sequence.associate_origin_action(
            origin="igp",
        )
        rule_sequence.associate_originator_action(
            originator=IPv4Address("9.9.9.9"),
        )
        rule_sequence.associate_community_by_variable_action(
            variable="test_community_variable",
            community_additive=True,
        )
        rule_sequence.associate_local_preference_action(
            value=100,
        )
        rule_sequence.associate_metric_action(
            value=100,
        )
        rule_sequence.associate_nexthop_action(
            nexthop=IPv4Address("8.8.8.7"),
        )
        rule_sequence.associate_metric_type_action(
            metric_type="type1",
        )
        rule_sequence.associate_omp_tag_action(
            omp_tag=100,
        )
        rule_sequence.associate_ospf_tag_action(
            ospf_tag=100,
        )
        rule_sequence.associate_weight_action(
            weight=100,
        )

        # Act
        parcel = convert(route_policy, uuid, context=self.context).output
        # Assert
        assert isinstance(parcel, RoutePolicyParcel)
        assert parcel.parcel_name == "test_route_policy"
        assert parcel.parcel_description == "description"
        assert parcel.default_action.value == "accept"

        assert len(parcel.sequences) == 1
        sequence = parcel.sequences[0]

        assert sequence.sequence_id.value == 1
        assert sequence.sequence_name.value == "test_sequence"
        assert len(sequence.match_entries) == 1
        match_entries = sequence.match_entries[0]

        assert match_entries.ipv4_address.ref_id == address_ref
        assert match_entries.as_path_list.ref_id == path_list_ref
        assert match_entries.bgp_local_preference.value == 100
        assert match_entries.metric.value == 100
        assert match_entries.ipv4_next_hop.ref_id == next_hop_ref
        assert match_entries.omp_tag.value == 100
        # assert match_entries.peer: there is not peer in the match_entries
        # assert match_entries.origin: there is not origin in the match_entries
        assert match_entries.community_list.criteria.value == "AND"
        assert match_entries.community_list.standard_community_list == [
            ReferenceId.from_uuid(u) for u in standard_community_list_ref
        ]
        assert match_entries.ext_community_list.ref_id == extended_community_list_ref

        assert len(sequence.actions) == 1
        accept = sequence.actions[0].accept

        # assert accept.aggregator: there is not aggregator in the accept
        assert accept.as_path.prepend == [as_global(i) for i in [100, 200]]
        # assert accept.as_path.exclude: there is not exclude in the accept
        # assert accept.atomic_aggregate: there is not atomic_aggregate in the accept
        assert accept.origin.value == "IGP"
        # assert accept.originator: there is not originator in the accept
        assert accept.community.additive == as_global(True)
        assert accept.community.community.value == "{{test_community_variable}}"
        assert accept.local_preference.value == 100
        assert accept.metric.value == 100
        assert accept.metric_type.value == "type1"
        assert accept.ipv4_next_hop.value == IPv4Address("8.8.8.7")
        assert accept.omp_tag.value == 100
        assert accept.ospf_tag.value == 100
        assert accept.weight.value == 100
