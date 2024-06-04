# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
import re
from typing import Dict, Union

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

logger = logging.getLogger(__name__)

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
            logger.info(f"Converted interface name: {if_name} -> {new_if_name}")
            return new_if_name
    return if_name


def parse_interface_name(data: Dict) -> Union[Global[str], Variable]:
    if_name = data.get("if_name")
    if isinstance(if_name, Variable):
        return if_name
    elif isinstance(if_name, Global):
        return as_global(convert_interface_name(if_name.value))
    raise CatalystwanConverterCantConvertException("Interface name is required")
