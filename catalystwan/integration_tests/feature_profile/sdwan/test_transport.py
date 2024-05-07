from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from typing import Literal
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, as_global
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.common import EncapType
from catalystwan.models.configuration.feature_profile.common import Prefix as CommonPrefix
from catalystwan.models.configuration.feature_profile.sdwan.transport.t1e1controller import (
    E1,
    T1,
    CableLengthLong,
    ChannelGroup,
    ClockSource,
    ControllerTxExList,
    ControllerType,
    E1Basic,
    E1Framing,
    E1Linecode,
    LengthLong,
    LineMode,
    Long,
    T1Basic,
    T1E1ControllerParcel,
    T1Framing,
    T1Linecode,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import (
    Address64V4PoolItem,
    DnsIpv4,
    DnsIpv6,
    Ipv4RouteItem,
    Ipv6RouteItem,
    ManagementVpnParcel,
    NewHostMappingItem,
    NextHopItem,
    OneOfIpRouteNull0,
    Prefix,
    ServiceItem,
    ServiceType,
    SubnetMask,
    TransportVpnParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.wan.interface.t1e1serial import (
    Advanced,
    AllowService,
    CoreRegion,
    Encapsulation,
    MultiRegionFabric,
    SecondaryRegion,
    T1E1SerialParcel,
    Tunnel,
)


class TestTransportFeatureProfileModels(TestFeatureProfileModels):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile("TestProfileService", "Description").id

    def test_when_fully_specified_management_vpn_parcel_expect_successful_post(self):
        # Arrange
        management_vpn_parcel = ManagementVpnParcel(
            parcel_name="FullySpecifiedManagementVpnParcel",
            description="Description",
            dns_ipv6=DnsIpv6(
                primary_dns_address_ipv6=as_global(IPv6Address("67ca:c2df:edfe:c8ec:b6cb:f9f4:eab0:ece6")),
                secondary_dns_address_ipv6=as_global(IPv6Address("8989:8d33:c00a:4d13:324d:8b23:8d77:a289")),
            ),
            dns_ipv4=DnsIpv4(
                primary_dns_address_ipv4=as_global(IPv4Address("68.138.29.222")),
                secondary_dns_address_ipv4=as_global(IPv4Address("122.89.114.112")),
            ),
            new_host_mapping=[
                NewHostMappingItem(
                    host_name=as_global("FullySpecifiedHost"),
                    list_of_ip=as_global(
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
                        length_long=as_global("-15db", LengthLong),
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

    def test_when_fully_specifed_transport_vpn_parcel_expect_successful_post(self):
        # Arrange
        transport_vpn_parcel = TransportVpnParcel(
            parcel_name="FullySpecifiedTransportVpnParcel",
            description="Description",
            dns_ipv6=DnsIpv6(
                primary_dns_address_ipv6=as_global(IPv6Address("67ca:c2df:edfe:c8ec:b6cb:f9f4:eab0:ece6")),
                secondary_dns_address_ipv6=as_global(IPv6Address("8989:8d33:c00a:4d13:324d:8b23:8d77:a289")),
            ),
            dns_ipv4=DnsIpv4(
                primary_dns_address_ipv4=as_global(IPv4Address("68.138.29.222")),
                secondary_dns_address_ipv4=as_global(IPv4Address("122.89.114.112")),
            ),
            new_host_mapping=[
                NewHostMappingItem(
                    host_name=as_global("FullySpecifiedHost"),
                    list_of_ip=as_global(
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()


class TestTransportFeatureProfileWanInterfaceModels(TestFeatureProfileModels):
    wan_uuid: UUID

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile("TestProfileService", "Description").id
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
