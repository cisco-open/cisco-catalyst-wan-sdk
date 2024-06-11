# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from typing import Callable, Dict, List, Set, Tuple, cast
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
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.policy_object_pusher import PolicyObjectPusher
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
        self._policy_object_pusher = PolicyObjectPusher(
            ux2_config=ux2_config, session=session, progress=progress, push_result=self._push_result
        )
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

        self._policy_object_pusher.push()
        dpop = self._policy_object_pusher.get_or_create_default_policy_object_profile()
        self._create_topology_groups(dpop)  # needs to be executed after vpn parcels and groups of interests are created
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
            logger.error(f"Error occured during credentials migration: {e}")

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
                logger.error(f"Error occured during config group creation: {e}")
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
                logger.error(f"Error occured during [{fp_name}] feature profile creation: {e}")
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

    def _create_topology_groups(self, default_policy_object_profile_id: UUID):
        profile_origin_map: Dict[str, Tuple[UUID, Set[UUID]]] = {}
        profile_api = self._session.api.sdwan_feature_profiles.topology
        group_api = self._session.endpoints.configuration.topology_group
        ttps = [p for p in self._ux2_config.feature_profiles if p.header.type == "topology"]
        for i, ttp in enumerate(ttps):
            profile = ttp.feature_profile
            try:
                profile_id = profile_api.create_profile(profile.name, profile.description).id
                self._push_result.rollback.add_feature_profile(profile_id, "topology")
                profile_origin_map[profile.name] = (profile_id, ttp.header.subelements)
                self._progress(
                    f"Creating Topology Profile: {profile.name}",
                    i + 1,
                    len(ttps),
                )
            except ManagerHTTPError as e:
                logger.error(f"Error occured during topology profile creation: {e}")

        ttgs = self._ux2_config.topology_groups
        for ttg in ttgs:
            group = ttg.topology_group
            profile_id, origins = profile_origin_map[group.name]
            group.add_profiles([profile_id, default_policy_object_profile_id])
            try:
                group_id = group_api.create_topology_group(group).id
                self._push_result.rollback.add_topology_group(group_id)
                self._progress(
                    f"Creating Topology Group: {group.name}",
                    i + 1,
                    len(ttps),
                )
            except ManagerHTTPError as e:
                logger.error(f"Error occured during topology group creation: {e}")

            for parcel in self._ux2_config.parcels_with_origin(origins):
                if isinstance(parcel, (CustomControlParcel, HubSpokeParcel, MeshParcel)):
                    try:
                        profile_api.create_parcel(profile_id, parcel)
                    except ManagerHTTPError as e:
                        logger.error(f"Error occured during topology profile creation: {e}")
                else:
                    logger.warning(f"Unexpected parcel type {type(parcel)}")
