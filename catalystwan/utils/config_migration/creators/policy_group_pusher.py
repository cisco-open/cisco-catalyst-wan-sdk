import logging

from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import TransformedPolicyGroup
from catalystwan.models.configuration.policy_group import PolicyGroup
from catalystwan.utils.config_migration.creators.pusher import Pusher, PusherConfig

logger = logging.getLogger(__name__)


class PolicyGroupPusher(Pusher):
    """Create Policy Groups that aggregate all the feature profiles that were the part of the same Device Template."""

    def __init__(self, config: PusherConfig) -> None:
        self.load_config(config)

    def push(self) -> None:
        pg_len = len(self._ux2_config.policy_groups)
        for i, pg in enumerate(self._ux2_config.policy_groups):
            self._progress(f"Creating Policy Group: {pg.policy_group.name}", i + 1, pg_len)
            self._replace_subelements_with_pushed_feature_profiles(pg)
            self._push_policy_group(pg.policy_group)

    def _replace_subelements_with_pushed_feature_profiles(self, policy_group: TransformedPolicyGroup) -> None:
        for ref in policy_group.header.subelements:
            if id_ := self._push_context.policy_group_feature_profiles_id_lookup.get(ref):
                policy_group.policy_group.add_profile(profile_uuid=id_)
            else:
                logger.warning(f"Could not find a pushed feature profile with ref {ref}")

    def _push_policy_group(
        self,
        policy_group: PolicyGroup,
    ) -> None:
        try:
            uuid = self._session.endpoints.configuration.policy_group.create_policy_group(policy_group).id
            if policy_group.profiles:
                associated_feature_profiles = self._push_result.report.get_standalone_feature_profiles_by_ids(
                    set([p.id for p in policy_group.profiles])
                )
            else:
                associated_feature_profiles = []
            self._push_result.report.add_pg_report(
                policy_group.name, uuid, feature_profiles=associated_feature_profiles
            )
        except ManagerHTTPError as e:
            logger.error(f"Failed to push policy group {policy_group.name}: {e}")
