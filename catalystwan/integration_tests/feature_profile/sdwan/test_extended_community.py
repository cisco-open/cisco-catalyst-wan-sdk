from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import ExtendedCommunityParcel
from catalystwan.typed_list import DataSequence

PROFILE_NAME = "Default_Policy_Object_Profile"


class TestExtendedCommunityParcel(TestFeatureProfileModels):
    policy_api: PolicyObjectFeatureProfileAPI

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.policy_api = cls.session.api.sdwan_feature_profiles.policy_object
        cls.profile_uuid = (
            ConfigurationFeatureProfile(cls.session.api.sdwan_feature_profiles.policy_object.session)
            .get_sdwan_feature_profiles()
            .filter(profile_name=PROFILE_NAME)
            .single_or_default()
        ).profile_id

    def setUp(self) -> None:
        self.created_id = None
        return super().setUp()

    def tearDown(self) -> None:
        if self.created_id:
            self.policy_api.delete(self.profile_uuid, ExtendedCommunityParcel, self.created_id)

        return super().tearDown()

    def test_get_all_extended_community_parcels(self):
        parcels = self.policy_api.get(self.profile_uuid, ExtendedCommunityParcel)
        assert type(parcels) is DataSequence

    def test_create_extended_community_parcel(self):
        ext = ExtendedCommunityParcel(parcel_name="ExampleTestName")
        ext.add_route_target_community(100, 2000)
        ext.add_route_target_community(300, 5000)
        ext.add_site_of_origin_community("1.2.3.4", 1000)
        ext.add_site_of_origin_community("10.20.30.40", 3000)

        self.created_id = self.policy_api.create_parcel(self.profile_uuid, ext).id
        parcel = self.policy_api.get(self.profile_uuid, ExtendedCommunityParcel, parcel_id=self.created_id)

        assert parcel.payload.parcel_name == "ExampleTestName"
        assert len(parcel.payload.entries) == 4
        assert parcel.payload.entries[0].extended_community.value == "rt 100:2000"
        assert parcel.payload.entries[1].extended_community.value == "rt 300:5000"
        assert parcel.payload.entries[2].extended_community.value == "soo 1.2.3.4:1000"
        assert parcel.payload.entries[3].extended_community.value == "soo 10.20.30.40:3000"
