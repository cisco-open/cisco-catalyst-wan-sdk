import logging
from typing import Callable, Mapping, Type, cast
from uuid import UUID

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    PushContext,
    TransformedParcel,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.common import RefIdItem, RefIdList
from catalystwan.models.configuration.feature_profile.parcel import AnyDnsSecurityParcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import NgfirewallParcel, PolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.ngfirewall import (
    AipAction,
    AppList,
    AppListFlat,
    DestinationFqdnList,
    DestinationGeoLocationList,
    DestinationPortList,
    DestinationScalableGroupTagList,
    NgFirewallSequence,
    ProtocolNameList,
    SourceDataPrefixList,
    SourceGeoLocationList,
    SourcePortList,
    SourceScalableGroupTagList,
)
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.policy import (
    AdvancedInspectionProfile,
    NgFirewallContainer,
    NgFirewallEntry,
    SslDecryption,
)
from catalystwan.session import ManagerSession

from .references_updater import ReferencesUpdater, update_parcels_references

logger = logging.getLogger(__name__)


class DnsSecurityReferencesUpdater(ReferencesUpdater):
    def update_references(self) -> None:
        parcel = cast(AnyDnsSecurityParcel, self.parcel)
        if local_domain_bypass_list := parcel.local_domain_bypass_list:
            target_uuid = self.get_target_uuid(local_domain_bypass_list.ref_id.value)
            parcel.local_domain_bypass_list = RefIdItem.from_uuid(target_uuid)


class SecurityPolicyReferencesUpdater(ReferencesUpdater):
    def _update_ng_firewall_entry_refs(self, entry: NgFirewallEntry) -> None:
        if type(entry.src_zone) is RefIdItem:
            entry.src_zone = RefIdItem.from_uuid(self.get_target_uuid(entry.src_zone.ref_id.value))

        if type(entry.dst_zone) is RefIdItem:
            entry.dst_zone = RefIdItem.from_uuid(self.get_target_uuid(entry.dst_zone.ref_id.value))

    def update_references(self) -> None:
        parcel = cast(PolicyParcel, self.parcel)
        for assembly in parcel.assembly:
            if type(assembly) is SslDecryption:
                target_uuid = self.get_target_uuid(assembly.ssl_decryption.ref_id.value)
                assembly.ssl_decryption = RefIdItem.from_uuid(target_uuid)
            elif type(assembly) is AdvancedInspectionProfile:
                target_uuid = self.get_target_uuid(assembly.advanced_inspection_profile.ref_id.value)
                assembly.advanced_inspection_profile = RefIdItem.from_uuid(target_uuid)
            elif type(assembly) is NgFirewallContainer:
                target_uuid = self.get_target_uuid(assembly.ng_firewall.ref_id.value)
                assembly.ng_firewall.ref_id.value = target_uuid

                for entry in assembly.ng_firewall.entries:
                    self._update_ng_firewall_entry_refs(entry)


class NgfirewallReferencesUpdater(ReferencesUpdater):
    def _update_actions(self, sequence: NgFirewallSequence) -> None:
        for action in sequence.actions:
            if type(action) is AipAction:
                uuid = self.get_target_uuid(action.parameter.ref_id.value)
                action.parameter = RefIdItem.from_uuid(uuid)

    def _update_match_entries(self, sequence: NgFirewallSequence) -> None:
        for entry in sequence.match.entries:
            if type(entry) is SourceDataPrefixList:
                uuids = entry.source_data_prefix_list.ref_id.value
                entry.source_data_prefix_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is DestinationFqdnList:
                uuids = entry.destination_fqdn_list.ref_id.value
                entry.destination_fqdn_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is SourceGeoLocationList:
                uuids = entry.source_geo_location_list.ref_id.value
                entry.source_geo_location_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is DestinationGeoLocationList:
                uuids = entry.destination_geo_location_list.ref_id.value
                entry.destination_geo_location_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is SourcePortList:
                uuids = entry.source_port_list.ref_id.value
                entry.source_port_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is DestinationPortList:
                uuids = entry.destination_port_list.ref_id.value
                entry.destination_port_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is SourceScalableGroupTagList:
                uuids = entry.source_scalable_group_tag_list.ref_id.value
                entry.source_scalable_group_tag_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is DestinationScalableGroupTagList:
                uuids = entry.destination_scalable_group_tag_list.ref_id.value
                entry.destination_scalable_group_tag_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is ProtocolNameList:
                uuids = entry.protocol_name_list.ref_id.value
                entry.protocol_name_list = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))
            elif type(entry) is AppList:
                entry.app_list = RefIdList.from_uuids(list(map(self.get_target_uuid, entry.app_list.ref_id.value)))
            elif type(entry) is AppListFlat:
                uuids = entry.app_list_flat.ref_id.value
                entry.app_list_flat = RefIdList.from_uuids(list(map(self.get_target_uuid, uuids)))

    def update_references(self) -> None:
        parcel = cast(NgfirewallParcel, self.parcel)
        for sequence in parcel.sequences:
            self._update_match_entries(sequence)
            self._update_actions(sequence)


REFERENCES_UPDATER_MAPPING: Mapping[type, Type[ReferencesUpdater]] = {
    AnyDnsSecurityParcel: DnsSecurityReferencesUpdater,
    NgfirewallParcel: NgfirewallReferencesUpdater,
    PolicyParcel: SecurityPolicyReferencesUpdater,
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
        self._embedded_security_api = session.api.sdwan_feature_profiles.embedded_security
        self._push_result: UX2ConfigPushResult = push_result
        self._progress: Callable[[str, int, int], None] = progress
        self.push_context = push_context

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
        update_parcels_references(parcel, self.push_context.id_lookup, REFERENCES_UPDATER_MAPPING)

        try:
            fw_id = self._embedded_security_api.create_parcel(profile_id, parcel).id
            report.add_created_parcel(parcel.parcel_name, fw_id)
            self.push_context.id_lookup[firewall.header.origin] = fw_id
        except ManagerHTTPError as e:
            logger.error(f"Error occured during creating NGFirewall in embedded security profile: {e.info}")
            report.add_failed_parcel(parcel_name=parcel.parcel_name, parcel_type=parcel.type_, error_info=e.info)

    def _push_policy_parcel(
        self, profile_id: UUID, policy: TransformedParcel, report: FeatureProfileBuildReport
    ) -> None:
        parcel = cast(PolicyParcel, policy.parcel)

        try:
            update_parcels_references(parcel, self.push_context.id_lookup, REFERENCES_UPDATER_MAPPING)
            security_policy_parcel_id = self._embedded_security_api.create_parcel(profile_id, parcel).id
            report.add_created_parcel(parcel.parcel_name, security_policy_parcel_id)
            self.push_context.id_lookup[policy.header.origin] = security_policy_parcel_id
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
            except ManagerHTTPError as e:
                logger.error(f"Error occured during DNS Security policy creation: {e.info}")
                feature_profile_report.add_failed_parcel(
                    parcel_name=parcel.parcel_name, parcel_type=parcel.type_, error_info=e.info
                )
