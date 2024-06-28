# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.policy.definition.zone_based_firewall import ZoneBasedFWPolicy
from catalystwan.models.policy.security import SecurityPolicy, UnifiedSecurityPolicy
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert
from catalystwan.utils.config_migration.converters.policy.security_policy import convert_security_policy


class TestSecurityPolicyConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.convert_context = PolicyConvertContext()
        self.policy_uuid = uuid4()

    def test_failed_due_to_missing_ng_firewall_entries(self):
        policy = UnifiedSecurityPolicy(policy_name="failed_policy")
        policy.add_ng_firewall(uuid4())

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)

        assert conversion_result.status == "failed"
        assert len(conversion_result.info) == 1
        assert conversion_result.output.parcel_name == "failed_policy"

    def test_converted_with_ng_firewall_assembly_uuid_zone_entries(self):
        src_zone = uuid4()
        dst_zone = uuid4()
        policy = UnifiedSecurityPolicy(policy_name="passed_convert1")
        ng_fw = policy.add_ng_firewall(uuid4())
        ng_fw.add_zone_pair(src_zone, dst_zone)

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)

        assert conversion_result.status == "complete"
        assert len(conversion_result.info) == 0
        assert conversion_result.output.parcel_name == "passed_convert1"
        assert len(conversion_result.output.assembly) == 1
        assert len(conversion_result.output.assembly[0].ng_firewall.entries) == 1
        assert conversion_result.output.assembly[0].ng_firewall.entries[0].src_zone.ref_id.value == str(src_zone)
        assert conversion_result.output.assembly[0].ng_firewall.entries[0].dst_zone.ref_id.value == str(dst_zone)
        assert self.convert_context.security_policy_residues[self.policy_uuid]

    def test_converted_with_ng_firewall_assembly_literal_zone_entries(self):
        src_zone = "default"
        dst_zone = "self"
        policy = UnifiedSecurityPolicy(policy_name="passed_convert1")
        ng_fw = policy.add_ng_firewall(uuid4())
        ng_fw.add_zone_pair(src_zone, dst_zone)

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)

        assert conversion_result.status == "complete"
        assert len(conversion_result.info) == 0
        assert conversion_result.output.parcel_name == "passed_convert1"
        assert len(conversion_result.output.assembly) == 1
        assert len(conversion_result.output.assembly[0].ng_firewall.entries) == 1
        assert conversion_result.output.assembly[0].ng_firewall.entries[0].src_zone.value == src_zone
        assert conversion_result.output.assembly[0].ng_firewall.entries[0].dst_zone.value == dst_zone
        assert self.convert_context.security_policy_residues[self.policy_uuid]

    def test_converted_with_ng_firewall_zone_entries(self):
        zone_based_fw_uuid = uuid4()
        zone_based_fw = ZoneBasedFWPolicy(name="zone_fw_1")
        zone_based_fw.add_zone_pair(uuid4(), uuid4())
        zone_based_fw.add_zone_pair(uuid4(), uuid4())

        out = convert(zone_based_fw, zone_based_fw_uuid, self.convert_context)  # move to zone based fw tests?
        assert out.status == "complete"
        assert len(self.convert_context.zone_based_firewall_residues[zone_based_fw_uuid]) == 2

        policy = UnifiedSecurityPolicy(policy_name="passed_convert2")
        policy.add_ng_firewall(zone_based_fw_uuid)

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)
        assert conversion_result.status == "complete"
        assert len(conversion_result.info) == 0
        assert conversion_result.output.parcel_name == "passed_convert2"
        assert len(conversion_result.output.assembly) == 1
        assert len(conversion_result.output.assembly[0].ng_firewall.entries) == 2
        assert self.convert_context.security_policy_residues[self.policy_uuid]

        for i, entry in enumerate(conversion_result.output.assembly[0].ng_firewall.entries):
            assert entry.src_zone.ref_id.value == str(zone_based_fw.definition.entries[i].source_zone_id)
            assert entry.dst_zone.ref_id.value == str(zone_based_fw.definition.entries[i].destination_zone_id)

    def test_converted_with_aip_action(self):
        aip_uuid = uuid4()
        policy = UnifiedSecurityPolicy(policy_name="policy")
        policy.add_advanced_inspection_profile(aip_uuid)

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)

        assert conversion_result.status == "complete"
        assert len(conversion_result.info) == 0
        assert len(conversion_result.output.assembly) == 1
        assert conversion_result.output.assembly[0].advanced_inspection_profile.ref_id.value == str(aip_uuid)
        assert self.convert_context.security_policy_residues[self.policy_uuid]

    def test_converted_with_dns_security_action(self):
        policy = UnifiedSecurityPolicy(policy_name="policy")
        policy.add_dns_security(uuid4())

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)

        assert conversion_result.status == "partial"
        assert len(conversion_result.info) == 1
        assert len(conversion_result.output.assembly) == 0
        assert self.convert_context.security_policy_residues[self.policy_uuid]

    def test_converted_with_ssl_decryption_security_action(self):
        ssl_uuid = uuid4()
        policy = SecurityPolicy(policy_name="policy")
        policy.add_ssl_decryption(ssl_uuid)

        conversion_result = convert_security_policy(policy, self.policy_uuid, self.convert_context)

        assert conversion_result.status == "complete"
        assert len(conversion_result.info) == 0
        assert len(conversion_result.output.assembly) == 1
        assert conversion_result.output.assembly[0].ssl_decryption.ref_id.value == str(ssl_uuid)
        assert self.convert_context.security_policy_residues[self.policy_uuid]
