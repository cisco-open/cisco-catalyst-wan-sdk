import logging
from typing import Callable, Mapping, Type
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import PushContext, UX2Config, UX2ConfigPushResult
from catalystwan.models.configuration.feature_profile.common import RefIdItem
from catalystwan.models.configuration.feature_profile.parcel import AnyDnsSecurityParcel, AnyParcel, list_types
from catalystwan.session import ManagerSession

from .references_updater import ReferencesUpdater, update_parcels_references

logger = logging.getLogger(__name__)


class DnsSecurityReferencesUpdater(ReferencesUpdater):
    def update_references(self):
        if local_domain_bypass_list := self.parcel.local_domain_bypass_list:
            v2_uuid = self.get_target_uuid(UUID(local_domain_bypass_list.ref_id.value))
            self.parcel.local_domain_bypass_list = RefIdItem.from_uuid(v2_uuid)


REFERENCES_UPDATER_MAPPING: Mapping[type, Type[ReferencesUpdater]] = {
    AnyDnsSecurityParcel: DnsSecurityReferencesUpdater,
}


class SecurityPolicyPusher:
    def __init__(
        self,
        ux2_config: UX2Config,
        session: ManagerSession,
        push_result: UX2ConfigPushResult,
        push_context: PushContext,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._ux2_config = ux2_config
        self._dns_security_api = session.api.sdwan_feature_profiles.dns_security
        self._push_result: UX2ConfigPushResult = push_result
        self._progress: Callable[[str, int, int], None] = progress
        self.push_context = push_context

    def push(self) -> None:
        self.push_dns_security_policies()

    def cast_(self, parcel: AnyParcel) -> AnyDnsSecurityParcel:
        return parcel  # type: ignore

    def push_dns_security_policies(self) -> None:
        dns_security_policies = [
            transformed_parcel
            for transformed_parcel in self._ux2_config.profile_parcels
            if type(transformed_parcel.parcel) in list_types(AnyDnsSecurityParcel)
        ]

        for i, dns_security_policy in enumerate(dns_security_policies):
            parcel = self.cast_(dns_security_policy.parcel)
            update_parcels_references(parcel, self.push_context.id_lookup, REFERENCES_UPDATER_MAPPING)

            try:
                profile_id = self._dns_security_api.create_profile(parcel.parcel_name, parcel.parcel_description).id
                self._push_result.rollback.add_feature_profile(profile_id, "dns-security")
                feature_profile_report = FeatureProfileBuildReport(
                    profile_name=parcel.parcel_name, profile_uuid=profile_id
                )
                self._push_result.report.security_policies.append(feature_profile_report)
            except ManagerHTTPError as e:
                logger.error(f"Error occured during DNS Security policy creation: {e.info}")
                self._push_result.report.security_policies.append(
                    FeatureProfileBuildReport(profile_name=parcel.parcel_name, profile_uuid=UUID(int=0))
                )
                continue

            try:
                parcel_id = self._dns_security_api.create_parcel(profile_id, parcel).id
                self.push_context.id_lookup[dns_security_policy.header.origin] = parcel_id
                feature_profile_report.add_created_parcel(dns_security_policy.parcel.parcel_name, parcel_id)
                msg = f"Creating DNS Security policies: {dns_security_policy.parcel.parcel_name}"
                self._progress(msg, i + 1, len(dns_security_policies))
            except ManagerHTTPError as e:
                logger.error(f"Error occured during DNS Security policy creation: {e.info}")
                feature_profile_report.add_failed_parcel(
                    parcel_name=parcel.parcel_name, parcel_type=parcel.type_, error_info=e.info
                )
