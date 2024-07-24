# Copyright 2024 Cisco Systems, Inc. and its affiliates
import re

NEGATIVE_VARIABLE_REGEX = re.compile(r"[^.\/\[\]a-zA-Z0-9_-]")

INTERFACE_NAME_MAPPING = {
    "ge": "GigabitEthernet",
    "eth": "Ethernet",
}


def convert_varname(orig: str) -> str:
    return NEGATIVE_VARIABLE_REGEX.sub("_", orig)


def convert_interface_name(if_name: str) -> str:
    for key, value in INTERFACE_NAME_MAPPING.items():
        if if_name.startswith(key):
            new_if_name = value + if_name[len(key) :]
            return new_if_name
    return if_name
