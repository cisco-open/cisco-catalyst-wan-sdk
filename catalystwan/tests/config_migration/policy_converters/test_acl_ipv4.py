# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv4Address, IPv4Network
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.policy.definition.access_control_list import AclPolicy
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestDeviceAccessIPv4Converter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_acl_ipv4_convert(self):
        # Arrange
        exp_name = "Acl-ipv4-policy"
        exp_description = "Acl-ipv4-policy-description"
        exp_default_action = "accept"
        exp_sequence_id = 13
        exp_sequence_name = "Acl-ipv4-sequence"
        exp_sequence_base_action = "accept"
        exp_class_map_list_id = uuid4()
        exp_destination_data_prefix_list_id = uuid4()
        exp_ports, exp_port_ranges = ([50, 59], [(100, 200), (300, 400)])
        exp_dscp = [41, 44]
        exp_packet_length = (4, 1000)
        exp_source_data_prefix_list_id = uuid4()

        exp_action_class_map_list_id = uuid4()
        exp_action_counter_name = "Acl-ipv4-counter"
        exp_action_dscp = 17
        exp_action_mirror_list_id = uuid4()
        exp_action_next_hop_ip = IPv4Address("10.0.0.1")
        exp_action_policer_list_id = uuid4()

        ins = AclPolicy(name=exp_name, description=exp_description)
        ins.set_default_action(exp_default_action)
        inseq = ins.add_sequence(id_=exp_sequence_id, name=exp_sequence_name, base_action=exp_sequence_base_action)

        inseq.match_class_map_list_entry(class_map_list_id=exp_class_map_list_id)
        inseq.match_destination_data_prefix_list(data_prefix_list_id=exp_destination_data_prefix_list_id)
        inseq.match_destination_port(ports=set(exp_ports), port_ranges=exp_port_ranges)
        inseq.match_dscp(dscp=exp_dscp)
        inseq.match_high_plp()
        inseq.match_packet_length(packet_lengths=exp_packet_length)
        inseq.match_source_data_prefix_list(data_prefix_list_id=exp_source_data_prefix_list_id)

        inseq.associate_class_map_list_action(class_map_list_id=exp_action_class_map_list_id)
        inseq.associate_count_action(counter_name=exp_action_counter_name)
        inseq.associate_dscp_action(dscp=exp_action_dscp)
        inseq.associate_log_action()
        inseq.associate_mirror_action(mirror_list_id=exp_action_mirror_list_id)
        inseq.associate_next_hop_action(next_hop=exp_action_next_hop_ip)
        inseq.associate_policer_list_action(policer_list_id=exp_action_policer_list_id)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output

        # Assert
        assert isinstance(outs, Ipv4AclParcel)
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
        assert match.destination_data_prefix.destination_data_prefix_list.ref_id.value == str(
            exp_destination_data_prefix_list_id
        )
        assert len(match.destination_ports) == 4
        expected_port_values = set(exp_ports + [f"{r[0]}-{r[1]}" for r in exp_port_ranges])
        observed_port_values = set([d.destination_port.value for d in match.destination_ports])
        assert observed_port_values == expected_port_values
        assert match.dscp.value == exp_dscp
        assert match.packet_length.value == f"{exp_packet_length[0]}-{exp_packet_length[1]}"
        assert match.source_data_prefix.source_data_prefix_list.ref_id.value == str(exp_source_data_prefix_list_id)
        # actions
        assert len(outseq.actions) == 1
        action = outseq.actions[0]
        assert action.accept is not None
        assert action.accept.counter_name.value == exp_action_counter_name
        assert action.accept.log.value is True
        assert action.accept.mirror.ref_id.value == str(exp_action_mirror_list_id)
        assert action.accept.policer.ref_id.value == str(exp_action_policer_list_id)
        assert action.accept.set_next_hop.value == str(exp_action_next_hop_ip)

    def test_acl_ipv4_convert_complementary(self):
        # Arrange
        exp_name = "Acl-ipv4-policy-2"
        exp_description = "Acl-ipv4-policy-description-2"
        exp_default_action = "drop"
        exp_sequence_id = 1
        exp_sequence_name = "Acl-ipv4-sequence-2"
        exp_sequence_base_action = "drop"

        exp_destination_prefix = IPv4Network("10.2.0.0/16")
        exp_protocols = {22, 23, 27}
        exp_source_prefix = IPv4Network("10.2.1.0/24")
        exp_action_counter_name = "Acl-ipv4-2-drop-cnt"

        ins = AclPolicy(name=exp_name, description=exp_description)
        ins.set_default_action(exp_default_action)
        inseq = ins.add_sequence(id_=exp_sequence_id, name=exp_sequence_name, base_action=exp_sequence_base_action)

        inseq.match_destination_ip(networks=[exp_destination_prefix])
        inseq.match_protocols(protocols=exp_protocols)
        inseq.match_source_ip(networks=[exp_source_prefix])

        inseq.associate_count_action(counter_name=exp_action_counter_name)
        inseq.associate_log_action()

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output

        # Assert
        assert isinstance(outs, Ipv4AclParcel)
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
        assert match.protocol.value == list(exp_protocols)
        assert match.source_data_prefix.source_ip_prefix.value == str(exp_source_prefix)
        # actions
        assert len(outseq.actions) == 1
        action = outseq.actions[0]
        assert action.drop is not None
        assert action.drop.counter_name.value == exp_action_counter_name
