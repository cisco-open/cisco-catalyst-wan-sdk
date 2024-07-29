# Copyright 2024 Cisco Systems, Inc. and its affiliates


from ipaddress import IPv4Address, IPv4Interface
from uuid import UUID

from catalystwan.api.templates.device_template.device_template import DeviceTemplate
from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.api.templates.models.cisco_secure_internet_gateway import (
    CiscoSecureInternetGatewayModel,
    Interface,
    InterfacePair,
    Service,
    Tracker,
)
from catalystwan.integration_tests.base import TestCaseBase, create_name_with_run_id
from catalystwan.utils.config_migration.runner import ConfigMigrationRunner


class TestMigrationFlow(TestCaseBase):
    runner: ConfigMigrationRunner

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.runner = ConfigMigrationRunner.collect_push_and_rollback(cls.session)
        cls.runner.run()

    def test_collect_artefact(self):
        # Arrange
        ux1_config = self.runner.load_collected_config()
        # Act, Assert
        assert ux1_config

    def test_transform_artefact(self):
        # Arrange
        transform_result = self.runner.load_transform_result()
        # Act, Assert
        assert transform_result.failed_items == list()

    def test_push_artefact(self):
        # Arrange
        push_result = self.runner.load_push_result()
        # Act, Assert
        assert push_result.report.failed_push_parcels == list()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.runner.clear_ux2()
        super().tearDownClass()


class TestPolicyGroupAggregation(TestCaseBase):
    runner: ConfigMigrationRunner
    sig_name: str
    sig_uuid: str
    device_template_name: str
    device_template_uuid: str

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # --------------------------------------
        # Create SIG Feature Template
        # --------------------------------------
        templates = cls.session.api.templates
        cls.sig_name = create_name_with_run_id("SIG")
        cisco_sig = CiscoSecureInternetGatewayModel(
            template_name=cls.sig_name,
            template_description="Comprehensive CiscoSecureInternetGateway Configuration",
            vpn_id=10,
            child_org_id="example_org",
            interface=[
                Interface(
                    if_name="GigabitEthernet0/0",
                    auto=True,
                    shutdown=False,
                    description="Main interface for SIG",
                    unnumbered=False,
                    address=IPv4Interface("192.168.1.1/24"),
                    tunnel_source=IPv4Address("192.168.1.1"),
                    tunnel_source_interface="Loopback0",
                    tunnel_route_via="192.168.2.1",
                    tunnel_destination="203.0.113.1",
                    application="sig",
                    tunnel_set="secure-internet-gateway-umbrella",
                    tunnel_dc_preference="primary-dc",
                    tcp_mss_adjust=1400,
                    mtu=1400,
                    dpd_interval=30,
                    dpd_retries=3,
                    ike_version=2,
                    pre_shared_secret="MyPreSharedSecret",  # pragma: allowlist secret
                    ike_rekey_interval=3600,
                    ike_ciphersuite="aes256-cbc-sha1",
                    ike_group="14",
                    pre_shared_key_dynamic=False,
                    ike_local_id="local-id",
                    ike_remote_id="remote-id",
                    ipsec_rekey_interval=3600,
                    ipsec_replay_window=32,
                    ipsec_ciphersuite="aes256-gcm",
                    perfect_forward_secrecy="group-14",
                    tracker=True,
                    track_enable=True,
                )
            ],
            service=[
                Service(
                    svc_type="sig",
                    interface_pair=[
                        InterfacePair(
                            active_interface="GigabitEthernet0/0",
                            active_interface_weight=10,
                            backup_interface="GigabitEthernet0/1",
                            backup_interface_weight=5,
                        )
                    ],
                    auth_required=True,
                    xff_forward_enabled=True,
                    ofw_enabled=False,
                    ips_control=True,
                    caution_enabled=False,
                    primary_data_center="Auto",
                    secondary_data_center="Auto",
                    ip=True,
                    idle_time=30,
                    display_time_unit="MINUTE",
                    ip_enforced_for_known_browsers=True,
                    refresh_time=5,
                    refresh_time_unit="MINUTE",
                    enabled=True,
                    block_internet_until_accepted=False,
                    force_ssl_inspection=True,
                    timeout=60,
                    data_center_primary="Auto",
                    data_center_secondary="Auto",
                )
            ],
            tracker_src_ip=IPv4Interface("192.0.2.1/32"),
            tracker=[
                Tracker(
                    name="health-check-tracker",
                    endpoint_api_url="https://api.example.com/health",
                    threshold=5,
                    interval=60,
                    multiplier=2,
                    tracker_type="SIG",
                )
            ],
        )
        cls.sig_uuid = templates.create(cisco_sig)
        # --------------------------------------
        # Create Device Template
        # --------------------------------------
        dt = DeviceTemplate.get(
            "Factory_Default_C8000V_V01",
            cls.session,
        )
        cls.device_template_name = create_name_with_run_id("DeviceTemplate_to_PolicyGroup")
        dt.template_name = cls.device_template_name
        dt.factory_default = False
        dt.associate_feature_template(cisco_sig.type, UUID(cls.sig_uuid))
        cls.device_template_uuid = templates.create(dt)
        # --------------------------------------
        # Run Migration
        # --------------------------------------
        cls.runner = ConfigMigrationRunner.collect_and_push(cls.session, filter=cls.device_template_name)
        cls.runner.set_dump_prefix("aggregation")
        cls.runner.set_filters(
            device_template_name=cls.device_template_name,
            feature_template_name=cls.sig_name,
        )
        cls.runner.run()

    def test_sss(self):
        """Test Policy Group Aggregation

        When:
        UX1.0: Device Template has associated a SIG Feature Template, Security Policy and Localized Policy

        Expect:
        UX2.0: Policy Group with associated SIG, Application Priority & SLA, Security, DNS Security Feature Profiles
        """
        # Act
        policy_group = (
            self.session.endpoints.configuration.policy_group.get_all()
            .filter(name=self.device_template_name)
            .single_or_default()
        )
        # Assert
        assert policy_group is not None
        assert policy_group.get_profile_by_name(self.sig_name) is not None

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.api.templates.delete(DeviceTemplate, cls.device_template_name)
        cls.session.api.templates.delete(FeatureTemplate, cls.sig_name)  # type: ignore
        cls.runner.clear_ux2()
        return super().tearDownClass()
