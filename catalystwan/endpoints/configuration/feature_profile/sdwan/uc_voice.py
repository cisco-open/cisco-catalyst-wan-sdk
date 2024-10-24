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
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice import AnyUcVoiceParcel
from catalystwan.typed_list import DataSequence


class UcVoiceFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/uc-voice")
    def create_uc_voice_feature_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/uc-voice")
    def get_uc_voice_feature_profiles(self, params: GetFeatureProfilesParams) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/uc-voice/{profile_id}")
    def get_uc_voice_feature_profile(self, profile_id: str, params: GetFeatureProfilesParams) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/uc-voice/{profile_id}")
    def edit_uc_voice_feature_profile(
        self, profile_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/uc-voice/{profile_id}")
    def delete_uc_voice_feature_profile(self, profile_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @post("/v1/feature-profile/sdwan/uc-voice/{profile_id}/{uc_voice_list_type}")
    def create(self, profile_id: UUID, uc_voice_list_type: str, payload: AnyUcVoiceParcel) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @delete("/v1/feature-profile/sdwan/uc-voice/{profile_id}/{uc_voice_list_type}/{parcel_id}")
    def delete(self, profile_id: UUID, uc_voice_list_type: str, parcel_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @put("/v1/feature-profile/sdwan/uc-voice/{profile_id}/{uc_voice_list_type}/{parcel_id}")
    def update(
        self,
        profile_id: UUID,
        uc_voice_list_type: str,
        parcel_id: UUID,
        payload: AnyUcVoiceParcel,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/uc-voice/{profile_id}/{uc_voice_list_type}/{parcel_id}")
    def get_by_id(self, profile_id: UUID, uc_voice_list_type: str, parcel_id: UUID) -> Parcel[AnyUcVoiceParcel]:
        ...

    @versions(supported_versions=(">=20.13"), raises=False)
    @get("/v1/feature-profile/sdwan/uc-voice/{profile_id}/{uc_voice_list_type}", resp_json_key="data")
    def get_all(self, profile_id: UUID, uc_voice_list_type: str) -> DataSequence[Parcel[AnyUcVoiceParcel]]:
        ...
