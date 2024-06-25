import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.amp import (
    AdvancedMalwareProtectionParcel,
)
from catalystwan.models.policy.definition.amp import (
    AdvancedMalwareProtectionDefinition,
    AdvancedMalwareProtectionPolicy,
)
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestAdvancedMalwareProtectionConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_amp_security_conversion(self):
        amp_v1_entry = AdvancedMalwareProtectionPolicy(
            name="amp_security",
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

        uuid = uuid4()
        parcel = convert(amp_v1_entry, uuid, context=self.context).output

        assert isinstance(parcel, AdvancedMalwareProtectionParcel)
        assert parcel.parcel_name == "amp_security"
        assert parcel.match_all_vpn.value is False
        assert parcel.file_reputation_cloud_server.value == "eur"
        assert parcel.file_reputation_est_server.value == "eur"
        assert parcel.file_reputation_alert.value == "warning"
        assert parcel.file_analysis_enabled.value is False
        assert parcel.file_analysis_file_types is None
        assert parcel.file_analysis_alert.value == "info"
        assert parcel.file_analysis_cloud_server.value == "eur"

        assert len(self.context.amp_target_vpns_id) == 1
        assert self.context.amp_target_vpns_id[uuid] == amp_v1_entry.definition.target_vpns

    def test_amp_unified_conversion(self):
        amp_v1_entry = AdvancedMalwareProtectionPolicy(
            name="amp_unified",
            mode="unified",
            definition=AdvancedMalwareProtectionDefinition(
                match_all_vpn=True,
                file_reputation_est_server="eur",
                file_reputation_cloud_server="eur",
                file_reputation_alert="info",
                file_analysis_enabled=False,
                file_analysis_file_types=[],
                file_analysis_alert="info",
                file_analysis_cloud_server="eur",
            ),
        )

        uuid = uuid4()
        parcel = convert(amp_v1_entry, uuid, context=self.context).output

        assert isinstance(parcel, AdvancedMalwareProtectionParcel)
        assert parcel.parcel_name == "amp_unified"
        assert parcel.match_all_vpn.value is True
        assert parcel.file_reputation_cloud_server.value == "eur"
        assert parcel.file_reputation_est_server.value == "eur"
        assert parcel.file_reputation_alert.value == "info"
        assert parcel.file_analysis_enabled.value is False
        assert parcel.file_analysis_file_types is None
        assert parcel.file_analysis_alert.value == "info"
        assert parcel.file_analysis_cloud_server.value == "eur"
        assert len(self.context.amp_target_vpns_id) == 0

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
                file_analysis_file_types=["pdf", "mscab"],
                file_analysis_cloud_server="",
            ),
        )

        uuid = uuid4()
        parcel = convert(amp_v1_entry, uuid, context=self.context).output

        assert isinstance(parcel, AdvancedMalwareProtectionParcel)
        assert parcel.parcel_name == "amp_empty_literals"
        assert parcel.match_all_vpn.value is True
        assert parcel.file_reputation_cloud_server.value == "eur"
        assert parcel.file_reputation_est_server.value == "eur"
        assert parcel.file_reputation_alert.value == "critical"
        assert parcel.file_analysis_enabled.value is True
        assert parcel.file_analysis_file_types.value == ["pdf", "mscab"]
        assert parcel.file_analysis_alert is None
        assert parcel.file_analysis_cloud_server is None
        assert len(self.context.amp_target_vpns_id) == 0
