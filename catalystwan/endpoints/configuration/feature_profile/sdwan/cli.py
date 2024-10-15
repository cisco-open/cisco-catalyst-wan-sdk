# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
)
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.cli import AnyCliParcel
from catalystwan.typed_list import DataSequence


class CliFeatureProfile(APIEndpoints):
    @versions(">=20.9")
    @get("/v1/feature-profile/sdwan/cli")
    def get_profiles(self, payload: Optional[GetFeatureProfilesParams]) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(">=20.9")
    @post("/v1/feature-profile/sdwan/cli")
    def create_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    @versions(">=20.9")
    @delete("/v1/feature-profile/sdwan/cli/{profile_id}")
    def delete_profile(self, profile_id: UUID) -> None:
        ...

    @versions(">=20.9")
    @get("/v1/feature-profile/sdwan/cli/{profile_id}/{parcel_type}")
    def get_all(self, profile_id: UUID, parcel_type: str) -> DataSequence[Parcel[AnyCliParcel]]:
        ...

    @versions(">=20.9")
    @get("/v1/feature-profile/sdwan/cli/{profile_id}/{parcel_type}/{parcel_id}")
    def get_by_id(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> Parcel[AnyCliParcel]:
        ...

    @versions(">=20.9")
    @post("/v1/feature-profile/sdwan/cli/{profile_id}/{parcel_type}")
    def create(self, profile_id: UUID, parcel_type: str, payload: AnyCliParcel) -> ParcelCreationResponse:
        ...

    @versions(">=20.9")
    @put("/v1/feature-profile/sdwan/cli/{profile_id}/{parcel_type}/{parcel_id}")
    def update(
        self, profile_id: UUID, parcel_type: str, parcel_id: UUID, payload: AnyCliParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(">=20.9")
    @delete("/v1/feature-profile/sdwan/cli/{profile_id}/{parcel_type}/{parcel_id}")
    def delete(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> None:
        ...
