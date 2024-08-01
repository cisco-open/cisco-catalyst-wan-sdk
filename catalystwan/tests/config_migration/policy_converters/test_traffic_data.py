# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv4Network
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.traffic_policy import (
    TrafficPolicyParcel,
)
from catalystwan.models.policy.definition.traffic_data import TrafficDataPolicy
from catalystwan.models.policy.policy_definition import PolicyAcceptDropAction
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestTrafficDataConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()
        self.name = "Test-Data-Policy-0"
        self.description = "This is data policy created for converter unittest"
        self.default_action = PolicyAcceptDropAction(type="accept")
        self.input = TrafficDataPolicy(
            default_action=self.default_action,
            name=self.name,
            description=self.description,
        )

    def test_sequences(self):
        # Arrange
        ins = self.input
        ins.add_sequence(name="seq-1", base_action="accept", sequence_ip_type="ipv4")
        ins.add_sequence(name="seq-2", base_action="accept", sequence_ip_type="ipv6")
        ins.add_sequence(name="seq-3", base_action="accept", sequence_ip_type="all")
        ins.add_sequence(name="seq-4", base_action="drop", sequence_ip_type="ipv4")
        ins.add_sequence(name="seq-5", base_action="drop", sequence_ip_type="ipv6")
        ins.add_sequence(name="seq-6", base_action="drop", sequence_ip_type="all")
        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 6
        for i, seq in enumerate(ins.sequences):
            assert outs.sequences[i].sequence_name.value == seq.sequence_name
            assert outs.sequences[i].sequence_id.value == seq.sequence_id
            assert outs.sequences[i].base_action.value == seq.base_action
            assert outs.sequences[i].sequence_ip_type.value == seq.sequence_ip_type
            assert outs.sequences[i].actions is None
            assert outs.sequences[i].match is None

    def test_match(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4")

        expected_app_list = uuid4()
        seq.match_app_list(expected_app_list)
        # seq.match_destination_data_prefix_list(uuid4())

        expected_destination_ip = [IPv4Network("11.0.0.0/16"), IPv4Network("12.0.0.0/12")]
        seq.match_destination_ip(expected_destination_ip)

        dst_port_range = (100, 110)
        dst_port_set = {30, 39}
        expected_destination_ports = [str(p) for p in dst_port_set] + [f"{dst_port_range[0]}-{dst_port_range[1]}"]
        seq.match_destination_port(ports=dst_port_set, port_ranges=[dst_port_range])

        expected_destination_region = "primary-region"
        seq.match_destination_region(expected_destination_region)

        expected_dns_app_list = uuid4()
        seq.match_dns_app_list(expected_dns_app_list)

        expected_dns = "request"
        seq.match_dns(expected_dns)

        expected_dscp = [10, 15]
        seq.match_dscp(expected_dscp)

        expected_icmp = ["echo-reply", "port-unreachable"]
        seq.match_icmp(expected_icmp)

        expected_packetlen = (32, 640)
        seq.match_packet_length(expected_packetlen)

        expected_source_ip = [IPv4Network("13.0.0.0/16"), IPv4Network("14.0.0.0/12")]
        seq.match_source_ip(expected_source_ip)

        src_port_range = (99, 109)
        src_port_set = {119}
        expected_source_ports = [str(p) for p in src_port_set] + [f"{src_port_range[0]}-{src_port_range[1]}"]
        seq.match_source_port(expected_source_ports)

        seq.match_tcp()

        expected_traffic_to = "access"
        seq.match_traffic_to(expected_traffic_to)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outm = outs.sequences[0].match.entries
        assert outm[0].app_list.ref_id.value == str(expected_app_list)
        assert outm[1].destination_ip.value == expected_destination_ip[0]
        assert set(outm[2].destination_port.value) == set(expected_destination_ports)
        assert outm[3].destination_region.value == expected_destination_region
        assert outm[4].dns_app_list.ref_id.value == str(expected_dns_app_list)
        assert outm[5].dns.value == expected_dns
        assert outm[6].dscp.value == expected_dscp
        assert outm[7].icmp_message.value == expected_icmp
        assert outm[8].packet_length.value == "-".join([str(i) for i in expected_packetlen])
        assert outm[9].source_ip.value == expected_source_ip[0]
        assert set(outm[10].source_port.value) == set(expected_source_ports)
        assert outm[11].tcp.value == "syn"
        assert outm[12].traffic_to.value == expected_traffic_to

    def test_match_complementary(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4")

        expected_destination_prefix_list = uuid4()
        seq.match_destination_data_prefix_list(expected_destination_prefix_list)

        expected_protocols = {111, 101}
        seq.match_protocols(expected_protocols)

        expected_source_prefix_list = uuid4()
        seq.match_source_data_prefix_list(expected_source_prefix_list)
        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outm = outs.sequences[0].match.entries
        assert outm[0].destination_data_prefix_list.ref_id.value == str(expected_destination_prefix_list)
        assert outm[1].protocol.value == [str(i) for i in expected_protocols]
        assert outm[2].source_data_prefix_list.ref_id.value == str(expected_source_prefix_list)

    def test_actions(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4", base_action="accept")

        expected_appqoe_tcp = True
        expected_appqoe_dre = True
        expected_appqoe_service_node_group = "SNG-APPQOE21"
        seq.associate_app_qoe_optimization_action(
            tcp=expected_appqoe_tcp, dre=expected_appqoe_dre, service_node_group=expected_appqoe_service_node_group
        )

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outa = outs.sequences[0].actions
        outa[0].appqoe_optimization.tcp_optimization.value == expected_appqoe_tcp
        outa[0].appqoe_optimization.dre_optimization.value == expected_appqoe_dre
        outa[0].appqoe_optimization.service_node_group.value == expected_appqoe_service_node_group
