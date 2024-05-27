from typing import List, Optional, cast

from catalystwan.models.configuration.feature_profile.sdwan.system.device_access import (
    DestinationPort,
    DeviceAccessIPv4Parcel,
    Sequence,
)
from catalystwan.models.policy.definition.device_access import DeviceAccessPolicy, DeviceAccessPolicySequenceMatchEntry
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


def device_access_ipv4_converter(in_: DeviceAccessPolicy, **context) -> DeviceAccessIPv4Parcel:
    device_access_ipv4_parcel = DeviceAccessIPv4Parcel(
        parcel_name=in_.name,
        parcel_description=in_.description,
    )

    default_action = in_.default_action.type
    device_access_ipv4_parcel.set_default_action(default_action)

    for sequence in in_.sequences:
        destination_port = get_destination_port(sequence.match.entries)
        if destination_port is None:
            raise CatalystwanConverterCantConvertException("Device Access requires destination port!")
        converted_sequence = device_access_ipv4_parcel.add_sequence(
            sequence_id=sequence.sequence_id,
            sequence_name=sequence.sequence_name,
            base_action=sequence.base_action,
            destination_port=destination_port,
        )
        add_matches(converted_sequence, sequence.match.entries)

    return device_access_ipv4_parcel


def get_destination_port(match_entries: List[DeviceAccessPolicySequenceMatchEntry]) -> Optional[DestinationPort]:
    for match_entry in match_entries:
        if match_entry.field == "destinationPort":
            return cast(DestinationPort, int(match_entry.value))
    return None


def add_matches(sequence: Sequence, match_entries: List[DeviceAccessPolicySequenceMatchEntry]):
    for match_entry in match_entries:
        if match_entry.field == "sourcePort":
            source_ports = [int(value) for value in match_entry.value.split()]
            sequence.match_source_ports(source_ports)

        elif match_entry.field == "sourceIp":
            if match_entry.vipVariableName is not None:
                sequence.match_source_data_prefix_ip_variable(match_entry.vipVariableName)
            elif match_entry.value is not None:
                sequence.match_source_data_prefix_ip_list(match_entry.value.split())

        elif match_entry.field == "sourceDataPrefixList":
            sequence.match_source_data_prefix_id(match_entry.ref[0])

        elif match_entry.field == "destinationIp":
            if match_entry.vipVariableName is not None:
                sequence.match_destination_data_prefix_ip_variable(match_entry.vipVariableName)
            elif match_entry.value is not None:
                sequence.match_destination_data_prefix_ip_list(match_entry.value.split())

        elif match_entry.field == "destinationDataPrefixList":
            sequence.match_destination_data_prefix_id(match_entry.ref[0])
