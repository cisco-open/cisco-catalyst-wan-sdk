# Copyright 2023 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import List, Literal
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_global
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.integration_tests.test_data import cellular_controller_parcel, cellular_profile_parcel, gps_parcel
from catalystwan.models.common import (
    CableLengthLongValue,
    CarrierType,
    ClockRate,
    CoreRegion,
    E1Framing,
    E1Linecode,
    EncapType,
    EthernetDuplexMode,
    IkeCiphersuite,
    IkeGroup,
    IpsecCiphersuite,
    LineMode,
    SecondaryRegion,
    T1Framing,
    T1Linecode,
    TLOCColor,
)
from catalystwan.models.configuration.feature_profile.common import AclQos
from catalystwan.models.configuration.feature_profile.common import AddressWithMask
from catalystwan.models.configuration.feature_profile.common import AddressWithMask as CommonPrefix
from catalystwan.models.configuration.feature_profile.common import AdvancedGre, AllowService
from catalystwan.models.configuration.feature_profile.common import Arp as CommonArp
from catalystwan.models.configuration.feature_profile.common import ChannelGroup, DNSIPv4, DNSIPv6
from catalystwan.models.configuration.feature_profile.common import (
    EthernetNatAttributesIpv4 as EthernetNatAttributesIpv4,
)
from catalystwan.models.configuration.feature_profile.common import (
    HostMapping,
    InterfaceStaticIPv4Address,
    MultilinkAuthenticationType,
    MultilinkClockSource,
    MultilinkControllerTxExList,
    MultilinkControllerType,
    MultilinkMethod,
    MultilinkNimList,
    MultilinkTxExName,
    MultiRegionFabric,
    ShapingRateDownstreamConfig,
    ShapingRateUpstreamConfig,
    SourceLoopback,
    StaticIPv4Address,
    StaticIPv4AddressConfig,
    StaticNat,
    TunnelSourceType,
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
from catalystwan.models.configuration.feature_profile.sdwan.transport.management.ethernet import (
    Advanced as ManagementEthernetAdvanced,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.management.ethernet import (
    InterfaceEthernetParcel as ManagementEthernetParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.management.ethernet import (
    InterfaceStaticIPv6Address,
    StaticIPv6Address,
    StaticIPv6AddressConfig,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.t1e1controller import (
    E1,
    T1,
    CableLengthLong,
    ClockSource,
    ControllerTxExList,
    ControllerType,
    E1Basic,
    Long,
    T1Basic,
    T1E1ControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import (
    Address64V4PoolItem,
    Ipv4RouteItem,
    Ipv6RouteItem,
    ManagementVpnParcel,
    NextHopItem,
    OneOfIpRouteNull0,
    Prefix,
    ServiceItem,
    ServiceType,
    SubnetMask,
    TransportVpnParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    Advanced as AdvancedCellular,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    Arp,
    InterfaceCellularParcel,
    NatAttributesIpv4,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.cellular import (
    Tunnel as TunnelCellular,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    Advanced as EthernetAdvanced,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    InterfaceEthernetParcel,
    NatAttributesIpv6,
    StaticNat66,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ethernet import (
    Tunnel as TunnelEthernet,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.gre import Basic, InterfaceGreParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.ipsec import (
    InterfaceIpsecParcel,
    PerfectForwardSecrecy,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.multilink import (
    InterfaceMultilinkParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    AclQos as AclQosPPPoE,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    Advanced as AdvancedPPPoE,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    AtmInterface,
    Chap,
    Dynamic,
    DynamicIntfIpAddress,
    Ethernet,
    InterfaceDslIPoEParcel,
    InterfaceDslPPPoAParcel,
    InterfaceDslPPPoEParcel,
    InterfaceEthPPPoEParcel,
    IPoEEthernet,
    NatProp,
    Pap,
    Ppp,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    Tunnel as TunnelPPPoE,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.protocol_over import (
    TunnelAdvancedOption,
    VbrNrtConfig,
    VbrRtConfig,
    Vdsl,
    VdslMode,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.t1e1serial import (
    Advanced,
    Encapsulation,
    T1E1SerialParcel,
    Tunnel,
)


class TestTransportFeatureProfileModels(TestFeatureProfileModels):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile("TestTransportService", "Description").id

    def test_when_fully_specified_management_vpn_parcel_expect_successful_post(self):
        # Arrange
        management_vpn_parcel = ManagementVpnParcel(
            parcel_name="FullySpecifiedManagementVpnParcel",
            description="Description",
            dns_ipv6=DNSIPv6(
                primary_dns_address_ipv6=as_global(IPv6Address("67ca:c2df:edfe:c8ec:b6cb:f9f4:eab0:ece6")),
                secondary_dns_address_ipv6=as_global(IPv6Address("8989:8d33:c00a:4d13:324d:8b23:8d77:a289")),
            ),
            dns_ipv4=DNSIPv4(
                primary_dns_address_ipv4=as_global(IPv4Address("68.138.29.222")),
                secondary_dns_address_ipv4=as_global(IPv4Address("122.89.114.112")),
            ),
            new_host_mapping=[
                HostMapping(
                    host_name=as_global("FullySpecifiedHost"),
                    list_of_ips=as_global(
                        [
                            "165.16.181.116",
                            "7a4c:1d87:8587:a6ec:21a6:48a7:00e8:1fef",
                        ]
                    ),
                )
            ],
            ipv6_route=[
                Ipv6RouteItem(
                    prefix=as_global(IPv6Interface("0::/16")),
                    one_of_ip_route=OneOfIpRouteNull0(),
                )
            ],
            ipv4_route=[
                Ipv4RouteItem(
                    prefix=Prefix(
                        ip_address=as_global(IPv4Address("202.153.165.234")),
                        subnet_mask=as_global("255.255.255.0", SubnetMask),
                    ),
                    next_hop=[
                        NextHopItem(
                            address=as_global(IPv4Address("1.1.1.1")),
                        )
                    ],
                )
            ],
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, management_vpn_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_t1e1controller_type_e1_parcel_expect_successful_post(self):
        # Arrange
        t1e1controller = T1E1ControllerParcel(
            parcel_name="FullySpecifiedT1E1ControllerParcel_type_e1",
            description="Description",
            type=as_global("e1", ControllerType),
            slot=as_global("TypeEOne"),
            controller_tx_ex_list=[
                ControllerTxExList(
                    basic=E1Basic(
                        e1=E1(
                            framing=as_global("crc4", E1Framing),
                            linecode=as_global("ami", E1Linecode),
                        )
                    ),
                    channel_group=[
                        ChannelGroup(
                            number=as_global(12),
                            timeslots=as_global("1"),
                        )
                    ],
                    clock_source=as_global("internal", ClockSource),
                    description=as_global("FullySpecifiedDescription"),
                    line_mode=as_global("primary", LineMode),
                )
            ],
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, t1e1controller).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_t1e1controller_type_t1_parcel_expect_successful_post(self):
        # Arrange
        t1e1controller = T1E1ControllerParcel(
            parcel_name="FullySpecifiedT1E1ControllerParcel_type_t1",
            description="Description",
            type=as_global("t1", ControllerType),
            slot=as_global("TypeTOne"),
            controller_tx_ex_list=[
                ControllerTxExList(
                    basic=T1Basic(
                        t1=T1(
                            framing=as_global("esf", T1Framing),
                            linecode=as_global("b8zs", T1Linecode),
                        )
                    ),
                    cable=CableLengthLong(
                        cable_length=as_global("long", Long),
                        length_long=as_global("-15db", CableLengthLongValue),
                    ),
                    channel_group=[
                        ChannelGroup(
                            number=as_global(12),
                            timeslots=as_global("1"),
                        )
                    ],
                    clock_source=as_global("internal", ClockSource),
                    description=as_global("FullySpecifiedDescription"),
                    line_mode=as_global("primary", LineMode),
                )
            ],
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, t1e1controller).id
        # Assert
        assert parcel_id

    def test_when_fully_specifed_gps_parcel_expect_successful_post(self):
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, gps_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specifed_cellular_controller_expect_successful_post(self):
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, cellular_controller_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specifed_cellular_profile_expect_successful_post(self):
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, cellular_profile_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_acl_ipv4_expect_successful_post(self):
        # Arrange
        acl_ipv4_parcel = Ipv4AclParcel(
            parcel_name="TestAclIpv4Parcel-Defaults",
            parcel_description="Test Acl Ipv4 Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, acl_ipv4_parcel).id
        self.api.get_parcel(self.profile_uuid, Ipv4AclParcel, parcel_id)
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
        self.api.get_parcel(self.profile_uuid, Ipv4AclParcel, parcel_id)
        # Assert
        assert parcel_id

    def test_when_default_values_acl_ipv6_expect_successful_post(self):
        # Arrange
        acl_ipv6_parcel = Ipv6AclParcel(
            parcel_name="TestAclIpv6Parcel-Defaults",
            parcel_description="Test Acl Ipv6 Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, acl_ipv6_parcel).id
        self.api.get_parcel(self.profile_uuid, Ipv6AclParcel, parcel_id)
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
        self.api.get_parcel(self.profile_uuid, Ipv6AclParcel, parcel_id)
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()


class TestTransportFeatureProfileTransportVpn(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.transport
        self.profile_uuid = self.api.create_profile("TestProfileService", "Description").id
        self.config_id = self.session.api.config_group.create(
            "TestConfigGroupTransport", "Descr", "sdwan", [self.profile_uuid]
        ).id

    def test_when_minimal_specifed_transport_vpn_parcel_expect_successful_post(self):
        # Arrange
        transport_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, transport_vpn_parcel).id
        # Assert
        assert parcel_id

    def test_when_set_dns_address_specifed_transport_vpn_parcel_expect_successful_post(self):
        # Arrange
        transport_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        # Act
        transport_vpn_parcel.set_dns_ipv4(as_global(IPv4Address("1.1.1.1")), as_global(IPv4Address("2.2.2.2")))

        parcel_id = self.api.create_parcel(self.profile_uuid, transport_vpn_parcel).id
        # Assert
        assert parcel_id

    def test_when_add_ipv4_route_specifed_transport_vpn_parcel_expect_successful_post(self):
        # Arrange
        transport_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        # Act
        next_hops = [
            (as_global(IPv4Address("2.2.2.2")), as_global(1)),
            (as_global(IPv4Address("3.3.3.3")), as_global(8)),
            (as_global(IPv4Address("4.4.4.4")), as_global(10)),
        ]
        transport_vpn_parcel.add_ipv4_route(
            as_global(IPv4Address("1.1.1.1")), as_global("255.255.255.255", SubnetMask), next_hops
        )
        parcel_id = self.api.create_parcel(self.profile_uuid, transport_vpn_parcel).id

        # Assert
        assert parcel_id

    def test_when_fully_specifed_transport_vpn_parcel_expect_successful_post(self):
        # Arrange
        transport_vpn_parcel = TransportVpnParcel(
            parcel_name="FullySpecifiedTransportVpnParcel",
            description="Description",
            dns_ipv6=DNSIPv6(
                primary_dns_address_ipv6=as_global(IPv6Address("67ca:c2df:edfe:c8ec:b6cb:f9f4:eab0:ece6")),
                secondary_dns_address_ipv6=as_global(IPv6Address("8989:8d33:c00a:4d13:324d:8b23:8d77:a289")),
            ),
            dns_ipv4=DNSIPv4(
                primary_dns_address_ipv4=as_global(IPv4Address("68.138.29.222")),
                secondary_dns_address_ipv4=as_global(IPv4Address("122.89.114.112")),
            ),
            new_host_mapping=[
                HostMapping(
                    host_name=as_global("FullySpecifiedHost"),
                    list_of_ips=as_global(
                        [
                            "165.16.181.116",
                            "7a4c:1d87:8587:a6ec:21a6:48a7:00e8:1fef",
                        ]
                    ),
                )
            ],
            ipv6_route=[
                Ipv6RouteItem(
                    prefix=as_global(IPv6Interface("0::/16")),
                    one_of_ip_route=OneOfIpRouteNull0(),
                )
            ],
            ipv4_route=[
                Ipv4RouteItem(
                    prefix=Prefix(
                        ip_address=as_global(IPv4Address("202.153.165.234")),
                        subnet_mask=as_global("255.255.255.0", SubnetMask),
                    ),
                    next_hop=[NextHopItem(address=as_global(IPv4Address("1.1.1.1")), distance=as_global(8))],
                )
            ],
            service=[ServiceItem(service_type=as_global("TE", ServiceType))],
            nat64_v4_pool=[
                Address64V4PoolItem(
                    name=as_global("FullySpecifiedNat64V4Pool"),
                    range_start=as_global(IPv4Address("3.3.3.3")),
                    range_end=as_global(IPv4Address("3.3.3.7")),
                    overload=as_global(True),
                )
            ],
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, transport_vpn_parcel).id
        # Assert
        assert parcel_id

    def tearDown(self) -> None:
        self.session.api.config_group.delete(self.config_id)
        self.api.delete_profile(self.profile_uuid)


class TestTransportFeatureProfileWanInterfaceModels(TestFeatureProfileModels):
    wan_uuid: UUID

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile("TestTransportService", "Description").id
        cls.wan_uuid = cls.api.create_parcel(
            cls.profile_uuid,
            TransportVpnParcel(
                parcel_name="TestTransportVpnParcel",
                parcel_description="Description",
            ),
        ).id

    def test_when_fully_specified_t1e1serial_interface_parcel_expect_successfull_post(self):
        # Arrange
        t1e1serial = T1E1SerialParcel(
            parcel_name="T1E1FullySpecifiedParcel",
            parcel_description="Description",
            interface_name=Global[str](value="Serial3"),
            address_v4=CommonPrefix(address=Global[str](value="1.1.1.1"), mask=Variable(value="{{NQokHq}}")),
            address_v6=Variable(value="{{i4i}}"),
            advanced=Advanced(
                ip_mtu=Global[int](value=1500),
                mtu=Global[int](value=1500),
                tcp_mss_adjust=Variable(value="{{f}}"),
                tloc_extension=Global[str](value="322"),
            ),
            allow_service=AllowService(
                bfd=Variable(value="{{GfwsBdVoSy7O8ABos}}"),
                bgp=Global[bool](value=True),
                dhcp=Global[bool](value=False),
                dns=Variable(value="{{3so}}"),
                https=Global[bool](value=True),
                icmp=Variable(value="{{n2Qz.wW}}"),
                netconf=Variable(value="{{0}}"),
                ntp=Global[bool](value=True),
                ospf=Global[bool](value=True),
                snmp=Global[bool](value=False),
                sshd=Variable(value="{{56lx}}"),
                stun=Global[bool](value=True),
            ),
            bandwidth=Variable(value="{{w}}"),
            bandwidth_downstream=Global[int](value=34),
            clock_rate=Variable(value="{{9_h.ePd}}"),
            encapsulation=[
                Encapsulation(
                    encap=Global[EncapType](value="gre"),
                    preference=Variable(value="{{I9]LwyD45eQIry]Z}}"),
                    weight=Global[int](value=32),
                ),
                Encapsulation(
                    encap=Global[EncapType](value="ipsec"),
                    preference=Variable(value="{{I9]LwyD45eQIry]Z}}"),
                    weight=Global[int](value=2),
                ),
                Encapsulation(
                    encap=Global[EncapType](value="gre"),
                    preference=Default[None](value=None),
                    weight=Global[int](value=112),
                ),
            ],
            encapsulation_serial=Variable(value="{{A8/8w4Qr}}"),
            multi_region_fabric=MultiRegionFabric(
                core_region=Global[CoreRegion](value="core-shared"),
                enable_core_region=Global[bool](value=False),
                enable_secondary_region=Global[bool](value=True),
                secondary_region=Global[SecondaryRegion](value="secondary-shared"),
            ),
            shutdown=Global[bool](value=True),
            tunnel=Tunnel(
                bind=Global[str](value="3123"),
                border=Variable(value="{{k0Ci4g}}"),
                carrier=Variable(value="{{SyMR13Poi}}"),
                clear_dont_fragment=Global[bool](value=False),
                color=Variable(value="{{ivc}}"),
                exclude_controller_group_list=Variable(value="{{z][Ih}}"),
                group=Variable(value="{{WlfX}}"),
                hello_interval=Global[int](value=1000),
                hello_tolerance=Global[int](value=123),
                last_resort_circuit=Global[bool](value=True),
                low_bandwidth_link=Global[bool](value=True),
                max_control_connections=Global[int](value=0),
                mode=Global[Literal["spoke"]](value="spoke"),
                nat_refresh_interval=Global[int](value=3),
                network_broadcast=Global[bool](value=True),
                per_tunnel_qos=Global[bool](value=True),
                per_tunnel_qos_aggregator=Global[bool](value=True),
                port_hop=Global[bool](value=True),
                restrict=Global[bool](value=True),
                vbond_as_stun_server=Global[bool](value=True),
                vmanage_connection_preference=Global[int](value=3),
            ),
            tunnel_interface=Global[bool](value=True),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, t1e1serial, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_ethpppoe_interface_parcel_expect_successfull_post(self):
        # Arrange
        ethpppoe_parcel = InterfaceEthPPPoEParcel(
            parcel_name="InterfaceEthPPPoEParcel",
            parcel_description="Description",
            acl_qos=AclQosPPPoE(
                adapt_period=Global[int](value=436),
                adaptive_qos=Global[bool](value=True),
                shaping_rate=Global[int](value=295),
                shaping_rate_downstream=Global[bool](value=False),
                shaping_rate_downstream_config=ShapingRateDownstreamConfig(
                    default_shaping_rate_downstream=Global[int](value=500),
                    max_shaping_rate_downstream=Global[int](value=77),
                    min_shaping_rate_downstream=Global[int](value=328),
                ),
                shaping_rate_upstream=Global[bool](value=True),
                shaping_rate_upstream_config=ShapingRateUpstreamConfig(
                    default_shaping_rate_upstream=Global[int](value=403),
                    max_shaping_rate_upstream=Global[int](value=82),
                    min_shaping_rate_upstream=Global[int](value=101),
                ),
            ),
            advanced=AdvancedPPPoE(
                ip_directed_broadcast=Global[bool](value=True),
                ip_mtu=Global[int](value=1500),
                tcp_mss=Global[int](value=560),
                tloc_extension=Global[str](value="FBVQf"),
            ),
            bandwidth_downstream=Global[int](value=102),
            bandwidth_upstream=Global[int](value=267),
            ethernet=Ethernet(
                if_name=Global[str](value="Ethernet1"),
                description=Global[str](value="ABAAABB"),
                vlan_id=Global[int](value=266),
            ),
            multi_region_fabric=MultiRegionFabric(
                core_region=Global[Literal["core", "core-shared"]](value="core"),
                enable_core_region=Global[bool](value=True),
            ),
            nat_prop=NatProp(
                nat=Global[bool](value=True), tcp_timeout=Global[int](value=301), udp_timeout=Global[int](value=11)
            ),
            ppp=Ppp(
                dial_pool_number=Global[int](value=2),
                method=Global[Literal["chap", "pap", "papandchap"]](value="chap"),
                callin=Global[Literal["Bidirectional", "Unidirectional"]](value="Bidirectional"),
                chap=Chap(hostname=Global[str](value="BBXwBBB"), ppp_auth_password=Global[str](value="BRyKDwlPkn")),
                pap=Pap(ppp_auth_password=Global[str](value="sAZWrMiNhD"), username=Global[str](value="BAAAAOZNQI")),
                ppp_max_payload=Global[int](value=276),
            ),
            service_provider=Global[str](value="MaBNDCAFdb"),
            shutdown=Global[bool](value=True),
            tunnel=TunnelPPPoE(
                bandwidth_percent=Global[int](value=43),
                border=Global[bool](value=False),
                clear_dont_fragment=Global[bool](value=False),
                color=Global[TLOCColor](value="private5"),
                low_bandwidth_link=Global[bool](value=False),
                max_control_connections=Global[int](value=5),
                mode=Global[Literal["hub", "spoke"]](value="hub"),
                network_broadcast=Global[bool](value=True),
                per_tunnel_qos=Global[bool](value=True),
                port_hop=Global[bool](value=False),
                restrict=Global[bool](value=True),
                tunnel_interface=Global[bool](value=True),
                tunnel_tcp_mss_adjust=Global[int](value=600),
                vbond_as_stun_server=Global[bool](value=True),
                vmanage_connection_preference=Global[int](value=2),
            ),
            tunnel_advanced_option=TunnelAdvancedOption(
                bind=Global[str](value="BAAREAA"),
                carrier=Global[CarrierType](value="carrier8"),
                gre_encap=Global[bool](value=True),
                gre_preference=Global[int](value=266),
                gre_weight=Global[int](value=11),
                hello_interval=Global[int](value=329),
                hello_tolerance=Global[int](value=373),
                ipsec_encap=Global[bool](value=True),
                ipsec_preference=Global[int](value=163),
                ipsec_weight=Global[int](value=244),
                last_resort_circuit=Global[bool](value=False),
                nat_refresh_interval=Global[int](value=30),
            ),
            tunnel_allow_service=AllowService(
                all=Global[bool](value=False),
                bgp=Global[bool](value=False),
                dhcp=Global[bool](value=False),
                dns=Global[bool](value=False),
                https=Global[bool](value=True),
                icmp=Global[bool](value=False),
                netconf=Global[bool](value=True),
                ntp=Global[bool](value=False),
                ospf=Global[bool](value=False),
                snmp=Global[bool](value=False),
                sshd=Global[bool](value=False),
                stun=Global[bool](value=False),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ethpppoe_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_dslpppoe_interface_parcel_expect_successfull_post(self):
        # Arrange
        ethpppoe_parcel = InterfaceDslPPPoEParcel(
            parcel_name="InterfaceDslPPPoEParcel",
            parcel_description="Description",
            acl_qos=AclQosPPPoE(
                adapt_period=Global[int](value=436),
                adaptive_qos=Global[bool](value=True),
                shaping_rate=Global[int](value=295),
                shaping_rate_downstream=Global[bool](value=False),
                shaping_rate_downstream_config=ShapingRateDownstreamConfig(
                    default_shaping_rate_downstream=Global[int](value=500),
                    max_shaping_rate_downstream=Global[int](value=77),
                    min_shaping_rate_downstream=Global[int](value=328),
                ),
                shaping_rate_upstream=Global[bool](value=True),
                shaping_rate_upstream_config=ShapingRateUpstreamConfig(
                    default_shaping_rate_upstream=Global[int](value=403),
                    max_shaping_rate_upstream=Global[int](value=82),
                    min_shaping_rate_upstream=Global[int](value=101),
                ),
            ),
            advanced=AdvancedPPPoE(
                ip_directed_broadcast=Global[bool](value=True),
                ip_mtu=Global[int](value=1500),
                tcp_mss=Global[int](value=560),
                tloc_extension=Global[str](value="FBVQf"),
            ),
            bandwidth_downstream=Global[int](value=102),
            bandwidth_upstream=Global[int](value=267),
            ethernet=Ethernet(
                if_name=Global[str](value="Ethernet1"),
                description=Global[str](value="ABAAABB"),
                vlan_id=Global[int](value=266),
            ),
            multi_region_fabric=MultiRegionFabric(
                core_region=Global[Literal["core", "core-shared"]](value="core"),
                enable_core_region=Global[bool](value=True),
            ),
            nat_prop=NatProp(
                nat=Global[bool](value=True), tcp_timeout=Global[int](value=301), udp_timeout=Global[int](value=11)
            ),
            ppp=Ppp(
                dial_pool_number=Global[int](value=2),
                method=Global[Literal["chap", "pap", "papandchap"]](value="chap"),
                callin=Global[Literal["Bidirectional", "Unidirectional"]](value="Bidirectional"),
                chap=Chap(hostname=Global[str](value="BBXwBBB"), ppp_auth_password=Global[str](value="BRyKDwlPkn")),
                pap=Pap(ppp_auth_password=Global[str](value="sAZWrMiNhD"), username=Global[str](value="BAAAAOZNQI")),
                ppp_max_payload=Global[int](value=276),
            ),
            service_provider=Global[str](value="MaBNDCAFdb"),
            shutdown=Global[bool](value=True),
            tunnel=TunnelPPPoE(
                bandwidth_percent=Global[int](value=43),
                border=Global[bool](value=False),
                clear_dont_fragment=Global[bool](value=False),
                color=Global[TLOCColor](value="private5"),
                low_bandwidth_link=Global[bool](value=False),
                max_control_connections=Global[int](value=5),
                mode=Global[Literal["hub", "spoke"]](value="hub"),
                network_broadcast=Global[bool](value=True),
                per_tunnel_qos=Global[bool](value=True),
                port_hop=Global[bool](value=False),
                restrict=Global[bool](value=True),
                tunnel_interface=Global[bool](value=True),
                tunnel_tcp_mss_adjust=Global[int](value=600),
                vbond_as_stun_server=Global[bool](value=True),
                vmanage_connection_preference=Global[int](value=2),
            ),
            tunnel_advanced_option=TunnelAdvancedOption(
                bind=Global[str](value="BAAREAA"),
                carrier=Global[CarrierType](value="carrier8"),
                gre_encap=Global[bool](value=True),
                gre_preference=Global[int](value=266),
                gre_weight=Global[int](value=11),
                hello_interval=Global[int](value=329),
                hello_tolerance=Global[int](value=373),
                ipsec_encap=Global[bool](value=True),
                ipsec_preference=Global[int](value=163),
                ipsec_weight=Global[int](value=244),
                last_resort_circuit=Global[bool](value=False),
                nat_refresh_interval=Global[int](value=30),
            ),
            tunnel_allow_service=AllowService(
                all=Global[bool](value=False),
                bgp=Global[bool](value=False),
                dhcp=Global[bool](value=False),
                dns=Global[bool](value=False),
                icmp=Global[bool](value=False),
                netconf=Global[bool](value=True),
                ntp=Global[bool](value=False),
                ospf=Global[bool](value=False),
                snmp=Global[bool](value=False),
                sshd=Global[bool](value=False),
                stun=Global[bool](value=False),
            ),
            vdsl=Vdsl(
                slot=Variable(value="{{GfwsBdVoSy7O8ABos}}"),
                mode=Global[VdslMode](value="ADSL1"),
                sra=Global[bool](value=True),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ethpppoe_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_correct_values_dlspppoa_interface_parcel_expect_successfull_post(self):
        """This test case don't cover all fields because the models
        inherets from the same parent class as DslPPPoE and EthPPPoE"""
        # Arrange
        dslpppoa_parcel = InterfaceDslPPPoAParcel(
            parcel_name="InterfaceDslPPPoAParcel",
            parcel_description="Description",
            atm_interface=AtmInterface(
                if_name=Global[str](value="ATM123213/0/0"),
                local_vpi_vci=Variable(value="{{[[[[}}"),
                description=Global[str](value="mkMuCZMEWq"),
                encapsulation=Default[Literal["AAL5MUX"]](value="AAL5MUX"),
                vbr_nrt_config=VbrNrtConfig(
                    burst_cell_size=Variable(value="{{GO}}"),
                    p_c_r=Variable(value="{{JIvj5lr}}"),
                    s_c_r=Variable(value="{{jn0LmZq8o4C}}"),
                ),
                vbr_rt_config=VbrRtConfig(
                    a_c_r=Variable(value="{{x}}"), burst_cell_size=Variable(value="{{G}}"), p_c_r=Global[int](value=481)
                ),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, dslpppoa_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_correct_values_dlsipoe_interface_parcel_expect_successfull_post(self):
        """This test case don't cover all fields because the models
        inherets from the same parent class as DslPPPoE and EthPPPoE"""
        # Arrange
        dslipoe_parcel = InterfaceDslIPoEParcel(
            parcel_name="InterfaceDslIPoEParcel",
            parcel_description="Description",
            ethernet=IPoEEthernet(
                if_name=Global[str](value="Ethernet3"),
                description=Global[str](value="ABAAABB"),
                vlan_id=Global[int](value=266),
                intf_ip_address=DynamicIntfIpAddress(
                    dynamic=Dynamic(
                        dhcp_helper=Global[str](value="1.1.1.1"),
                        dynamic_dhcp_distance=Global[int](value=3),
                    )
                ),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, dslipoe_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_gre_interface_parcel_expect_successful_post(self):
        # Arrange
        gre_parcel = InterfaceGreParcel(
            parcel_name="InterfaceGreParcel",
            parcel_description="Description",
            basic=Basic(
                address=CommonPrefix(
                    address=Global[IPv4Address](value=IPv4Address("39.5.0.97")),
                    mask=Variable(value="{{QPg11165441vY1}}"),
                ),
                if_name=Global[str](value="gre23"),
                tunnel_destination=Global[IPv4Address](value=IPv4Address("3.3.3.3")),
                clear_dont_fragment=Global[bool](value=True),
                description=Global[str](value="QsLBBBBBCF"),
                mtu=Global[int](value=1500),
                shutdown=Global[bool](value=True),
                tcp_mss_adjust=Global[int](value=600),
                tunnel_source_type=TunnelSourceType(
                    source_loopback=SourceLoopback(
                        tunnel_route_via=Global[str](value="xSVIxuF"),
                        tunnel_source_interface=Global[str](value="YnBabgxBUm"),
                    )
                ),
            ),
            advanced=AdvancedGre(application=Global[Literal["none", "sig"]](value="sig")),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, gre_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_ipsec_interface_parcel_expect_successful_post(self):
        ipsec_parcel = InterfaceIpsecParcel(
            parcel_name="InterfaceIpsecParcel",
            parcel_description="Description",
            address=CommonPrefix(
                address=Global[IPv4Address](value=IPv4Address("127.211.176.149")),
                mask=Global[SubnetMask](value="255.255.255.0"),
            ),
            application=Global[Literal["none", "sig"]](value="none"),
            clear_dont_fragment=Global[bool](value=False),
            if_description=Default[None](value=None),
            dpd_interval=Default[int](value=10),
            dpd_retries=Default[int](value=3),
            if_name=Global[str](value="ipsec232"),
            ike_ciphersuite=Global[IkeCiphersuite](value="aes256-cbc-sha1"),
            ike_group=Global[IkeGroup](value="16"),
            ike_local_id=Global[str](value="TZilY"),
            ike_rekey_interval=Default[int](value=14400),
            ike_remote_id=Default[None](value=None),
            ike_version=Default[int](value=1),
            ipsec_ciphersuite=Global[IpsecCiphersuite](value="aes256-gcm"),
            ipsec_rekey_interval=Default[int](value=3600),
            ipsec_replay_window=Default[int](value=512),
            mtu=Default[int](value=1500),
            perfect_forward_secrecy=Global[PerfectForwardSecrecy](value="group-16"),
            pre_shared_secret=Global[str](value="iEKeBeVb"),
            shutdown=Default[bool](value=True),
            tcp_mss_adjust=Default[None](value=None),
            tunnel_destination=CommonPrefix(
                address=Global[IPv4Address](value=IPv4Address("192.0.0.171")), mask=Variable(value="{{Dr}}")
            ),
            tunnel_source=CommonPrefix(
                address=Global[IPv4Address](value=IPv4Address("192.52.193.221")),
                mask=Global[SubnetMask](value="255.255.254.0"),
            ),
            ike_mode=Global[Literal["main", "aggresive"]](value="main"),
            tracker=Global[str](value="AFrHA"),
            tunnel_route_via=Global[str](value="AAAfxC"),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ipsec_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_cellular_interface_parcel_expect_successful_post(self):
        # Arrange
        cellular_parcel = InterfaceCellularParcel(
            parcel_name="InterfaceCellularParcel",
            parcel_description="Description",
            encapsulation=[
                Encapsulation(
                    encap=Global[EncapType](value="ipsec"),
                    preference=Variable(value="{{yvJr}}"),
                    weight=Variable(value="{{]MJ}}"),
                ),
                Encapsulation(
                    encap=Global[EncapType](value="ipsec"),
                    preference=None,
                    weight=Variable(value="{{_qmTNgmXr5h1vu5pMjMsTXF24}}"),
                ),
                Encapsulation(
                    encap=Global[EncapType](value="ipsec"), preference=Default[None](value=None), weight=None
                ),
            ],
            interface_description=Global[str](value="CkmMzlz"),
            interface_name=Global[str](value="xnaohVUa"),
            nat=Global[bool](value=True),
            shutdown=Global[bool](value=False),
            tunnel_interface=Global[bool](value=True),
            acl_qos=AclQos(
                adaptive_qos=Global[bool](value=True),
            ),
            advanced=AdvancedCellular(
                intrf_mtu=Global[int](value=1500),
                ip_directed_broadcast=Global[bool](value=True),
                ip_mtu=Global[int](value=600),
                tcp_mss=Global[int](value=600),
                tloc_extension=Global[str](value="PgcsRYBJOJ"),
                tracker=Global[str](value="gMivIg"),
            ),
            allow_service=AllowService(
                all=Global[bool](value=True),
                bfd=Global[bool](value=False),
                bgp=Global[bool](value=True),
                dhcp=Global[bool](value=True),
                dns=Global[bool](value=False),
                https=Global[bool](value=False),
                icmp=Global[bool](value=False),
                netconf=Global[bool](value=True),
                ntp=Global[bool](value=True),
                ospf=Global[bool](value=True),
                snmp=Global[bool](value=False),
                ssh=Global[bool](value=False),
                stun=Global[bool](value=True),
            ),
            arp=[
                Arp(
                    ip_address=Global[IPv4Address](value=IPv4Address("203.0.113.2")),
                    mac_address=Global[str](value="DC:F1:17:22:FA:3D"),
                ),
                Arp(ip_address=Global[str](value="3.2.1.1"), mac_address=Global[str](value="BF:DB:A1:F0:4B:C8")),
                Arp(
                    ip_address=Global[IPv4Address](value=IPv4Address("192.0.0.170")),
                    mac_address=Global[str](value="1B:5A:0F:AB:9E:CE"),
                ),
            ],
            bandwidth_downstream=Global[int](value=247),
            bandwidth_upstream=Global[int](value=185),
            dhcp_helper=Global[List[str]](value=["1.1.1.1", "2.2.2.2"]),
            multi_region_fabric=MultiRegionFabric(
                core_region=None,
                enable_core_region=None,
                enable_secondary_region=Global[bool](value=False),
                secondary_region=Default[SecondaryRegion](value="secondary-shared"),
            ),
            nat_attributes_ipv4=NatAttributesIpv4(
                tcp_timeout=Global[int](value=456), udp_timeout=Global[int](value=163)
            ),
            service_provider=Global[str](value="XaQzKLzx"),
            tunnel=TunnelCellular(
                bind=Global[str](value="VwOXkG"),
                border=Global[bool](value=False),
                carrier=Global[CarrierType](value="carrier1"),
                clear_dont_fragment=Global[bool](value=True),
                color=Global[TLOCColor](value="silver"),
                hello_interval=Global[int](value=173),
                hello_tolerance=Global[int](value=67),
                last_resort_circuit=Global[bool](value=True),
                low_bandwidth_link=Global[bool](value=False),
                max_control_connections=Global[int](value=10),
                mode=Global[Literal["spoke"]](value="spoke"),
                nat_refresh_interval=Global[int](value=4),
                network_broadcast=Global[bool](value=False),
                per_tunnel_qos=Global[bool](value=True),
                port_hop=Global[bool](value=True),
                restrict=Global[bool](value=False),
                tunnel_tcp_mss=Global[int](value=600),
                vbond_as_stun_server=Global[bool](value=False),
                vmanage_connection_preference=Global[int](value=2),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, cellular_parcel, self.wan_uuid).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_ethernet_interface_expect_successfull_post(self):
        # Arrange
        ethernet_parcel = InterfaceEthernetParcel(
            parcel_name="InterfaceEthernetParcel",
            parcel_description="Description",
            interface_description=Global[str](value="Description"),
            encapsulation=[
                Encapsulation(
                    encap=Global[Literal["ipsec", "gre"]](value="ipsec"),
                    preference=Default[None](value=None),
                    weight=Variable(value="{{1fk}}"),
                ),
                Encapsulation(encap=Global[EncapType](value="gre"), preference=None, weight=Global[int](value=92)),
            ],
            interface_name=Global[str](value="Ethernet3"),
            interface_ip_address=InterfaceStaticIPv4Address(
                static=StaticIPv4AddressConfig(
                    primary_ip_address=StaticIPv4Address(
                        ip_address=Default[None](value=None), subnet_mask=Default[None](value=None)
                    ),
                    secondary_ip_address=None,
                )
            ),
            nat=Global[bool](value=True),
            shutdown=Global[bool](value=False),
            tunnel_interface=Global[bool](value=True),
            advanced=EthernetAdvanced(
                arp_timeout=Global[int](value=97),
                autonegotiate=Global[bool](value=False),
                duplex=Global[Literal["full", "half", "auto"]](value="auto"),
                icmp_redirect_disable=Global[bool](value=True),
                intrf_mtu=Global[int](value=1500),
                ip_directed_broadcast=Global[bool](value=True),
                ip_mtu=Global[int](value=600),
                load_interval=Global[int](value=189),
                mac_address=Global[str](value="1B:5A:0F:AB:9E:CE"),
                media_type=Global[Literal["auto-select", "rj45", "sfp"]](value="sfp"),
                speed=Global[Literal["10", "100", "1000", "10000", "2500"]](value="10000"),
                tracker=Global[str](value="TlQCYe"),
            ),
            allow_service=AllowService(
                bfd=None,
                all=None,
                bgp=Default[bool](value=False),
                dhcp=Variable(value="{{DwA}}"),
                dns=Variable(value="{{ZpbcB9SD-}}"),
                https=None,
                icmp=Variable(value="{{l8}}"),
                netconf=Variable(value="{{dn_.}}"),
                ntp=None,
                ospf=None,
                snmp=None,
                sshd=None,
                stun=Variable(value="{{IOg/gP626}}"),
                ssh=Default[bool](value=True),
            ),
            arp=[
                CommonArp(
                    ip_address=Global[IPv4Address](value=IPv4Address("203.0.113.2")),
                    mac_address=Global[str](value="DC:F1:17:22:FA:3D"),
                ),
                CommonArp(ip_address=Global[str](value="3.2.1.1"), mac_address=Global[str](value="BF:DB:A1:F0:4B:C8")),
                CommonArp(
                    ip_address=Global[IPv4Address](value=IPv4Address("192.0.0.170")),
                    mac_address=Global[str](value="1B:5A:0F:AB:9E:CE"),
                ),
            ],
            auto_detect_bandwidth=Global[bool](value=False),
            bandwidth_downstream=Global[int](value=168),
            bandwidth_upstream=Global[int](value=113),
            block_non_source_ip=Global[bool](value=True),
            dhcp_helper=Global[List[str]](value=["1.1.1.1,2.3.3.3"]),
            iperf_server=Global[str](value="OXYQIcr"),
            multi_region_fabric=MultiRegionFabric(
                core_region=None,
                enable_core_region=None,
                enable_secondary_region=Global[bool](value=False),
                secondary_region=Default[SecondaryRegion](value="secondary-shared"),
            ),
            nat_attributes_ipv4=EthernetNatAttributesIpv4(
                nat_type=Variable(value="{{Qs6}}"),
                udp_timeout=Variable(value="{{2DdkYshx]a}}"),
                tcp_timeout=Variable(value="{{U}}"),
                new_static_nat=[
                    StaticNat(
                        source_ip=Variable(value="{{-_m}}"),
                        translate_ip=Global[IPv4Address](value=IPv4Address("100.125.239.247")),
                        static_nat_direction=Global[Literal["inside", "outside"]](value="outside"),
                        source_vpn=Global[int](value=422),
                    ),
                    StaticNat(
                        source_ip=Global[str](value="hWhYrEZZ"),
                        translate_ip=Variable(value="{{xskEgr6}}"),
                        static_nat_direction=Default[Literal["inside", "outside"]](value="inside"),
                        source_vpn=Default[int](value=0),
                    ),
                ],
            ),
            nat_attributes_ipv6=NatAttributesIpv6(
                nat64=Global[bool](value=False),
                nat66=Global[bool](value=True),
                static_nat66=[
                    StaticNat66(
                        source_prefix=Global[str](value="0::/16"),
                        source_vpn_id=Global[int](value=10),
                        egress_interface=Global[bool](value=False),
                        translated_source_prefix=Global[str](value="0::/16"),
                    ),
                    StaticNat66(
                        source_prefix=Global[str](value="2::/16"),
                        source_vpn_id=Global[int](value=282),
                        egress_interface=Global[bool](value=True),
                        translated_source_prefix=None,
                    ),
                ],
            ),
            nat_ipv6=Global[bool](value=True),
            service_provider=Global[str](value="HpZoKuVPSR"),
            tunnel=TunnelEthernet(
                bandwidth_percent=Global[int](value=50),
                bind=Global[str](value="aDzWWarP"),
                border=Global[bool](value=False),
                carrier=Global[CarrierType](value="carrier1"),
                clear_dont_fragment=Global[bool](value=True),
                color=Global[TLOCColor](value="bronze"),
                cts_sgt_propagation=Global[bool](value=False),
                exclude_controller_group_list=Global[List[int]](value=[]),
                group=Global[int](value=87),
                hello_interval=Global[int](value=388),
                hello_tolerance=Global[int](value=33),
                last_resort_circuit=Global[bool](value=False),
                low_bandwidth_link=Global[bool](value=False),
                max_control_connections=Global[int](value=2),
                nat_refresh_interval=Global[int](value=5),
                network_broadcast=Global[bool](value=True),
                per_tunnel_qos=Global[bool](value=True),
                port_hop=Global[bool](value=False),
                restrict=Global[bool](value=False),
                tloc_extension_gre_to=None,
                v_bond_as_stun_server=Global[bool](value=True),
                v_manage_connection_preference=Global[int](value=5),
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.wan_uuid).id
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
            all=Global[bool](value=True),
            authentication_type=Default[Literal[MultilinkAuthenticationType]](value="unidirectional"),
            bandwidth_upstream=Global[int](value=21),
            bgp=Global[bool](value=True),
            bind=Global[str](value="JmwcJz"),
            border=Global[bool](value=True),
            carrier=Global[Literal[CarrierType]](value="carrier8"),
            clear_dont_fragment_sdwan_tunnel=Global[bool](value=True),
            control_connections=Global[bool](value=False),
            controller_tx_ex_list=controller_tx_ex_list,
            controller_type=Global[Literal[MultilinkControllerType]](value="T1/E1"),
            delay_value=Global[int](value=99),
            dhcp=Global[bool](value=False),
            disable=Global[bool](value=True),
            dns=Global[bool](value=False),
            exclude_controller_group_list=Global[str](value="12 13 14"),
            gre_encap=Global[bool](value=True),
            gre_preference=Global[int](value=91),
            gre_weight=Global[int](value=48),
            groups=Global[int](value=363),
            hello_interval=Global[int](value=224),
            hello_tolerance=Global[int](value=214),
            hostname=Global[str](value="oitSeZBfw"),
            https=Global[bool](value=False),
            icmp=Global[bool](value=True),
            interleave=Global[bool](value=False),
            ip_directed_broadcast=Global[bool](value=True),
            ipsec_encap=Global[bool](value=False),
            ipsec_preference=Global[int](value=498),
            ipsec_weight=Global[int](value=135),
            ipv4_acl_egress=None,
            ipv4_acl_ingress=None,
            ipv6_acl_egress=None,
            ipv6_acl_ingress=None,
            last_resort_circuit=Global[bool](value=True),
            low_bandwidth_link=Global[bool](value=False),
            mask_ipv4=Global[SubnetMask](value="255.255.255.254"),
            max_control_connections=Global[int](value=50),
            mtu=Global[int](value=5266),
            multi_region_fabric=MultiRegionFabric(
                core_region=None,
                enable_core_region=None,
                enable_secondary_region=None,
                secondary_region=None,
            ),
            nat_refresh_interval=Global[int](value=33),
            netconf=Global[bool](value=False),
            network_broadcast=Global[bool](value=False),
            nim_list=nim_list,
            ntp=Global[bool](value=True),
            ospf=Global[bool](value=True),
            password=Global[str](value="hyBBiuDgO"),
            port_hop=Global[bool](value=False),
            ppp_auth_password=Global[str](value="aCBBBxnzsw"),
            restrict=Global[bool](value=False),
            shaping_rate=Global[int](value=294),
            shutdown=Global[bool](value=False),
            snmp=Global[bool](value=False),
            sshd=Global[bool](value=False),
            stun=Global[bool](value=False),
            tcp_mss_adjust=Global[int](value=1267),
            tloc_extension=Global[str](value="ATM"),
            tunnel_interface=Global[bool](value=True),
            tunnel_tcp_mss_adjust=Global[int](value=1269),
            username_string=Global[str](value="ONBBAAB"),
            value=Global[Literal[TLOCColor]](value="silver"),
            vbond_as_stun_server=Global[bool](value=False),
            vmanage_connection_preference=Global[int](value=7),
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, multilink_parcel, self.wan_uuid).id

        assert parcel_id

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()


class TestTransportFeatureProfileWanManagementModels(TestFeatureProfileModels):
    wan_uuid: UUID

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile("TestTransportService", "Description").id
        cls.wan_uuid = cls.api.create_parcel(
            cls.profile_uuid,
            ManagementVpnParcel(
                parcel_name="TestTransportVpnParcel",
                parcel_description="Description",
            ),
        ).id

    def test_when_fully_specified_ethernet_parcel_expect_successful_post(self):
        v4_address = InterfaceStaticIPv4Address(
            static=StaticIPv4AddressConfig(
                primary_ip_address=StaticIPv4Address(
                    ip_address=Default[None](value=None), subnet_mask=Default[None](value=None)
                ),
                secondary_ip_address=None,
            )
        )
        v6_address = InterfaceStaticIPv6Address(
            static=StaticIPv6AddressConfig(
                primary_ip_v6_address=StaticIPv6Address(address=Global[IPv6Interface](value="0::/16"))
            )
        )
        arp = [
            CommonArp(
                ip_address=Global[IPv4Address](value=IPv4Address("203.0.113.2")),
                mac_address=Global[str](value="DC:F1:17:22:FA:3D"),
            ),
            CommonArp(ip_address=Global[str](value="3.2.1.1"), mac_address=Global[str](value="BF:DB:A1:F0:4B:C8")),
            CommonArp(
                ip_address=Global[IPv4Address](value=IPv4Address("192.0.0.170")),
                mac_address=Global[str](value="1B:5A:0F:AB:9E:CE"),
            ),
        ]
        advanced = ManagementEthernetAdvanced(
            arp_timeout=Global[int](value=97),
            ip_directed_broadcast=Global[bool](value=True),
            ip_mtu=Global[int](value=600),
            load_interval=Global[int](value=189),
            autonegotiate=Global[bool](value=False),
            duplex=Global[EthernetDuplexMode](value="auto"),
            icmp_redirect_disable=Global[bool](value=True),
            intrf_mtu=Global[int](value=1550),
            mac_address=Global[str](value="1B:5A:0F:AB:9E:CE"),
            media_type=Global[Literal["auto-select", "rj45", "sfp"]](value="sfp"),
            speed=Global[Literal["10", "100", "1000", "10000", "2500"]](value="10000"),
            tcp_mss=Global[int](value=1444),
        )
        ethernet_parcel = ManagementEthernetParcel(
            parcel_name="Test",
            parcel_description="Description",
            advanced=advanced,
            interface_name=Global[str](value="GlobalEthernet1"),
            interface_description=Global[str](value="Test"),
            intf_ip_address=v4_address,
            shutdown=Global[bool](value=True),
            arp=arp,
            auto_detect_bandwidth=Global[bool](value=False),
            dhcp_helper=Global[List[str]](value=["1.1.1.1", "2.2.2.2"]),
            intf_ip_v6_address=v6_address,
            iperf_server=Global[str](value="OXYQIcr"),
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, ethernet_parcel, self.wan_uuid).id

        assert parcel_id

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
