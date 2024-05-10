import pytest

from catalystwan.exceptions import ManagerHTTPError
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.cli import ConfigParcel


class TestCliConfigParcel(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.cli
        self.profile_id = self.api.create_profile("TestCliProfileService", "Description").id
        self.config_group_id = self.session.api.config_group.create(
            "TestCLIConfigGroup", "TestCLIConfigGroup", "sdwan", [self.profile_id]
        ).id

    def test_create_cli_config_parcel(self):
        config_parcel = ConfigParcel(
            parcel_name="ConfigCliDefault", parcel_description="Config CLI Parcel", config="test-config"
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, config_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel_by_id(self.profile_id, parcel_id).payload

        assert parcel.parcel_name == "ConfigCliDefault"
        assert parcel.config == "test-config"

    def test_update_cli_config_parcel(self):
        config_parcel = ConfigParcel(
            parcel_name="ConfigCliDefault", parcel_description="Config CLI Parcel", config="test-config"
        )
        parcel_id = self.api.create_parcel(self.profile_id, config_parcel).id
        parcel = self.api.get_parcel_by_id(self.profile_id, parcel_id).payload
        parcel.config = "updated-config"
        self.api.update_parcel(self.profile_id, parcel_id, parcel)
        parcel = self.api.get_parcel_by_id(self.profile_id, parcel_id).payload

        assert parcel.config == "updated-config"

    def test_delete_cli_config_parcel(self):
        config_parcel = ConfigParcel(
            parcel_name="ConfigCliDefault", parcel_description="Config CLI Parcel", config="test-config"
        )
        parcel_id = self.api.create_parcel(self.profile_id, config_parcel).id
        self.api.delete_parcel(self.profile_id, parcel_id)

        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel_by_id(self.profile_id, parcel_id).payload

    def tearDown(self) -> None:
        self.session.api.config_group.delete(self.config_group_id)
        self.api.delete_profile(self.profile_id)
