# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Optional
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.endpoints import JSON, APIEndpoints, delete, get, post, put, versions
from catalystwan.models.configuration.feature_profile.common import (
    FeatureProfileCreationPayload,
    FeatureProfileCreationResponse,
    FeatureProfileInfo,
    GetFeatureProfilesParams,
    SchemaTypeQuery,
)
from catalystwan.models.configuration.feature_profile.parcel import Parcel, ParcelId
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.aaa import AAAParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.banner import BannerParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.basic import BasicParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.bfd import BFDParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.global_parcel import GlobalParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import LoggingParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.mrf import MRFParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.ntp import NtpParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.omp import OMPParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.security import SecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.snmp import SNMPParcel
from catalystwan.typed_list import DataSequence


class SystemFeatureProfile(APIEndpoints):
    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{parcel_type}/schema", resp_json_key="request")
    def get_schema(self, parcel_type: str, params: SchemaTypeQuery) -> JSON:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system")
    def get_sdwan_system_feature_profiles(
        self, payload: Optional[GetFeatureProfilesParams]
    ) -> DataSequence[FeatureProfileInfo]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/system")
    def create_sdwan_system_feature_profile(
        self, payload: FeatureProfileCreationPayload
    ) -> FeatureProfileCreationResponse:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/system/{profile_id}")
    def delete_sdwan_system_feature_profile(self, profile_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/system/{profile_id}/aaa")
    def create_aaa_profile_parcel_for_system(self, profile_id: UUID, payload: _ParcelBase) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/feature-profile/sdwan/system/{profile_id}/aaa/{parcel_id}")
    def edit_aaa_profile_parcel_for_system(self, profile_id: UUID, parcel_id: UUID, payload: _ParcelBase) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/{parcel_type}", resp_json_key="data")
    def get_all(self, profile_id: UUID, parcel_type: UUID) -> DataSequence[Parcel[AnySystemParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/{parcel_type}/{parcel_id}")
    def get_by_id(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> Parcel[AnySystemParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/aaa", resp_json_key="data")
    def get_all_aaa(self, profile_id: UUID) -> DataSequence[Parcel[AAAParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/aaa/{parcel_id}")
    def get_by_id_aaa(self, profile_id: UUID, parcel_id: UUID) -> Parcel[AAAParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/banner", resp_json_key="data")
    def get_all_banner(self, profile_id: UUID) -> DataSequence[Parcel[BannerParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/banner/{parcel_id}")
    def get_by_id_banner(self, profile_id: UUID, parcel_id: UUID) -> Parcel[BannerParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/basic", resp_json_key="data")
    def get_all_basic(self, profile_id: UUID) -> DataSequence[Parcel[BasicParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/basic/{parcel_id}")
    def get_by_id_basic(self, profile_id: UUID, parcel_id: UUID) -> Parcel[BasicParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/bfd", resp_json_key="data")
    def get_all_bfd(self, profile_id: UUID) -> DataSequence[Parcel[BFDParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/bfd/{parcel_id}")
    def get_by_id_bfd(self, profile_id: UUID, parcel_id: UUID) -> Parcel[BFDParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/global", resp_json_key="data")
    def get_all_global(self, profile_id: UUID) -> DataSequence[Parcel[GlobalParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/global/{parcel_id}")
    def get_by_id_global(self, profile_id: UUID, parcel_id: UUID) -> Parcel[GlobalParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/logging", resp_json_key="data")
    def get_all_logging(self, profile_id: UUID) -> DataSequence[Parcel[LoggingParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/logging/{parcel_id}")
    def get_by_id_logging(self, profile_id: UUID, parcel_id: UUID) -> Parcel[LoggingParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/mrf", resp_json_key="data")
    def get_all_mrf(self, profile_id: UUID) -> DataSequence[Parcel[MRFParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/mrf/{parcel_id}")
    def get_by_id_mrf(self, profile_id: UUID, parcel_id: UUID) -> Parcel[MRFParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/ntp", resp_json_key="data")
    def get_all_ntp(self, profile_id: UUID) -> DataSequence[Parcel[NtpParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/ntp/{parcel_id}")
    def get_by_id_ntp(self, profile_id: UUID, parcel_id: UUID) -> Parcel[NtpParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/omp", resp_json_key="data")
    def get_all_omp(self, profile_id: UUID) -> DataSequence[Parcel[OMPParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/omp/{parcel_id}")
    def get_by_id_omp(self, profile_id: UUID, parcel_id: UUID) -> Parcel[OMPParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/security", resp_json_key="data")
    def get_all_security(self, profile_id: UUID) -> DataSequence[Parcel[SecurityParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/security/{parcel_id}")
    def get_by_id_security(self, profile_id: UUID, parcel_id: UUID) -> Parcel[SecurityParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/snmp", resp_json_key="data")
    def get_all_snmp(self, profile_id: UUID) -> DataSequence[Parcel[SNMPParcel]]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @get("/v1/feature-profile/sdwan/system/{profile_id}/snmp/{parcel_id}")
    def get_by_id_snmp(self, profile_id: UUID, parcel_id: UUID) -> Parcel[SNMPParcel]:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @put("/v1/feature-profile/sdwan/system/{profile_id}/{parcel_type}/{parcel_id}")
    def update(self, profile_id: UUID, parcel_type: str, parcel_id: UUID, payload: AnySystemParcel) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @delete("/v1/feature-profile/sdwan/system/{profile_id}/{parcel_type}/{parcel_id}")
    def delete(self, profile_id: UUID, parcel_type: str, parcel_id: UUID) -> None:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/system/{system_id}/bfd")
    def create_bfd_profile_parcel_for_system(self, system_id: str, payload: _ParcelBase) -> ParcelId:
        ...

    @versions(supported_versions=(">=20.9"), raises=False)
    @post("/v1/feature-profile/sdwan/system/{profile_id}/{parcel_type}")
    def create(self, profile_id: UUID, parcel_type: str, payload: AnySystemParcel) -> ParcelId:
        ...
