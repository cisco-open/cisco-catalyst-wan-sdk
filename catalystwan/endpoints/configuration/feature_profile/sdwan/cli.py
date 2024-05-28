# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
)
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelId
from catalystwan.models.configuration.feature_profile.sdwan.cli import ConfigParcel
from catalystwan.typed_list import DataSequence


class CliFeatureProfile(APIEndpoints):
    # @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/cli")
    def get_profiles(self, payload: Optional[GetFeatureProfilesParams]) -> DataSequence[FeatureProfileInfo]:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/cli")
    def create_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/cli/{profile_id}")
    def delete_profile(self, profile_id: UUID) -> None:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/cli/{profile_id}/config")
    def get_all(self, profile_id: UUID) -> DataSequence[Parcel]:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/cli/{profile_id}/config/{parcel_id}")
    def get_by_id(self, profile_id: UUID, parcel_id: UUID) -> Parcel[ConfigParcel]:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/cli/{profile_id}/config")
    def create(self, profile_id: UUID, payload: ConfigParcel) -> ParcelId:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/feature-profile/sdwan/cli/{profile_id}/config/{parcel_id}")
    def update(self, profile_id: UUID, parcel_id: UUID, payload: ConfigParcel) -> None:
        ...

    # @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/cli/{profile_id}/config/{parcel_id}")
    def delete(self, profile_id: UUID, parcel_id: UUID) -> None:
        ...
