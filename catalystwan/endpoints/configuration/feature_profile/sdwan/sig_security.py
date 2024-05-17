# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from pydantic import BaseModel, Field

from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    GetReferenceCountFeatureProfilesPayload,
    SchemaTypeQuery,
)
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelCreationResponse, ParcelSequence
from catalystwan.models.configuration.feature_profile.sdwan.sig_security.sig_security import SIGParcel
from catalystwan.typed_list import DataSequence


class SIGSecurityProfileParams(BaseModel):
    references: bool = Field(default=False)


class SIGSecurity(APIEndpoints):
    @versions(">=20.12", raises=False)
    @get("/v1/feature-profile/sdwan/sig-security/sig/schema", resp_json_key="request")
    def get_sig_security_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...

    @versions(">=20.12")
    @get("/v1/feature-profile/sdwan/sig-security")
    def get_sig_security_feature_profiles(
        self, params: GetReferenceCountFeatureProfilesPayload
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(">=20.12")
    @post("/v1/feature-profile/sdwan/sig-security")
    def create_sig_security_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(">=20.12")
    @get("/v1/feature-profile/sdwan/sig-security/{profile_id}")
    def get_sig_security_feature_profile(
        self, profile_id: str, params: SIGSecurityProfileParams
    ) -> FeatureProfileDetail:
        ...

    @versions(">=20.12")
    @put("/v1/feature-profile/sdwan/sig-security/{profile_id}")
    def edit_sig_security_feature_profile(
        self, profile_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(">=20.12")
    @delete("/v1/feature-profile/sdwan/sig-security/{profile_id}")
    def delete_sig_security_feature_profile(self, profile_id: str) -> None:
        ...

    @versions(">=20.12")
    @get("/v1/feature-profile/sdwan/sig-security/{profile_id}/sig")
    def get_sig_security_parcels(self, profile_id: str) -> ParcelSequence[SIGParcel]:
        ...

    @versions(">=20.12")
    @post("/v1/feature-profile/sdwan/sig-security/{profile_id}/sig")
    def create_sig_security_parcel(self, profile_id: str, payload: SIGParcel) -> ParcelCreationResponse:
        ...

    @versions(">=20.12")
    @get("/v1/feature-profile/sdwan/sig-security/{profile_id}/sig/{parcel_id}")
    def get_sig_security_parcel(self, profile_id: str, parcel_id: str) -> Parcel[SIGParcel]:
        ...

    @versions(">=20.12")
    @put("/v1/feature-profile/sdwan/sig-security/{profile_id}/sig/{parcel_id}")
    def edit_sig_security_parcel(self, profile_id: str, parcel_id: str, payload: SIGParcel) -> ParcelCreationResponse:
        ...

    @versions(">=20.12")
    @delete("/v1/feature-profile/sdwan/sig-security/{profile_id}/sig/{parcel_id}")
    def delete_sig_security_parcel(self, profile_id: str, parcel_id: str) -> None:
        ...
