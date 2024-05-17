from ipaddress import IPv4Address

from catalystwan.api.configuration_groups.parcel import Global
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.common import IkeCiphersuite
from catalystwan.models.configuration.feature_profile.sdwan.sig_security.sig_security import (
    Application,
    IkeGroup,
    Interface,
    InterfaceMetadataSharing,
    InterfacePair,
    IpsecReplayWindow,
    PerfectForwardSecrecy,
    Service,
    SIGParcel,
    SigProvider,
    TimeUnit,
    Tracker,
    TrackerType,
    TunnelDcPreference,
    TunnelSet,
)


class TestSIGSecurityProfileModels(TestFeatureProfileModels):
    @classmethod
    def setUp(cls) -> None:
        cls.api = cls.session.api.sdwan_feature_profiles.sig_security
        cls.profile_uuid = cls.api.create_profile("TestProfile", "Description").id

    def test_when_fully_specified_sig_generic_ipsec_parcel_expect_successful_post(self):
        interface_pair = InterfacePair(
            active_interface=Global[str](value="ipsec1"),
            active_interface_weight=Global[int](value=1),
            backup_interface=Global[str](value="None"),
            backup_interface_weight=Global[int](value=1),
        )
        service = Service(
            interface_pair=[interface_pair],
        )
        tracker = Tracker(
            name=Global[str](value="tracker1"),
            endpoint_api_url=Global[str](value="http://test.com"),
            threshold=Global[int](value=305),
            interval=Global[int](value=90),
            multiplier=Global[int](value=4),
            tracker_type=Global[TrackerType](value="SIG"),
        )
        interface = Interface(
            if_name=Global[str](value="ipsec1"),
            auto=Global[bool](value=False),
            shutdown=Global[bool](value=True),
            description=Global[str](value="test"),
            unnumbered=Global[bool](value=True),
            tunnel_source_interface=Global[str](value="Ethernet"),
            tunnel_route_via=Global[str](value="Ethernet"),
            tunnel_destination=Global[str](value="10.0.0.1"),
            application=Global[Application](value="sig"),
            tunnel_set=Global[TunnelSet](value="secure-internet-gateway-other"),
            tcp_mss_adjust=Global[int](value=555),
            mtu=Global[int](value=1444),
            dpd_interval=Global[int](value=14),
            dpd_retries=Global[int](value=4),
            ike_version=Global[int](value=2),
            pre_shared_secret=Global[str](value="a"),
            ike_rekey_interval=Global[int](value=1444),
            ike_ciphersuite=Global[IkeCiphersuite](value="aes128-cbc-sha2"),
            ike_group=Global[IkeGroup](value="14"),
            ike_local_id=Global[str](value="15"),
            ike_remote_id=Global[str](value="15"),
            ipsec_rekey_interval=Global[int](value=15555),
            ipsec_replay_window=Global[IpsecReplayWindow](value=128),
            perfect_forward_secrecy=Global[PerfectForwardSecrecy](value="group-19"),
        )

        sig_parcel = SIGParcel(
            parcel_name="SIGParcelIntegrationTest",
            parcel_description="SIGParcelIntegrationTest",
            sig_provider=Global[SigProvider](value="Generic"),
            interface_metadata_sharing=InterfaceMetadataSharing(src_vpn=Global[bool](value=False)),
            interface=[interface],
            service=service,
            tracker_src_ip=Global[IPv4Address](value="10.0.0.1"),
            tracker=[tracker],
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, sig_parcel).id

        assert parcel_id

    def test_when_fully_specified_sig_generic_gre_parcel_expect_successful_post(self):
        interface_pair = InterfacePair(
            active_interface=Global[str](value="gre1"),
            active_interface_weight=Global[int](value=1),
            backup_interface=Global[str](value="None"),
            backup_interface_weight=Global[int](value=1),
        )
        service = Service(
            interface_pair=[interface_pair],
        )
        interface = Interface(
            if_name=Global[str](value="gre1"),
            auto=Global[bool](value=False),
            shutdown=Global[bool](value=True),
            description=Global[str](value="t"),
            unnumbered=Global[bool](value=True),
            tunnel_source_interface=Global[str](value="FastEthernet"),
            tunnel_route_via=Global[str](value="FastEthernet"),
            tunnel_destination=Global[str](value="10.0.0.1"),
            application=Global[Application](value="sig"),
            tunnel_set=Global[TunnelSet](value="secure-internet-gateway-other"),
            tcp_mss_adjust=Global[int](value=555),
            mtu=Global[int](value=666),
        )
        tracker = Tracker(
            name=Global[str](value="tracker1"),
            endpoint_api_url=Global[str](value="http://test.com"),
            threshold=Global[int](value=305),
            interval=Global[int](value=90),
            multiplier=Global[int](value=4),
            tracker_type=Global[TrackerType](value="SIG"),
        )
        sig_parcel = SIGParcel(
            parcel_name="SIGParcelIntegrationTest",
            parcel_description="SIGParcelIntegrationTest",
            sig_provider=Global[SigProvider](value="Generic"),
            interface_metadata_sharing=InterfaceMetadataSharing(src_vpn=Global[bool](value=False)),
            interface=[interface],
            service=service,
            tracker_src_ip=Global[IPv4Address](value="10.0.0.1"),
            tracker=[tracker],
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, sig_parcel).id

        assert parcel_id

    def test_when_fully_specified_sig_umbrella_parcel_expect_successful_post(self):
        interface_pair = InterfacePair(
            active_interface=Global[str](value="ipsec1"),
            active_interface_weight=Global[int](value=1),
            backup_interface=Global[str](value="None"),
            backup_interface_weight=Global[int](value=1),
        )
        service = Service(
            interface_pair=[interface_pair],
            data_center_primary=Global[str](value="us1-a.vpn.sig.umbrella.com"),
            data_center_secondary=Global[str](value="us1-b.vpn.sig.umbrella.com"),
        )
        interface = Interface(
            if_name=Global[str](value="ipsec1"),
            auto=Global[bool](value=True),
            shutdown=Global[bool](value=True),
            description=Global[str](value="T"),
            unnumbered=Global[bool](value=True),
            tunnel_source_interface=Global[str](value="FastEthernet"),
            tunnel_route_via=Global[str](value="FastEthernet"),
            tunnel_destination=Global[str](value="dynamic"),
            application=Global[Application](value="sig"),
            tunnel_set=Global[TunnelSet](value="secure-internet-gateway-umbrella"),
            tunnel_dc_preference=Global[TunnelDcPreference](value="primary-dc"),
            tcp_mss_adjust=Global[int](value=555),
            mtu=Global[int](value=1444),
            dpd_interval=Global[int](value=14),
            dpd_retries=Global[int](value=44),
            ike_version=Global[int](value=2),
            ike_rekey_interval=Global[int](value=1444),
            ike_ciphersuite=Global[IkeCiphersuite](value="aes128-cbc-sha1"),
            ike_group=Global[IkeGroup](value="2"),
            pre_shared_key_dynamic=Global[bool](value=True),
            ipsec_rekey_interval=Global[int](value=555),
            ipsec_replay_window=Global[IpsecReplayWindow](value=256),
            perfect_forward_secrecy=Global[PerfectForwardSecrecy](value="group-15"),
            tracker=Global[str](value="tracker1"),
            track_enable=Global[bool](value=True),
        )
        tracker = Tracker(
            name=Global[str](value="tracker1"),
            endpoint_api_url=Global[str](value="http://test1.com"),
            threshold=Global[int](value=344),
            interval=Global[int](value=33),
            multiplier=Global[int](value=4),
            tracker_type=Global[TrackerType](value="SIG"),
        )
        sig_parcel = SIGParcel(
            parcel_name="SIGParcelIntegrationTest",
            parcel_description="SIGParcelIntegrationTest",
            sig_provider=Global[SigProvider](value="Umbrella"),
            interface_metadata_sharing=InterfaceMetadataSharing(src_vpn=Global[bool](value=False)),
            interface=[interface],
            service=service,
            tracker_src_ip=Global[IPv4Address](value="10.0.0.1"),
            tracker=[tracker],
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, sig_parcel).id

        assert parcel_id

    def test_when_fully_specified_sig_zscaler_ipsec_parcel_expect_successful_post(self):
        interface_pair = InterfacePair(
            active_interface=Global[str](value="ipsec1"),
            active_interface_weight=Global[int](value=1),
            backup_interface=Global[str](value="None"),
            backup_interface_weight=Global[int](value=1),
        )
        service = Service(
            interface_pair=[interface_pair],
            auth_required=Global[bool](value=True),
            xff_forward_enabled=Global[bool](value=True),
            ofw_enabled=Global[bool](value=False),
            ips_control=Global[bool](value=False),
            secondary_data_center=Global[str](value="fra4-vpn.zscalerbeta.net"),
            ip=Global[bool](value=True),
            idle_time=Global[int](value=444),
            display_time_unit=Global[TimeUnit](value="HOUR"),
            ip_enforced_for_known_browsers=Global[bool](value=True),
            refresh_time=Global[int](value=444),
            refresh_time_unit=Global[TimeUnit](value="HOUR"),
        )
        interface = Interface(
            if_name=Global[str](value="ipsec1"),
            auto=Global[bool](value=True),
            shutdown=Global[bool](value=False),
            description=Global[str](value="A"),
            unnumbered=Global[bool](value=True),
            tunnel_source_interface=Global[str](value="FortyGigabitEthernet"),
            tunnel_route_via=Global[str](value="FortyGigabitEthernet"),
            tunnel_destination=Global[str](value="dynamic"),
            application=Global[Application](value="sig"),
            tunnel_set=Global[TunnelSet](value="secure-internet-gateway-zscaler"),
            tunnel_dc_preference=Global[TunnelDcPreference](value="primary-dc"),
            mtu=Global[int](value=1400),
            dpd_interval=Global[int](value=10),
            dpd_retries=Global[int](value=3),
            ike_version=Global[int](value=2),
            ike_group=Global[IkeGroup](value="2"),
            pre_shared_key_dynamic=Global[bool](value=True),
            ipsec_replay_window=Global[IpsecReplayWindow](value=256),
            perfect_forward_secrecy=Global[PerfectForwardSecrecy](value="group-14"),
        )
        tracker = Tracker(
            name=Global[str](value="tracker1"),
            endpoint_api_url=Global[str](value="http://test1.com"),
            threshold=Global[int](value=344),
            interval=Global[int](value=33),
            multiplier=Global[int](value=4),
            tracker_type=Global[TrackerType](value="SIG"),
        )
        sig_parcel = SIGParcel(
            parcel_name="SIGParcelIntegrationTest",
            parcel_description="SIGParcelIntegrationTest",
            sig_provider=Global[SigProvider](value="Zscaler"),
            interface_metadata_sharing=InterfaceMetadataSharing(src_vpn=Global[bool](value=False)),
            interface=[interface],
            service=service,
            tracker_src_ip=Global[IPv4Address](value="10.0.0.1"),
            tracker=[tracker],
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, sig_parcel).id

        assert parcel_id

    def test_when_fully_specified_sig_zscaler_gre_parcel_expect_successful_post(self):
        interface_pair = InterfacePair(
            active_interface=Global[str](value="gre1"),
            active_interface_weight=Global[int](value=1),
            backup_interface=Global[str](value="None"),
            backup_interface_weight=Global[int](value=1),
        )
        service = Service(
            interface_pair=[interface_pair],
            primary_data_center=Global[str](value="10.0.0.1"),
            secondary_data_center=Global[str](value="10.0.0.1"),
        )
        interface = Interface(
            if_name=Global[str](value="gre1"),
            auto=Global[bool](value=True),
            shutdown=Global[bool](value=False),
            description=Global[str](value="eee"),
            unnumbered=Global[bool](value=True),
            tunnel_source_interface=Global[str](value="Ethernet"),
            tunnel_route_via=Global[str](value="Ethernet"),
            tunnel_destination=Global[str](value="dynamic"),
            application=Global[Application](value="sig"),
            tunnel_set=Global[TunnelSet](value="secure-internet-gateway-zscaler"),
            tunnel_dc_preference=Global[TunnelDcPreference](value="primary-dc"),
            tcp_mss_adjust=Global[int](value=555),
            mtu=Global[int](value=1444),
            dpd_interval=Global[int](value=11),
            dpd_retries=Global[int](value=4),
            track_enable=Global[bool](value=True),
            tunnel_public_ip=Global[str](value="10.0.0.1"),
        )
        tracker = Tracker(
            name=Global[str](value="tracker1"),
            endpoint_api_url=Global[str](value="http://test1.com"),
            threshold=Global[int](value=344),
            interval=Global[int](value=33),
            multiplier=Global[int](value=4),
            tracker_type=Global[TrackerType](value="SIG"),
        )
        sig_parcel = SIGParcel(
            parcel_name="SIGParcelIntegrationTest",
            parcel_description="SIGParcelIntegrationTest",
            sig_provider=Global[SigProvider](value="Zscaler"),
            interface_metadata_sharing=InterfaceMetadataSharing(src_vpn=Global[bool](value=False)),
            interface=[interface],
            service=service,
            tracker_src_ip=Global[IPv4Address](value="10.0.0.1"),
            tracker=[tracker],
        )

        parcel_id = self.api.create_parcel(self.profile_uuid, sig_parcel).id

        assert parcel_id

    @classmethod
    def tearDown(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
