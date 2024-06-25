# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.aip import (
    AdvancedInspectionProfileParcel,
)
from catalystwan.models.policy.definition.aip import (
    AdvancedInspectionProfileDefinition,
    AdvancedInspectionProfilePolicy,
)
from catalystwan.models.policy.policy_definition import Reference
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestAdvancedInspectionProfileParcel(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_advanced_inspection_profile_conversion(self):
        # Arrange
        ip = uuid4()
        uf = uuid4()
        amp = uuid4()
        sdp = uuid4()
        aip = AdvancedInspectionProfilePolicy(
            name="aip",
            description="test_description",
            optimized="false",
            definition=AdvancedInspectionProfileDefinition(
                tls_decryption_action="skipDecrypt",
                intrusion_prevention=Reference(ref=ip),
                url_filtering=Reference(ref=uf),
                advanced_malware_protection=Reference(ref=amp),
                ssl_utd_decrypt_profile=Reference(ref=sdp),
            ),
        )
        uuid = uuid4()
        # Act
        parcel = convert(aip, uuid, context=self.context).output
        # Assert
        assert isinstance(parcel, AdvancedInspectionProfileParcel)
        assert parcel.parcel_name == "aip"
        assert parcel.parcel_description == "test_description"
        assert parcel.tls_decryption_action.value == "skipDecrypt"
        assert parcel.intrusion_prevention.ref_id.value == str(ip)
        assert parcel.url_filtering.ref_id.value == str(uf)
        assert parcel.advanced_malware_protection.ref_id.value == str(amp)
        assert parcel.ssl_decryption_profile.ref_id.value == str(sdp)
