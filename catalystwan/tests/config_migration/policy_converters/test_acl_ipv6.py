# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv6Address, IPv6Network
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.policy.definition.access_control_list_ipv6 import AclIPv6Policy
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestDeviceAccessIPv6Converter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_acl_ipv6_convert(self):
        # Arrange
        exp_name = "Acl-ipv6-policy"
        exp_description = "Acl-ipv6-policy-description"
        exp_default_action = "accept"
        exp_sequence_id = 1
        exp_sequence_name = "Acl-ipv6-sequence"
        exp_sequence_base_action = "accept"
        exp_class_map_list_id = uuid4()
        exp_destination_data_prefix_list_id = uuid4()
        exp_next_header = 127
        exp_ports, exp_port_ranges = ([50, 59], [(100, 200), (300, 400)])
        exp_packet_length = (4, 1000)
        exp_source_data_prefix_list_id = uuid4()
        exp_traffic_class = [15, 17, 19]

        exp_action_class_map_list_id = uuid4()
        exp_action_counter_name = "Acl-ipv6-counter"
        exp_action_mirror_list_id = uuid4()
        exp_action_next_hop_ip = IPv6Address("2001:0DB8:ABCD:0012:0000:0000:0000:0001")
        exp_action_policer_list_id = uuid4()
        exp_action_traffic_class = 21

        ins = AclIPv6Policy(id_=exp_sequence_id, name=exp_name, description=exp_description)
        ins.set_default_action(exp_default_action)
        inseq = ins.add_sequence(id_=exp_sequence_id, name=exp_sequence_name, base_action=exp_sequence_base_action)

        inseq.match_class_map_list_entry(class_map_list_id=exp_class_map_list_id)
        inseq.match_destination_data_prefix_list(data_prefix_list_id=exp_destination_data_prefix_list_id)
        inseq.match_destination_port(ports=set(exp_ports), port_ranges=exp_port_ranges)
        inseq.match_high_plp()
        inseq.match_next_header(next_header=exp_next_header)
        inseq.match_packet_length(packet_lengths=exp_packet_length)
        inseq.match_source_data_prefix_list(data_prefix_list_id=exp_source_data_prefix_list_id)
        inseq.match_traffic_class(traffic_class=exp_traffic_class)

        inseq.associate_class_map_list_action(class_map_list_id=exp_action_class_map_list_id)
        inseq.associate_count_action(counter_name=exp_action_counter_name)
        inseq.associate_log_action()
        inseq.associate_mirror_action(mirror_list_id=exp_action_mirror_list_id)
        inseq.associate_next_hop_action(next_hop=exp_action_next_hop_ip)
        inseq.associate_policer_list_action(policer_list_id=exp_action_policer_list_id)
        inseq.associate_traffic_class_action(traffic_class=exp_action_traffic_class)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output

        # Assert
        assert isinstance(outs, Ipv6AclParcel)
        assert outs.parcel_name == ins.name
        assert outs.parcel_description == ins.description
        assert outs.default_action.value == ins.default_action.type
        # sequence
        assert len(outs.sequences) == 1
        outseq = outs.sequences[0]
        outseq.sequence_id = exp_sequence_id
        outseq.sequence_name == exp_sequence_name
        outseq.base_action == exp_sequence_base_action
        # matches
        assert len(outseq.match_entries) == 1
        match = outseq.match_entries[0]
        assert match.destination_data_prefix.destination_data_prefix_list.ref_id.value == str(
            exp_destination_data_prefix_list_id
        )
        assert len(match.destination_ports) == 4
        expected_port_values = set(exp_ports + [f"{r[0]}-{r[1]}" for r in exp_port_ranges])
        observed_port_values = set([d.destination_port.value for d in match.destination_ports])
        assert observed_port_values == expected_port_values
        assert match.packet_length.value == f"{exp_packet_length[0]}-{exp_packet_length[1]}"
        assert match.source_data_prefix.source_data_prefix_list.ref_id.value == str(exp_source_data_prefix_list_id)
        assert match.traffic_class.value == exp_traffic_class
        # actions
        assert len(outseq.actions) == 1
        action = outseq.actions[0]
        assert action.accept is not None
        assert action.accept.counter_name.value == exp_action_counter_name
        assert action.accept.log.value is True
        assert action.accept.mirror.ref_id.value == str(exp_action_mirror_list_id)
        assert action.accept.policer.ref_id.value == str(exp_action_policer_list_id)
        assert action.accept.set_next_hop.value == str(exp_action_next_hop_ip)
        assert action.accept.set_traffic_class.value == exp_action_traffic_class

    def test_acl_ipv6_convert_complementary(self):
        # Arrange
        exp_name = "Acl-ipv6-policy-2"
        exp_description = "Acl-ipv6-policy-description-2"
        exp_default_action = "drop"
        exp_sequence_id = 15
        exp_sequence_name = "Acl-ipv6-sequence-2"
        exp_sequence_base_action = "drop"

        exp_destination_prefix = IPv6Network("2001:db8:abcd:0012::0/96")
        exp_source_prefix = IPv6Network("2001:db8:abcd:0012::0/112")
        exp_action_counter_name = "Acl-ipv6-2-drop-cnt"

        ins = AclIPv6Policy(name=exp_name, description=exp_description)
        ins.set_default_action(exp_default_action)
        inseq = ins.add_sequence(id_=exp_sequence_id, name=exp_sequence_name, base_action=exp_sequence_base_action)

        inseq.match_destination_ip(networks=[exp_destination_prefix])
        inseq.match_source_ip(networks=[exp_source_prefix])

        inseq.associate_count_action(counter_name=exp_action_counter_name)
        inseq.associate_log_action()

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output

        # Assert
        assert isinstance(outs, Ipv6AclParcel)
        assert outs.parcel_name == ins.name
        assert outs.parcel_description == ins.description
        assert outs.default_action.value == ins.default_action.type
        # sequence
        assert len(outs.sequences) == 1
        outseq = outs.sequences[0]
        outseq.sequence_name == exp_sequence_name
        outseq.base_action == exp_sequence_base_action
        # matches
        assert len(outseq.match_entries) == 1
        match = outseq.match_entries[0]
        assert match.destination_data_prefix.destination_ip_prefix.value == str(exp_destination_prefix)
        assert match.source_data_prefix.source_ip_prefix.value == str(exp_source_prefix)
        # actions
        assert len(outseq.actions) == 1
        action = outseq.actions[0]
        assert action.drop is not None
        assert action.drop.counter_name.value == exp_action_counter_name
