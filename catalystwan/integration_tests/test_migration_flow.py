# Copyright 2024 Cisco Systems, Inc. and its affiliates


from ipaddress import IPv4Interface
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
from catalystwan.models.policy.definition.aip import (
    AdvancedInspectionProfileDefinition,
    AdvancedInspectionProfilePolicy,
)
from catalystwan.models.policy.definition.dns_security import DnsSecurityDefinition, DnsSecurityPolicy
from catalystwan.models.policy.definition.intrusion_prevention import (
    IntrusionPreventionDefinition,
    IntrusionPreventionPolicy,
)
from catalystwan.models.policy.definition.qos_map import QoSMapPolicy
from catalystwan.models.policy.definition.zone_based_firewall import ZoneBasedFWPolicy
from catalystwan.models.policy.list.class_map import ClassMapList
from catalystwan.models.policy.list.local_domain import LocalDomainList
from catalystwan.models.policy.list.umbrella_data import UmbrellaDataList
from catalystwan.models.policy.localized import LocalizedPolicy, LocalizedPolicySettings
from catalystwan.models.policy.policy_definition import Reference
from catalystwan.models.policy.security import UnifiedSecurityPolicy
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


COPY_DEVICE_TEMPLATE_FROM = "Factory_Default_C8000V_V01"


class TestPolicyGroupAggregation(TestCaseBase):
    runner: ConfigMigrationRunner
    sig_name: str
    sig_uuid: str
    device_template_name: str
    device_template_uuid: str
    pol_dict: Dict[str, UUID]
    localized_policy_name: str
    security_policy_name: str
    dns_security_name: str
    queue_names: List[str]
    qos_map_name: str

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.pol_dict = {}
        cls.queue_names = ["VOICE", "CRITICAL_DATA", "BULK", "DEFAULT", "INTERACTIVE_VIDEO", "CONTROL_SIGNALING"]
        cls.sig_name = create_name_with_run_id("SIG")
        cls.localized_policy_name = create_name_with_run_id("LocalizedPolicy")
        cls.security_policy_name = create_name_with_run_id("SecurityPolicy")
        cls.dns_security_name = create_name_with_run_id("DnsSecurity")
        cls.qos_map_name = create_name_with_run_id("QosMapPolicy")
        cls.device_template_name = create_name_with_run_id("DeviceTemplate_to_PolicyGroup")
        cls.runner = ConfigMigrationRunner.collect_push_and_rollback(cls.session)
        cls.runner.set_dump_prefix("aggregation")
        cls.runner.set_filters(
            dt_filter=cls.device_template_name,
            lp_filter=cls.localized_policy_name,
            sp_filter=cls.security_policy_name,
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
        self._create_security_policy()
        self._create_device_template()
        # Act
        self.runner.run()
        push_result = self.runner.load_push_result()
        # Assert
        assert len(push_result.report.policy_groups) == 1
        policy_group = push_result.report.policy_groups[0]
        assert policy_group.name.startswith(self.device_template_name)
        feature_profiles = policy_group.feature_profiles
        assert len([fp for fp in feature_profiles if fp.profile_name.startswith(self.sig_name)]) == 1
        assert len([fp for fp in feature_profiles if fp.profile_name.startswith(self.localized_policy_name)]) == 1
        assert len([fp for fp in feature_profiles if fp.profile_name.startswith(self.security_policy_name)]) == 1
        assert len([fp for fp in feature_profiles if fp.profile_name.startswith(self.dns_security_name)]) == 1

    def _create_device_template(self) -> None:
        templates = self.session.api.templates
        dt = DeviceTemplate.get(COPY_DEVICE_TEMPLATE_FROM, self.session)
        dt.template_name = self.device_template_name
        dt.factory_default = False
        dt.associate_feature_template(CiscoSecureInternetGatewayModel.type, UUID(self.sig_uuid))
        dt.associate_policy(self.pol_dict["Localized-Policy"])
        dt.associate_security_policy(self.pol_dict["UnifiedSecurityPolicy"])
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
                    if_name="ipsec255",
                    auto=True,
                    shutdown=False,
                    description="Main interface for SIG",
                    unnumbered=False,
                    address=IPv4Interface("192.168.0.0/24"),
                    tunnel_source_interface="GigabitEthernet3",
                    tunnel_route_via="GigabitEthernet3",
                    tunnel_destination="dynamic",
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
                            active_interface="ipsec255",
                            active_interface_weight=10,
                            backup_interface="None",
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
            tracker_src_ip=IPv4Interface("192.168.0.0/32"),
            tracker=[
                Tracker(
                    name="health-check-tracker",
                    endpoint_api_url="http://api.example.com/health",
                    threshold=100,
                    interval=60,
                    multiplier=2,
                    tracker_type="SIG",
                )
            ],
        )
        self.sig_uuid = templates.create(cisco_sig)

    def _create_security_policy(self) -> None:
        api = self.session.api.policy
        # --------------------------
        # DNS Security Policy
        # --------------------------
        ldl = LocalDomainList(name=create_name_with_run_id("LocalDomainList"))
        ldl.add_domain(".*.cisco.com")
        ldl.add_domain("cisco.com")
        self.pol_dict["LocalDomainList"] = api.lists.create(ldl)
        # Must be defined in vManage manually
        umbrella_data = api.lists.get(UmbrellaDataList).single_or_default()
        definition = DnsSecurityDefinition.create_match_all_vpns_config(
            umbrella_default=True,
            umbrella_data=Reference(ref=umbrella_data.list_id),
            dns_crypt=True,
            dns_server_ip="10.0.2.1",
            local_domain_bypass_list=Reference(ref=self.pol_dict["LocalDomainList"]),
            child_org_id=54020,
        )
        dsp = DnsSecurityPolicy(name=self.dns_security_name, definition=definition)
        self.pol_dict["DnsSecurityPolicy"] = api.definitions.create(dsp)
        # --------------------------
        # Zone Based Firewall Policy
        # --------------------------
        ipp = IntrusionPreventionPolicy(
            name=create_name_with_run_id("IntrusionPreventionPolicy"),
            mode="unified",
            definition=IntrusionPreventionDefinition(signature_set="balanced", inspection_mode="detection"),
        )
        self.pol_dict["IntrusionPreventionPolicy"] = api.definitions.create(ipp)
        aip = AdvancedInspectionProfilePolicy(
            name=create_name_with_run_id("AIP"),
            definition=AdvancedInspectionProfileDefinition(
                tls_decryption_action="decrypt",
                intrusion_prevention=Reference(ref=self.pol_dict["IntrusionPreventionPolicy"]),
            ),
        )
        self.pol_dict["AdvancedInspectionProfilePolicy"] = api.definitions.create(aip)
        zbfwp = ZoneBasedFWPolicy(name=create_name_with_run_id("ZoneBasedFWPolicy"))
        zbfwp.mode = "unified"
        zbfwp.add_zone_pair("self", "default")
        zbfwp_seq = zbfwp.add_ipv4_rule(name=create_name_with_run_id("IPv4Rule"), base_action="inspect")
        zbfwp_seq.set_advanced_inspection_profile_action(profile_id=self.pol_dict["AdvancedInspectionProfilePolicy"])
        zbfwp_seq.match_source_port(ports=set([34000, 34568]))
        zbfwp_seq.match_destination_ports(ports=set([34775, 37732]))
        self.pol_dict["ZoneBasedFWPolicy"] = api.definitions.create(zbfwp)
        # --------------------------
        # Unified Security Policy
        # --------------------------
        usp = UnifiedSecurityPolicy(policy_name=self.security_policy_name)
        usp.add_dns_security(self.pol_dict["DnsSecurityPolicy"])
        usp.add_ng_firewall(self.pol_dict["ZoneBasedFWPolicy"])
        self.pol_dict["UnifiedSecurityPolicy"] = api.security.create(usp)

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
        # ----------------------------
        # Delete Localized Policy
        # ----------------------------
        policy.localized.delete(cls.pol_dict["Localized-Policy"])
        policy.definitions.delete(QoSMapPolicy, cls.pol_dict["QosMap-Policy"])
        policy.lists.delete(ClassMapList, cls.pol_dict["VOICE"])
        policy.lists.delete(ClassMapList, cls.pol_dict["CRITICAL_DATA"])
        policy.lists.delete(ClassMapList, cls.pol_dict["BULK"])
        policy.lists.delete(ClassMapList, cls.pol_dict["DEFAULT"])
        policy.lists.delete(ClassMapList, cls.pol_dict["INTERACTIVE_VIDEO"])
        policy.lists.delete(ClassMapList, cls.pol_dict["CONTROL_SIGNALING"])
        # ----------------------------
        # Delete Security Policy
        # ----------------------------
        policy.security.delete(cls.pol_dict["UnifiedSecurityPolicy"])
        policy.definitions.delete(ZoneBasedFWPolicy, cls.pol_dict["ZoneBasedFWPolicy"])
        policy.definitions.delete(AdvancedInspectionProfilePolicy, cls.pol_dict["AdvancedInspectionProfilePolicy"])
        policy.definitions.delete(IntrusionPreventionPolicy, cls.pol_dict["IntrusionPreventionPolicy"])
        policy.definitions.delete(DnsSecurityPolicy, cls.pol_dict["DnsSecurityPolicy"])
        policy.lists.delete(LocalDomainList, cls.pol_dict["LocalDomainList"])

        cls.runner.clear_ux2()
        return super().tearDownClass()
