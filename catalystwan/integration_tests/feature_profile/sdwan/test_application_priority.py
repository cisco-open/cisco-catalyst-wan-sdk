# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import List

import pytest

from catalystwan.api.configuration_groups.parcel import Default, Global
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.integration_tests.base import IS_API_20_12, TestCaseBase, create_name_with_run_id
from catalystwan.models.common import (
    AcceptDropActionType,
    DestinationRegion,
    DNSEntryType,
    EncapType,
    IcmpMsgType,
    LossProtectionType,
    SequenceIpType,
    ServiceChainNumber,
    ServiceType,
    TLOCColor,
    TrafficTargetType,
)
from catalystwan.models.configuration.feature_profile.sdwan.application_priority import (
    PolicySettingsParcel,
    QosMap,
    QosPolicyParcel,
    TrafficPolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.qos_policy import QosPolicyTarget
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.traffic_policy import (
    AppqoeOptimization,
    AppqoeOptimizationAction,
    BackupSlaPreferredColorAction,
    CflowdAction,
    CountAction,
    DestinationIpMatch,
    DestinationPortMatch,
    DestinationRegionMatch,
    DnsMatch,
    DscpMatch,
    FallbackToRoutingAction,
    IcmpMessageMatch,
    LocalTlocList,
    LogAction,
    LossCorrection,
    LossCorrectionAction,
    Match,
    Nat,
    NatAction,
    NatPoolAction,
    PacketLengthMatch,
    PreferredRemoteColor,
    ProtocolMatch,
    RedirectDns,
    RedirectDnsAction,
    SecureServiceEdgeInstance,
    Sequence,
    ServiceAreaMatch,
    ServiceAreaValue,
    ServiceChain,
    ServiceTloc,
    SetAction,
    SetDscp,
    SetLocalTlocList,
    SetNextHop,
    SetNextHopIpv6,
    SetNextHopLoose,
    SetPreferredRemoteColor,
    SetService,
    SetServiceChain,
    SetTloc,
    SetVpn,
    SigAction,
    SourceIpMatch,
    SourcePortMatch,
    Sse,
    SseAction,
    TcpMatch,
    Tloc,
    TrafficCategory,
    TrafficCategoryMatch,
    TrafficClass,
    TrafficClassMatch,
    TrafficPolicyTarget,
    TrafficToMatch,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.policy.centralized import TrafficDataDirection


@unittest.skipIf(IS_API_20_12, "PolicySettingsParcel is not supported in 20.12")
class TestPolicySettingsParcel(TestCaseBase):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile(
            create_name_with_run_id("TestApplicationPriorityProfile"), "Description"
        ).id

    def test_create_policy_settings_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

        assert parcel.parcel_name == "policy_settings_test_parcel"

    def test_update_policy_settings_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
            app_visibility=Default[bool](value=False),
            flow_visibility=Global[bool](value=True),
            app_visibility_ipv6=Global[bool](value=True),
            flow_visibility_ipv6=Global[bool](value=True),
        )
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload
        parcel.app_visibility = Global[bool](value=True)
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

        # Assert
        assert parcel.app_visibility == Global[bool](value=True)

    def test_delete_qos_policy_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
            app_visibility=Global[bool](value=True),
            flow_visibility=Global[bool](value=True),
            app_visibility_ipv6=Global[bool](value=True),
            flow_visibility_ipv6=Global[bool](value=True),
        )
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, PolicySettingsParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)


class TestQosPolicyParcel(TestCaseBase):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile(
            create_name_with_run_id("TestApplicationPriorityProfile"), "Description"
        ).id

    def test_create_qos_policy_parcel(self):
        qos_policy_parcel = QosPolicyParcel(
            name="qos_policy_test_parcel",
            qos_map=QosMap(qos_schedulers=[]),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, qos_policy_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload

        assert parcel.parcel_name == "qos_policy_test_parcel"
        assert len(parcel.qos_map.qos_schedulers) == 0

    def test_update_qos_policy_parcel(self):
        qos_policy_parcel = QosPolicyParcel(
            name="qos_policy_test_parcel",
            qos_map=QosMap(qos_schedulers=[]),
            target=QosPolicyTarget(interfaces=Global[List[str]](value=["GigabitEthernet1"])),
        )
        parcel_id = self.api.create_parcel(self.profile_id, qos_policy_parcel).id
        parcel = self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload
        parcel.target = QosPolicyTarget(interfaces=Global[List[str]](value=["GigabitEthernet2"]))
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload

        # Assert
        assert parcel.target == QosPolicyTarget(interfaces=Global[List[str]](value=["GigabitEthernet2"]))

    def test_delete_qos_policy_parcel(self):
        qos_policy_parcel = QosPolicyParcel(
            name="qos_policy_test_parcel",
            qos_map=QosMap(qos_schedulers=[]),
        )
        parcel_id = self.api.create_parcel(self.profile_id, qos_policy_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, QosPolicyParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)


@unittest.skip("Prepare for 20.12")
class TestTrafficPolicyParcel(TestCaseBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service_api = cls.session.api.sdwan_feature_profiles.service
        cls.service_profile_uuid = cls.service_api.create_profile(
            create_name_with_run_id("TestProfileServiceVpn"), "Description"
        ).id
        cls.vpn_name_1 = create_name_with_run_id("TestVpnParcelForTraffic")
        cls.service_api.create_parcel(
            cls.service_profile_uuid,
            LanVpnParcel(parcel_name=cls.vpn_name_1, parcel_description="Test Vpn Parcel", vpn_id=Global[int](value=2)),
        )
        cls.vpn_name_2 = create_name_with_run_id("TestVpnParcelForTraffic2")
        cls.service_api.create_parcel(
            cls.service_profile_uuid,
            LanVpnParcel(parcel_name=cls.vpn_name_2, parcel_description="Test Vpn Parcel", vpn_id=Global[int](value=2)),
        )

    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile(
            create_name_with_run_id("TestApplicationPriorityProfile"), "Description"
        ).id

    def test_create_traffic_policy_parcel(self):
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[AcceptDropActionType](value="accept"),
            target=TrafficPolicyTarget(
                direction=Global[TrafficDataDirection](value="all"), vpn=Global[List[str]](value=[self.vpn_name_1])
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

        assert parcel.parcel_name == "traffic_policy_test_parcel"

    def test_create_complex_traffic_policy_parcel(self):
        sequences = []
        sequence1 = Sequence(
            actions=[
                BackupSlaPreferredColorAction(backup_sla_preferred_color=Global[List[TLOCColor]](value=["mpls"])),
                RedirectDnsAction(redirect_dns=RedirectDns()),
                AppqoeOptimizationAction(
                    appqoe_optimization=AppqoeOptimization(
                        service_node_group=Global[str](value="SNG-APPQOE"),
                    )
                ),
                LossCorrectionAction(
                    loss_correction=LossCorrection(loss_correction_type=Global[LossProtectionType](value="fecAdaptive"))
                ),
                CountAction(count=Global[str](value="my_counter")),
                LogAction(log=Global[bool](value=True)),
                CflowdAction(cflowd=Global[bool](value=True)),
                NatPoolAction(nat_pool=Global[int](value=1)),
                FallbackToRoutingAction(fallback_to_routing=Global[bool](value=True)),
                SseAction(
                    sse=Sse(
                        secure_service_edge=Global[Global[bool]](value=Global[bool](value=True)),
                        secure_service_edge_instance=Global[SecureServiceEdgeInstance](value="zScaler"),
                    )
                ),
                SetAction(
                    set=[
                        SetDscp(dscp=Global[int](value=1)),
                        SetNextHop(next_hop=Global[IPv4Address](value=IPv4Address("10.0.1.1"))),
                        SetNextHopLoose(next_hop_loose=Global[bool](value=True)),
                        SetPreferredRemoteColor(
                            preferred_remote_color=PreferredRemoteColor(color=Global[List[TLOCColor]](value=["mpls"]))
                        ),
                        SetService(
                            service=ServiceTloc(
                                tloc=Tloc(
                                    color=Global[List[TLOCColor]](value=["mpls"]),
                                    encap=Global[EncapType](value="ipsec"),
                                    ip=Global[IPv4Address](value=IPv4Address("10.0.1.1")),
                                ),
                                type=Global[ServiceType](value="FW"),
                                vpn=Global[int](value=1),
                            )
                        ),
                    ]
                ),
            ],
            base_action=Global[AcceptDropActionType](value="accept"),
            match=Match(
                entries=[
                    ServiceAreaMatch(service_area=Global[List[ServiceAreaValue]](value=["common"])),
                    TrafficCategoryMatch(traffic_category=Global[TrafficCategory](value="all")),
                    TrafficClassMatch(traffic_class=Global[TrafficClass](value="bronze")),
                    DscpMatch(dscp=Global[int](value=0)),
                    PacketLengthMatch(packet_length=Global[str](value="1000")),
                    ProtocolMatch(protocol=Global[List[str]](value=["1", "16"])),
                    IcmpMessageMatch(icmp_message=Global[List[IcmpMsgType]](value=["echo"])),
                    SourceIpMatch(source_ip=Global[IPv4Network](value=IPv4Network("192.168.1.1/32"))),
                    SourcePortMatch(source_port=Global[List[str]](value=["22"])),
                    DestinationIpMatch(destination_ip=Global[IPv4Network](value=IPv4Network("10.0.0.1/32"))),
                    DestinationPortMatch(destination_port=Global[List[str]](value=["80"])),
                    TcpMatch(),
                    DestinationRegionMatch(destination_region=Global[DestinationRegion](value="other-region")),
                    TrafficToMatch(traffic_to=Global[TrafficTargetType](value="access")),
                    DnsMatch(dns=Global[DNSEntryType](value="request")),
                ]
            ),
            sequence_id=Global[int](value=1),
            sequence_ip_type=Global[SequenceIpType](value="ipv4"),
            sequence_name=Global[str](value="seq1"),
        )
        sequence2 = Sequence(
            actions=[
                NatAction(nat=Nat(use_vpn=Global[bool](value=True))),
                SigAction(sig=Global[bool](value=True)),
                SetAction(
                    set=[
                        SetVpn(vpn=Global[int](value=1)),
                        SetServiceChain(
                            service_chain=ServiceChain(
                                local=Global[bool](value=True),
                                restrict=Global[bool](value=True),
                                type=Global[ServiceChainNumber](value="SC1"),
                            )
                        ),
                    ]
                ),
            ],
            base_action=Global[AcceptDropActionType](value="accept"),
            match=Match(entries=[]),
            sequence_id=Global[int](value=2),
            sequence_ip_type=Global[SequenceIpType](value="ipv4"),
            sequence_name=Global[str](value="seq2"),
        )
        sequence3 = Sequence(
            actions=[
                SetAction(
                    set=[
                        SetNextHopIpv6(next_hop_ipv6=Global[IPv6Address](value=IPv6Address("2001::1"))),
                        SetLocalTlocList(local_tloc_list=LocalTlocList(color=Global[List[TLOCColor]](value=["mpls"]))),
                        SetTloc(
                            tloc=Tloc(
                                color=Global[List[TLOCColor]](value=["mpls"]),
                                encap=Global[EncapType](value="ipsec"),
                                ip=Global[IPv4Address](value=IPv4Address("10.0.1.1")),
                            )
                        ),
                    ]
                ),
            ],
            base_action=Global[AcceptDropActionType](value="accept"),
            match=Match(entries=[]),
            sequence_id=Global[int](value=3),
            sequence_ip_type=Global[SequenceIpType](value="ipv6"),
            sequence_name=Global[str](value="seq3"),
        )
        sequence3.match_tcp()
        sequence3.match_source_ipv6(IPv6Network("2001::0/64"))
        sequence3.match_source_ipv6(IPv6Network("2002::0/64"))
        sequence3.match_protocol("1")
        sequence3.match_protocol("16")
        sequence3.match_traffic_category("all")
        sequence3.match_service_area("skype")
        sequence3.match_service_area("exchange")
        sequences.append(sequence1)
        sequences.append(sequence2)
        sequences.append(sequence3)
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[AcceptDropActionType](value="accept"),
            sequences=sequences,
            target=TrafficPolicyTarget(
                direction=Global[TrafficDataDirection](value="all"), vpn=Global[List[str]](value=[self.vpn_name_1])
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

        assert parcel.parcel_name == "traffic_policy_test_parcel"

    def test_update_traffic_policy_parcel(self):
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[AcceptDropActionType](value="accept"),
            target=TrafficPolicyTarget(
                direction=Global[TrafficDataDirection](value="all"), vpn=Global[List[str]](value=[self.vpn_name_1])
            ),
        )
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload
        parcel.target = TrafficPolicyTarget(
            direction=Global[TrafficDataDirection](value="service"), vpn=Global[List[str]](value=[self.vpn_name_2])
        )
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

        # Assert
        assert parcel.target == TrafficPolicyTarget(
            direction=Global[TrafficDataDirection](value="service"), vpn=Global[List[str]](value=[self.vpn_name_2])
        )

    def test_delete_traffic_policy_parcel(self):
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[AcceptDropActionType](value="accept"),
            target=TrafficPolicyTarget(
                direction=Global[TrafficDataDirection](value="all"), vpn=Global[List[str]](value=[self.vpn_name_1])
            ),
        )
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, TrafficPolicyParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.service_api.delete_profile(cls.service_profile_uuid)
