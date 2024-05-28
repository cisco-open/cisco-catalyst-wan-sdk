# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
)
from catalystwan.models.configuration.feature_profile.parcel import ParcelAssociationPayload, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.service import (
    AnyLanVpnInterfaceParcel,
    AnyTopLevelServiceParcel,
)
from catalystwan.typed_list import DataSequence


class ServiceFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/service")
    def get_sdwan_service_feature_profiles(
        self, payload: Optional[GetFeatureProfilesParams]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service")
    def create_sdwan_service_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{profile_uuid}")
    def delete_sdwan_service_feature_profile(self, profile_uuid: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{profile_uuid}/{parcel_type}")
    def create_service_parcel(
        self, profile_uuid: UUID, parcel_type: str, payload: AnyTopLevelServiceParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/service/{profile_uuid}/{parcel_type}/{parcel_uuid}")
    def delete_service_parcel(self, profile_uuid: UUID, parcel_type: str, parcel_uuid: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{profile_uuid}/lan/vpn/{vpn_uuid}/{parcel_type}")
    def create_lan_vpn_sub_parcel(
        self, profile_uuid: UUID, vpn_uuid: UUID, parcel_type: str, payload: AnyLanVpnInterfaceParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{profile_uuid}/lan/vpn/{vpn_uuid}/{parcel_type}")
    def associate_parcel_with_vpn(
        self, profile_uuid: UUID, vpn_uuid: UUID, parcel_type: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...

    # Ethernet, IPSec, SVI
    @versions(supported_versions=(">=20.9"), raises=False)
    @post(
        "/v1/feature-profile/sdwan/service/{profile_uuid}/lan/vpn/"
        "{vpn_uuid}/{interface_parcel_type}/{interface_uuid}/dhcp-server"
    )
    def associate_dhcp_server_with_vpn_interface(
        self,
        profile_uuid: UUID,
        vpn_uuid: UUID,
        interface_parcel_type: str,
        interface_uuid: UUID,
        payload: ParcelAssociationPayload,
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/service/{profile_id}/lan/vpn/{vpn_id}/{parcel_type}")
    def associate_with_vpn(
        self, profile_id: UUID, vpn_id: UUID, parcel_type: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...
