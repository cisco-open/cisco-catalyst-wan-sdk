from typing import Type

from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.integration_tests.base import TestCaseBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel


class PolicyTestCaseBase(TestCaseBase):
    policy_api: PolicyObjectFeatureProfileAPI
    parcel_type: Type[AnyPolicyObjectParcel]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.policy_api = cls.session.api.sdwan_feature_profiles.policy_object
        cls.profile_uuid = (
            ConfigurationFeatureProfile(cls.session)
            .get_sdwan_feature_profiles()
            .filter(profile_type="policy-object")
            .single_or_default()
        ).profile_id

    def setUp(self) -> None:
        self.created_id = None
        return super().setUp()

    def tearDown(self) -> None:
        if self.created_id:
            self.policy_api.delete(self.profile_uuid, self.parcel_type, self.created_id)

        return super().tearDown()
