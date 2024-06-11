# Copyright 2023 Cisco Systems, Inc. and its affiliates
from catalystwan.integration_tests.profile_builder.base import TestFeatureProfileBuilder
from catalystwan.integration_tests.test_data import (
    bgp_parcel,
    cellular_controller_parcel,
    cellular_profile_parcel,
    gps_parcel,
    ospf_parcel,
    ospfv3ipv4_parcel,
    ospfv3ipv6_parcel,
)
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import TransportVpnParcel


class TestTransportFeatureProfileBuilder(TestFeatureProfileBuilder):
    def setUp(self) -> None:
        self.fp_name = "FeatureProfileBuilderTransport"
        self.fp_description = "Transport feature profile"
        self.builder = self.session.api.builders.feature_profiles.create_builder("transport")
        self.builder.add_profile_name_and_description(
            feature_profile=FeatureProfileCreationPayload(name=self.fp_name, description=self.fp_description)
        )
        self.api = self.session.api.sdwan_feature_profiles.transport

    def test_when_build_profile_with_cellular_controller_and_subelements_expect_success(self):
        # Arrange
        parent_tag = self.builder.add_parcel_cellular_controller(cellular_controller_parcel)
        self.builder.add_cellular_controller_subparcel(parent_tag, cellular_profile_parcel)
        self.builder.add_cellular_controller_subparcel(parent_tag, gps_parcel)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def test_when_build_profile_with_vpn_and_routing_attached_expect_success(self):
        # Arrange
        service_vpn_parcel = TransportVpnParcel(
            parcel_name="MinimumSpecifiedTransportVpnParcel",
            description="Description",
        )
        vpn_tag = self.builder.add_parcel_vpn(service_vpn_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, ospf_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, ospfv3ipv4_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, ospfv3ipv6_parcel)
        self.builder.add_parcel_routing_attached(vpn_tag, bgp_parcel)
        # Act
        report = self.builder.build()
        # Assert
        assert len(report.failed_parcels) == 0

    def tearDown(self) -> None:
        target_profile = self.api.get_profiles().filter(profile_name=self.fp_name).single_or_default()
        if target_profile:
            # In case of a failed test, the profile might not have been created
            self.api.delete_profile(target_profile.profile_id)
