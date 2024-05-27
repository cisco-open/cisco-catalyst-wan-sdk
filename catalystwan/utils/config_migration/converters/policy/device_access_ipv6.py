import re
from typing import List, Optional, cast

from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import (
    DestinationPort,
    DeviceAccessIPv6Parcel,
    Sequence,
)
from catalystwan.models.policy.definition.device_access_ipv6 import (
    DeviceAccessIPv6Policy,
    DeviceAccessIPv6PolicySequenceMatchEntry,
)
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


def device_access_ipv6_converter(in_: DeviceAccessIPv6Policy, **context) -> DeviceAccessIPv6Parcel:
    device_access_ipv6_parcel = DeviceAccessIPv6Parcel(
        parcel_name=in_.name,
        parcel_description=in_.description,
    )

    default_action = in_.default_action.type
    device_access_ipv6_parcel.set_default_action(default_action)

    for sequence in in_.sequences:
        destination_port = get_destination_port(sequence.match.entries)
        if destination_port is None:
            raise CatalystwanConverterCantConvertException("Device Access requires destination port!")
        converted_sequence = device_access_ipv6_parcel.add_sequence(
            sequence_id=sequence.sequence_id,
            sequence_name=sequence.sequence_name,
            base_action=sequence.base_action,
            destination_port=destination_port,
        )
        add_matches(converted_sequence, sequence.match.entries)

    return device_access_ipv6_parcel


def get_destination_port(match_entries: List[DeviceAccessIPv6PolicySequenceMatchEntry]) -> Optional[DestinationPort]:
    for match_entry in match_entries:
        if match_entry.field == "destinationPort":
            return cast(DestinationPort, int(match_entry.value))
    return None


def add_matches(sequence: Sequence, match_entries: List[DeviceAccessIPv6PolicySequenceMatchEntry]):
    for match_entry in match_entries:
        if match_entry.field == "sourcePort":
            source_ports = [int(value) for value in match_entry.value.split()]
            sequence.match_source_ports(source_ports)

        elif match_entry.field == "sourceIpv6":
            sequence.match_source_data_prefix_ip_list(re.split(r"[,\s]+", match_entry.value))

        elif match_entry.field == "sourceDataIpv6PrefixList":
            sequence.match_source_data_prefix_id(match_entry.ref[0])

        elif match_entry.field == "destinationIpv6":
            sequence.match_destination_data_prefix_ip_list(re.split(r"[,\s]+", match_entry.value))

        elif match_entry.field == "destinationDataIpv6PrefixList":
            sequence.match_destination_data_prefix_id(match_entry.ref[0])
