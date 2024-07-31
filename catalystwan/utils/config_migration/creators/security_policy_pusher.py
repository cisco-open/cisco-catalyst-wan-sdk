# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from typing import cast
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import TransformedParcel
from catalystwan.models.configuration.feature_profile.parcel import AnyDnsSecurityParcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import NgfirewallParcel, PolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.policy import NgFirewallContainer
from catalystwan.utils.config_migration.creators.pusher import Pusher, PusherConfig

from .references_updater import update_parcel_references

logger = logging.getLogger(__name__)


class SecurityPolicyPusher(Pusher):
    def __init__(
        self,
        config: PusherConfig,
    ) -> None:
        self.load_config(config)
        self._dns_security_api = self._session.api.sdwan_feature_profiles.dns_security
        self._app_profile_api = self._session.api.sdwan_feature_profiles.application_priority
        self._embedded_security_api = self._session.api.sdwan_feature_profiles.embedded_security

    def push(self) -> None:
        self.push_dns_security_policies()
        self.push_embedded_security_policies()

    def _push_embedded_security_profile(self, name: str, description: str) -> FeatureProfileBuildReport:
        try:
            profile_id = self._embedded_security_api.create_profile(name, description).id
            self._push_result.rollback.add_feature_profile(profile_id, "embedded-security")
            feature_profile_report = FeatureProfileBuildReport(profile_name=name, profile_uuid=profile_id)
        except ManagerHTTPError as e:
            logger.error(f"Error occured during Embedded Security profile creation: {e.info}")
            feature_profile_report = FeatureProfileBuildReport(profile_name=name, profile_uuid=UUID(int=0))

        self._push_result.report.security_policies.append(feature_profile_report)
        return feature_profile_report

    def _push_ngfirewall_parcel(
        self, profile_id: UUID, firewall: TransformedParcel, report: FeatureProfileBuildReport
    ) -> None:
        parcel = cast(NgfirewallParcel, firewall.parcel)
        parcel = update_parcel_references(parcel, self._push_context.id_lookup)

        try:
            fw_id = self._embedded_security_api.create_parcel(profile_id, parcel).id
            report.add_created_parcel(parcel.parcel_name, fw_id)
            self._push_context.id_lookup[firewall.header.origin] = fw_id
        except ManagerHTTPError as e:
            logger.error(f"Error occured during creating NGFirewall in embedded security profile: {e.info}")
            report.add_failed_parcel(parcel_name=parcel.parcel_name, parcel_type=parcel.type_, error_info=e.info)

    def _push_policy_parcel(
        self, profile_id: UUID, policy: TransformedParcel, report: FeatureProfileBuildReport
    ) -> None:
        parcel = cast(PolicyParcel, policy.parcel)

        try:
            parcel = update_parcel_references(parcel, self._push_context.id_lookup)
            security_policy_parcel_id = self._embedded_security_api.create_parcel(profile_id, parcel).id
            report.add_created_parcel(parcel.parcel_name, security_policy_parcel_id)
            self._push_context.id_lookup[policy.header.origin] = security_policy_parcel_id
            self._push_context.policy_group_feature_profiles_id_lookup[policy.header.origin] = profile_id
        except ManagerHTTPError as e:
            logger.error(f"Error occured during creating PolicyParcel in embedded security profile: {e.info}")
            report.add_failed_parcel(parcel_name=parcel.parcel_name, parcel_type=parcel.type_, error_info=e.info)

    def push_embedded_security_policies(self) -> None:
        security_policies = [
            transformed_parcel
            for transformed_parcel in self._ux2_config.profile_parcels
            if type(transformed_parcel.parcel) in list_types(PolicyParcel)
        ]

        ng_firewalls = [
            transformed_parcel
            for transformed_parcel in self._ux2_config.profile_parcels
            if type(transformed_parcel.parcel) in list_types(NgfirewallParcel)
        ]

        for i, security_policy in enumerate(security_policies):
            parcel = cast(PolicyParcel, security_policy.parcel)
            msg = f"Creating Embedded Security policies: {parcel.parcel_name}"
            self._progress(msg, i + 1, len(security_policies))

            # 1.Create the embedded security profile id
            profile_report = self._push_embedded_security_profile(parcel.parcel_name, parcel.parcel_description)
            if (profile_id := profile_report.profile_uuid) == UUID(int=0):
                continue
            self._push_context.policy_group_feature_profiles_id_lookup[security_policy.header.origin] = profile_id

            # 2.Find the referenced ngfirewall objects, update refs and push
            fw_ids = [asm.ng_firewall.ref_id.value for asm in parcel.assembly if type(asm) is NgFirewallContainer]
            matched_fws = [fw for fw in ng_firewalls if fw.header.origin in fw_ids]
            for matched_fw in matched_fws:
                self._push_ngfirewall_parcel(profile_id, matched_fw, profile_report)

            # 3.Update the security policy parcel references and push
            self._push_policy_parcel(profile_id, security_policy, profile_report)

    def push_dns_security_policies(self) -> None:
        dns_security_policies = [
            transformed_parcel
            for transformed_parcel in self._ux2_config.profile_parcels
            if type(transformed_parcel.parcel) in list_types(AnyDnsSecurityParcel)
        ]

        for i, dns_security_policy in enumerate(dns_security_policies):
            msg = f"Creating DNS Security policies: {dns_security_policy.parcel.parcel_name}"
            self._progress(msg, i + 1, len(dns_security_policies))

            parcel = cast(AnyDnsSecurityParcel, dns_security_policy.parcel)
            parcel = update_parcel_references(parcel, self._push_context.id_lookup)

            try:
                profile_id = self._dns_security_api.create_profile(parcel.parcel_name, parcel.parcel_description).id
                self._push_result.rollback.add_feature_profile(profile_id, "dns-security")
                feature_profile_report = FeatureProfileBuildReport(
                    profile_name=parcel.parcel_name, profile_uuid=profile_id
                )
                self._push_result.report.security_policies.append(feature_profile_report)
                self._push_context.policy_group_feature_profiles_id_lookup[
                    dns_security_policy.header.origin
                ] = profile_id
            except ManagerHTTPError as e:
                logger.error(f"Error occured during DNS Security policy creation: {e.info}")
                self._push_result.report.security_policies.append(
                    FeatureProfileBuildReport(profile_name=parcel.parcel_name, profile_uuid=UUID(int=0))
                )
                continue

            try:
                parcel_id = self._dns_security_api.create_parcel(profile_id, parcel).id
                self._push_context.id_lookup[dns_security_policy.header.origin] = parcel_id
                feature_profile_report.add_created_parcel(dns_security_policy.parcel.parcel_name, parcel_id)
            except ManagerHTTPError as e:
                logger.error(f"Error occured during DNS Security policy creation: {e.info}")
                feature_profile_report.add_failed_parcel(
                    parcel_name=parcel.parcel_name, parcel_type=parcel.type_, error_info=e.info
                )
