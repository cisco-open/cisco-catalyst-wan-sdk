# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from uuid import uuid4

from packaging.version import Version  # type: ignore

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.traffic_policy import (
    SetAction,
    TrafficPolicyParcel,
)
from catalystwan.models.policy.definition.traffic_data import TrafficDataPolicy
from catalystwan.models.policy.policy_definition import PolicyAcceptDropAction
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestTrafficDataConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext(platform_version=Version("21"))
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

        # Arrange: 0
        expected_app_list = uuid4()
        seq.match_app_list(expected_app_list)

        # Arrange: 1
        expected_destination_ip = [IPv4Network("11.0.0.0/16"), IPv4Network("12.0.0.0/12")]
        seq.match_destination_ip(expected_destination_ip)

        # Arrange: 2
        dst_port_range = (100, 110)
        dst_port_set = {30, 39}
        expected_destination_ports = [str(p) for p in dst_port_set] + [f"{dst_port_range[0]}-{dst_port_range[1]}"]
        seq.match_destination_port(ports=dst_port_set, port_ranges=[dst_port_range])

        # Arrange: 3
        expected_destination_region = "primary-region"
        seq.match_destination_region(expected_destination_region)

        # Arrange: 4
        expected_dns_app_list = uuid4()
        seq.match_dns_app_list(expected_dns_app_list)

        # Arrange: 5
        expected_dns = "request"
        seq.match_dns(expected_dns)

        # Arrange: 6
        expected_dscp = [10, 15]
        seq.match_dscp(expected_dscp)

        # Arrange: 7
        expected_icmp = ["echo-reply", "port-unreachable"]
        seq.match_icmp(expected_icmp)

        # Arrange: 8
        expected_packetlen = (32, 640)
        seq.match_packet_length(expected_packetlen)

        # Arrange: 9
        expected_source_ip = [IPv4Network("13.0.0.0/16"), IPv4Network("14.0.0.0/12")]
        seq.match_source_ip(expected_source_ip)

        # Arrange: 10
        src_port_range = (99, 109)
        src_port_set = {119}
        expected_source_ports = [str(p) for p in src_port_set] + [f"{src_port_range[0]}-{src_port_range[1]}"]
        seq.match_source_port(expected_source_ports)

        # Arrange: 11
        seq.match_tcp()

        # Arrange: 12
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

        # Arrange: 0
        expected_destination_prefix_list = uuid4()
        seq.match_destination_data_prefix_list(expected_destination_prefix_list)

        # Arrange: 1
        expected_protocols = {111, 101}
        seq.match_protocols(expected_protocols)

        # Arrange: 2
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

    def test_match_complementary_ipv6(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv6")

        # Arrange: 0
        expected_destination_ipv6_prefix = [IPv6Network(2**60), IPv6Network(2**61)]
        seq.match_destination_ipv6(expected_destination_ipv6_prefix)

        # Arrange: 1
        expected_source_ipv6_prefix = [IPv6Network(2**62), IPv6Network(2**63)]
        seq.match_source_ipv6(expected_source_ipv6_prefix)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outm = outs.sequences[0].match.entries
        assert outm[0].destination_ipv6.value == expected_destination_ipv6_prefix[0]
        assert outm[1].source_ipv6.value == expected_source_ipv6_prefix[0]

    def test_actions(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4", base_action="accept")

        # Arrange: 0
        expected_counter_name = "Counter1"
        seq.associate_count_action(expected_counter_name)

        # Arrange: 1
        seq.associate_log_action()

        # Arrange: 2
        seq.associate_cflowd_action()

        # Arrange: 3
        expected_nat_pool = [4, 7]
        expected_nat_interface = ["Ethernet1", "GigabitEthernet2"]
        seq.associate_nat_action(fallback=True, dia_pool=expected_nat_pool, dia_interface=expected_nat_interface)

        # Arrange: 4
        expected_dns_type = "umbrella"
        seq.associate_redirect_dns_action(dns_type=expected_dns_type)

        # Arrange: 5
        seq.associate_secure_internet_gateway_action(fallback_to_routing=False)

        # Arrange: 6 (not guaranteed to be in that specific index - relies on current implementation)
        expected_appqoe_tcp = True
        expected_appqoe_dre = True
        expected_appqoe_service_node_group = "SNG-APPQOE21"
        seq.associate_app_qoe_optimization_action(
            tcp=expected_appqoe_tcp, dre=expected_appqoe_dre, service_node_group=expected_appqoe_service_node_group
        )

        # Arrange: 7 (not guaranteed to be in that specific index - relies on current implementation)
        expected_fec_threshold = 12
        seq.associate_loss_correction_fec_action(adaptive=True, threshold=expected_fec_threshold)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outa = outs.sequences[0].actions
        outa[0].count.value == expected_counter_name
        outa[1].log.value is True
        outa[2].cflowd.value is True
        outa[3].nat.use_vpn.value is True
        outa[3].nat.dia_interface.value == expected_nat_interface
        outa[3].nat.dia_pool.value == expected_nat_pool
        outa[3].nat.fallback.value is True
        outa[3].nat.bypass.value is False
        outa[4].redirect_dns.field.value == "dnsHost"
        outa[4].redirect_dns.value.value == expected_dns_type
        outa[5].sig.value is True
        outa[6].appqoe_optimization.tcp_optimization.value == expected_appqoe_tcp
        outa[6].appqoe_optimization.dre_optimization.value == expected_appqoe_dre
        outa[6].appqoe_optimization.service_node_group.value == expected_appqoe_service_node_group
        outa[7].loss_correction.loss_correction_type.value == "fecAdaptive"
        outa[7].loss_correction.loss_correct_fec.value == expected_fec_threshold

    def test_set_actions(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4", base_action="accept")

        # Arrange: 0
        expected_dscp = 28
        seq.associate_dscp_action(expected_dscp)

        # Arrange: 1
        fwclass = "FW-Class-Name"
        expected_fwclass_id = uuid4()
        seq.associate_forwarding_class_action(fwclass)
        self.context.fwclass_id_by_name[fwclass] = expected_fwclass_id

        # Arrange: 2
        expected_local_tloc_color = ["gold", "blue"]
        expected_local_tloc_encap = "ipsec"
        expected_local_tloc_restrict = True
        seq.associate_local_tloc_action(
            color=expected_local_tloc_color, encap=expected_local_tloc_encap, restrict=expected_local_tloc_restrict
        )

        # Arrange: 3, 4
        expected_next_hop = IPv4Address("15.1.0.1")
        expected_next_hop_loose = True
        seq.associate_next_hop_action(expected_next_hop, expected_next_hop_loose)

        # Arrange 5
        expected_policer_list_id = uuid4()
        seq.associate_policer_list_action(expected_policer_list_id)

        # Arrange: 6
        expected_service_type = "FW"
        expected_service_vpn = 74
        expected_service_tloc_ip = IPv4Address("10.3.4.5")
        expected_service_tloc_color = "green"
        expected_service_tloc_encap = "gre"
        seq.associate_service_action(
            service_type=expected_service_type,
            vpn=expected_service_vpn,
            ip=expected_service_tloc_ip,
            color=expected_service_tloc_color,
            encap=expected_service_tloc_encap,
        )

        # Arrange: 7
        expected_vpn = 42
        seq.associate_vpn_action(expected_vpn)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outa = outs.sequences[0].actions
        assert len(outa) == 1
        assert isinstance(outa[0], SetAction)
        outas = outa[0].set
        outas[0].dscp.value == expected_dscp
        outas[1].forwarding_class.ref_id.value == str(expected_fwclass_id)
        outas[2].local_tloc_list.color.value == expected_local_tloc_color
        outas[2].local_tloc_list.encap.value == expected_local_tloc_encap
        outas[2].local_tloc_list.restrict == expected_local_tloc_restrict
        outas[3].next_hop.value == expected_next_hop
        outas[4].next_hop_loose == expected_next_hop_loose
        outas[5].policer.ref_id.value == str(expected_policer_list_id)
        outas[6].service.type.value == expected_service_type
        outas[6].service.vpn.value == expected_service_vpn
        outas[6].service.tloc.ip.value == expected_service_tloc_ip
        outas[6].service.tloc.color.value == [expected_service_tloc_color]
        outas[6].service.tloc.encap.value == expected_service_tloc_encap
        outas[7].vpn.value == expected_vpn

    def test_set_actions_complementary(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4", base_action="accept")

        # Arrange: 0
        expected_pref_clr_grp = uuid4()
        seq.associate_preffered_color_group(expected_pref_clr_grp)

        # Arrange: 1, 2
        expected_next_hop = IPv6Address("2001:0000:130F:0000:0000:09C0:876A:130B")
        expected_next_hop_loose = False
        seq.associate_next_hop_action(expected_next_hop, expected_next_hop_loose)

        # Arrange: 3
        expected_service_type = "IDP"
        expected_service_vpn = 75
        expected_service_tloc_list_id = uuid4()
        seq.associate_service_action(
            service_type=expected_service_type,
            vpn=expected_service_vpn,
            tloc_list_id=expected_service_tloc_list_id,
        )

        # Arrange: 4
        expected_tloc_ip = IPv4Address("10.9.8.7")
        expected_tloc_color = "bronze"
        expected_tloc_encap = "ipsec"
        seq.associate_tloc_action(ip=expected_tloc_ip, color=expected_tloc_color, encap=expected_tloc_encap)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outa = outs.sequences[0].actions
        assert len(outa) == 1
        assert isinstance(outa[0], SetAction)
        outas = outa[0].set
        outas[0].preferred_color_group.ref_id.value == str(expected_pref_clr_grp)
        outas[1].next_hop_ipv6.value == expected_next_hop
        outas[2].next_hop_loose == expected_next_hop_loose
        outas[3].service.type.value == expected_service_type
        outas[3].service.vpn.value == expected_service_vpn
        outas[3].service.tloc_list.ref_id == str(expected_service_tloc_list_id)
        outas[4].tloc.ip == expected_tloc_ip
        outas[4].tloc.color == expected_tloc_color
        outas[4].tloc.encap == expected_tloc_encap

    def test_set_actions_complementary_2(self):
        # Arrange
        ins = self.input
        seq = ins.add_sequence(name="seq-1", sequence_ip_type="ipv4", base_action="accept")

        # Arrange: 0
        expected_tloc_list_id = uuid4()
        seq.associate_tloc_action(tloc_list_id=expected_tloc_list_id)

        # Act
        outs = convert(in_=ins, uuid=uuid4(), context=self.context).output
        # Assert
        assert isinstance(outs, TrafficPolicyParcel)
        assert len(outs.sequences) == 1
        outa = outs.sequences[0].actions
        assert len(outa) == 1
        assert isinstance(outa[0], SetAction)
        outas = outa[0].set
        outas[0].tloc_list.ref_id.value == str(expected_tloc_list_id)
