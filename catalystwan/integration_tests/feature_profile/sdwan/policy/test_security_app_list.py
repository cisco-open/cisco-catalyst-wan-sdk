# Copyright 2024 Cisco Systems, Inc. and its affiliates
from catalystwan.integration_tests.base import create_name_with_run_id
from catalystwan.integration_tests.feature_profile.sdwan.policy.base import PolicyTestCaseBase
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.application_list import (
    SecurityApplicationListParcel,
)
from catalystwan.typed_list import DataSequence


class TestSecurityApplicationListParcel(PolicyTestCaseBase):
    parcel_type = SecurityApplicationListParcel

    def test_get_all_parcels(self):
        parcels = self.policy_api.get(self.profile_uuid, self.parcel_type)
        assert type(parcels) is DataSequence

    def test_createsecurity_application_list_parcel(self):
        # Arrange
        parcel_name = create_name_with_run_id("sal")
        sal = SecurityApplicationListParcel(parcel_name=parcel_name)
        sal.add_application_family("web")
        sal.add_application_family("file-server")
        sal.add_application_family("audio-video")
        # Act
        self.created_id = self.policy_api.create_parcel(self.profile_uuid, sal).id
        parcel = self.policy_api.get(self.profile_uuid, self.parcel_type, parcel_id=self.created_id)
        # Assert
        assert parcel.payload.parcel_name == parcel_name
        assert len(parcel.payload.entries) == 3
        assert parcel.payload.entries[0].app_list_family.value == "web"
        assert parcel.payload.entries[1].app_list_family.value == "file-server"
        assert parcel.payload.entries[2].app_list_family.value == "audio-video"
