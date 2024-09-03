# Copyright 2024 Cisco Systems, Inc. and its affiliates

import re
from dataclasses import InitVar, dataclass, field
from ipaddress import IPv4Interface, IPv6Interface
from typing import Any, Dict, Iterator, List, Literal, Mapping, Optional, Sequence, Set, Tuple, Union, get_args
from uuid import UUID

from annotated_types import Ge, Le
from packaging.specifiers import SpecifierSet  # type: ignore
from packaging.version import Version  # type: ignore
from pydantic import Field, NonNegativeInt, PlainSerializer, PositiveInt, SerializationInfo, ValidationInfo
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
    >>>         return VersionedField.dump(self.model_fields, handler(self), info)
    """

    versions: InitVar[str]
    versions_set: SpecifierSet = field(init=False)
    serialization_alias: Optional[str] = None
    forbidden: bool = False

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
                if versioned_field.forbidden:
                    del model_dict[current_field_name]
                elif new_field_name is not None and new_field_name != current_field_name:
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


def str_as_ipv4_list(val: Union[str, Sequence[IPv4Interface]]) -> Sequence[IPv4Interface]:
    if isinstance(val, str):
        return [IPv4Interface(element) for element in val.split()]
    return val


def str_as_ipv6_list(val: Union[str, Sequence[IPv6Interface]]) -> Sequence[IPv6Interface]:
    if isinstance(val, str):
        return [IPv6Interface(element) for element in val.split()]
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
    Field(min_length=1),
]

SpaceSeparatedNonNegativeIntList = Annotated[
    List[NonNegativeInt],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_positive_int_list),
    Field(min_length=1),
]

SpaceSeparatedIPv4 = Annotated[
    List[IPv4Interface],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_ipv4_list),
    Field(min_length=1),
]

SpaceSeparatedIPv6 = Annotated[
    List[IPv6Interface],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_ipv6_list),
    Field(min_length=1),
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

DestinationRegion = Literal[
    "primary-region",
    "secondary-region",
    "other-region",
]

DNSEntryType = Literal[
    "request",
    "response",
]

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
InterfaceTypePattern = re.compile(r"^(?:" + "|".join(map(re.escape, get_args(InterfaceType))) + r")[\x00-\x7F]*$")

InterfaceStr = Annotated[
    str,
    Field(pattern=InterfaceTypePattern),
]


def str_as_interface_list(val: Union[str, Sequence[InterfaceStr]]) -> Sequence[InterfaceStr]:
    if isinstance(val, str):
        return [InterfaceStr(element) for element in val.split()]
    return val


SpaceSeparatedInterfaceStr = Annotated[
    List[InterfaceStr],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_interface_list),
]

StaticNatDirection = Literal["inside", "outside"]

Protocol = Literal["tcp", "udp"]

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


SpaceSeparatedTLOCColorStr = Annotated[
    List[TLOCColor],
    PlainSerializer(lambda x: " ".join(map(str, x)), return_type=str, when_used="json-unless-none"),
    BeforeValidator(str_as_str_list),
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
    "appqoe",
    "FW",
    "IDP",
    "IDS",
    "netsvc1",
    "netsvc2",
    "netsvc3",
    "netsvc4",
    "netsvc5",
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

IcmpMsgType = Literal[
    "administratively-prohibited",
    "dod-host-prohibited",
    "dod-net-prohibited",
    "echo",
    "echo-reply",
    "echo-reply-no-error",
    "extended-echo",
    "extended-echo-reply",
    "general-parameter-problem",
    "host-isolated",
    "host-precedence-unreachable",
    "host-redirect",
    "host-tos-redirect",
    "host-tos-unreachable",
    "host-unknown",
    "host-unreachable",
    "interface-error",
    "malformed-query",
    "multiple-interface-match",
    "net-redirect",
    "net-tos-redirect",
    "net-tos-unreachable",
    "net-unreachable",
    "network-unknown",
    "no-room-for-option",
    "option-missing",
    "packet-too-big",
    "parameter-problem",
    "photuris",
    "port-unreachable",
    "precedence-unreachable",
    "protocol-unreachable",
    "reassembly-timeout",
    "redirect",
    "router-advertisement",
    "router-solicitation",
    "source-route-failed",
    "table-entry-error",
    "time-exceeded",
    "timestamp-reply",
    "timestamp-request",
    "ttl-exceeded",
    "unreachable",
]

Icmp6MsgType = Literal[
    "beyond-scope",
    "cp-advertisement",
    "cp-solicitation",
    "destination-unreachable",
    "dhaad-reply",
    "dhaad-request",
    "echo-reply",
    "echo-request",
    "header",
    "hop-limit",
    "ind-advertisement",
    "ind-solicitation",
    "mld-query",
    "mld-reduction",
    "mld-report",
    "mldv2-report",
    "mpd-advertisement",
    "mpd-solicitation",
    "mr-advertisement",
    "mr-solicitation",
    "mr-termination",
    "nd-na",
    "nd-ns",
    "next-header-type",
    "ni-query",
    "ni-query-name",
    "ni-query-v4-address",
    "ni-query-v6-address",
    "ni-response",
    "ni-response-qtype-unknown",
    "ni-response-refuse",
    "ni-response-success",
    "no-admin",
    "no-route",
    "packet-too-big",
    "parameter-option",
    "parameter-problem",
    "port-unreachable",
    "reassembly-timeout",
    "redirect",
    "reject-route",
    "renum-command",
    "renum-result",
    "renum-seq-number",
    "router-advertisement",
    "router-renumbering",
    "router-solicitation",
    "rpl-control",
    "source-policy",
    "source-route-header",
    "time-exceeded",
    "unreachable",
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

DNSTypeEntryType = Literal[
    "host",
    "umbrella",
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

LossProtectionType = Literal[
    "fecAdaptive",
    "fecAlways",
    "packetDuplication",
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


Timezone = Literal[
    "Europe/Andorra",
    "Asia/Dubai",
    "Asia/Kabul",
    "America/Antigua",
    "America/Anguilla",
    "Europe/Tirane",
    "Asia/Yerevan",
    "Africa/Luanda",
    "Antarctica/McMurdo",
    "Antarctica/Rothera",
    "Antarctica/Palmer",
    "Antarctica/Mawson",
    "Antarctica/Davis",
    "Antarctica/Casey",
    "Antarctica/Vostok",
    "Antarctica/DumontDUrville",
    "Antarctica/Syowa",
    "America/Argentina/Buenos_Aires",
    "America/Argentina/Cordoba",
    "America/Argentina/Salta",
    "America/Argentina/Jujuy",
    "America/Argentina/Tucuman",
    "America/Argentina/Catamarca",
    "America/Argentina/La_Rioja",
    "America/Argentina/San_Juan",
    "America/Argentina/Mendoza",
    "America/Argentina/San_Luis",
    "America/Argentina/Rio_Gallegos",
    "America/Argentina/Ushuaia",
    "Pacific/Pago_Pago",
    "Europe/Vienna",
    "Australia/Lord_Howe",
    "Antarctica/Macquarie",
    "Australia/Hobart",
    "Australia/Currie",
    "Australia/Melbourne",
    "Australia/Sydney",
    "Australia/Broken_Hill",
    "Australia/Brisbane",
    "Australia/Lindeman",
    "Australia/Adelaide",
    "Australia/Darwin",
    "Australia/Perth",
    "Australia/Eucla",
    "America/Aruba",
    "Europe/Mariehamn",
    "Asia/Baku",
    "Europe/Sarajevo",
    "America/Barbados",
    "Asia/Dhaka",
    "Europe/Brussels",
    "Africa/Ouagadougou",
    "Europe/Sofia",
    "Asia/Bahrain",
    "Africa/Bujumbura",
    "Africa/Porto-Novo",
    "America/St_Barthelemy",
    "Atlantic/Bermuda",
    "Asia/Brunei",
    "America/La_Paz",
    "America/Kralendijk",
    "America/Noronha",
    "America/Belem",
    "America/Fortaleza",
    "America/Recife",
    "America/Araguaina",
    "America/Maceio",
    "America/Bahia",
    "America/Sao_Paulo",
    "America/Campo_Grande",
    "America/Cuiaba",
    "America/Santarem",
    "America/Porto_Velho",
    "America/Boa_Vista",
    "America/Manaus",
    "America/Eirunepe",
    "America/Rio_Branco",
    "America/Nassau",
    "Asia/Thimphu",
    "Africa/Gaborone",
    "Europe/Minsk",
    "America/Belize",
    "America/St_Johns",
    "America/Halifax",
    "America/Glace_Bay",
    "America/Moncton",
    "America/Goose_Bay",
    "America/Blanc-Sablon",
    "America/Toronto",
    "America/Nipigon",
    "America/Thunder_Bay",
    "America/Iqaluit",
    "America/Pangnirtung",
    "America/Resolute",
    "America/Atikokan",
    "America/Rankin_Inlet",
    "America/Winnipeg",
    "America/Rainy_River",
    "America/Regina",
    "America/Swift_Current",
    "America/Edmonton",
    "America/Cambridge_Bay",
    "America/Yellowknife",
    "America/Inuvik",
    "America/Creston",
    "America/Dawson_Creek",
    "America/Vancouver",
    "America/Whitehorse",
    "America/Dawson",
    "Indian/Cocos",
    "Africa/Kinshasa",
    "Africa/Lubumbashi",
    "Africa/Bangui",
    "Africa/Brazzaville",
    "Europe/Zurich",
    "Africa/Abidjan",
    "Pacific/Rarotonga",
    "America/Santiago",
    "Pacific/Easter",
    "Africa/Douala",
    "Asia/Shanghai",
    "Asia/Harbin",
    "Asia/Chongqing",
    "Asia/Urumqi",
    "Asia/Kashgar",
    "America/Bogota",
    "America/Costa_Rica",
    "America/Havana",
    "Atlantic/Cape_Verde",
    "America/Curacao",
    "Indian/Christmas",
    "Asia/Nicosia",
    "Europe/Prague",
    "Europe/Berlin",
    "Europe/Busingen",
    "Africa/Djibouti",
    "Europe/Copenhagen",
    "America/Dominica",
    "America/Santo_Domingo",
    "Africa/Algiers",
    "America/Guayaquil",
    "Pacific/Galapagos",
    "Europe/Tallinn",
    "Africa/Cairo",
    "Africa/El_Aaiun",
    "Africa/Asmara",
    "Europe/Madrid",
    "Africa/Ceuta",
    "Atlantic/Canary",
    "Africa/Addis_Ababa",
    "Europe/Helsinki",
    "Pacific/Fiji",
    "Atlantic/Stanley",
    "Pacific/Chuuk",
    "Pacific/Pohnpei",
    "Pacific/Kosrae",
    "Atlantic/Faroe",
    "Europe/Paris",
    "Africa/Libreville",
    "Europe/London",
    "America/Grenada",
    "Asia/Tbilisi",
    "America/Cayenne",
    "Europe/Guernsey",
    "Africa/Accra",
    "Europe/Gibraltar",
    "America/Godthab",
    "America/Danmarkshavn",
    "America/Scoresbysund",
    "America/Thule",
    "Africa/Banjul",
    "Africa/Conakry",
    "America/Guadeloupe",
    "Africa/Malabo",
    "Europe/Athens",
    "Atlantic/South_Georgia",
    "America/Guatemala",
    "Pacific/Guam",
    "Africa/Bissau",
    "America/Guyana",
    "Asia/Hong_Kong",
    "America/Tegucigalpa",
    "Europe/Zagreb",
    "America/Port-au-Prince",
    "Europe/Budapest",
    "Asia/Jakarta",
    "Asia/Pontianak",
    "Asia/Makassar",
    "Asia/Jayapura",
    "Europe/Dublin",
    "Asia/Jerusalem",
    "Europe/Isle_of_Man",
    "Asia/Kolkata",
    "Indian/Chagos",
    "Asia/Baghdad",
    "Asia/Tehran",
    "Atlantic/Reykjavik",
    "Europe/Rome",
    "Europe/Jersey",
    "America/Jamaica",
    "Asia/Amman",
    "Asia/Tokyo",
    "Africa/Nairobi",
    "Asia/Bishkek",
    "Asia/Phnom_Penh",
    "Pacific/Tarawa",
    "Pacific/Enderbury",
    "Pacific/Kiritimati",
    "Indian/Comoro",
    "America/St_Kitts",
    "Asia/Pyongyang",
    "Asia/Seoul",
    "Asia/Kuwait",
    "America/Cayman",
    "Asia/Almaty",
    "Asia/Qyzylorda",
    "Asia/Aqtobe",
    "Asia/Aqtau",
    "Asia/Oral",
    "Asia/Vientiane",
    "Asia/Beirut",
    "America/St_Lucia",
    "Europe/Vaduz",
    "Asia/Colombo",
    "Africa/Monrovia",
    "Africa/Maseru",
    "Europe/Vilnius",
    "Europe/Luxembourg",
    "Europe/Riga",
    "Africa/Tripoli",
    "Africa/Casablanca",
    "Europe/Monaco",
    "Europe/Chisinau",
    "Europe/Podgorica",
    "America/Marigot",
    "Indian/Antananarivo",
    "Pacific/Majuro",
    "Pacific/Kwajalein",
    "Europe/Skopje",
    "Africa/Bamako",
    "Asia/Rangoon",
    "Asia/Ulaanbaatar",
    "Asia/Hovd",
    "Asia/Choibalsan",
    "Asia/Macau",
    "Pacific/Saipan",
    "America/Martinique",
    "Africa/Nouakchott",
    "America/Montserrat",
    "Europe/Malta",
    "Indian/Mauritius",
    "Indian/Maldives",
    "Africa/Blantyre",
    "America/Mexico_City",
    "America/Cancun",
    "America/Merida",
    "America/Monterrey",
    "America/Matamoros",
    "America/Mazatlan",
    "America/Chihuahua",
    "America/Ojinaga",
    "America/Hermosillo",
    "America/Tijuana",
    "America/Santa_Isabel",
    "America/Bahia_Banderas",
    "Asia/Kuala_Lumpur",
    "Asia/Kuching",
    "Africa/Maputo",
    "Africa/Windhoek",
    "Pacific/Noumea",
    "Africa/Niamey",
    "Pacific/Norfolk",
    "Africa/Lagos",
    "America/Managua",
    "Europe/Amsterdam",
    "Europe/Oslo",
    "Asia/Kathmandu",
    "Pacific/Nauru",
    "Pacific/Niue",
    "Pacific/Auckland",
    "Pacific/Chatham",
    "Asia/Muscat",
    "America/Panama",
    "America/Lima",
    "Pacific/Tahiti",
    "Pacific/Marquesas",
    "Pacific/Gambier",
    "Pacific/Port_Moresby",
    "Asia/Manila",
    "Asia/Karachi",
    "Europe/Warsaw",
    "America/Miquelon",
    "Pacific/Pitcairn",
    "America/Puerto_Rico",
    "Asia/Gaza",
    "Asia/Hebron",
    "Europe/Lisbon",
    "Atlantic/Madeira",
    "Atlantic/Azores",
    "Pacific/Palau",
    "America/Asuncion",
    "Asia/Qatar",
    "Indian/Reunion",
    "Europe/Bucharest",
    "Europe/Belgrade",
    "Europe/Kaliningrad",
    "Europe/Moscow",
    "Europe/Volgograd",
    "Europe/Samara",
    "Asia/Yekaterinburg",
    "Asia/Omsk",
    "Asia/Novosibirsk",
    "Asia/Novokuznetsk",
    "Asia/Krasnoyarsk",
    "Asia/Irkutsk",
    "Asia/Yakutsk",
    "Asia/Khandyga",
    "Asia/Vladivostok",
    "Asia/Sakhalin",
    "Asia/Ust-Nera",
    "Asia/Magadan",
    "Asia/Kamchatka",
    "Asia/Anadyr",
    "Africa/Kigali",
    "Asia/Riyadh",
    "Pacific/Guadalcanal",
    "Indian/Mahe",
    "Africa/Khartoum",
    "Europe/Stockholm",
    "Asia/Singapore",
    "Atlantic/St_Helena",
    "Europe/Ljubljana",
    "Arctic/Longyearbyen",
    "Europe/Bratislava",
    "Africa/Freetown",
    "Europe/San_Marino",
    "Africa/Dakar",
    "Africa/Mogadishu",
    "America/Paramaribo",
    "Africa/Juba",
    "Africa/Sao_Tome",
    "America/El_Salvador",
    "America/Lower_Princes",
    "Asia/Damascus",
    "Africa/Mbabane",
    "America/Grand_Turk",
    "Africa/Ndjamena",
    "Indian/Kerguelen",
    "Africa/Lome",
    "Asia/Bangkok",
    "Asia/Dushanbe",
    "Pacific/Fakaofo",
    "Asia/Dili",
    "Asia/Ashgabat",
    "Africa/Tunis",
    "Pacific/Tongatapu",
    "Europe/Istanbul",
    "America/Port_of_Spain",
    "Pacific/Funafuti",
    "Asia/Taipei",
    "Africa/Dar_es_Salaam",
    "Europe/Kiev",
    "Europe/Uzhgorod",
    "Europe/Zaporozhye",
    "Europe/Simferopol",
    "Africa/Kampala",
    "Pacific/Johnston",
    "Pacific/Midway",
    "Pacific/Wake",
    "America/New_York",
    "America/Detroit",
    "America/Kentucky/Louisville",
    "America/Kentucky/Monticello",
    "America/Indiana/Indianapolis",
    "America/Indiana/Vincennes",
    "America/Indiana/Winamac",
    "America/Indiana/Marengo",
    "America/Indiana/Petersburg",
    "America/Indiana/Vevay",
    "America/Chicago",
    "America/Indiana/Tell_City",
    "America/Indiana/Knox",
    "America/Menominee",
    "America/North_Dakota/Center",
    "America/North_Dakota/New_Salem",
    "America/North_Dakota/Beulah",
    "America/Denver",
    "America/Boise",
    "America/Phoenix",
    "America/Los_Angeles",
    "America/Anchorage",
    "America/Juneau",
    "America/Sitka",
    "America/Yakutat",
    "America/Nome",
    "America/Adak",
    "America/Metlakatla",
    "Pacific/Honolulu",
    "America/Montevideo",
    "Asia/Samarkand",
    "Asia/Tashkent",
    "Europe/Vatican",
    "America/St_Vincent",
    "America/Caracas",
    "America/Tortola",
    "America/St_Thomas",
    "Asia/Ho_Chi_Minh",
    "Pacific/Efate",
    "Pacific/Wallis",
    "Pacific/Apia",
    "Asia/Aden",
    "Indian/Mayotte",
    "Africa/Johannesburg",
    "Africa/Lusaka",
    "Africa/Harare",
    "UTC",
]

TrafficTargetType = Literal[
    "access",
    "core",
    "service",
]

DeviceModel = Literal[
    "None",
    "vsmart",
    "vedge-cloud",
    "vmanage",
    "vedge-ISR1100-6G",
    "vedge-ISR1100X-6G",
    "vedge-ISR1100-4G",
    "vedge-ISR1100X-4G",
    "vedge-ISR1100-4GLTE",
    "vedge-cloud",
    "vedge-1000",
    "vedge-2000",
    "vedge-100",
    "vedge-100-B",
    "vedge-100-WM",
    "vedge-100-M",
    "vedge-5000",
    "vedge-IR-1101",
    "vedge-ESR-6300",
    "vedge-IR-1821",
    "vedge-IR-1831",
    "vedge-IR-1833",
    "vedge-IR-1835",
    "vedge-ASR-1001-X",
    "vedge-ASR-1002-X",
    "vedge-ASR-1002-HX",
    "vedge-ASR-1001-HX",
    "vedge-C8500L-8G4X",
    "vedge-C8500-12X4QC",
    "vedge-C8500-12X",
    "vedge-C8500L-8S4X",
    "vedge-ASR-1006-X",
    "vedge-C8500-20X6C",
    "vedge-CSR-1000v",
    "vedge-C8000V",
    "vedge-ISR-4331",
    "vedge-ISR-4431",
    "vedge-ISR-4461",
    "vedge-ISR-4451-X",
    "vedge-ISR-4321",
    "vedge-ISR-4351",
    "vedge-ISR-4221",
    "vedge-ISR-4221X",
    "vedge-C1111-8PW",
    "vedge-C1111-8PLTELAW",
    "vedge-C1111-8PLTEEAW",
    "vedge-C1113-8PMLTEEA",
    "vedge-C1116-4P",
    "vedge-C1116-4PLTEEA",
    "vedge-C1117-4P",
    "vedge-C1117-4PM",
    "vedge-C1117-4PLTEEA",
    "vedge-C1111-8PLTELA",
    "vedge-C1111-8PLTEEA",
    "vedge-C1121-8PLTEPW",
    "vedge-C1121-8PLTEP",
    "vedge-C1121X-8PLTEP",
    "vedge-C1111-4PLTEEA",
    "vedge-C1161X-8PLTEP",
    "vedge-C8300-2N2S-6T",
    "vedge-C8300-1N1S-6T",
    "vedge-C8300-1N1S-4T2X",
    "vedge-C8300-2N2S-4T2X",
    "vedge-C8200-1N-4T",
    "vedge-C8200L-1N-4T",
    "vedge-ISRv",
]

SLAClassCriteria = Literal[
    "loss",
    "latency",
    "jitter",
    "loss-latency",
    "loss-jitter",
    "latency-loss",
    "latency-jitter",
    "jitter-latency",
    "jitter-loss",
    "loss-latency-jitter",
    "loss-jitter-latency",
    "latency-loss-jitter",
    "latency-jitter-loss",
    "jitter-latency-loss",
    "jitter-loss-latency",
]
