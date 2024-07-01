# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from ipaddress import AddressValueError, IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import List, Optional, Union, get_args

from catalystwan.api.configuration_groups.parcel import Global, Variable, as_global, as_variable
from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.models.common import (
    EthernetDuplexMode,
    EthernetNatType,
    IkeCiphersuite,
    IkeMode,
    IpsecCiphersuite,
    MetricType,
    PfsGroup,
    SubnetMask,
    TLOCColor,
    VrrpTrackerAction,
)
from catalystwan.models.configuration.feature_profile.common import TunnelApplication
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospf import (
    AdvertiseType,
    AreaType,
    AuthenticationType,
    RedistributeProtocolOspf,
)
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospfv3 import NetworkType
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import MediaType
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import GreTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import IpsecTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import Direction
from catalystwan.models.configuration.feature_profile.sdwan.service.switchport import (
    ControlDirection,
    Duplex,
    HostMode,
    PortControl,
    SwitchportMode,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.wireless_lan import (
    CountryCode,
    QosProfile,
    RadioType,
    SecurityType,
)
from catalystwan.models.configuration.feature_profile.sdwan.system.logging_parcel import (
    AuthType,
    CypherSuite,
    Priority,
    TlsVersion,
)
from catalystwan.models.configuration.feature_profile.sdwan.system.mrf import EnableMrfMigration, Role
from catalystwan.utils.config_migration.converters.utils import convert_varname

"""List of all literals that can be casted."""
CastableLiterals = Union[
    Priority,
    TlsVersion,
    AuthType,
    CypherSuite,
    Role,
    EnableMrfMigration,
    TLOCColor,
    SubnetMask,
    Direction,
    IkeCiphersuite,
    IkeMode,
    IpsecCiphersuite,
    PfsGroup,
    TunnelApplication,
    GreTunnelMode,
    VrrpTrackerAction,
    Duplex,
    EthernetDuplexMode,
    MediaType,
    EthernetNatType,
    IpsecTunnelMode,
    NetworkType,
    AuthenticationType,
    AreaType,
    AdvertiseType,
    RedistributeProtocolOspf,
    MetricType,
    SwitchportMode,
    PortControl,
    HostMode,
    ControlDirection,
    CountryCode,
    RadioType,
    QosProfile,
    SecurityType,
]

CastedTypes = Union[
    Global[bool],
    Global[str],
    Global[int],
    Global[List[str]],
    Global[List[int]],
    Global[IPv4Address],
    Global[IPv6Address],
    Global[IPv4Interface],
    Global[IPv6Interface],
    Global[CastableLiterals],
    Variable,
]

logger = logging.getLogger(__name__)


def to_snake_case(s: str) -> str:
    """Converts a string from kebab-case to snake_case."""
    return s.replace("-", "_")


def cast_value_to_global(value: Union[DeviceVariable, str, int, List[str], List[int]]) -> CastedTypes:
    if isinstance(value, DeviceVariable):
        converted_name = convert_varname(value.name)
        if converted_name != value.name:
            logger.info(f"Converted variable name: {value.name} -> {converted_name}")
        return as_variable(value=converted_name)
    if isinstance(value, list):
        value_type = Global[List[int]] if isinstance(value[0], int) else Global[List[str]]
        return value_type(value=value)  # type: ignore
    if isinstance(value, str):
        for cast_func in [try_cast_to_literal, try_cast_to_bool, try_cast_to_address]:
            if global_value := cast_func(value):
                return global_value
    return as_global(value)  # type: ignore


def try_cast_to_address(value: str) -> Optional[Global]:
    """Tries to cast a string to an IP address or interface."""
    for address_type in [IPv4Address, IPv6Address, IPv4Interface, IPv6Interface]:
        try:
            return Global[address_type](value=address_type(value))  # type: ignore
        except AddressValueError:
            pass
    return None


def try_cast_to_literal(value: str) -> Optional[Global[CastableLiterals]]:
    """Tries to cast a string to a literal."""
    for literal in get_args(CastableLiterals):
        if value in get_args(literal):
            return Global[literal](value=value)  # type: ignore
    return None


def try_cast_to_bool(value: str) -> Optional[Global[bool]]:
    """Tries to cast the given value to a boolean."""
    if value.lower() == "true":
        return Global[bool](value=True)
    elif value.lower() == "false":
        return Global[bool](value=False)
    return None


def transform_dict(d: dict) -> dict:
    """Transforms a nested dictionary into a normalized form."""

    def transform_value(value: Union[dict, list, str, int]) -> Union[CastedTypes, dict, list]:
        if isinstance(value, dict):
            return transform_dict(value)
        elif isinstance(value, list):
            if all(isinstance(v, dict) for v in value):
                return [transform_value(item) for item in value]
        return cast_value_to_global(value)

    return {to_snake_case(key): transform_value(val) for key, val in d.items()}


def template_values_normalization(template_values: dict) -> dict:
    """Normalizes template_values by changing keys to snake_case and
    cast all values to Global types or Variables."""
    return transform_dict(template_values)
