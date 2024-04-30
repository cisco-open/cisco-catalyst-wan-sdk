from ipaddress import IPv4Address, IPv6Address

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
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
    T1Basic,
    T1E1ControllerParcel,
    T1Framing,
    T1Linecode,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn_management import (
    DnsIpv4,
    DnsIpv6,
    Ipv4RouteItem,
    Ipv6RouteItem,
    ManagementVpn,
    NewHostMappingItem,
    NextHopItem,
    OneOfIpRouteNull0,
    Prefix,
    SubnetMask,
)


class TestTransportFeatureProfileModels(TestFeatureProfileModels):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.transport
        cls.profile_uuid = cls.api.create_profile("TestProfileService", "Description").id

    def test_when_fully_specified_management_vpn_parcel_expect_successful_post(self):
        # Arrange
        management_vpn_parcel = ManagementVpn(
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
                    prefix=as_global("0::/16"),
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
                        cable_length=as_global("long", CableLengthLong),
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
