# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileDetail,
    FeatureProfileEditPayload,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
    SchemaTypeQuery,
)
from catalystwan.models.configuration.feature_profile.parcel import (
    Parcel,
    ParcelAssociationPayload,
    ParcelCreationResponse,
    ParcelId,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport import (
    AnyTransportParcel,
    CellularControllerParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.vpn import ManagementVpnParcel
from catalystwan.typed_list import DataSequence


class TransportFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/transport")
    def create_transport_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_transport_feature_profiles(self, params: GetFeatureProfilesParams) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}")
    def get_transport_feature_profile(self, profile_id: UUID, params: GetFeatureProfilesParams) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put("/v1/feature-profile/sdwan/transport/{profile_id}")
    def edit_transport_feature_profile(
        self, profile_id: UUID, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{profile_id}")
    def delete_transport_feature_profile(self, profile_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/{parcel_type}")
    def create_transport_parcel(
        self, profile_id: UUID, parcel_type: str, payload: _ParcelBase
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/wan/vpn/{vpn_id}/{parcel_type}")
    def create_transport_vpn_sub_parcel(
        self, profile_id: UUID, vpn_id: UUID, parcel_type: str, payload: _ParcelBase
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{vpn_id}/{parcel_type}")
    def create_management_vpn_sub_parcel(
        self, profile_id: UUID, vpn_id: UUID, parcel_type: str, payload: _ParcelBase
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}/{parcel_type}")
    def get_transport_parcels(self, profile_id: UUID, parcel_type: str) -> DataSequence[Parcel[AnyTransportParcel]]:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/{profile_id}/{parcel_type}/{parcel_id}")
    def get_transport_parcel(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> Parcel[AnyTransportParcel]:
        ...

    #
    # ManagementVPN parcel
    #
    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn")
    def create_management_vpn_parcel(self, profile_id: UUID, payload: _ParcelBase) -> ParcelCreationResponse:
        ...

    # @versions(supported_versions=(">=20.12"), raises=False)
    # @get("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn")
    # def get_management_vpn_parcels(self, profile_id: UUID) -> ParcelSequence[ManagementVPN]:
    #     ...

    # @versions(supported_versions=(">=20.12"), raises=False)
    # @get("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    # def get_management_vpn_parcel(self, profile_id: UUID, parcel_id: str) -> Parcel[ManagementVPN]:
    #     ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def edit_management_vpn_parcel(
        self, profile_id: UUID, parcel_id: str, payload: ManagementVpnParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{profile_id}/management/vpn/{parcel_id}")
    def delete_management_vpn_parcel(self, profile_id: UUID, parcel_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport")
    def get_sdwan_transport_feature_profiles(
        self, payload: Optional[GetFeatureProfilesParams]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/transport/cellular-controller/schema", resp_json_key="request")
    def get_sdwan_transport_cellular_controller_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport")
    def create_sdwan_transport_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/transport/{transport_id}")
    def delete_sdwan_transport_feature_profile(self, transport_id: str) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{transport_id}/cellular-controller")
    def create_cellular_controller_profile_parcel_for_transport(
        self, transport_id: str, payload: CellularControllerParcel
    ) -> ParcelId:
        ...

    #
    # Cellular controller
    #

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/cellular-controller/{cellular_controler_id}/{parcel_type}")
    def associate_with_cellular_controller(
        self, profile_id: UUID, cellular_controler_id: UUID, parcel_type: str, payload: ParcelAssociationPayload
    ) -> ParcelId:
        ...

    #
    # Routing
    #

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/transport/{profile_id}/wan/vpn/{vpn_id}/{parcel_type}")
    def associate_with_vpn(
        self, profile_id: UUID, vpn_id: UUID, parcel_type: str, payload: ParcelAssociationPayload
    ) -> ParcelCreationResponse:
        ...
