# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from ipaddress import IPv6Interface
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import DeviceAccessIPv6Parcel
from catalystwan.models.policy.definition.device_access_ipv6 import (
    DeviceAccessIPv6Policy,
    DeviceAccessIPv6PolicySequence,
)
from catalystwan.models.policy.policy_definition import PolicyAcceptDropAction
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestDeviceAccessIpv6Converter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_device_access_ipv6_convert_when_prefix_list_is_uuid(self):
        # Arrange
        destination_data_prefix_uuid = uuid4()
        destination_port = 161
        source_data_prefix_uuid = uuid4()
        policy = DeviceAccessIPv6Policy(
            name="device_access_ipv6",
            description="test_description",
            sequences=[],
            default_action=PolicyAcceptDropAction(type="drop"),
        )
        seq = DeviceAccessIPv6PolicySequence(
            sequence_id=1,
            sequence_name="test_sequence",
            base_action="accept",
            sequence_ip_type="ipv6",
        )
        seq.match_destination_data_prefix_list(data_prefix_list_id=destination_data_prefix_uuid)
        seq.match_device_access_protocol(port=destination_port)
        seq.match_source_data_prefix_list(data_prefix_list_id=source_data_prefix_uuid)
        seq.match_source_port(ports={80}, port_ranges=[(30, 32)])
        policy.sequences.append(seq)
        uuid = uuid4()
        # Act
        parcel = convert(policy, uuid, context=self.context).output
        # Assert
        assert isinstance(parcel, DeviceAccessIPv6Parcel)
        assert parcel.parcel_name == "device_access_ipv6"
        assert parcel.parcel_description == "test_description"
        assert parcel.default_action.value == "drop"
        assert len(parcel.sequences) == 1

        seq = parcel.sequences[0]
        assert seq.sequence_name.value == "test_sequence"
        assert seq.base_action.value == "accept"
        assert seq.sequence_id.value == 1
        assert seq.match_entries.destination_data_prefix.destination_data_prefix_list.ref_id.value == str(
            destination_data_prefix_uuid
        )
        assert seq.match_entries.destination_port.value == destination_port
        assert seq.match_entries.source_data_prefix.source_data_prefix_list.ref_id.value == str(source_data_prefix_uuid)
        assert seq.match_entries.source_ports.value == [30, 31, 32, 80]

    def test_device_access_ipv6_convert_when_prefix_list_is_ip(self):
        # Arrange
        destination_ip = [IPv6Interface("::3e46/128"), IPv6Interface("::3e47/128")]
        destination_port = 161
        source_ip = [IPv6Interface("::3e48/128"), IPv6Interface("::3e49/128")]
        policy = DeviceAccessIPv6Policy(
            name="device_access_ipv6",
            description="test_description",
            sequences=[],
            default_action=PolicyAcceptDropAction(type="drop"),
        )
        seq = DeviceAccessIPv6PolicySequence(
            sequence_id=1,
            sequence_name="test_sequence",
            base_action="accept",
            sequence_ip_type="ipv6",
        )
        seq.match_destination_ip(networks=destination_ip)
        seq.match_device_access_protocol(port=destination_port)
        seq.match_source_ip(networks=source_ip)
        seq.match_source_port(ports={80}, port_ranges=[(30, 32)])
        policy.sequences.append(seq)
        uuid = uuid4()
        # Act
        parcel = convert(policy, uuid, context=self.context).output
        # Assert
        assert isinstance(parcel, DeviceAccessIPv6Parcel)
        assert parcel.parcel_name == "device_access_ipv6"
        assert parcel.parcel_description == "test_description"
        assert parcel.default_action.value == "drop"
        assert len(parcel.sequences) == 1

        seq = parcel.sequences[0]
        assert seq.sequence_name.value == "test_sequence"
        assert seq.base_action.value == "accept"
        assert seq.sequence_id.value == 1
        assert seq.match_entries.destination_data_prefix.destination_ip_prefix_list.value == destination_ip
        assert seq.match_entries.destination_port.value == destination_port
        assert seq.match_entries.source_data_prefix.source_ip_prefix_list.value == source_ip
        assert seq.match_entries.source_ports.value == [30, 31, 32, 80]
