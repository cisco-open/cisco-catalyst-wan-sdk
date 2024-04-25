from ipaddress import IPv4Address
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import Global, as_global, as_variable
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.common import SubnetMask
from catalystwan.models.configuration.feature_profile.common import Prefix
from catalystwan.models.configuration.feature_profile.sdwan.service.acl import Ipv4AclParcel, Ipv6AclParcel
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
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import (
    BasicGre,
    GreAddress,
    InterfaceGreParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import InterfaceIpsecParcel, IpsecAddress
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
from catalystwan.models.configuration.feature_profile.sdwan.service.ospf import OspfParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.ospfv3 import (
    Ospfv3InterfaceParametres,
    Ospfv3IPv4Area,
    Ospfv3IPv4Parcel,
    Ospfv3IPv6Area,
    Ospfv3IPv6Parcel,
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
        ospf_parcel = OspfParcel(
            parcel_name="TestOspfParcel",
            parcel_description="Test Ospf Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ospf_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_ospfv3_ipv4_expect_successful_post(self):
        # Arrange
        ospfv3ipv4_parcel = Ospfv3IPv4Parcel(
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
        ospfv3ipv4_parcel = Ospfv3IPv6Parcel(
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
        parcel_id = self.api.create_parcel(self.profile_uuid, ospfv3ipv4_parcel).id
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
                        prefix=Prefix(
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
                address=GreAddress(
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
            address=IpsecAddress(address=as_global("10.0.0.1"), mask=as_global("255.255.255.0")),
            tunnel_destination=IpsecAddress(address=as_global("10.0.0.5"), mask=as_global("255.255.255.0")),
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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
