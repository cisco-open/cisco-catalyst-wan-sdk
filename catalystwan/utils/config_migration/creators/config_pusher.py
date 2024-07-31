# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from typing import Callable
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import PushContext, UX2Config, UX2ConfigPushResult
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.config_group_pusher import ConfigGroupPusher
from catalystwan.utils.config_migration.creators.groups_of_interests_pusher import GroupsOfInterestPusher
from catalystwan.utils.config_migration.creators.localized_policy_pusher import LocalizedPolicyPusher
from catalystwan.utils.config_migration.creators.policy_group_pusher import PolicyGroupPusher
from catalystwan.utils.config_migration.creators.pusher import PusherConfig
from catalystwan.utils.config_migration.creators.security_policy_pusher import SecurityPolicyPusher
from catalystwan.utils.config_migration.creators.topology_groups_pusher import TopologyGroupsPusher

logger = logging.getLogger(__name__)


class UX2ConfigPusher:
    def __init__(
        self,
        session: ManagerSession,
        ux2_config: UX2Config,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._session = session
        self._push_context = PushContext()
        self._push_result = UX2ConfigPushResult()
        self._ux2_config = ux2_config
        self._progress = progress
        self._configure_pushers()

    def _configure_pushers(self):
        config = PusherConfig(
            ux2_config=self._ux2_config,
            session=self._session,
            push_result=self._push_result,
            push_context=self._push_context,
            progress=self._progress,
        )
        self._config_group_pusher = ConfigGroupPusher(config)
        self._groups_of_interests_pusher = GroupsOfInterestPusher(config)
        self._localized_policy_feature_pusher = LocalizedPolicyPusher(config)
        self._security_policy_pusher = SecurityPolicyPusher(config)
        self._topology_groups_pusher = TopologyGroupsPusher(config)
        self._policy_group_pusher = PolicyGroupPusher(config)

    def push(self) -> UX2ConfigPushResult:
        # Do not change the order of the push
        self._create_sigs()
        self._create_cloud_credentials()
        self._create_thread_grid_api()
        self._create_cflowd()
        self._config_group_pusher.push()
        self._groups_of_interests_pusher.push()
        self._localized_policy_feature_pusher.push()
        self._security_policy_pusher.push()
        self._topology_groups_pusher.push()
        self._policy_group_pusher.push()
        self._push_result.report.set_failed_push_parcels_flat_list()
        self._push_result.set_groups_rollback()
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
                self._push_context.policy_group_feature_profiles_id_lookup[sig.header.origin] = profile_uuid
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
