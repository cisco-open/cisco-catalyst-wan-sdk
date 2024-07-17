# Copyright 2024 Cisco Systems, Inc. and its affiliates

from catalystwan.integration_tests.base import create_name_with_run_id
from catalystwan.integration_tests.feature_profile.sdwan.policy.base import PolicyTestCaseBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import ExtendedCommunityParcel
from catalystwan.typed_list import DataSequence


class TestExtendedCommunityParcel(PolicyTestCaseBase):
    parcel_type = ExtendedCommunityParcel

    def test_get_all_parcels(self):
        parcels = self.policy_api.get(self.profile_uuid, self.parcel_type)
        assert type(parcels) is DataSequence

    def test_create_extended_community_parcel(self):
        # Arrange
        parcel_name = create_name_with_run_id("ext")
        ext = ExtendedCommunityParcel(parcel_name=parcel_name)
        ext.add_route_target_community(100, 2000)
        ext.add_route_target_community(300, 5000)
        ext.add_site_of_origin_community("1.2.3.4", 1000)
        ext.add_site_of_origin_community("10.20.30.40", 3000)
        # Act
        self.created_id = self.policy_api.create_parcel(self.profile_uuid, ext).id
        parcel = self.policy_api.get(self.profile_uuid, self.parcel_type, parcel_id=self.created_id)
        # Assert
        assert parcel.payload.parcel_name == parcel_name
        assert len(parcel.payload.entries) == 4
        assert parcel.payload.entries[0].extended_community.value == "rt 100:2000"
        assert parcel.payload.entries[1].extended_community.value == "rt 300:5000"
        assert parcel.payload.entries[2].extended_community.value == "soo 1.2.3.4:1000"
        assert parcel.payload.entries[3].extended_community.value == "soo 10.20.30.40:3000"
