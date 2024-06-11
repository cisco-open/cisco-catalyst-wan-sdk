# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
)
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.application_priority import AnyApplicationPriorityParcel
from catalystwan.typed_list import DataSequence


class ApplicationPriorityFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/application-priority")
    def create_application_priority_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/application-priority")
    def get_application_priority_feature_profiles(
        self, params: GetFeatureProfilesParams
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/application-priority/{profile_id}")
    def get_application_priority_feature_profile(
        self, profile_id: str, params: GetFeatureProfilesParams
    ) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put("/v1/feature-profile/sdwan/application-priority/{profile_id}")
    def edit_application_priority_feature_profile(
        self, profile_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete("/v1/feature-profile/sdwan/application-priority/{profile_id}")
    def delete_application_priority_feature_profile(self, profile_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/application-priority/{profile_id}/{application_priority_list_type}")
    def create(
        self, profile_id: UUID, application_priority_list_type: str, payload: AnyApplicationPriorityParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete(
        "/v1/feature-profile/sdwan/application-priority/{profile_id}/{application_priority_list_type}/{list_object_id}"
    )
    def delete(self, profile_id: UUID, application_priority_list_type: str, list_object_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put(
        "/v1/feature-profile/sdwan/application-priority/{profile_id}/{application_priority_list_type}/{list_object_id}"
    )
    def update(
        self,
        profile_id: UUID,
        application_priority_list_type: str,
        list_object_id: UUID,
        payload: AnyApplicationPriorityParcel,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/application-priority/{profile_id}/{application_priority_list_type}/{list_object_id}"
    )
    def get_by_id(self, profile_id: UUID, application_priority_list_type: str, list_object_id: UUID) -> Parcel:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get(
        "/v1/feature-profile/sdwan/application-priority/{profile_id}/{application_priority_list_type}",
        resp_json_key="data",
    )
    def get_all(self, profile_id: UUID, application_priority_list_type: str) -> DataSequence[Parcel]:
        ...
