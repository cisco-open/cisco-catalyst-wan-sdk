# Copyright 2024 Cisco Systems, Inc. and its affiliates


from ipaddress import IPv4Address, IPv4Interface
from typing import Dict, List
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
from catalystwan.models.policy.definition.qos_map import QoSMapPolicy
from catalystwan.models.policy.list.class_map import ClassMapList
from catalystwan.models.policy.localized import LocalizedPolicy, LocalizedPolicySettings
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
    pol_dict: Dict[str, UUID]
    localized_policy_name: str
    queue_names: List[str]
    qos_map_name: str

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.pol_dict = {}
        cls.queue_names = ["VOICE", "CRITICAL_DATA", "BULK", "DEFAULT", "INTERACTIVE_VIDEO", "CONTROL_SIGNALING"]
        cls.sig_name = create_name_with_run_id("SIG")
        cls.localized_policy_name = create_name_with_run_id("LocalizedPolicy")
        cls.qos_map_name = create_name_with_run_id("QosMapPolicy")
        cls.device_template_name = create_name_with_run_id("DeviceTemplate_to_PolicyGroup")
        cls.runner = ConfigMigrationRunner.collect_and_push(cls.session)
        cls.runner.set_dump_prefix("aggregation")
        cls.runner.set_filters(
            dt_filter=cls.device_template_name,
            lp_filter=cls.localized_policy_name,
        )

    def test_policy_groups_aggregation(self):
        """Test Policy Group Aggregation

        When:
        UX1.0: Device Template has associated a SIG Feature Template, Security Policy and Localized Policy

        Expect:
        UX2.0: Policy Group with associated SIG, Application Priority & SLA, Security, DNS Security Feature Profiles
        """
        # Arrange
        self._create_sig_feature_template()
        self._create_localized_policy()
        self._create_device_template()
        # Act
        self.runner.run()
        # Assert
        policy_group = (
            self.session.endpoints.configuration.policy_group.get_all()
            .filter(name=self.device_template_name)
            .single_or_default()
        )
        assert policy_group is not None
        assert policy_group.get_profile_by_name(self.sig_name) is not None
        assert policy_group.get_profile_by_name(self.localized_policy_name) is not None

    def _create_device_template(self) -> None:
        templates = self.session.api.templates
        dt = DeviceTemplate.get("Factory_Default_C8000V_V01", self.session)
        dt.template_name = self.device_template_name
        dt.factory_default = False
        dt.associate_feature_template(CiscoSecureInternetGatewayModel.type, UUID(self.sig_uuid))
        dt.associate_policy(self.pol_dict["Localized-Policy"])
        self.device_template_uuid = templates.create(dt)

    def _create_sig_feature_template(self) -> None:
        templates = self.session.api.templates
        cisco_sig = CiscoSecureInternetGatewayModel(
            template_name=self.sig_name,
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
        self.sig_uuid = templates.create(cisco_sig)

    def _create_localized_policy(self) -> None:
        api = self.session.api.policy
        for i, name in enumerate(self.queue_names):
            class_map = ClassMapList(name=create_name_with_run_id(name))
            class_map.assign_queue(i)
            self.pol_dict[name] = api.lists.create(class_map)
        qos_map = QoSMapPolicy(name=self.qos_map_name, description="QoS Map Policy")
        qos_map.add_scheduler(queue=1, class_map_ref=self.pol_dict["CRITICAL_DATA"], bandwidth=30, buffer=30)
        qos_map.add_scheduler(queue=2, class_map_ref=self.pol_dict["BULK"], bandwidth=10, buffer=10)
        qos_map.add_scheduler(queue=3, class_map_ref=self.pol_dict["DEFAULT"], bandwidth=20, buffer=20)
        qos_map.add_scheduler(queue=4, class_map_ref=self.pol_dict["INTERACTIVE_VIDEO"], bandwidth=20, buffer=20)
        qos_map.add_scheduler(
            queue=5, class_map_ref=self.pol_dict["CONTROL_SIGNALING"], bandwidth=10, buffer=10, drops="tail-drop"
        )
        self.pol_dict["QosMap-Policy"] = api.definitions.create(qos_map)
        loc_pol = LocalizedPolicy(policy_name=self.localized_policy_name, policy_description="desc text")
        loc_pol.set_definition(
            [],
            LocalizedPolicySettings(
                cloud_qos=True,
                cloud_qos_service_side=True,
            ),
        )
        loc_pol.add_qos_map(self.pol_dict["QosMap-Policy"])
        self.pol_dict["Localized-Policy"] = api.localized.create(loc_pol)

    @classmethod
    def tearDownClass(cls) -> None:
        templates = cls.session.api.templates
        templates.delete(DeviceTemplate, cls.device_template_name)
        templates.delete(FeatureTemplate, cls.sig_name)  # type: ignore

        policy = cls.session.api.policy
        policy.localized.delete(cls.pol_dict["Localized-Policy"])
        policy.definitions.delete(QoSMapPolicy, cls.pol_dict["QosMap-Policy"])
        policy.lists.delete(ClassMapList, cls.pol_dict["VOICE"])
        policy.lists.delete(ClassMapList, cls.pol_dict["CRITICAL_DATA"])
        policy.lists.delete(ClassMapList, cls.pol_dict["BULK"])
        policy.lists.delete(ClassMapList, cls.pol_dict["DEFAULT"])
        policy.lists.delete(ClassMapList, cls.pol_dict["INTERACTIVE_VIDEO"])
        policy.lists.delete(ClassMapList, cls.pol_dict["CONTROL_SIGNALING"])

        cls.runner.clear_ux2()
        return super().tearDownClass()
