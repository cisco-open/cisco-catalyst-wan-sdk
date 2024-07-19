from typing import Optional

from catalystwan.integration_tests.base import TestCaseBase
from catalystwan.models.settings import ThreatGridApi


class TestThreadGridApi(TestCaseBase):
    created_thread: Optional[ThreatGridApi] = None

    def test_thread_grid_api(self):
        # Arrange
        thread = ThreatGridApi()
        thread.set_region_api_key("eur", "1234567890")
        thread.set_region_api_key("nam", "0987654321")
        # Act
        response = self.session.endpoints.configuration_settings.create_threat_grid_api_key(thread)
        self.created_thread = response.single_or_default()
        # Assert
        assert self.created_thread is not None
        assert self.created_thread.entries[0].region == "nam"
        assert self.created_thread.entries[0].apikey == "0987654321"
        assert self.created_thread.entries[1].region == "eur"
        assert self.created_thread.entries[1].apikey == "1234567890"

    def tearDown(self) -> None:
        if self.created_thread:
            self.session.endpoints.configuration_settings.create_threat_grid_api_key(ThreatGridApi())
        return super().tearDown()
