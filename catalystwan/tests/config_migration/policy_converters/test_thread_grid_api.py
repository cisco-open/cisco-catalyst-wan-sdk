# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.policy.list.threat_grid_api_key import ThreatGridApiKeyEntry, ThreatGridApiKeyList
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert


class TestThreadGridApiConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_thread_grid_api_conversion(self):
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
        convert(policy, context=self.context)
        thread = self.context.thread_grid_api
        # Assert
        assert len(thread.entries) == 2
        assert thread.entries[0].region == "nam"
        assert thread.entries[0].apikey == "456"
        assert thread.entries[1].region == "eur"
        assert thread.entries[1].apikey == "123"
