# Copyright 2024 Cisco Systems, Inc. and its affiliates
from catalystwan.utils.config_migration.converters.utils import convert_interface_name


def test_convert_interface_name_when_name_in_mapping_expect_correct_covert():
    in_ = ["ge0/2", "ge2/0/1", "ge1/1/1", "eth0", "eth0/1/1"]
    expected_out = ["GigabitEthernet0/2", "GigabitEthernet2/0/1", "GigabitEthernet1/1/1", "Ethernet0", "Ethernet0/1/1"]

    for i, o in zip(in_, expected_out):
        assert convert_interface_name(i) == o


def test_convert_interface_name_when_name_not_in_mapping_expect_same_name():
    in_ = [
        "xe0/2",
        "ATM0/2",
        "Vlan1",
    ]

    for i in in_:
        assert convert_interface_name(i) == i
