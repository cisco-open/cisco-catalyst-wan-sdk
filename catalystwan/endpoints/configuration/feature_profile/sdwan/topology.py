# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

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
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelCreationResponse
from catalystwan.models.configuration.feature_profile.sdwan.topology import AnyTopologyParcel
from catalystwan.typed_list import DataSequence


class TopologyFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/topology")
    def create_topology_feature_profile(self, payload: FeatureProfileCreationPayload) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/topology")
    def get_topology_feature_profiles(self, params: GetFeatureProfilesParams) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @get("/v1/feature-profile/sdwan/topology/{profile_id}")
    def get_topology_feature_profile(self, profile_id: str, params: GetFeatureProfilesParams) -> FeatureProfileDetail:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @put("/v1/feature-profile/sdwan/topology/{profile_id}")
    def edit_topology_feature_profile(
        self, profile_id: str, payload: FeatureProfileEditPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.12"), raises=False)
    @delete("/v1/feature-profile/sdwan/topology/{profile_id}")
    def delete_topology_feature_profile(self, profile_id: str) -> None:
        ...

    #
    # Create/Delete/Get Any Topology Parcel
    #

    @versions(supported_versions=(">=20.12"), raises=False)
    @post("/v1/feature-profile/sdwan/topology/{profile_id}/{parcel_type}")
    def create_any_parcel(
        self, profile_id: UUID, parcel_type: str, payload: AnyTopologyParcel
    ) -> ParcelCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/topology/{profile_id}/{parcel_type}/{parcel_id}")
    def delete_any_parcel(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/topology/{profile_id}/{parcel_type}/{parcel_id}")
    def get_any_parcel_by_id(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> Parcel[AnyTopologyParcel]:
        ...

    #
    # Mesh Parcel
    #
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/topology/mesh/schema", resp_json_key="request")
    def get_mesh_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...

    #
    # Hub and Spoke Parcel
    #
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/topology/hubspoke/schema", resp_json_key="request")
    def get_hubspoke_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...

    #
    # Custom Control Parcel
    #
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/topology/custom-control/schema", resp_json_key="request")
    def get_custom_control_parcel_schema(self, params: SchemaTypeQuery) -> JSON:
        ...
