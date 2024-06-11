from typing import Callable
from venv import logger

from catalystwan.exceptions import CatalystwanException
from catalystwan.models.configuration.config_migration import UX2RollbackInfo
from catalystwan.models.configuration.feature_profile.parcel import find_type
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.factories.feature_profile_api import FeatureProfileAPIFactory


class UX2ConfigReverter:
    def __init__(self, session: ManagerSession) -> None:
        self._session = session

    def rollback(self, rollback_info: UX2RollbackInfo, progress: Callable[[str, int, int], None]) -> bool:
        all_deleted = True
        for i, cg_id in enumerate(rollback_info.config_group_ids):
            try:
                self._session.endpoints.configuration_group.delete_config_group(cg_id)
                progress("Removing Configuration Groups", i + 1, len(rollback_info.config_group_ids))
            except CatalystwanException as e:
                all_deleted = False
                logger.error(f"Error occured during deleting config group {cg_id}: {e}")

        for i, tg_id in enumerate(rollback_info.topology_group_ids):
            try:
                self._session.endpoints.configuration.topology_group.delete(tg_id)
                progress("Removing Topology Groups", i + 1, len(rollback_info.topology_group_ids))
            except CatalystwanException as e:
                all_deleted = False
                logger.error(f"Error occured during deleting topolofy group {cg_id}: {e}")

        for i, feature_profile_entry in enumerate(rollback_info.feature_profile_ids):
            feature_profile_id, type_ = feature_profile_entry
            try:
                api = FeatureProfileAPIFactory.get_api(type_, self._session)
                if (
                    type_ == "policy-object"
                ):  # policy-objects are populated only in default policy object profile and handled separately
                    continue
                api.delete_profile(feature_profile_id)  # type: ignore
                progress("Removing Feature Profiles", i + 1, len(rollback_info.feature_profile_ids))
            except CatalystwanException as e:
                all_deleted = False
                logger.error(f"Error occured during deleting feature profile {feature_profile_id}: {e}")

        if rollback_info.default_policy_object_profile is not None:
            profile_id = rollback_info.default_policy_object_profile.profile_id
            api = self._session.api.sdwan_feature_profiles.policy_object

            # removing order shall be reversed, otherwise some parcels may not be removed due to reference count != 0
            rollback_info.default_policy_object_profile.parcels.reverse()

            for i, parcel in enumerate(rollback_info.default_policy_object_profile.parcels):
                parcel_id, parcel_type_str = parcel
                parcel_type = find_type(parcel_type_str, AnyPolicyObjectParcel)
                try:
                    api.delete(profile_id, parcel_type, parcel_id)
                    progress(
                        "Removing Default Policy Object Profile Parcels",
                        i + 1,
                        len(rollback_info.default_policy_object_profile.parcels),
                    )
                except CatalystwanException as e:
                    all_deleted = False
                    logger.error(f"Error occured during deleting feature profile {feature_profile_id}: {e}")

        return all_deleted
