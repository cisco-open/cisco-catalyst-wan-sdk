# Copyright 2024 Cisco Systems, Inc. and its affiliates
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
from catalystwan.models.configuration.feature_profile.parcel import Parcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.session import ManagerSession
from catalystwan.typed_list import DataSequence
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
        self._create_cloud_credentials()
        self._create_config_groups()
        self._insert_groups_of_interest_in_default_policy_object_profile()
        self._push_result.report.set_failed_push_parcels_flat_list()
        logger.debug(f"Configuration push completed. Rollback configuration {self._push_result}")
        return self._push_result

    def _create_cloud_credentials(self):
        cloud_credentials = self._ux2_config.cloud_credentials
        if cloud_credentials is None:
            return
        try:
            self._session.endpoints.configuration_settings.create_cloud_credentials(cloud_credentials)
        except ManagerHTTPError as e:
            logger.error(f"Error occured during credentials migration: {e.info}")

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
            try:
                cg_id = self._session.endpoints.configuration_group.create_config_group(config_group_payload).id
            except ManagerHTTPError as e:
                logger.error(f"Error occured during config group creation: {e.info}")
                self._push_result.report.add_feature_profiles_not_assosiated_with_config_group(
                    feature_profiles=created_profiles
                )
            else:
                self._push_result.rollback.add_config_group(cg_id)
                self._push_result.report.add_report(
                    name=transformed_config_group.config_group.name,
                    uuid=cg_id,
                    feature_profiles=created_profiles,
                )

    def _insert_groups_of_interest_in_default_policy_object_profile(self):
        api = self._session.api.sdwan_feature_profiles.policy_object
        profile_id = api.get_profiles().find(solution="sdwan", created_by="system").profile_id
        profile_rollback = self._push_result.rollback.add_default_policy_object_profile(profile_id)

        # will hold system created parcels id by type and name when detected
        existing_parcels: Dict[AnyPolicyObjectParcel, Dict[str, UUID]] = {}

        transformed_policy_parcels = [
            any_transformed_parcel
            for any_transformed_parcel in self._ux2_config.profile_parcels
            if type(any_transformed_parcel.parcel) in list_types(AnyPolicyObjectParcel)
        ]

        for i, transformed_policy_parcel in enumerate(transformed_policy_parcels):
            parcel = transformed_policy_parcel.parcel
            header = transformed_policy_parcel.header
            parcel_type: AnyPolicyObjectParcel = type(parcel)
            # update existing system created parcels
            if not existing_parcels.get(parcel_type):
                existing_parcels[parcel_type] = {}
                exsisting_parcel_list = cast(
                    DataSequence[Parcel[AnyPolicyObjectParcel]],
                    api.get(profile_id, parcel_type).filter(created_by="system"),
                )
                for ep in exsisting_parcel_list:
                    if not isinstance(ep.parcel_id, UUID):
                        id_ = UUID(ep.parcel_id)
                    else:
                        id_ = ep.parcel_id
                    existing_parcels[parcel_type][ep.payload.parcel_name] = id_

            # if parcel with given name exists we skip it
            if not existing_parcels[parcel_type].get(header.origname):
                try:
                    parcel_id = api.create(profile_id=profile_id, payload=parcel).id
                    profile_rollback.add_parcel(parcel.type_, parcel_id)
                    self._push_result.report.groups_of_interest.add_created(parcel.parcel_name, parcel_id)
                    self._progress(
                        f"Creating Policy Object Parcel: {parcel.parcel_name}",
                        i + 1,
                        len(transformed_policy_parcels),
                    )
                except ManagerHTTPError as e:
                    logger.error(f"Error occured during config group creation: {e.info}")
                    self._push_result.report.groups_of_interest.add_failed(parcel, e)

    def _create_feature_profile_and_parcels(self, feature_profiles_ids: List[UUID]) -> List[FeatureProfileBuildReport]:
        feature_profiles: List[FeatureProfileBuildReport] = []
        for feature_profile_id in feature_profiles_ids:
            transformed_feature_profile = self._config_map.feature_profile_map[feature_profile_id]
            fp_name = transformed_feature_profile.feature_profile.name
            logger.debug(
                f"Creating feature profile: {fp_name} "
                f"with origin uuid: {transformed_feature_profile.header.origin} "
                f"and parcels: {transformed_feature_profile.header.subelements}"
            )
            profile_type = cast(ProfileType, transformed_feature_profile.header.type)
            if profile_type in ["policy-object", "sig-security"]:
                # TODO: Add builders for those profiles
                logger.debug(f"Skipping profile: {fp_name}")
                continue
            pusher = ParcelPusherFactory.get_pusher(self._session, profile_type)
            parcels = self._create_parcels_list(transformed_feature_profile)
            try:
                profile = pusher.push(transformed_feature_profile.feature_profile, parcels, self._config_map.parcel_map)
                feature_profiles.append(profile)
                self._push_result.rollback.add_feature_profile(profile.profile_uuid, profile_type)
            except ManagerHTTPError as e:
                logger.error(f"Error occured during [{fp_name}] feature profile creation: {e.info}")
            except Exception:
                logger.critical(f"Unexpected error occured during [{fp_name}] feature profile creation", exc_info=True)
        return feature_profiles

    def _create_parcels_list(self, transformed_feature_profile: TransformedFeatureProfile) -> List[TransformedParcel]:
        logger.debug(f"Creating parcels for feature profile: {transformed_feature_profile.feature_profile.name}")
        parcels = []
        for element_uuid in transformed_feature_profile.header.subelements:
            transformed_parcel = self._config_map.parcel_map.get(element_uuid)
            if not transformed_parcel:
                # Device templates can have assigned feature templates but when we download the
                # feature templates from the enpoint some templates don't exist in the response
                logger.error(f"Parcel with origin uuid {element_uuid} not found in the config map")
            else:
                parcels.append(transformed_parcel)
        return parcels
