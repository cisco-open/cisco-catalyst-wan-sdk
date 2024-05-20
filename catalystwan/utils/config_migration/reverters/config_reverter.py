from typing import Callable
from venv import logger

from catalystwan.exceptions import CatalystwanException
from catalystwan.models.configuration.config_migration import UX2RollbackInfo
from catalystwan.utils.config_migration.factories.feature_profile_api import FeatureProfileAPIFactory


class UX2ConfigReverter:
    def __init__(self, session) -> None:
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

        for i, feature_profile_entry in enumerate(rollback_info.feature_profile_ids):
            feature_profile_id, type_ = feature_profile_entry
            try:
                api = FeatureProfileAPIFactory.get_api(type_, self._session)
                if type_ == "policy-object":
                    continue
                api.delete_profile(feature_profile_id)  # type: ignore
                progress("Removing Feature Profiles", i + 1, len(rollback_info.feature_profile_ids))
            except CatalystwanException as e:
                all_deleted = False
                logger.error(f"Error occured during deleting feature profile {feature_profile_id}: {e}")
        return all_deleted
