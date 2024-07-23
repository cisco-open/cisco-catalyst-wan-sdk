# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from typing import Callable

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    PushContext,
    TopologyGroupReport,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.references_updater import update_parcel_references

logger = logging.getLogger(__name__)


class TopologyGroupsPusher:
    def __init__(
        self,
        ux2_config: UX2Config,
        session: ManagerSession,
        push_result: UX2ConfigPushResult,
        push_context: PushContext,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._ux2_config = ux2_config
        self._session = session
        self._push_result = push_result
        self._push_context = push_context
        self._progress = progress
        self.push_context = push_context

    def push(self) -> None:
        if self.push_context.default_policy_object_profile_id is None:
            logger.error("Cannot create Topology Group without Default Policy Object Profile")
            return
        profile_api = self._session.api.sdwan_feature_profiles.topology
        group_api = self._session.endpoints.configuration.topology_group

        # Top-Down starting from Topology Groups
        ttgs = self._ux2_config.topology_groups
        ttps_map = {
            ttp.header.origin: ttp for ttp in self._ux2_config.feature_profiles if ttp.header.type == "topology"
        }
        for i, ttg in enumerate(ttgs):
            self._progress(
                f"Creating Topology Group: {ttg.topology_group.name}",
                i + 1,
                len(ttgs),
            )

            # Create Topology Feature Profile
            ttp = ttps_map.get(ttg.header.origin)
            if ttp is None:
                logger.error(f"Topology Profile not found for Topology Group {ttg.topology_group.name}")
                continue
            profile = ttp.feature_profile
            try:
                profile_id = profile_api.create_profile(profile.name, profile.description).id
                profile_report = FeatureProfileBuildReport(profile_name=profile.name, profile_uuid=profile_id)
                self._push_result.rollback.add_feature_profile(profile_id, "topology")

            except ManagerHTTPError as e:
                logger.error(f"Error occured during Topology Profile creation: {e}")
                continue

            # Push Topology Feature Profile Parcels
            for transformed_parcel in self._ux2_config.list_transformed_parcels_with_origin(ttp.header.subelements):
                parcel = update_parcel_references(transformed_parcel.parcel, self.push_context.id_lookup)
                if isinstance(parcel, (CustomControlParcel, HubSpokeParcel, MeshParcel)):
                    try:
                        parcel_id = profile_api.create_parcel(profile_id, parcel).id
                        profile_report.add_created_parcel(parcel_name=parcel.parcel_name, parcel_uuid=parcel_id)
                        self.push_context.id_lookup[transformed_parcel.header.origin] = parcel_id
                    except ManagerHTTPError as e:
                        logger.error(f"Error occured during topology profile parcel creation: {e}")
                        profile_report.add_failed_parcel(
                            parcel_name=parcel.parcel_name,
                            parcel_type=parcel.type_,
                            error_info=e.info,
                            request=e.request,
                        )
                else:
                    logger.warning(f"Unexpected parcel type {type(parcel)}")

            # Push Topology Group
            group = ttg.topology_group
            group.add_profiles([profile_id, self.push_context.default_policy_object_profile_id])
            try:
                group_id = group_api.create(group).id
                self._push_result.rollback.add_topology_group(group_id)
                group_report = TopologyGroupReport(name=group.name, uuid=group_id, feature_profiles=[profile_report])
                self._push_result.report.topology_groups.append(group_report)
                self._push_context.id_lookup[ttg.header.origin] = group_id
            except ManagerHTTPError as e:
                logger.error(f"Error occured during topology group creation: {e}")
                continue
