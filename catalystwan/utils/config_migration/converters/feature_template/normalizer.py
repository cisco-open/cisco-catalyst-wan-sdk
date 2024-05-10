from ipaddress import AddressValueError, IPv4Address, IPv4Interface, IPv6Address, IPv6Interface
from typing import Any, Dict, List, Literal, Optional, Union, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.common import (
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
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ethernet import DuplexMode, MediaType, NatType
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.gre import GreTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.ipsec import IpsecTunnelMode
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import Direction
from catalystwan.models.configuration.feature_profile.sdwan.service.ospf import (
    AdvertiseType,
    AreaType,
    AuthenticationType,
    RedistributeProtocolOspf,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.ospfv3 import NetworkType
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
    DuplexMode,
    MediaType,
    NatType,
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
]


def to_snake_case(s: str) -> str:
    """Converts a string from kebab-case to snake_case."""
    return s.replace("-", "_")


def cast_value_to_global(value: Union[str, int, List[str], List[int]]) -> CastedTypes:
    """Casts value to Global."""
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


def template_definition_normalization(template_definition: dict) -> dict:
    """Normalizes a template definition by changing keys to snake_case and casting all leafs values to global types."""
    return transform_dict(template_definition)


def normalize_to_model_definition(d: dict, model_fields: Dict[str, FieldInfo]) -> dict:
    """Attempts to cast fields into types given in model definition."""

    def get_global(field_info: FieldInfo):
        def extract_from_annotation(annotation):
            if get_origin(annotation) is Union:
                for nested_annotation in get_args(annotation):
                    extracted_value = extract_from_annotation(nested_annotation)
                    if issubclass(extracted_value, Global):
                        return extracted_value
            return annotation

        annotation = field_info.annotation
        return extract_from_annotation(annotation)

    def transform_value(value: Union[dict, list, str, int], field_info: FieldInfo) -> Any:
        if value is None:
            return value
        elif isinstance(value, dict):
            return value
        elif isinstance(value, list):
            if get_origin(field_info.annotation) is not List:
                return value
            annotation = get_args(field_info.annotation)[0]
            if issubclass(get_args(annotation)[0], BaseModel):
                return value
            return [transform_value(item, field_info) for item in value]

        global_type = get_global(field_info)
        cast_type = global_type.model_fields["value"].annotation
        if isinstance(value, Global):
            value = value.value
        try:
            if get_origin(cast_type) is Literal:
                literal_args = get_args(cast_type)
                if all(isinstance(v, str) for v in literal_args):
                    return global_type(value=str(value))  # type: ignore
                if all(isinstance(v, int) for v in literal_args):
                    return global_type(value=int(value))  # type: ignore
                return global_type(value=value)
            elif cast_type is bool:
                return global_type(value=True)
            else:
                return global_type(value=cast_type(value))
        except ValueError:
            return value

    result = {}
    for key, val in d.items():
        try:
            result[to_snake_case(key)] = transform_value(val, model_fields[to_snake_case(key)])
        except KeyError:
            pass
    return result


def flatten_datapaths(original_dict: dict) -> dict:
    """
    Flattens datapaths. Conflicting leaf names within the same level need to be resolved manually beforehand.
    Does not attempt to traverse list values, since they're usually nested models.
    """

    def get_flattened_dict(
        original_dict: dict,
        flattened_dict: Optional[dict] = None,
    ):
        if flattened_dict is None:
            flattened_dict = {}
        for key, value in original_dict.items():
            if isinstance(value, dict):
                get_flattened_dict(value, flattened_dict)
            else:
                flattened_dict[key] = value
        return flattened_dict

    flattened_dict: dict = {}
    get_flattened_dict(original_dict, flattened_dict)
    return flattened_dict
