# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.policy.definition.intrusion_prevention import (
    IntrusionPreventionDefinition,
    IntrusionPreventionPolicy,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestAdvancedMalwareProtectionConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_intrusion_prevention_unified_conversion(self):
        # Arrange
        ipp = IntrusionPreventionPolicy(
            name="ip_unified",
            mode="unified",
            definition=IntrusionPreventionDefinition(
                signature_set="balanced",
                inspection_mode="detection",
                signature_white_list=None,
                log_level="error",
                logging=[],
                target_vpns=[1, 2, 3],
                custom_signature=False,
            ),
        )
        uuid = uuid4()
        # Act
        parcel = convert(ipp, uuid, context=self.context)
        # Assert
        assert parcel.parcel_name == "ip_unified"
        assert parcel.signature_set.value == "balanced"
        assert parcel.inspection_mode.value == "detection"
        assert parcel.signature_allowed_list is None
        assert parcel.log_level.value == "error"
        assert parcel.custom_signature.value is False

        assert len(self.context.intrusion_prevention_target_vpns_id) == 1
        assert self.context.intrusion_prevention_target_vpns_id[uuid] == ipp.definition.target_vpns

    def test_intrusion_prevention_security_conversion(self):
        # Arrange
        ipp = IntrusionPreventionPolicy(
            name="ip_security",
            mode="security",
            definition=IntrusionPreventionDefinition(
                signature_set="balanced",
                inspection_mode="detection",
                signature_white_list=None,
                log_level="error",
                logging=[],
                target_vpns=[1, 2, 3],
                custom_signature=False,
            ),
        )
        uuid = uuid4()
        # Act
        with self.assertRaises(CatalystwanConverterCantConvertException) as ccce:
            convert(ipp, uuid, context=self.context)
        # Assert
        assert len(self.context.intrusion_prevention_target_vpns_id) == 0
        assert "Policy Mode 'security' is not supported for Intrusion Prevention Policy" in str(ccce.exception)
