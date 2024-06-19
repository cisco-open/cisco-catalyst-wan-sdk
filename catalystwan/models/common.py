# Copyright 2024 Cisco Systems, Inc. and its affiliates

from dataclasses import InitVar, dataclass, field
from typing import Any, Dict, Iterator, List, Literal, Mapping, Optional, Sequence, Set, Tuple, Union
from uuid import UUID

from annotated_types import Ge, Le
from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import NonNegativeInt, PlainSerializer, PositiveInt, SerializationInfo, ValidationInfo
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
    def model_iterate(
        model_fields: Dict[str, FieldInfo], info: Union[SerializationInfo, ValidationInfo]
    ) -> Iterator[Tuple[str, FieldInfo, "VersionedField"]]:
        """Itrerates over model fields that matches a version given in context (Serialization info or ValidationInfo)

        Yields:
            Tuple[str, FieldInfo, VersionedField]: a tuple containing field name, FieldInfo and VersionedField
        """
        if info.context is not None:
            api_version: Optional[Version] = info.context.get("api_version")
            if api_version is not None:
                for field_name, field_info in model_fields.items():
                    versioned_fields = [meta for meta in field_info.metadata if isinstance(meta, VersionedField)]
                    for versioned_field in versioned_fields:
                        if api_version in versioned_field.versions_set:
                            yield (field_name, field_info, versioned_field)

    @staticmethod
    def dump(
        model_fields: Dict[str, FieldInfo],
        model_dict: Dict[str, Any],
        info: SerializationInfo,
        replaced_keys: Optional[Mapping[str, Tuple[Optional[str], str]]] = None,
    ) -> Dict[str, Any]:
        """To be reused in methods decorated with pydantic.model_serializer
        Args:
            model_fields (Dict[str, FieldInfo]): obtained from BaseModel class
            model_dict (Dict[str, Any]): obtained from serialized BaseModel instance
            serialization_info (SerializationInfo): passed from serializer
            replaced_keys (Dict[str, Tuple(Optional[str], str)]): field names that were replaced
                previously during serialization
                (Tuple represent path and new field name - this currently supports up to 1 level deep alias path only)

        Returns:
            Dict[str, Any]: model_dict with updated field names according to matching runtime version
        """
        for field_name, field_info, versioned_field in VersionedField.model_iterate(model_fields, info):
            current_field_name = field_info.serialization_alias or field_info.alias or field_name
            new_field_name = versioned_field.serialization_alias
            if current_field_name in model_dict:
                model_dict[new_field_name] = model_dict[current_field_name]
                del model_dict[current_field_name]
            elif replaced_keys is not None:
                if current_field_path := replaced_keys.get(current_field_name):
                    path, name = current_field_path
                    dict_ = model_dict[path] if path is not None else model_dict
                    dict_[new_field_name] = dict_[name]
                    del dict_[name]
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


def str_as_uuid_list(val: Union[str, Sequence[UUID]]) -> Sequence[UUID]:
    if isinstance(val, str):
        return [UUID(uuid_) for uuid_ in val.split()]
    return val


def str_as_positive_int_list(val: Union[str, Sequence[PositiveInt]]) -> Sequence[PositiveInt]:
    if isinstance(val, str):
        return [PositiveInt(element) for element in val.split()]
    return val


def str_as_str_list(val: Union[str, Sequence[str]]) -> Sequence[str]:
    if isinstance(val, str):
        return val.split()
    return val


IntStr = Annotated[
    int,
    PlainSerializer(lambda x: str(x), return_type=str, when_used="json-unless-none"),
    BeforeValidator(lambda x: int(x)),
]

IntRange = Tuple[int, Optional[int]]

SpaceSeparatedUUIDList = Annotated[
    List[UUID],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_uuid_list),
]


SpaceSeparatedNonNegativeIntList = Annotated[
    List[NonNegativeInt],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_positive_int_list),
]


def int_range_str_validator(value: Union[str, int, IntRange], ascending: bool = True) -> IntRange:
    """
    Validates input given as string containing integer pair separated by hyphen
    eg: '1-3' or single number '1'
    """
    if isinstance(value, str):
        int_list = [int(i) for i in value.strip().split("-")]
        assert 0 < len(int_list) <= 2, "Number range string must contain one or two numbers"
        first = int_list[0]
        second = None if len(int_list) == 1 else int_list[1]
        int_range = (first, second)
    elif isinstance(value, int):
        int_range = (value, None)
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

AcceptDropActionType = Literal["accept", "drop"]
AcceptRejectActionType = Literal["accept", "reject"]
DeviceAccessProtocolPort = Literal[161, 22]

CarrierType = Literal[
    "default",
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
]

ControlPathType = Literal[
    "direct-path",
    "hierarchical-path",
    "transport-gateway-path",
]

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


MultiRegionRole = Literal[
    "border-router",
    "edge-router",
]

OriginProtocol = Literal[
    "aggregate",
    "bgp",
    "bgp-external",
    "bgp-internal",
    "connected",
    "eigrp",
    "ospf",
    "ospf-inter-area",
    "ospf-intra-area",
    "ospf-external1",
    "ospf-external2",
    "rip",
    "static",
    "eigrp-summary",
    "eigrp-internal",
    "eigrp-external",
    "lisp",
    "nat-dia",
    "natpool",
    "isis",
    "isis-level1",
    "isis-level2",
    "egp",
    "igp",
    "incomplete",
]

ServiceType = Literal[
    "FW",
    "IDP",
    "IDS",
    "netsvc1",
    "netsvc2",
    "netsvc3",
    "netsvc4",
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

SequenceIpType = Literal[
    "ipv4",
    "ipv6",
    "all",
]

TLOCActionType = Literal[
    "strict",
    "primary",
    "backup",
    "ecmp",
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

VpnId = Annotated[
    IntStr,
    Ge(0),
    Le(65530),
]

PolicyModeType = Literal["security", "unified"]

CoreRegion = Literal[
    "core",
    "core-shared",
]

SecondaryRegion = Literal[
    "secondary-only",
    "secondary-shared",
]

WebReputation = Literal["low-risk", "moderate-risk", "high-risk", "suspicious", "trustworthy"]

WebCategory = Literal[
    "abused-drugs",
    "abortion",
    "adult-and-pornography",
    "alcohol-and-tobacco",
    "auctions",
    "bot-nets",
    "business-and-economy",
    "cdns",
    "cheating",
    "computer-and-internet-info",
    "computer-and-internet-security",
    "games",
    "gambling",
    "financial-services",
    "fashion-and-beauty",
    "entertainment-and-arts",
    "educational-institutions",
    "dynamic-content",
    "dead-sites",
    "confirmed-spam-sources",
    "cult-and-occult",
    "dating",
    "government",
    "gross",
    "hacking",
    "hate-and-racism",
    "health-and-medicine",
    "home",
    "hunting-and-fishing",
    "illegal",
    "image-and-video-search",
    "individual-stock-advice-and-tools",
    "internet-communications",
    "internet-portals",
    "job-search",
    "keyloggers-and-monitoring",
    "kids",
    "legal",
    "local-information",
    "malware-sites",
    "marijuana",
    "p2p",
    "parked-sites",
    "pay-to-surf",
    "personal-sites-and-blogs",
    "philosophy-and-political-advocacy",
    "phishing-and-other-frauds",
    "private-ip-addresses",
    "proxy-avoid-and-anonymizers",
    "questionable",
    "real-estate",
    "recreation-and-hobbies",
    "reference-and-research",
    "religion",
    "search-engines",
    "sex-education",
    "shareware-and-freeware",
    "shopping",
    "social-network",
    "society",
    "sports",
    "spam-urls",
    "spyware-and-adware",
    "streaming-media",
    "swimsuits-and-intimate-apparel",
    "training-and-tools",
    "translation",
    "travel",
    "uncategorized",
    "unconfirmed-spam-sources",
    "violence",
    "weapons",
    "web-advertisements",
    "web-based-email",
    "web-hosting",
    "open-http-proxies",
    "online-personal-storage",
    "online-greeting-cards",
    "nudity",
    "news-and-media",
    "music",
    "motor-vehicles",
    "military",
]

IkeMode = Literal[
    "main",
    "aggresive",
]

IkeCiphersuite = Literal[
    "aes256-cbc-sha1",
    "aes256-cbc-sha2",
    "aes128-cbc-sha1",
    "aes128-cbc-sha2",
]

IkeGroup = Literal[
    "2",
    "14",
    "15",
    "16",
    "19",
    "20",
    "21",
    "24",
]

IpsecCiphersuite = Literal[
    "aes256-cbc-sha1",
    "aes256-cbc-sha384",
    "aes256-cbc-sha256",
    "aes256-cbc-sha512",
    "aes256-gcm",
    "null-sha1",
    "null-sha384",
    "null-sha256",
    "null-sha512",
]

PfsGroup = Literal[
    "group-1",
    "group-2",
    "group-5",
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-20",
    "group-21",
    "group-24",
    "none",
]

VrrpTrackerAction = Literal[
    "Decrement",
    "Shutdown",
]

TunnelMode = Literal[
    "hub",
    "spoke",
]

Duplex = Literal[
    "full",
    "half",
]

EthernetDuplexMode = Literal[
    "full",
    "half",
    "auto",
]

MediaType = Literal[
    "auto-select",
    "rj45",
    "sfp",
]

Speed = Literal[
    "10",
    "100",
    "1000",
    "10000",
    "2500",
]

EthernetNatType = Literal["pool", "loopback", "interface"]

EthernetDirection = Literal[
    "inside",
    "outside",
]

ClockRate = Literal[
    "1000000",
    "115200",
    "1200",
    "125000",
    "14400",
    "148000",
    "19200",
    "192000",
    "2000000",
    "2400",
    "250000",
    "256000",
    "28800",
    "32000",
    "38400",
    "384000",
    "4000000",
    "4800",
    "48000",
    "500000",
    "512000",
    "5300000",
    "56000",
    "57600",
    "64000",
    "72000",
    "768000",
    "800000",
    "8000000",
    "9600",
]

LineMode = Literal[
    "primary",
    "secondary",
]

T1Framing = Literal[
    "esf",
    "sf",
]

T1Linecode = Literal[
    "ami",
    "b8zs",
]

E1Framing = Literal[
    "crc4",
    "no-crc4",
]

E1Linecode = Literal[
    "ami",
    "hdb3",
]

CableLengthShortValue = Literal[
    "110ft",
    "220ft",
    "330ft",
    "440ft",
    "550ft",
    "660ft",
]

CableLengthLongValue = Literal[
    "-15db",
    "-22.5db",
    "-7.5db",
    "0db",
]
