import pytest

from catalystwan.api.configuration_groups.parcel import Default, Global
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.application_priority import PolicySettingsParcel


class TestApplicationPriorityParcel(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile("TestApplicationPriorityProfile", "Description").id

    def test_create_policy_settings_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

        assert parcel.parcel_name == "policy_settings_test_parcel"

    def test_update_policy_settings_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
            app_visibility=Default[bool](value=False),
            flow_visibility=Global[bool](value=True),
            app_visibility_ipv6=Global[bool](value=True),
            flow_visibility_ipv6=Global[bool](value=True),
        )
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload
        parcel.app_visibility = Global[bool](value=True)
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

        # Assert
        assert parcel.app_visibility == Global[bool](value=True)

    def test_delete_cli_config_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
            app_visibility=Global[bool](value=True),
            flow_visibility=Global[bool](value=True),
            app_visibility_ipv6=Global[bool](value=True),
            flow_visibility_ipv6=Global[bool](value=True),
        )
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, PolicySettingsParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)
