# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.policy.list.threat_grid_api_key import ThreatGridApiKeyEntry, ThreatGridApiKeyList
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert


class TestThreatGridApiConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_threat_grid_api_conversion(self):
        # Arrange
        policy = ThreatGridApiKeyList(
            name="ThreatGridApiKeyList",
            description="ThreatGridApiKeyList",
            entries=[
                ThreatGridApiKeyEntry(region="eur", api_key="123"),
                ThreatGridApiKeyEntry(region="nam", api_key="456"),
            ],
        )
        # Act -- This action adds object to the context
        convert(policy, uuid4(), self.context)
        threat = self.context.threat_grid_api
        # Assert
        assert threat.get_region_api_key("eur") == "123"
        assert threat.get_region_api_key("nam") == "456"
