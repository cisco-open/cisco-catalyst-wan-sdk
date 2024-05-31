# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import Literal
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_global, as_variable
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.common import (
    CableLengthLongValue,
    ClockRate,
    E1Framing,
    E1Linecode,
    LineMode,
    SubnetMask,
    T1Framing,
    T1Linecode,
)
from catalystwan.models.configuration.feature_profile.common import (
    AddressWithMask,
    ChannelGroup,
    MultilinkAuthenticationType,
    MultilinkClockSource,
    MultilinkControllerTxExList,
    MultilinkControllerType,
    MultilinkMethod,
    MultilinkNimList,
    MultilinkTxExName,
)
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.bgp import AddressFamily as BgpAddressFamily
from catalystwan.models.configuration.feature_profile.sdwan.routing.bgp import (
    AddressFamilyItem,
    FamilyType,
    Ipv6AddressFamily,
    Ipv6AggregateAddres,
    Ipv6NeighborItem,
    Ipv6NetworkItem,
    Ipv6RedistributeItem,
    MaxPrefixConfigRestart,
    NeighborItem,
    NetworkItem,
    RedistributeItem,
    RoutingBgpParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospf import RoutingOspfParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospfv3 import (
    Ospfv3InterfaceParametres,
    Ospfv3IPv4Area,
    Ospfv3IPv6Area,
    RoutingOspfv3IPv4Parcel,
    RoutingOspfv3IPv6Parcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.dhcp_server import (
    AddressPool,
    LanVpnDhcpServerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.eigrp import (
    AddressFamily,
    EigrpParcel,
    SummaryAddress,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import InterfaceEthernetParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import BasicGre, InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.multilink import InterfaceMultilinkParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.svi import InterfaceSviParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    AutoRpAttributes,
    BsrCandidateAttributes,
    IgmpAttributes,
    IgmpInterfaceParameters,
    LocalConfig,
    MsdpAttributes,
    MsdpPeer,
    MsdpPeerAttributes,
    MulticastBasicAttributes,
    MulticastParcel,
    PimAttributes,
    PimBsrAttributes,
    PimInterfaceParameters,
    RPAnnounce,
    RpDiscoveryScope,
    SsmAttributes,
    SsmFlag,
    StaticJoin,
    StaticRpAddress,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.switchport import (
    ControlDirection,
    Duplex,
    HostMode,
    PortControl,
    Speed,
    StaticMacAddress,
    SwitchportInterface,
    SwitchportMode,
    SwitchportParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.wireless_lan import (
    SSID,
    CountryCode,
    MeIpConfig,
    MeStaticIpConfig,
    QosProfile,
    RadioType,
    SecurityConfig,
    SecurityType,
    WirelessLanParcel,
)


class TestServiceFeatureProfileModels(TestFeatureProfileModels):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.service
        cls.profile_uuid = cls.api.create_profile("TestProfileService", "Description").id

    def test_when_default_values_dhcp_server_parcel_expect_successful_post(self):
        # Arrange
        dhcp_server_parcel = LanVpnDhcpServerParcel(
            parcel_name="DhcpServerDefault",
            parcel_description="Dhcp Server Parcel",
            address_pool=AddressPool(
                network_address=Global[IPv4Address](value=IPv4Address("10.0.0.2")),
                subnet_mask=Global[SubnetMask](value="255.255.255.255"),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, dhcp_server_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_service_vpn_parcel_expect_successful_post(self):
        # Arrange
        vpn_parcel = LanVpnParcel(
            parcel_name="TestVpnParcel",
            parcel_description="Test Vpn Parcel",
            vpn_id=Global[int](value=2),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, vpn_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_ospf_parcel_expect_successful_post(self):
        # Arrange
        ospf_parcel = RoutingOspfParcel(
            parcel_name="TestRoutingOspfParcel",
            parcel_description="Test Ospf Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ospf_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_ospfv3_ipv4_expect_successful_post(self):
        # Arrange
        ospfv3ipv4_parcel = RoutingOspfv3IPv4Parcel(
            parcel_name="TestOspfv3ipv4",
            parcel_description="Test Ospfv3ipv4 Parcel",
            area=[
                Ospfv3IPv4Area(
                    area_number=as_global(5),
                    interfaces=[Ospfv3InterfaceParametres(name=as_global("GigabitEthernet0/0/0"))],
                )
            ],
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ospfv3ipv4_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_ospfv3_ipv6_expect_successful_post(self):
        # Arrange
        ospfv3ipv6_parcel = RoutingOspfv3IPv6Parcel(
            parcel_name="TestOspfv3ipv6",
            parcel_description="Test Ospfv3ipv6 Parcel",
            area=[
                Ospfv3IPv6Area(
                    area_number=as_global(7),
                    interfaces=[Ospfv3InterfaceParametres(name=as_global("GigabitEthernet0/0/0"))],
                )
            ],
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ospfv3ipv6_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_eigrp_parcel_expect_successful_post(self):
        eigrp_parcel = EigrpParcel(
            parcel_name="TestEigrpParcel",
            parcel_description="Test Eigrp Parcel",
            as_number=Global[int](value=1),
            address_family=AddressFamily(
                network=[
                    SummaryAddress(
                        prefix=AddressWithMask(
                            address=as_global("10.3.2.1"),
                            mask=as_global("255.255.255.0"),
                        )
                    )
                ]
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, eigrp_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_route_policy_parcel_expect_successful_post(self):
        # Arrange
        route_policy_parcel = RoutePolicyParcel(
            parcel_name="TestRoutePolicyParcel",
            parcel_description="Test Route Policy Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, route_policy_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_acl_ipv4_expect_successful_post(self):
        # Arrange
        acl_ipv4_parcel = Ipv4AclParcel(
            parcel_name="TestAclIpv4Parcel",
            parcel_description="Test Acl Ipv4 Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, acl_ipv4_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_acl_ipv4_expect_successful_post(self):
        # Arrange
        acl_ipv4_parcel = Ipv4AclParcel(
            parcel_name="TestAclIpv4Parcel-Full",
            parcel_description="Test Acl Ipv4 Parcel",
        )
        # Arrange Sequence 1
        seq1 = acl_ipv4_parcel.add_sequence("Sequence1", 10, "accept")
        seq1.match_destination_data_prefix(IPv4Interface("10.0.0.0/16"))
        seq1.match_dscp([50, 55])
        seq1.match_icmp_msg(["dod-host-prohibited", "extended-echo", "dod-net-prohibited"])
        seq1.match_packet_length((1000, 8000))
        seq1.match_protocol([1])
        seq1.match_source_data_prefix(IPv4Interface("11.0.0.0/16"))
        # Arrange Sequence 2
        seq2 = acl_ipv4_parcel.add_sequence("Sequence2", 20, "drop")
        seq2.match_destination_data_prefix_variable("varDestPrefix2")
        seq2.match_source_data_prefix_variable("varSrcPrefix2")
        seq2.match_destination_ports([233])
        seq2.match_source_ports([1, 3, (10, 100), (50, 200), 600])
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, acl_ipv4_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_acl_ipv6_expect_successful_post(self):
        # Arrange
        acl_ipv6_parcel = Ipv6AclParcel(
            parcel_name="TestAclIpv6Parcel",
            parcel_description="Test Acl Ipv6 Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, acl_ipv6_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_acl_ipv6_expect_successful_post(self):
        # Arrange
        acl_ipv6_parcel = Ipv6AclParcel(
            parcel_name="TestAclIpv6Parcel-Full",
            parcel_description="Test Acl Ipv6 Parcel",
        )
        # Arrange Sequence 1
        seq1 = acl_ipv6_parcel.add_sequence("Sequence1", 10, "accept")
        seq1.match_destination_data_prefix(IPv6Interface("2001:db8:abcd:0012::/64"))
        seq1.match_icmp_msg(["cp-solicitation", "ind-advertisement"])
        seq1.match_packet_length((1000, 8000))
        seq1.match_source_data_prefix(IPv6Interface("2001:db8:1111:0012::/64"))
        seq1.match_traffic_class([3])
        # Arrange Sequence 2
        seq2 = acl_ipv6_parcel.add_sequence("Sequence2", 20, "drop")
        seq2.match_destination_ports([233])
        seq2.match_source_ports([1, 3, (10, 100), (50, 200), 600])
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, acl_ipv6_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_routing_bgp_expect_successful_post(self):
        # Arrange
        bgp_parcel = RoutingBgpParcel(
            parcel_name="TestRoutingBgpParcel",
            parcel_description="Description",
            as_num=Global[int](value=50),
            router_id=Global[IPv4Address](value=IPv4Address("192.0.0.4")),
            propagate_aspath=Global[bool](value=True),
            propagate_community=Global[bool](value=True),
            external=Global[int](value=255),
            internal=Global[int](value=255),
            local=Global[int](value=195),
            keepalive=Global[int](value=200),
            holdtime=Global[int](value=246),
            always_compare=Global[bool](value=True),
            deterministic=Global[bool](value=True),
            missing_as_worst=Global[bool](value=True),
            compare_router_id=Global[bool](value=False),
            multipath_relax=Global[bool](value=True),
            neighbor=[
                NeighborItem(
                    address=Global[IPv4Address](value=IPv4Address("192.175.48.31")),
                    description=Global[str](value="sJQwaemlk"),
                    shutdown=Global[bool](value=True),
                    remote_as=Global[int](value=330),
                    local_as=Global[int](value=409),
                    keepalive=Global[int](value=500),
                    holdtime=Global[int](value=204),
                    if_name=Variable(value="{{lbgp_1_ipv4_conf_1_updateSrcIntf}}"),
                    next_hop_self=Global[bool](value=True),
                    send_community=Global[bool](value=True),
                    send_ext_community=Global[bool](value=False),
                    ebgp_multihop=Global[int](value=147),
                    password=Global[str](value="Qzxpq"),
                    send_label=Global[bool](value=True),
                    as_override=Global[bool](value=False),
                    as_number=Variable(value="{{lbgp_1_ipv4_conf_1_asNumber}}"),
                    address_family=[
                        AddressFamilyItem(
                            family_type=Global[FamilyType](value="ipv4-unicast"),
                            max_prefix_config=MaxPrefixConfigRestart(
                                policy_type=Global[Literal["restart"]](value="restart"),
                                prefix_num=Global[int](value=11),
                                threshold=Global[int](value=10),
                                restart_interval=Global[int](value=10),
                            ),
                        ),
                    ],
                ),
            ],
            ipv6_neighbor=[
                Ipv6NeighborItem(
                    address=Global[IPv6Address](value=IPv6Address("f555:b620:61fc:798a:ece3:4364:58c3:8656")),
                    description=Global[str](value="VOBWPfHlS"),
                    shutdown=Global[bool](value=True),
                    remote_as=Global[int](value=20),
                    local_as=Global[int](value=479),
                    keepalive=Global[int](value=165),
                    holdtime=Global[int](value=147),
                    if_name=Variable(value="{{lbgp_1_ipv6_conf_1_updateSrcIntf}}"),
                    next_hop_self=Global[bool](value=True),
                    send_community=Global[bool](value=True),
                    send_ext_community=Global[bool](value=False),
                    ebgp_multihop=Global[int](value=21),
                    password=Global[str](value="vaPsP"),
                    as_override=Global[bool](value=True),
                    as_number=Global[int](value=10),
                    address_family=[
                        AddressFamilyItem(
                            family_type=Global[FamilyType](value="ipv6-unicast"),
                            max_prefix_config=MaxPrefixConfigRestart(
                                policy_type=Global[Literal["restart"]](value="restart"),
                                prefix_num=Global[int](value=11),
                                threshold=Global[int](value=10),
                                restart_interval=Global[int](value=10),
                            ),
                        ),
                    ],
                )
            ],
            address_family=BgpAddressFamily(
                name=Default[None](value=None),
                network=[
                    NetworkItem(
                        prefix=AddressWithMask(address=Variable(value="{{cYQ4ud15}}"), mask=Variable(value="{{LdKTD}}"))
                    )
                ],
                paths=Global[int](value=32),
                originate=Global[bool](value=True),
                filter=Global[bool](value=True),
                redistribute=[
                    RedistributeItem(
                        protocol=Global[Literal["static", "connected", "ospf", "ospfv3", "nat", "omp"]](value="ospf"),
                    )
                ],
            ),
            ipv6_address_family=Ipv6AddressFamily(
                ipv6_aggregate_address=[
                    Ipv6AggregateAddres(
                        prefix=Global[IPv6Interface](value=IPv6Interface("0::/16")),
                        as_set=Global[bool](value=True),
                        summary_only=Global[bool](value=False),
                    )
                ],
                ipv6_network=[
                    Ipv6NetworkItem(prefix=Global[IPv6Interface](value=IPv6Interface("2002::/16"))),
                ],
                paths=Global[int](value=2),
                originate=Global[bool](value=True),
                name=Default[None](value=None),
                filter=Global[bool](value=True),
                redistribute=[
                    Ipv6RedistributeItem(
                        protocol=Global[Literal["static", "connected", "ospf", "omp"]](value="connected"),
                        route_policy=Default[None](value=None),
                    )
                ],
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, bgp_parcel).id
        # Assert
        assert parcel_id

    def test_when_correct_values_switchport_parcel_expect_successful_post(self):
        # Arrange
        switchport_default_values_parcel = SwitchportParcel(
            parcel_name="TestSwitchportParcelDefaultValues",
            parcel_description="Test Switchport Parcel",
        )
        switchport_fully_specified_parcel = SwitchportParcel(
            parcel_name="TestSwitchportParcelFullySpecified",
            parcel_description="Test Switchport Parcel",
            age_time=Global[int](value=100),
            static_mac_address=[
                StaticMacAddress(
                    mac_address=as_global("00:00:00:00:00:00"),
                    vlan=Global[int](value=1),
                    interface_name=as_global("GigabitEthernet0/0/0"),
                )
            ],
            interface=[
                SwitchportInterface(
                    interface_name=as_global("GigabitEthernet0/0/0"),
                    mode=Global[SwitchportMode](value="access"),
                    shutdown=Global[bool](value=True),
                    speed=Global[Speed](value="10"),
                    duplex=Global[Duplex](value="full"),
                    switchport_access_vlan=Global[int](value=1),
                    switchport_trunk_allowed_vlans=Global[str](value="1-10"),
                    switchport_trunk_native_vlan=Global[int](value=1),
                    voice_vlan=Global[int](value=1),
                    host_mode=Global[HostMode](value="single-host"),
                    port_control=Global[PortControl](value="auto"),
                    control_direction=Global[ControlDirection](value="both"),
                    pae_enable=Global[bool](value=True),
                    guest_vlan=Global[int](value=1),
                    critical_vlan=Global[int](value=1),
                    enable_voice=Global[bool](value=True),
                )
            ],
        )
        switchport_parcels = [switchport_default_values_parcel, switchport_fully_specified_parcel]
        # Act
        for switchport_parcel in switchport_parcels:
            with self.subTest(switchport_parcel=switchport_parcel.parcel_name):
                parcel_id = self.api.create_parcel(self.profile_uuid, switchport_parcel).id
                # Assert
                assert parcel_id
                # Cleanup
                self.api.delete_parcel(self.profile_uuid, SwitchportParcel, parcel_id)

    def test_when_default_values_multicast_expect_successful_post(self):
        # Arrange
        multicast_parcel = MulticastParcel(
            parcel_name="TestMulticastParcel",
            parcel_description="Test Multicast Parcel",
            basic=MulticastBasicAttributes(),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, multicast_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_values_multicast_expect_successful_post(self):
        # Arrange
        multicast_parcel = MulticastParcel(
            parcel_name="TestMulticastParcel_FullySpecified",
            parcel_description="Test Multicast Parcel",
            basic=MulticastBasicAttributes(
                spt_only=as_global(True),
                local_config=LocalConfig(
                    local=as_global(True),
                    threshold=as_global(10),
                ),
            ),
            igmp=IgmpAttributes(
                interface=[
                    IgmpInterfaceParameters(
                        interface_name=as_global("GigabitEthernet0/0/0"),
                        version=as_global(2),
                        join_group=[
                            StaticJoin(
                                group_address=Global[IPv4Address](value=IPv4Address("239.255.255.255")),
                            )
                        ],
                    )
                ]
            ),
            pim=PimAttributes(
                ssm=SsmAttributes(ssm_range_config=SsmFlag(enable_ssm_flag=as_global(True), range=as_global("20"))),
                interface=[
                    PimInterfaceParameters(
                        interface_name=as_global("GigabitEthernet0/0/0"),
                        query_interval=as_global(10),
                        join_prune_interval=as_global(10),
                    )
                ],
                rp_address=[
                    StaticRpAddress(
                        address=Global[IPv4Address](value=IPv4Address("40.2.3.1")),
                        access_list=as_global("TestAccessList"),
                        override=as_global(True),
                    )
                ],
                auto_rp=AutoRpAttributes(
                    enable_auto_rp_flag=as_global(False),
                    send_rp_announce_list=[
                        RPAnnounce(interface_name=as_global("GigabitEthernet0/0/0"), scope=as_global(3))
                    ],
                    send_rp_discovery=[
                        RPAnnounce(interface_name=as_global("GigabitEthernet0/0/0"), scope=as_global(3))
                    ],
                ),
                pim_bsr=PimBsrAttributes(
                    rp_candidate=[
                        RpDiscoveryScope(
                            interface_name=as_global("GigabitEthernet0/0/0"),
                            group_list=as_global("TestGroupList"),
                            interval=as_global(10),
                            priority=as_global(10),
                        )
                    ],
                    bsr_candidate=[
                        BsrCandidateAttributes(
                            interface_name=as_global("GigabitEthernet0/0/0"),
                            mask=as_global(10),
                            priority=as_global(10),
                            accept_rp_candidate=as_global("True"),
                        )
                    ],
                ),
            ),
            msdp=MsdpAttributes(
                msdp_list=[
                    MsdpPeer(
                        mesh_group=as_global("TestMeshGroup"),
                        peer=[
                            MsdpPeerAttributes(
                                peer_ip=Global[IPv4Address](value=IPv4Address("5.5.5.5")),
                                connect_source_intf=as_global("GigabitEthernet0/0/0"),
                                remote_as=as_global(10),
                                password=as_global("TestPassword"),
                                keepalive_holdtime=as_global(20),
                                keepalive_interval=as_global(10),
                                sa_limit=as_global(10),
                            )
                        ],
                    )
                ]
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, multicast_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_values_wireless_lan_expect_successful_post(self):
        # Arrange
        wireless_lan_parcel = WirelessLanParcel(
            parcel_name="TestWirelessLanParcel",
            parcel_description="Test Wireless Lan Parcel",
            enable_2_4G=as_global(True),
            enable_5G=as_global(True),
            country=as_global("US", CountryCode),
            username=as_global("admin"),
            password=as_variable("{{wireless_lan_password}}"),
            ssid=[
                SSID(
                    name=as_global("TestSSID"),
                    admin_state=as_global(True),
                    vlan_id=as_global(1),
                    broadcast_ssid=as_global(True),
                    radio_type=as_global("all", RadioType),
                    qos_profile=as_global("platinum", QosProfile),
                    security_config=SecurityConfig(
                        security_type=as_global("enterprise", SecurityType),
                        radius_server_ip=as_global(IPv4Address("1.1.1.1")),
                        radius_server_port=as_global(1884),
                        radius_server_secret=as_global("23452345245"),
                    ),
                )
            ],
            me_ip_config=MeIpConfig(
                me_dynamic_ip_enabled=as_global(False),
                me_static_ip_config=MeStaticIpConfig(
                    me_ipv4_address=as_global(IPv4Address("10.2.3.2")),
                    netmask=as_global("255.255.255.0", SubnetMask),
                    default_gateway=as_global(IPv4Address("10.0.0.1")),
                ),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, wireless_lan_parcel).id
        # Assert
        assert parcel_id

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()


class TestServiceFeatureProfileVPNSubparcelModels(TestFeatureProfileModels):
    vpn_parcel_uuid: UUID

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.service
        cls.profile_uuid = cls.api.create_profile("TestProfileService", "Description").id
        cls.vpn_parcel_uuid = cls.api.create_parcel(
            cls.profile_uuid,
            LanVpnParcel(
                parcel_name="TestVpnParcel", parcel_description="Test Vpn Parcel", vpn_id=Global[int](value=2)
            ),
        ).id

    def test_when_default_values_gre_parcel_expect_successful_post(self):
        # Arrange
        gre_parcel = InterfaceGreParcel(
            parcel_name="TestGreParcel",
            parcel_description="Test Gre Parcel",
            basic=BasicGre(
                if_name=as_global("gre1"),
                address=AddressWithMask(
                    address=as_global("1.1.1.1"),
                    mask=as_global("255.255.255.0"),
                ),
                tunnel_destination=as_global(IPv4Address("4.4.4.4")),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, gre_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_default_values_svi_parcel_expect_successful_post(self):
        # Arrange
        svi_parcel = InterfaceSviParcel(
            parcel_name="TestSviParcel",
            parcel_description="Test Svi Parcel",
            interface_name=as_global("Vlan1"),
            svi_description=as_global("Test Svi Description"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, svi_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_default_values_ethernet_parcel_expect_successful_post(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcel",
            parcel_description="Test Ethernet Parcel",
            interface_name=as_global("HundredGigE"),
            ethernet_description=as_global("Test Ethernet Description"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_set_dynamic_interface_ip_address_for_ethernet_parcel(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcelSets",
            interface_name=as_global("HundredGigE"),
        )
        ethernet_parcel.set_dynamic_interface_ip_address(as_global(123))

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id

        # Assert
        assert parcel_id

    def test_set_dynamic_interface_ip_address_as_variable_for_ethernet_parcel(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcelVariable",
            interface_name=as_global("HundredGigE"),
        )
        ethernet_parcel.set_dynamic_interface_ip_address(as_variable("address"))

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id

        # Assert
        assert parcel_id

    def test_set_primary_static_interface_ip_address_for_ethernet_parcel(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcelPrimaryStaticOne",
            interface_name=as_global("HundredGigE"),
        )
        ethernet_parcel.set_static_primary_interface_ip_address(as_global("1.1.1.1"))

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id

        # Assert
        assert parcel_id

    def test_set_primary_static_interface_ip_address_as_variable_for_ethernet_parcel(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcelPrimaryStaticVariable",
            interface_name=as_global("HundredGigE"),
        )
        ethernet_parcel.set_static_primary_interface_ip_address(as_variable("address"))

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id

        # Assert
        assert parcel_id

    def test_set_primary_static_with_mask_interface_ip_address_for_ethernet_parcel(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcelPrimaryStaticMask",
            interface_name=as_global("HundredGigE"),
        )
        ethernet_parcel.set_static_primary_interface_ip_address(as_global("1.1.1.1"))
        ethernet_parcel.add_static_secondary_interface_ip_address(as_global("3.3.3.3"), as_global("255.255.255.128"))

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id

        # Assert
        assert parcel_id

    def test_set_primary_static_with_mask_interface_ip_address_as_varialbles_for_ethernet_parcel(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="TestEthernetParcelPrimaryStaticMaskVariable",
            interface_name=as_global("HundredGigE"),
        )
        ethernet_parcel.set_static_primary_interface_ip_address(as_variable("static_ip_address"))
        ethernet_parcel.add_static_secondary_interface_ip_address(
            as_variable("second_ip_address"), as_variable("second_mask")
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id

        # Assert
        assert parcel_id

    def test_when_default_values_ipsec_parcel_expect_successful_post(self):
        # Arrange
        ipsec_parcel = InterfaceIpsecParcel(
            parcel_name="TestIpsecParcel",
            parcel_description="Test Ipsec Parcel",
            interface_name=as_global("ipsec2"),
            ipsec_description=as_global("Test Ipsec Description"),
            pre_shared_secret=as_global("123"),
            ike_local_id=as_global("123"),
            ike_remote_id=as_global("123"),
            application=as_variable("{{ipsec_application}}"),
            tunnel_source_interface=as_variable("{{ipsec_ipsecSourceInterface}}"),
            address=AddressWithMask(address=as_global("10.0.0.1"), mask=as_global("255.255.255.0")),
            tunnel_destination=AddressWithMask(address=as_global("10.0.0.5"), mask=as_global("255.255.255.0")),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ipsec_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_routing_parcel_and_vpn_uuid_present_expect_create_then_assign_to_vpn(self):
        # Arrange
        multicast_parcel = MulticastParcel(
            parcel_name="TestMulticastParcel",
            parcel_description="Test Multicast Parcel",
            basic=MulticastBasicAttributes(),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, multicast_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_multilink_interface_parcel_expect_successful_post(self):
        nim_list = [
            MultilinkNimList(
                if_name=Global[str](value="Serial1"),
                bandwidth=Global[int](value=10),
                clock_rate=Global[ClockRate](value="1200"),
                description=Global[str](value="desc"),
            ),
            MultilinkNimList(
                if_name=Global[str](value="Serial2"),
                bandwidth=Global[int](value=12),
                clock_rate=Global[ClockRate](value="115200"),
                description=None,
            ),
        ]
        controller_tx_ex_list = [
            MultilinkControllerTxExList(
                channel_group=[
                    ChannelGroup(
                        number=Global[int](value=12),
                        timeslots=Global[str](value="12"),
                    )
                ],
                number=Global[str](value="1/1/1"),
                clock_source=Global[MultilinkClockSource](value="internal"),
                description=Global[str](value="desc"),
                e1_framing=Global[E1Framing](value="crc4"),
                e1_linecode=Global[E1Linecode](value="ami"),
                line_mode=Global[LineMode](value="primary"),
                long=None,
                name=Global[MultilinkTxExName](value="E1"),
                short=None,
                t1_framing=None,
                t1_linecode=None,
            ),
            MultilinkControllerTxExList(
                channel_group=[
                    ChannelGroup(
                        number=Global[int](value=13),
                        timeslots=Global[str](value="13"),
                    )
                ],
                number=Global[str](value="2/2/2"),
                clock_source=Global[MultilinkClockSource](value="loop-timed"),
                description=Global[str](value="desc"),
                e1_framing=None,
                e1_linecode=None,
                line_mode=Global[LineMode](value="secondary"),
                long=Global[CableLengthLongValue](value="-15db"),
                name=Global[MultilinkTxExName](value="T1"),
                short=None,
                t1_framing=Global[T1Framing](value="esf"),
                t1_linecode=Global[T1Linecode](value="ami"),
            ),
        ]

        multilink_parcel = InterfaceMultilinkParcel(
            parcel_name="Test",
            parcel_description="Description",
            group_number=Global[int](value=299),
            if_name=Global[str](value="Multilink1"),
            method=Global[Literal[MultilinkMethod]](value="CHAP"),
            address_ipv4=Global[IPv4Address](value=IPv4Address("192.175.48.4")),
            address_ipv6=Global[IPv6Interface](value=IPv6Interface("::3e46/100")),
            authentication_type=Default[Literal[MultilinkAuthenticationType]](value="unidirectional"),
            bandwidth_upstream=Global[int](value=21),
            clear_dont_fragment_sdwan_tunnel=Global[bool](value=True),
            control_connections=Global[bool](value=False),
            controller_tx_ex_list=controller_tx_ex_list,
            controller_type=Global[Literal[MultilinkControllerType]](value="T1/E1"),
            delay_value=Global[int](value=99),
            disable=Global[bool](value=True),
            hostname=Global[str](value="oitSeZBfw"),
            interleave=Global[bool](value=False),
            ip_directed_broadcast=Global[bool](value=True),
            ipv4_acl_egress=None,
            ipv4_acl_ingress=None,
            ipv6_acl_egress=None,
            ipv6_acl_ingress=None,
            mask_ipv4=Global[SubnetMask](value="255.255.255.254"),
            mtu=Global[int](value=5266),
            nim_list=nim_list,
            password=Global[str](value="hyBBiuDgO"),
            ppp_auth_password=Global[str](value="aCBBBxnzsw"),
            shaping_rate=Global[int](value=294),
            shutdown=Global[bool](value=False),
            tcp_mss_adjust=Global[int](value=1267),
            tloc_extension=Global[str](value="ATM"),
            username_string=Global[str](value="ONBBAAB"),
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, multilink_parcel, self.vpn_parcel_uuid).id

        assert parcel_id

    def test_when_default_values_ethernet_interface_expect_successful_post(self):
        # For 20.13 when we send "advanced.intfruMtu" as Default 1500
        # endpoint returns 400
        # catalystwan.exceptions.ManagerHTTPError:
        # message='Invalid Payload'
        # details="Invalid Payload: doesn't support user settable interface mtu for sub interface"
        # code='PPARC0012'

        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            name="vedge-C8000V_interface_*GigabitEthernet3.2*_FT_84.xml",
            description="interface_Description",
            interface_name=as_global("GigabitEthernet3.2"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.vpn_parcel_uuid).id
        # Assert
        assert parcel_id

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
