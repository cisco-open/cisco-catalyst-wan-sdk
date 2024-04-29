from ipaddress import IPv4Address, IPv6Address

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
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
