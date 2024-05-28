import unittest
import uuid
from ipaddress import IPv4Network

from catalystwan.models.configuration.feature_profile.sdwan.system.device_access import DeviceAccessIPv4Parcel
from catalystwan.models.policy.definition.device_access import DeviceAccessPolicy
from catalystwan.utils.config_migration.converters.policy.device_access_ipv4 import device_access_ipv4_converter


class TestDeviceAccessIPv4Converter(unittest.TestCase):
    def test_device_access_ipv4_default(self):
        device_access_policy = DeviceAccessPolicy(name="device_access")
        device_access_parcel = device_access_ipv4_converter(device_access_policy)

        assert type(device_access_parcel) is DeviceAccessIPv4Parcel

    def test_device_access_ipv4_full(self):
        device_access_policy = DeviceAccessPolicy(name="device_access")
        sequence_1 = device_access_policy.add_acl_sequence(name="sequence1", device_access_protocol=22)
        sequence_1.match_destination_ip([IPv4Network("10.0.0.1/32"), IPv4Network("10.0.0.2/32")])
        sequence_1.match_source_ip([IPv4Network("10.0.0.3/32"), IPv4Network("10.0.0.4/32")])
        sequence_1.match_source_port({1, 2, 3})

        sequence_2 = device_access_policy.add_acl_sequence(name="sequence2", device_access_protocol=161)
        sequence_2.match_destination_data_prefix_list(uuid.uuid4())
        sequence_2.match_source_data_prefix_list([uuid.uuid4()])
        sequence_2.match_source_port({1, 2, 3})

        device_access_parcel = device_access_ipv4_converter(device_access_policy)

        assert type(device_access_parcel) is DeviceAccessIPv4Parcel
