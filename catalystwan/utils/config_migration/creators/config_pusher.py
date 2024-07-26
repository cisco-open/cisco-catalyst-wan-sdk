# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from typing import Callable, Dict, List, cast
from uuid import UUID

from pydantic import BaseModel

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.endpoints.configuration_group import ProfileId
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    PushContext,
    TransformedFeatureProfile,
    TransformedParcel,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.common import ProfileType
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.groups_of_interests_pusher import GroupsOfInterestPusher
from catalystwan.utils.config_migration.creators.localized_policy_pusher import LocalizedPolicyPusher
from catalystwan.utils.config_migration.creators.security_policy_pusher import SecurityPolicyPusher
from catalystwan.utils.config_migration.creators.topology_groups_pusher import TopologyGroupsPusher
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
        self._push_context = PushContext()
        self._config_map = self._create_config_map(ux2_config)
        self._push_result = UX2ConfigPushResult()

        self._groups_of_interests_pusher = GroupsOfInterestPusher(
            ux2_config=ux2_config,
            session=session,
            progress=progress,
            push_result=self._push_result,
            push_context=self._push_context,
        )
        self._localized_policy_feature_pusher = LocalizedPolicyPusher(
            ux2_config=ux2_config,
            session=session,
            progress=progress,
            push_result=self._push_result,
            push_context=self._push_context,
        )
        self._security_policy_pusher = SecurityPolicyPusher(
            ux2_config=ux2_config,
            session=session,
            progress=progress,
            push_result=self._push_result,
            push_context=self._push_context,
        )
        self._topology_groups_pusher = TopologyGroupsPusher(
            ux2_config=ux2_config,
            session=session,
            progress=progress,
            push_result=self._push_result,
            push_context=self._push_context,
        )

        self._ux2_config = ux2_config
        self._progress = progress

    def _create_config_map(self, ux2_config: UX2Config) -> ConfigurationMapping:
        return ConfigurationMapping(
            feature_profile_map={item.header.origin: item for item in ux2_config.feature_profiles},
            parcel_map={item.header.origin: item for item in ux2_config.profile_parcels},
        )

    def push(self) -> UX2ConfigPushResult:
        self._create_sigs()
        self._create_cloud_credentials()
        self._create_thread_grid_api()
        self._create_cflowd()
        self._create_config_groups()
        self._groups_of_interests_pusher.push()
        self._localized_policy_feature_pusher.push()
        self._security_policy_pusher.push()
        self._topology_groups_pusher.push()
        self._push_result.report.set_failed_push_parcels_flat_list()
        logger.debug(f"Configuration push completed. Rollback configuration {self._push_result}")
        return self._push_result

    def _create_sigs(self):
        api = self._session.api.sdwan_feature_profiles.sig_security
        sigs = [p for p in self._ux2_config.profile_parcels if p.header.type == "sig"]
        profiles = []
        for sig in sigs:
            self._ux2_config.profile_parcels.remove(sig)
            try:
                profile_name = sig.header.origname
                profile_uuid = api.create_profile(profile_name, "Feature Profile created from SIG Feature Template").id
                parcel_uuid = api.create_parcel(profile_uuid, sig.parcel).id
                created_parcel = (sig.parcel.parcel_name, parcel_uuid)
                profiles.append(
                    FeatureProfileBuildReport(
                        profile_name=profile_name, profile_uuid=profile_uuid, created_parcels=[created_parcel]
                    )
                )
                self._push_result.rollback.add_feature_profile(profile_uuid, "sig-security")
            except ManagerHTTPError as e:
                logger.error(f"Error occured during sig creation: {e}")
        self._push_result.report.add_standalone_feature_profiles(profiles)

    def _create_cloud_credentials(self):
        cloud_credentials = self._ux2_config.cloud_credentials
        if cloud_credentials is None:
            return
        try:
            credentials = self._session.endpoints.configuration_settings.get_cloud_credentials().single_or_default()
            if credentials is None:
                self._session.endpoints.configuration_settings.create_cloud_credentials(cloud_credentials)
                return
            if credentials.umbrella_sig_auth_key is None and credentials.umbrella_sig_auth_secret is None:
                credentials.umbrella_org_id = cloud_credentials.umbrella_org_id
                credentials.umbrella_sig_auth_key = cloud_credentials.umbrella_sig_auth_key
                credentials.umbrella_sig_auth_secret = cloud_credentials.umbrella_sig_auth_secret
            if credentials.zscaler_organization is None:
                credentials.zscaler_organization = cloud_credentials.zscaler_organization
                credentials.zscaler_partner_base_uri = cloud_credentials.zscaler_partner_base_uri
                credentials.zscaler_partner_key = cloud_credentials.zscaler_partner_key
                credentials.zscaler_username = cloud_credentials.zscaler_username
                credentials.zscaler_password = cloud_credentials.zscaler_password
            self._session.endpoints.configuration_settings.create_cloud_credentials(credentials)
        except ManagerHTTPError as e:
            logger.error(f"Error occured during credentials migration: {e}")

    def _create_thread_grid_api(self):
        thread_grid_api = self._ux2_config.thread_grid_api
        if thread_grid_api is None:
            return
        try:
            self._session.api.administration_settings.update(thread_grid_api)
        except ManagerHTTPError as e:
            logger.error(f"Error occured during threat grid api migration: {e}")

    def _create_cflowd(self):
        if self._ux2_config.cflowd is None:
            return
        try:
            nodes = self._session.endpoints.network_hierarchy.list_nodes()
            node = next((n for n in nodes if n.data.label == "GLOBAL"), None)
            if node is None:
                return
            self._session.endpoints.network_hierarchy.create_cflowd(UUID(node.id), self._ux2_config.cflowd)
        except ManagerHTTPError as e:
            logger.error(f"Error occured during Cflowd migration: {e}")

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
                self._push_result.report.add_standalone_feature_profiles(feature_profiles=created_profiles)
            else:
                self._push_result.rollback.add_config_group(cg_id)
                self._push_result.report.add_report(
                    name=transformed_config_group.config_group.name,
                    uuid=cg_id,
                    feature_profiles=created_profiles,
                )
                self._push_context.id_lookup[transformed_config_group.header.origin] = cg_id

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
                self._push_context.id_lookup[feature_profile_id] = profile.profile_uuid
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
