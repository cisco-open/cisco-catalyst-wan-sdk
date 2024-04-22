# Copyright 2023 Cisco Systems, Inc. and its affiliates

from dataclasses import InitVar, dataclass, field
from typing import Any, Dict, List, Literal, Optional, Sequence, Set, Tuple, Union
from uuid import UUID

from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import PlainSerializer, SerializationInfo
from pydantic.fields import FieldInfo
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated


@dataclass()
class VersionedField:
    """
    This class could be used as field type annotation for pydantic.BaseModel fields.
    Together with dedicated @model_serializer it allows pick different serialization alias.
    When version provided as specifier set eg. ">=20.13" matches Manager API version detected at runtime
    original serialization_alias will be overriden.

    Example:
    >>> from catalystwan.models.common import VersionedField
    >>> from pydantic import BaseModel, SerializationInfo, SerializerFunctionWrapHandler, model_serializer
    >>> from typing_extensions import Annotated
    >>>
    >>> class Payload(BaseModel):
    >>>     snake_case: Annotated[int, VersionedField(versions="<=20.12", serialization_alias="kebab-case")]
    >>>
    >>> @model_serializer(mode="wrap", when_used="json")
    >>>     def serialize(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> Dict[str, Any]:
    >>>         return VersionedField.update_model_fields(self.model_fields, handler(self), info)
    """

    versions: InitVar[str]
    versions_set: SpecifierSet = field(init=False)
    serialization_alias: str

    def __post_init__(self, versions):
        self.versions_set = SpecifierSet(versions)

    @staticmethod
    def update_model_fields(
        model_fields: Dict[str, FieldInfo], model_dict: Dict[str, Any], serialization_info: SerializationInfo
    ) -> Dict[str, Any]:
        """To be reused in methods decorated with pydantic.model_serializer
        Args:
            model_fields (Dict[str, FieldInfo]): obtained from BaseModel class
            model_dict (Dict[str, Any]): obtained from serialized BaseModel instance
            serialization_info (SerializationInfo): passed from serializer

        Returns:
            Dict[str, Any]: model_dict with updated field names according to matching runtime version
        """
        if serialization_info.context is not None:
            api_version: Optional[Version] = serialization_info.context.get("api_version")
            if api_version is not None:
                for field_name, field_info in model_fields.items():
                    versioned_fields = [meta for meta in field_info.metadata if isinstance(meta, VersionedField)]
                    for versioned_field in versioned_fields:
                        if api_version in versioned_field.versions_set:
                            current_field_name = field_info.serialization_alias or field_info.alias or field_name
                            if model_dict.get(current_field_name) is not None:
                                model_dict[versioned_field.serialization_alias] = model_dict[current_field_name]
                                del model_dict[current_field_name]
        return model_dict


def check_fields_exclusive(values: Dict, field_names: Set[str], at_least_one: bool = False) -> bool:
    """Helper method to check fields are mutually exclusive

    Args:
        values (Dict): BaseModel field values
        field_names (Set[str]): set of field names that we want to be mutually exclusive
        at_least_one (bool, optional): Additionaly check if at least one of fields is not None

    Raises:
        ValueError: When fields are not mutually exclusive

    Returns:
        bool: True if at least one field was present
    """
    assigned = [values.get(field_name) for field_name in field_names if values.get(field_name) is not None]
    if len(assigned) == 0 and at_least_one:
        raise ValueError(f"At least one of given fields {field_names} must be assigned")
    if len(assigned) > 1:
        raise ValueError(f"Fields {field_names} are mutually exclusive")
    return True if len(assigned) > 0 else False


def check_any_of_exclusive_field_sets(values: Dict, field_sets: List[Tuple[Set[str], bool]]):
    """This is very specific validator but common in policy definitions model.
    It checks that fields in each of the sets are mutually exclusive and also
    guarantees that at least one of the values is present from all sets.

    Args:
        values (Dict): BaseModel field values
        field_sets (Set[Tuple[Set[str]], bool]): Set of tuples each tuple should
        contain field names set and flag to check if at least one of fields is present within a set

    Raises:
        ValueError: When fields are not mutually exclusive or none of the field values is present

    """
    any_assigned = False
    for field_names, at_least_one in field_sets:
        if check_fields_exclusive(values, field_names, at_least_one):
            any_assigned = True
    if not any_assigned:
        all_sets_field_names = [s[0] for s in field_sets]
        raise ValueError(f"One of {all_sets_field_names} must be assigned")


IntStr = Annotated[
    int,
    PlainSerializer(lambda x: str(x), return_type=str, when_used="json-unless-none"),
    BeforeValidator(lambda x: int(x)),
]

IntRange = Tuple[int, Optional[int]]


def int_range_str_validator(value: Union[str, IntRange], ascending: bool = True) -> IntRange:
    """Validates input given as string containing integer pair separated by hyphen eg: '1-3' or single number '1'"""
    if isinstance(value, str):
        int_list = [int(i) for i in value.strip().split("-")]
        assert 0 < len(int_list) <= 2, "Number range must contain one or two numbers"
        first = int_list[0]
        second = None if len(int_list) == 1 else int_list[1]
        int_range = (first, second)
    else:
        int_range = value
    if ascending and int_range[1] is not None:
        assert int_range[0] < int_range[1], "Numbers in range must be in ascending order"
    return int_range


def int_range_serializer(value: IntRange) -> str:
    """Serializes integer pair as string separated by hyphen eg: '1-3' or single number '1'"""
    return "-".join((str(i) for i in value if i is not None))


IntRangeStr = Annotated[
    IntRange,
    PlainSerializer(int_range_serializer, return_type=str, when_used="json-unless-none"),
    BeforeValidator(int_range_str_validator),
]


def str_as_uuid_list(val: Union[str, Sequence[UUID]]) -> Sequence[UUID]:
    if isinstance(val, str):
        return [UUID(uuid_) for uuid_ in val.split()]
    return val


def str_as_str_list(val: Union[str, Sequence[str]]) -> Sequence[str]:
    if isinstance(val, str):
        return val.split()
    return val


EncapType = Literal[
    "ipsec",
    "gre",
]


InterfaceType = Literal[
    "Ethernet",
    "FastEthernet",
    "FiveGigabitEthernet",
    "FortyGigabitEthernet",
    "GigabitEthernet",
    "HundredGigE",
    "Loopback",
    "TenGigabitEthernet",
    "Tunnel",
    "TwentyFiveGigabitEthernet",
    "TwentyFiveGigE",
    "TwoGigabitEthernet",
    "VirtualPortGroup",
    "Vlan",
]

TLOCColor = Literal[
    "default",
    "mpls",
    "metro-ethernet",
    "biz-internet",
    "public-internet",
    "lte",
    "3g",
    "red",
    "green",
    "blue",
    "gold",
    "silver",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
]


WellKnownBGPCommunities = Literal[
    "internet",
    "local-AS",
    "no-advertise",
    "no-export",
]

ServiceChainNumber = Literal[
    "SC1",
    "SC2",
    "SC3",
    "SC4",
    "SC5",
    "SC6",
    "SC7",
    "SC8",
    "SC9",
    "SC10",
    "SC11",
    "SC12",
    "SC13",
    "SC14",
    "SC15",
    "SC16",
]

ICMPMessageType = Literal[
    "echo", "echo-reply", "unreachable", "net-unreachable", "host-unreachable", "protocol-unreachable"
]

MetricType = Literal["type1", "type2"]

SubnetMask = Literal[
    "255.255.255.255",
    "255.255.255.254",
    "255.255.255.252",
    "255.255.255.248",
    "255.255.255.240",
    "255.255.255.224",
    "255.255.255.192",
    "255.255.255.128",
    "255.255.255.0",
    "255.255.254.0",
    "255.255.252.0",
    "255.255.248.0",
    "255.255.240.0",
    "255.255.224.0",
    "255.255.192.0",
    "255.255.128.0",
    "255.255.0.0",
    "255.254.0.0",
    "255.252.0.0",
    "255.240.0.0",
    "255.224.0.0",
    "255.192.0.0",
    "255.128.0.0",
    "255.0.0.0",
    "254.0.0.0",
    "252.0.0.0",
    "248.0.0.0",
    "240.0.0.0",
    "224.0.0.0",
    "192.0.0.0",
    "128.0.0.0",
    "0.0.0.0",
]
