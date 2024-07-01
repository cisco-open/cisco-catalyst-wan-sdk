# Copyright 2024 Cisco Systems, Inc. and its affiliates
import re
from typing import Dict, Union

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.feature_template.base import FTConverter

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


def parse_interface_name(converter: FTConverter, data: Dict) -> Union[Global[str], Variable]:
    if_name = data.get("if_name")
    if isinstance(if_name, Variable):
        return if_name
    elif isinstance(if_name, Global):
        converted_if_name = convert_interface_name(if_name.value)
        if converted_if_name != if_name.value:
            converter._convert_result.update_status(
                "partial", f"Converted interface name: {if_name.value} -> {converted_if_name}"
            )
        return as_global(converted_if_name)
    raise CatalystwanConverterCantConvertException("Interface name is required")
