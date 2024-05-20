# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from typing import Callable, Dict, List, cast
from uuid import UUID

from pydantic import BaseModel

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.endpoints.configuration_group import ProfileId
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    TransformedFeatureProfile,
    TransformedParcel,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.factories.parcel_pusher import ParcelPusherFactory

logger = logging.getLogger(__name__)


class ConfigurationMapping(BaseModel):
    feature_profile_map: Dict[UUID, TransformedFeatureProfile]
    parcel_map: Dict[UUID, TransformedParcel]


class UX2ConfigPusher:
    def __init__(
        self,
        session: ManagerSession,
        ux2_config: UX2Config,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._session = session
        self._config_map = self._create_config_map(ux2_config)
        self._push_result = UX2ConfigPushResult()
        self._ux2_config = ux2_config
        self._progress = progress

    def _create_config_map(self, ux2_config: UX2Config) -> ConfigurationMapping:
        return ConfigurationMapping(
            feature_profile_map={item.header.origin: item for item in ux2_config.feature_profiles},
            parcel_map={item.header.origin: item for item in ux2_config.profile_parcels},
        )

    def push(self) -> UX2ConfigPushResult:
        try:
            self._create_cloud_credentials()
        except ManagerHTTPError as e:
            logger.error(f"Error occured during credentials migration: {e.info}")
        self._create_config_groups()
        self._push_result.report.set_failed_push_parcels_flat_list()
        logger.debug(f"Configuration push completed. Rollback configuration {self._push_result}")
        return self._push_result

    def _create_cloud_credentials(self):
        cloud_credentials = self._ux2_config.cloud_credentials
        if cloud_credentials is None:
            return
        self._session.endpoints.configuration_settings.create_cloud_credentials(cloud_credentials)

    def _create_config_groups(self):
        config_groups = self._ux2_config.config_groups
        config_groups_length = len(config_groups)
        for i, transformed_config_group in enumerate(config_groups):
            self._progress(
                f"Creating Configuration Group: {transformed_config_group.config_group.name}",
                i + 1,
                config_groups_length,
            )
            logger.debug(
                f"Creating config group: {transformed_config_group.config_group.name} "
                f"with origin uuid: {transformed_config_group.header.origin} "
                f"and feature profiles: {transformed_config_group.header.subelements}"
            )
            config_group_payload = transformed_config_group.config_group
            created_profiles = self._create_feature_profile_and_parcels(transformed_config_group.header.subelements)
            config_group_payload.profiles = [ProfileId(id=profile.profile_uuid) for profile in created_profiles]
            cg_id = self._session.endpoints.configuration_group.create_config_group(config_group_payload).id
            self._push_result.rollback.add_config_group(cg_id)
            self._push_result.report.add_report(
                name=transformed_config_group.config_group.name,
                uuid=cg_id,
                feature_profiles=created_profiles,
            )

    def _create_feature_profile_and_parcels(self, feature_profiles_ids: List[UUID]) -> List[FeatureProfileBuildReport]:
        feature_profiles: List[FeatureProfileBuildReport] = []
        for i, feature_profile_id in enumerate(feature_profiles_ids):
            transformed_feature_profile = self._config_map.feature_profile_map[feature_profile_id]
            logger.debug(
                f"Creating feature profile: {transformed_feature_profile.feature_profile.name} "
                f"with origin uuid: {transformed_feature_profile.header.origin} "
                f"and parcels: {transformed_feature_profile.header.subelements}"
            )
            profile_type = cast(ProfileType, transformed_feature_profile.header.type)
            if profile_type in ["policy-object", "sig-security"]:
                # TODO: Add builders for those profiles
                logger.debug(f"Skipping profile: {transformed_feature_profile.feature_profile.name}")
                continue
            pusher = ParcelPusherFactory.get_pusher(self._session, profile_type)
            parcels = self._create_parcels_list(transformed_feature_profile)
            profile = pusher.push(transformed_feature_profile.feature_profile, parcels, self._config_map.parcel_map)
            feature_profiles.append(profile)
            self._push_result.rollback.add_feature_profile(profile.profile_uuid, profile_type)
        return feature_profiles

    def _create_parcels_list(self, transformed_feature_profile: TransformedFeatureProfile) -> List[TransformedParcel]:
        logger.debug(f"Creating parcels for feature profile: {transformed_feature_profile.feature_profile.name}")
        parcels = []
        for element_uuid in transformed_feature_profile.header.subelements:
            transformed_parcel = self._config_map.parcel_map.get(element_uuid)
            if not transformed_parcel:
                # Device templates can have assigned feature templates but when we download the
                # featrue templates from the enpoint some templates don't exist in the response
                logger.error(f"Parcel with origin uuid {element_uuid} not found in the config map")
            else:
                parcels.append(transformed_parcel)
        return parcels
