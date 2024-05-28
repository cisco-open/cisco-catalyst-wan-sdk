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
from catalystwan.models.configuration.feature_profile.sdwan.dns_security import AnyDnsSecurityParcel
from catalystwan.typed_list import DataSequence


class DnsSecurityFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/dns-security")
    def create_dns_security_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/dns-security")
    def get_dns_security_feature_profiles(self, params: GetFeatureProfilesParams) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/dns-security/{profile_id}")
    def get_dns_security_feature_profile(
        self, profile_id: str, params: GetFeatureProfilesParams
    ) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put("/v1/feature-profile/sdwan/dns-security/{profile_id}")
    def edit_dns_security_feature_profile(
        self, profile_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete("/v1/feature-profile/sdwan/dns-security/{profile_id}")
    def delete_dns_security_feature_profile(self, profile_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/dns-security/{profile_id}/{dns_security_list_type}")
    def create(
        self, profile_id: UUID, dns_security_list_type: str, payload: AnyDnsSecurityParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete("/v1/feature-profile/sdwan/dns-security/{profile_id}/{dns_security_list_type}/{list_object_id}")
    def delete(self, profile_id: UUID, dns_security_list_type: str, list_object_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put("/v1/feature-profile/sdwan/dns-security/{profile_id}/{dns_security_list_type}/{list_object_id}")
    def update(
        self,
        profile_id: UUID,
        dns_security_list_type: str,
        list_object_id: UUID,
        payload: AnyDnsSecurityParcel,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/dns-security/{profile_id}/{dns_security_list_type}/{list_object_id}")
    def get_by_id(self, profile_id: UUID, dns_security_list_type: str, list_object_id: UUID) -> Parcel:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/dns-security/{profile_id}/{dns_security_list_type}", resp_json_key="data")
    def get_all(self, profile_id: UUID, dns_security_list_type: str) -> DataSequence[Parcel]:
        ...
