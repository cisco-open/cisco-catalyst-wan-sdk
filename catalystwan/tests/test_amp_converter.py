import unittest

from catalystwan.models.policy.definition.amp import (
    AdvancedMalwareProtectionDefinition,
    AdvancedMalwareProtectionPolicy,
)
from catalystwan.utils.config_migration.converters.policy.policy_definitions import advanced_malware_protection


class TestAdvancedMalwareProtectionConverter(unittest.TestCase):
    def test_amp_security_conversion(self):
        amp_v1_entry = AdvancedMalwareProtectionPolicy(
            name="amp2",
            mode="security",
            definition=AdvancedMalwareProtectionDefinition(
                match_all_vpn=False,
                file_reputation_est_server="eur",
                file_reputation_cloud_server="eur",
                file_reputation_alert="warning",
                file_analysis_enabled=False,
                file_analysis_file_types=[],
                file_analysis_alert="info",
                file_analysis_cloud_server="eur",
                target_vpns=[1, 2, 3],
            ),
        )

        advanced_malware_protection(amp_v1_entry)

    def test_amp_unified_conversion(self):
        amp_v1_entry = AdvancedMalwareProtectionPolicy(
            name="amp_unified",
            mode="unified",
            definition=AdvancedMalwareProtectionDefinition(
                match_all_vpn=True,
                file_reputation_est_server="eur",
                file_reputation_cloud_server="eur",
                file_reputation_alert="warning",
                file_analysis_enabled=False,
                file_analysis_file_types=[],
                file_analysis_alert="info",
                file_analysis_cloud_server="eur",
            ),
        )

        advanced_malware_protection(amp_v1_entry)

    def test_amp_conversion_with_empty_literals(self):
        amp_v1_entry = AdvancedMalwareProtectionPolicy(
            name="amp_empty_literals",
            mode="unified",
            definition=AdvancedMalwareProtectionDefinition(
                match_all_vpn=True,
                file_reputation_est_server="eur",
                file_reputation_cloud_server="eur",
                file_reputation_alert="critical",
                file_analysis_enabled=True,
                file_analysis_alert="",
                file_analysis_file_types=["pdf"],
                file_analysis_cloud_server="",
            ),
        )

        advanced_malware_protection(amp_v1_entry)
