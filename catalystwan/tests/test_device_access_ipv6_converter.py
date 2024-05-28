import unittest
from ipaddress import IPv6Network

from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import DeviceAccessIPv6Parcel
from catalystwan.models.policy.definition.device_access_ipv6 import DeviceAccessIPv6Policy
from catalystwan.utils.config_migration.converters.policy.device_access_ipv6 import device_access_ipv6_converter


class TestDeviceAccessIPv4Converter(unittest.TestCase):
    def test_device_access_ipv6_default(self):
        device_access_policy = DeviceAccessIPv6Policy(name="device_access")
        device_access_parcel = device_access_ipv6_converter(device_access_policy)

        assert type(device_access_parcel) is DeviceAccessIPv6Parcel

    def test_device_access_ipv4_full(self):
        device_access_policy = DeviceAccessIPv6Policy(name="device_access")
        sequence = device_access_policy.add_acl_sequence(name="sequence1", device_access_protocol=22)
        sequence.match_destination_ip([IPv6Network("::3e46/128"), IPv6Network("::3e47/128")])
        sequence.match_source_ip([IPv6Network("::3e48/128"), IPv6Network("::3e49/128")])
        sequence.match_source_port({1, 2, 3})

        device_access_parcel = device_access_ipv6_converter(device_access_policy)

        assert type(device_access_parcel) is DeviceAccessIPv6Parcel
