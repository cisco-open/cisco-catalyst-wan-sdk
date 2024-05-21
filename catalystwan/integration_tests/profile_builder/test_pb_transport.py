from catalystwan.integration_tests.profile_builder.base import TestFeatureProfileBuilder
from catalystwan.integration_tests.test_data import cellular_controller_parcel, cellular_profile_parcel, gps_parcel
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload


class TestTransportFeatureProfileBuilder(TestFeatureProfileBuilder):
    def setUp(self) -> None:
        self.fp_name = "FeatureProfileBuilderTransport"
        self.fp_description = "Transport feature profile"
        self.builder = self.session.api.builders.feature_profiles.create_builder("transport")
        self.builder.add_profile_name_and_description(
            feature_profile=FeatureProfileCreationPayload(name=self.fp_name, description=self.fp_description)
        )

    def test_when_build_profile_with_cellular_controller_and_subelements_expect_success(self):
        # Arrange
        parent_tag = self.builder.add_parcel_cellular_controller(cellular_controller_parcel)
        self.builder.add_cellular_controller_subparcel(parent_tag, cellular_profile_parcel)
        self.builder.add_cellular_controller_subparcel(parent_tag, gps_parcel)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def tearDown(self) -> None:
        target_profile = (
            self.session.api.sdwan_feature_profiles.transport.get_profiles()
            .filter(profile_name=self.fp_name)
            .single_or_default()
        )
        if target_profile:
            # In case of a failed test, the profile might not have been created
            self.session.api.sdwan_feature_profiles.transport.delete_profile(target_profile.profile_id)
