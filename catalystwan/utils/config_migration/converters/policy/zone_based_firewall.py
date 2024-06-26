# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Network
from typing import List, Optional, Union, cast
from uuid import UUID

from pydantic import ValidationError

from catalystwan.models.configuration.config_migration import ConvertResult, PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.ngfirewall import (
    AipAction,
    AppList,
    AppListFlat,
    DestinationDataPrefixList,
    DestinationFqdn,
    DestinationFqdnList,
    DestinationGeoLocation,
    DestinationGeoLocationList,
    DestinationIp,
    DestinationPort,
    DestinationPortList,
    DestinationScalableGroupTagList,
    GeoLocation,
    LogAction,
    Match,
)
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.ngfirewall import (
    MatchEntry as MatchEntryV2,
)
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security.ngfirewall import (
    NgfirewallParcel,
    NgFirewallSequence,
    Protocol,
    ProtocolName,
    ProtocolNameList,
    ProtocolNameMatch,
    SourceDataPrefixList,
    SourceGeoLocation,
    SourceGeoLocationList,
    SourceIp,
    SourcePort,
    SourcePortList,
    SourceScalableGroupTagList,
)
from catalystwan.models.policy.definition.zone_based_firewall import (
    AdvancedInspectionProfileAction,
    ConnectionEventsAction,
)
from catalystwan.models.policy.definition.zone_based_firewall import LogAction as LogActionV1
from catalystwan.models.policy.definition.zone_based_firewall import ZoneBasedFWPolicy
from catalystwan.models.policy.policy_definition import ActionEntry, MatchEntry


def split_value(match_entry) -> List[str]:
    return match_entry.value.split(" ")


def convert_sequence_match_entry(
    match_entry: MatchEntry, convert_result: ConvertResult[NgfirewallParcel]
) -> Optional[MatchEntryV2]:
    if match_entry.field == "sourceDataPrefixList":
        return SourceDataPrefixList.create(match_entry.ref)
    elif match_entry.field == "destinationDataPrefixList":
        return DestinationDataPrefixList.create(match_entry.ref)
    elif match_entry.field == "destinationFqdnList":
        return DestinationFqdnList.create(match_entry.ref)
    elif match_entry.field == "sourceGeoLocationList":
        return SourceGeoLocationList.create(match_entry.ref)
    elif match_entry.field == "destinationGeoLocationList":
        return DestinationGeoLocationList.create(match_entry.ref)
    elif match_entry.field == "sourcePortList":
        return SourcePortList.create(match_entry.ref)
    elif match_entry.field == "destinationPortList":
        return DestinationPortList.create(match_entry.ref)
    elif match_entry.field == "sourceScalableGroupTagList":
        return SourceScalableGroupTagList.create(match_entry.ref)
    elif match_entry.field == "destinationScalableGroupTagList":
        return DestinationScalableGroupTagList.create(match_entry.ref)
    elif match_entry.field == "protocolNameList":
        return ProtocolNameList.create(match_entry.ref)
    elif match_entry.field == "appList":
        return AppList.create(match_entry.ref)
    elif match_entry.field == "appListFlat":
        return AppListFlat.create(match_entry.ref)
    elif match_entry.field == "sourceIp":
        if match_entry.value is not None:
            return SourceIp.from_ip_networks(list(map(IPv4Network, split_value(match_entry))))
        elif match_entry.vip_variable_name is not None:
            return SourceIp.from_variable(match_entry.vip_variable_name)
        convert_result.update_status("partial", "SrcIP match entry does not contain value/vipVariableName")
        return None
    elif match_entry.field == "destinationIp":
        if match_entry.value is not None:
            return DestinationIp.from_ip_networks(list(map(IPv4Network, split_value(match_entry))))
        elif match_entry.vip_variable_name is not None:
            return DestinationIp.from_variable(match_entry.vip_variable_name)
        convert_result.update_status("partial", "DstIP match entry does not contain value/vipVariableName")
        return None
    elif match_entry.field == "destinationFqdn":
        return DestinationFqdn.from_domain_names(split_value(match_entry))
    elif match_entry.field == "sourcePort":
        return SourcePort.from_str_list(split_value(match_entry))
    elif match_entry.field == "destinationPort":
        return DestinationPort.from_str_list(split_value(match_entry))
    elif match_entry.field == "sourceGeoLocation":
        return SourceGeoLocation.from_geo_locations_list(cast(List[GeoLocation], split_value(match_entry)))
    elif match_entry.field == "destinationGeoLocation":
        return DestinationGeoLocation.from_geo_locations_list(cast(List[GeoLocation], split_value(match_entry)))
    elif match_entry.field == "protocolName":
        return ProtocolNameMatch.from_protocol_name_list(cast(List[ProtocolName], split_value(match_entry)))
    elif match_entry.field == "protocol":
        return Protocol.from_protocol_id_list(split_value(match_entry))

    # TODO:
    # SourceIdentityList, SourceSecurityGroup, DestinationSecurityGroup
    # SourceIdentityUser,SourceIdentityUserGroup, App, AppFamily
    convert_result.update_status(
        "partial", f"Unknown conversion of firewall sequence match entry with type: {match_entry.field}"
    )
    return None


def convert_sequence_match(match, convert_result: ConvertResult[NgfirewallParcel]):
    entries = [convert_sequence_match_entry(entry, convert_result) for entry in match.entries]
    return Match(entries=[entry for entry in entries if entry is not None])


def convert_sequence_actions(
    actions: List[Union[LogActionV1, AdvancedInspectionProfileAction, ConnectionEventsAction]],
    convert_result: ConvertResult[NgfirewallParcel],
) -> List[Union[LogAction, AipAction]]:
    converted_actions = [convert_sequence_action_entry(action, convert_result) for action in actions]
    filtered_actions = [action for action in converted_actions if action is not None]
    return filtered_actions


def convert_sequence_action_entry(
    action: ActionEntry, convert_result: ConvertResult[NgfirewallParcel]
) -> Optional[Union[LogAction, AipAction]]:
    if action.type == "log":
        return LogAction.from_sequence_action("log")
    elif action.type == "advancedInspectionProfile":
        return AipAction.from_uuid(action.parameter.ref)
    elif action.type == "connectionEvents":
        return LogAction.from_sequence_action("connectionEvents")

    convert_result.update_status("partial", f"Unknown conversion of firewall sequence action type: {type(action)}")
    return None


def convert_zone_based_fw(
    in_: ZoneBasedFWPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[NgfirewallParcel]:
    convert_result = ConvertResult[NgfirewallParcel]()

    if in_.definition.entries:
        context.zone_based_firewall_residues[uuid] = in_.definition.entries

    try:
        sequences = [
            NgFirewallSequence.create(
                **sequence.model_dump(exclude={"sequence_ip_type", "ruleset", "sequence_type", "match", "actions"}),
                match=convert_sequence_match(sequence.match, convert_result),
                actions=convert_sequence_actions(sequence.actions, convert_result),
            )
            for sequence in in_.definition.sequences
        ]

        parcel = NgfirewallParcel.create(
            parcel_name=in_.name,
            parcel_description=in_.description,
            default_action_type=in_.definition.default_action.type,
            sequences=sequences,
        )
        convert_result.output = parcel

    except ValidationError as e:
        convert_result.update_status("failed", f"Cannot convert zone based firewall due to error {e}")

    return convert_result
