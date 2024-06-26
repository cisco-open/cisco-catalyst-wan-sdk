# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Union
from uuid import UUID

from catalystwan.models.configuration.config_migration import (
    ConvertResult,
    PolicyConvertContext,
    SecurityPolicyResidues,
)
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import PolicyParcel, PolicySettings
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.policy import NgFirewallEntry
from catalystwan.models.policy.security import (
    AnySecurityPolicyInfo,
    NGFirewallAssemblyItem,
    SecurityPolicySettings,
    ZoneBasedFWAssemblyItem,
)


def convert_security_policy(
    in_: AnySecurityPolicyInfo, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[PolicyParcel]:
    convert_result = ConvertResult[PolicyParcel]()

    settings = in_.policy_definition.settings
    if type(settings) is SecurityPolicySettings:
        residues = SecurityPolicyResidues(
            high_speed_logging_setting=settings.high_speed_logging,
            logging_setting=settings.logging,
            zone_to_no_zone_internet_setting=settings.zone_to_no_zone_internet,
            platform_match_setting=settings.platform_match,
        )
    else:
        residues = SecurityPolicyResidues(
            high_speed_logging_setting=settings.high_speed_logging,
        )

    context.security_policy_residues[uuid] = residues

    try:
        convert_result.output = PolicyParcel(
            parcel_name=in_.policy_name,
            parcel_description=in_.policy_description,
            settings=PolicySettings.create(
                **in_.policy_definition.settings.model_dump(
                    exclude={"high_speed_logging", "logging", "zone_to_no_zone_internet", "platform_match"}
                )
            ),
        )

        for assembly in in_.policy_definition.assembly:
            if assembly.type == "zoneBasedFW":
                entries = _convert_security_policy_entries(assembly, context)
                convert_result.output.add_ng_firewall_assembly(ng_firewall_id=assembly.definition_id, entries=entries)
            elif assembly.type == "advancedInspectionProfile":
                convert_result.output.add_advanced_inspection_profile_assembly(assembly.definition_id)
            elif assembly.type == "sslDecryption":
                convert_result.output.add_ssl_decryption_assembly(assembly.definition_id)
            else:
                convert_result.update_status(
                    "partial", f"Unknown conversion of security policy assembly type: {assembly.type}"
                )
    except Exception as e:
        convert_result.update_status("failed", f"Cannot convert SecurityPolicy due to an error {e}")

    return convert_result


def _convert_security_policy_entries(
    assembly: Union[ZoneBasedFWAssemblyItem, NGFirewallAssemblyItem], context: PolicyConvertContext
) -> List[NgFirewallEntry]:
    target_entries = []

    if assembly.entries:
        for entry in assembly.entries:
            target_entries.append(NgFirewallEntry.create(entry.src_zone_list_id, entry.dst_zone_list_id))

    if firewall_entries_residues := context.zone_based_firewall_residues.get(assembly.definition_id):  # change
        for entry_2 in firewall_entries_residues:
            target_entries.append(NgFirewallEntry.create(entry_2.source_zone_id, entry_2.destination_zone_id))

    return target_entries
