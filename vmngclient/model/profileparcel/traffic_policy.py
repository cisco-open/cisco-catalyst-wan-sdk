# mypy: disable-error-code="valid-type"
# generated by datamodel-codegen:
#   filename:  apidocs/schema/profileparcel/sdwan/application-priority/traffic-policy/post/request_schema.json
#   timestamp: 2023-09-07T08:34:35+00:00

from __future__ import annotations

from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import List, Optional, Union

from pydantic import BaseModel, Extra, Field, conint, constr


class Entries(BaseModel):
    pass


class SlaClass(BaseModel):
    pass


class Set(BaseModel):
    pass


class Actions(BaseModel):
    pass


class CgFpPpNameDef(BaseModel):
    __root__: constr(regex=r'^[^&<>! "]+$', min_length=1, max_length=128)  # noqa: F722


class GlobalOptionTypeDef(Enum):
    global_ = "global"


class UuidDef(BaseModel):
    __root__: constr(regex=r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")  # noqa: F722


class BooleanDef(BaseModel):
    __root__: bool


class Ipv4PrefixDef(BaseModel):
    __root__: constr(
        regex=r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\/)([0-2]?[0-9]$|[3]?[0-2])"  # noqa: F722, E501
    )


class Ipv6PrefixDef(BaseModel):
    __root__: constr(
        regex=r"((^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*(\/)(\b([0-9]{1,2}|1[01][0-9]|12[0-8])\b)$))"  # noqa: F722, E501
    )


class OneOfMatchEntriesSourceIpv6OptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Ipv6PrefixDef


class OneOfMatchEntriesSourceIpv6OptionsDef(BaseModel):
    __root__: OneOfMatchEntriesSourceIpv6OptionsDefItem


class ColorDef(Enum):
    field_3g = "3g"
    biz_internet = "biz-internet"
    blue = "blue"
    bronze = "bronze"
    custom1 = "custom1"
    custom2 = "custom2"
    custom3 = "custom3"
    default = "default"
    gold = "gold"
    green = "green"
    lte = "lte"
    metro_ethernet = "metro-ethernet"
    mpls = "mpls"
    private1 = "private1"
    private2 = "private2"
    private3 = "private3"
    private4 = "private4"
    private5 = "private5"
    private6 = "private6"
    public_internet = "public-internet"
    red = "red"
    silver = "silver"


class Count(BaseModel):
    __root__: constr(min_length=1, max_length=20)


class DestinationRegion(Enum):
    primary_region = "primary-region"
    secondary_region = "secondary-region"
    other_region = "other-region"


class Dns(Enum):
    request = "request"
    response = "response"


class Ipv4AddressDef(BaseModel):
    class Config:
        extra = Extra.forbid

    __root__: IPv4Address


class Ipv6AddressDef(BaseModel):
    class Config:
        extra = Extra.forbid

    __root__: IPv6Address


class MatchEntriesDscpDef(BaseModel):
    __root__: conint(ge=0, le=63)


class MatchEntriesIcmp6MessageDef(Enum):
    beyond_scope = "beyond-scope"
    cp_advertisement = "cp-advertisement"
    cp_solicitation = "cp-solicitation"
    destination_unreachable = "destination-unreachable"
    dhaad_reply = "dhaad-reply"
    dhaad_request = "dhaad-request"
    echo_reply = "echo-reply"
    echo_request = "echo-request"
    header = "header"
    hop_limit = "hop-limit"
    ind_advertisement = "ind-advertisement"
    ind_solicitation = "ind-solicitation"
    mld_query = "mld-query"
    mld_reduction = "mld-reduction"
    mld_report = "mld-report"
    mldv2_report = "mldv2-report"
    mpd_advertisement = "mpd-advertisement"
    mpd_solicitation = "mpd-solicitation"
    mr_advertisement = "mr-advertisement"
    mr_solicitation = "mr-solicitation"
    mr_termination = "mr-termination"
    nd_na = "nd-na"
    nd_ns = "nd-ns"
    next_header_type = "next-header-type"
    ni_query = "ni-query"
    ni_query_name = "ni-query-name"
    ni_query_v4_address = "ni-query-v4-address"
    ni_query_v6_address = "ni-query-v6-address"
    ni_response = "ni-response"
    ni_response_qtype_unknown = "ni-response-qtype-unknown"
    ni_response_refuse = "ni-response-refuse"
    ni_response_success = "ni-response-success"
    no_admin = "no-admin"
    no_route = "no-route"
    packet_too_big = "packet-too-big"
    parameter_option = "parameter-option"
    parameter_problem = "parameter-problem"
    port_unreachable = "port-unreachable"
    reassembly_timeout = "reassembly-timeout"
    redirect = "redirect"
    reject_route = "reject-route"
    renum_command = "renum-command"
    renum_result = "renum-result"
    renum_seq_number = "renum-seq-number"
    router_advertisement = "router-advertisement"
    router_renumbering = "router-renumbering"
    router_solicitation = "router-solicitation"
    rpl_control = "rpl-control"
    source_policy = "source-policy"
    source_route_header = "source-route-header"
    time_exceeded = "time-exceeded"
    unreachable = "unreachable"


class MatchEntriesIcmpMessageDef(Enum):
    administratively_prohibited = "administratively-prohibited"
    dod_host_prohibited = "dod-host-prohibited"
    dod_net_prohibited = "dod-net-prohibited"
    echo = "echo"
    echo_reply = "echo-reply"
    echo_reply_no_error = "echo-reply-no-error"
    extended_echo = "extended-echo"
    extended_echo_reply = "extended-echo-reply"
    general_parameter_problem = "general-parameter-problem"
    host_isolated = "host-isolated"
    host_precedence_unreachable = "host-precedence-unreachable"
    host_redirect = "host-redirect"
    host_tos_redirect = "host-tos-redirect"
    host_tos_unreachable = "host-tos-unreachable"
    host_unknown = "host-unknown"
    host_unreachable = "host-unreachable"
    interface_error = "interface-error"
    malformed_query = "malformed-query"
    multiple_interface_match = "multiple-interface-match"
    net_redirect = "net-redirect"
    net_tos_redirect = "net-tos-redirect"
    net_tos_unreachable = "net-tos-unreachable"
    net_unreachable = "net-unreachable"
    network_unknown = "network-unknown"
    no_room_for_option = "no-room-for-option"
    option_missing = "option-missing"
    packet_too_big = "packet-too-big"
    parameter_problem = "parameter-problem"
    photuris = "photuris"
    port_unreachable = "port-unreachable"
    precedence_unreachable = "precedence-unreachable"
    protocol_unreachable = "protocol-unreachable"
    reassembly_timeout = "reassembly-timeout"
    redirect = "redirect"
    router_advertisement = "router-advertisement"
    router_solicitation = "router-solicitation"
    source_route_failed = "source-route-failed"
    table_entry_error = "table-entry-error"
    time_exceeded = "time-exceeded"
    timestamp_reply = "timestamp-reply"
    timestamp_request = "timestamp-request"
    ttl_exceeded = "ttl-exceeded"
    unreachable = "unreachable"


class MatchEntriesTcpDef(Enum):
    syn = "syn"


class MatchEntriesTrafficClassOptionsDef(Enum):
    gold_voip_telephony = "gold-voip-telephony"
    gold_broadcast_video = "gold-broadcast-video"
    gold_real_time_interactive = "gold-real-time-interactive"
    gold_multimedia_conferencing = "gold-multimedia-conferencing"
    gold_multimedia_streaming = "gold-multimedia-streaming"
    gold_network_control = "gold-network-control"
    gold_signaling = "gold-signaling"
    gold_ops_admin_mgmt = "gold-ops-admin-mgmt"
    gold_transactional_data = "gold-transactional-data"
    gold_bulk_data = "gold-bulk-data"
    silver = "silver"
    bronze = "bronze"


class NatPool(BaseModel):
    __root__: conint(ge=1, le=31)


class ProtocolDef(BaseModel):
    __root__: constr(regex=r"^(0|[1-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")  # noqa: F722, E501


class RedirectDn(Enum):
    umbrella = "umbrella"
    host = "host"


class RedirectDns(BaseModel):
    __root__: Union[RedirectDn, Ipv4AddressDef]


class RedirectDnsTypes(Enum):
    ip_address = "ipAddress"
    dns_host = "dnsHost"


class SequencesBaseActionDef(Enum):
    drop = "drop"
    accept = "accept"


class SequencesSequenceIdDef(BaseModel):
    __root__: conint(ge=1, le=65536)


class SequencesSequenceIpTypeDef(Enum):
    ipv4 = "ipv4"
    ipv6 = "ipv6"
    all = "all"


class SequencesSequenceNameDef(BaseModel):
    __root__: str


class TargetDirectionDef(Enum):
    service = "service"
    tunnel = "tunnel"
    all = "all"


class TargetVpnDef(BaseModel):
    __root__: str


class TrafficTo(Enum):
    core = "core"
    service = "service"
    access = "access"


class VpnDef(BaseModel):
    class Config:
        extra = Extra.forbid

    __root__: conint(ge=0, le=65530)


class Encap(Enum):
    ipsec = "ipsec"
    gre = "gre"


class EncapDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Encap


class PortNoDef(BaseModel):
    __root__: constr(
        regex=r"^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"  # noqa: F722, E501
    )


class PortRangeDef(BaseModel):
    __root__: constr(
        regex=r"^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\-(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"  # noqa: F722, E501
    )


class SequencesMatchEntriesPacketLengthDef(BaseModel):
    __root__: constr(
        regex=r"^(0|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"  # noqa: F722, E501
    )


class SequencesMatchEntriesPacketLengthRangeDef(BaseModel):
    __root__: constr(
        regex=r"^([0-9]|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\-([1-9]|[1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"  # noqa: F722, E501
    )


class TypeDefinition(Enum):
    fw = "FW"
    ids = "IDS"
    idp = "IDP"
    netsvc1 = "netsvc1"
    netsvc2 = "netsvc2"
    netsvc3 = "netsvc3"
    netsvc4 = "netsvc4"
    appqoe = "appqoe"


class RefId(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: UuidDef


class ParcelReferenceDef(BaseModel):
    class Config:
        extra = Extra.forbid

    ref_id: RefId = Field(..., alias="refId")


class BooleanDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: BooleanDef


class BooleanDefModel(BaseModel):
    __root__: BooleanDefItem


class ColorMatchListDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[ColorDef] = Field(..., min_items=1, unique_items=True)


class CountDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Count


class DestinationRegionDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: DestinationRegion


class DnsDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Dns


class Ipv4PrefixDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Ipv4PrefixDef


class Ipv4PrefixDefModel(BaseModel):
    __root__: Ipv4PrefixDefItem


class UseVpn(BaseModel):
    option_type: Optional[GlobalOptionTypeDef] = Field(None, alias="optionType")
    value: Optional[BooleanDefModel] = None


class NatDef(BaseModel):
    class Config:
        extra = Extra.forbid

    use_vpn: UseVpn = Field(..., alias="useVpn")
    fallback: Optional[BooleanDefModel] = None


class NatPoolDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: NatPool


class OneOfMatchEntriesDestinationIpv6OptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Ipv6PrefixDef


class OneOfMatchEntriesDestinationIpv6OptionsDef(BaseModel):
    __root__: OneOfMatchEntriesDestinationIpv6OptionsDefItem


class OneOfMatchEntriesDscpOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: MatchEntriesDscpDef


class OneOfMatchEntriesDscpOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesDscpOptionsDefItem


class OneOfMatchEntriesIcmp6MessageOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[MatchEntriesIcmp6MessageDef] = Field(..., min_items=1, unique_items=True)


class OneOfMatchEntriesIcmp6MessageOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesIcmp6MessageOptionsDefItem


class OneOfMatchEntriesIcmpMessageOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[MatchEntriesIcmpMessageDef] = Field(..., min_items=1, unique_items=True)


class OneOfMatchEntriesIcmpMessageOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesIcmpMessageOptionsDefItem


class OneOfMatchEntriesProtocolOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[ProtocolDef] = Field(..., min_items=1, unique_items=True)


class OneOfMatchEntriesProtocolOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesProtocolOptionsDefItem


class OneOfMatchEntriesTcpOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: MatchEntriesTcpDef


class OneOfMatchEntriesTcpOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesTcpOptionsDefItem


class OneOfMatchEntriesTrafficClassOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: MatchEntriesTrafficClassOptionsDef


class OneOfMatchEntriesTrafficClassOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesTrafficClassOptionsDefItem


class FieldModel(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: RedirectDnsTypes


class Value(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: RedirectDns


class OneOfRedirectDnsDef(BaseModel):
    field: Optional[FieldModel] = None
    value: Optional[Value] = None


class OneOfSequencesBaseActionOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: SequencesBaseActionDef


class OneOfSequencesBaseActionOptionsDef(BaseModel):
    __root__: OneOfSequencesBaseActionOptionsDefItem


class OneOfSequencesSequenceIdOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: SequencesSequenceIdDef


class OneOfSequencesSequenceIdOptionsDef(BaseModel):
    __root__: OneOfSequencesSequenceIdOptionsDefItem


class OneOfSequencesSequenceIpTypeOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: SequencesSequenceIpTypeDef


class OneOfSequencesSequenceIpTypeOptionsDef(BaseModel):
    __root__: OneOfSequencesSequenceIpTypeOptionsDefItem


class OneOfSequencesSequenceNameOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: SequencesSequenceNameDef


class OneOfSequencesSequenceNameOptionsDef(BaseModel):
    __root__: OneOfSequencesSequenceNameOptionsDefItem


class OneOfTargetDirectionOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: TargetDirectionDef


class OneOfTargetDirectionOptionsDef(BaseModel):
    __root__: OneOfTargetDirectionOptionsDefItem


class OneOfTargetVpnOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[TargetVpnDef] = Field(..., min_items=1, unique_items=True)


class OneOfTargetVpnOptionsDef(BaseModel):
    __root__: OneOfTargetVpnOptionsDefItem


class SlaClassDef(BaseModel):
    class Config:
        extra = Extra.forbid

    sla_name: Optional[ParcelReferenceDef] = Field(None, alias="slaName")
    preferred_color: Optional[ColorMatchListDef] = Field(None, alias="preferredColor")
    preferred_color_group: Optional[ParcelReferenceDef] = Field(None, alias="preferredColorGroup")
    strict: Optional[BooleanDefModel] = None
    fallback_to_best_path: Optional[BooleanDefModel] = Field(None, alias="fallbackToBestPath")


class TrafficToDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: TrafficTo


class EncapListDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[Encap] = Field(..., min_items=1, unique_items=True)


class Ipv4AddressDefModel(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Ipv4AddressDef


class Ipv6AddressDefModel(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Ipv6AddressDef


class OneOfSequencesMatchEntriesPacketLengthValueDef(BaseModel):
    __root__: Union[SequencesMatchEntriesPacketLengthDef, SequencesMatchEntriesPacketLengthRangeDef]


class PortValueDef(BaseModel):
    __root__: Union[PortNoDef, PortRangeDef]


class TlocDef(BaseModel):
    class Config:
        extra = Extra.forbid

    color: ColorMatchListDef
    encap: EncapDef
    ip: Ipv4AddressDefModel


class TypeDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: TypeDefinition


class VpnDefModel(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: VpnDef


class Restrict(BaseModel):
    __root__: BooleanDefModel


class Target(BaseModel):
    class Config:
        extra = Extra.forbid

    vpn: Optional[OneOfTargetVpnOptionsDef] = Field(None, description="")
    direction: Optional[OneOfTargetDirectionOptionsDef] = Field(None, description="")


class OneOfMatchEntriesDestinationPortOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[PortValueDef] = Field(..., min_items=1)


class OneOfMatchEntriesDestinationPortOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesDestinationPortOptionsDefItem


class OneOfMatchEntriesPacketLengthOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: OneOfSequencesMatchEntriesPacketLengthValueDef


class OneOfMatchEntriesPacketLengthOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesPacketLengthOptionsDefItem


class OneOfMatchEntriesSourcePortOptionsDefItem(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: List[PortValueDef] = Field(..., min_items=1)


class OneOfMatchEntriesSourcePortOptionsDef(BaseModel):
    __root__: OneOfMatchEntriesSourcePortOptionsDefItem


class ServiceItem(BaseModel):
    class Config:
        extra = Extra.forbid

    tloc: TlocDef
    vpn: VpnDefModel
    type: TypeDef


class ServiceItem1(BaseModel):
    class Config:
        extra = Extra.forbid

    tloc_list: ParcelReferenceDef = Field(..., alias="tlocList")
    vpn: VpnDefModel
    type: TypeDef


class RestrictDef(BaseModel):
    class Config:
        extra = Extra.forbid

    option_type: GlobalOptionTypeDef = Field(..., alias="optionType")
    value: Restrict


class Entry(BaseModel):
    class Config:
        extra = Extra.forbid

    app_list: Optional[ParcelReferenceDef] = Field(None, alias="appList", description="App list Reference")
    saas_app_list: Optional[ParcelReferenceDef] = Field(
        None, alias="saasAppList", description="Saas App list Reference"
    )
    dns_app_list: Optional[ParcelReferenceDef] = Field(None, alias="dnsAppList", description="dns App list Reference")
    traffic_class: Optional[OneOfMatchEntriesTrafficClassOptionsDef] = Field(
        None, alias="trafficClass", description="Traffic Class"
    )
    dscp: Optional[OneOfMatchEntriesDscpOptionsDef] = Field(None, description="DSCP number")
    packet_length: Optional[OneOfMatchEntriesPacketLengthOptionsDef] = Field(
        None, alias="packetLength", description="Packet Length"
    )
    protocol: Optional[OneOfMatchEntriesProtocolOptionsDef] = Field(
        None,
        description="protocol (0-255) range or individual number separated by space",
    )
    icmp_message: Optional[OneOfMatchEntriesIcmpMessageOptionsDef] = Field(
        None, alias="icmpMessage", description="ICMP Message"
    )
    icmp6_message: Optional[OneOfMatchEntriesIcmp6MessageOptionsDef] = Field(
        None, alias="icmp6Message", description="ICMP6 Message"
    )
    source_data_prefix_list: Optional[ParcelReferenceDef] = Field(
        None, alias="sourceDataPrefixList", description="Source Data Prefix Parcel UUID"
    )
    source_data_ipv6_prefix_list: Optional[ParcelReferenceDef] = Field(
        None,
        alias="sourceDataIpv6PrefixList",
        description="Source Data Prefix Parcel UUID",
    )
    source_ip: Optional[Ipv4PrefixDefModel] = Field(None, alias="sourceIp", description="Source Data IP Prefix")
    source_ipv6: Optional[OneOfMatchEntriesSourceIpv6OptionsDef] = Field(
        None, alias="sourceIpv6", description="Source Data IP Prefix"
    )
    source_port: Optional[OneOfMatchEntriesSourcePortOptionsDef] = Field(
        None,
        alias="sourcePort",
        description="Source Port (0-65535) range or individual number separated by space",
    )
    destination_data_prefix_list: Optional[ParcelReferenceDef] = Field(
        None,
        alias="destinationDataPrefixList",
        description="Destination Data Prefix Parcel UUID",
    )
    destination_data_ipv6_prefix_list: Optional[ParcelReferenceDef] = Field(
        None,
        alias="destinationDataIpv6PrefixList",
        description="Destination Data Prefix Parcel UUID",
    )
    destination_ip: Optional[Ipv4PrefixDefModel] = Field(
        None, alias="destinationIp", description="Destination Data IP Prefix"
    )
    destination_ipv6: Optional[OneOfMatchEntriesDestinationIpv6OptionsDef] = Field(
        None, alias="destinationIpv6", description="Destination Data IP Prefix"
    )
    destination_port: Optional[OneOfMatchEntriesDestinationPortOptionsDef] = Field(
        None,
        alias="destinationPort",
        description="Destination Port (0-65535) range or individual number separated by space",
    )
    tcp: Optional[OneOfMatchEntriesTcpOptionsDef] = Field(None, description="TCP States")
    destination_region: Optional[DestinationRegionDef] = Field(
        None, alias="destinationRegion", description="Destination Region"
    )
    traffic_to: Optional[TrafficToDef] = Field(None, alias="trafficTo", description="Traffic to")
    dns: Optional[DnsDef] = Field(None, description="Dns")


class Match(BaseModel):
    class Config:
        extra = Extra.forbid

    entries: Union[List[Entry], Entries] = Field(..., unique_items=True)


class LocalTlocList(BaseModel):
    class Config:
        extra = Extra.forbid

    color: ColorMatchListDef
    restrict: Optional[RestrictDef] = None
    encap: EncapListDef


class SetProperties(BaseModel):
    class Config:
        extra = Extra.forbid

    dscp: Optional[OneOfMatchEntriesDscpOptionsDef] = None
    policer: Optional[ParcelReferenceDef] = None
    preferred_color_group: Optional[ParcelReferenceDef] = Field(None, alias="preferredColorGroup")
    forwarding_class: Optional[ParcelReferenceDef] = Field(None, alias="forwardingClass")
    local_tloc_list: Optional[LocalTlocList] = Field(None, alias="localTlocList")
    tloc: Optional[TlocDef] = None
    tloc_list: Optional[ParcelReferenceDef] = Field(None, alias="tlocList")
    service: Optional[Union[ServiceItem, ServiceItem1]] = None
    next_hop: Optional[Ipv4AddressDefModel] = Field(None, alias="nextHop")
    next_hop_ipv6: Optional[Ipv6AddressDefModel] = Field(None, alias="nextHopIpv6")
    next_hop_loose: Optional[BooleanDefModel] = Field(None, alias="nextHopLoose")
    vpn: Optional[VpnDefModel] = None


class Action(BaseModel):
    class Config:
        extra = Extra.forbid

    sla_class: Optional[Union[List[SlaClassDef], SlaClass]] = Field(None, alias="slaClass", description="slaClass")
    backup_sla_preferred_color: Optional[ColorMatchListDef] = Field(
        None, alias="backupSlaPreferredColor", description="Backup SLA perferred color"
    )
    set: Optional[Union[List[SetProperties], Set]] = None
    redirect_dns: Optional[OneOfRedirectDnsDef] = Field(None, alias="redirectDns")
    count: Optional[CountDef] = None
    log: Optional[BooleanDefModel] = None
    cloud_saas: Optional[BooleanDefModel] = Field(None, alias="cloudSaas")
    cflowd: Optional[BooleanDefModel] = None
    nat_pool: Optional[NatPoolDef] = Field(None, alias="natPool")
    nat: Optional[NatDef] = None
    sig: Optional[BooleanDefModel] = None
    fallback_to_routing: Optional[BooleanDefModel] = Field(None, alias="fallbackToRouting")


class Sequence(BaseModel):
    class Config:
        extra = Extra.forbid

    sequence_id: Optional[OneOfSequencesSequenceIdOptionsDef] = Field(
        None, alias="sequenceId", description="Sequence Id"
    )
    sequence_name: Optional[OneOfSequencesSequenceNameOptionsDef] = Field(
        None, alias="sequenceName", description="Sequence Name"
    )
    base_action: Optional[OneOfSequencesBaseActionOptionsDef] = Field(
        None, alias="baseAction", description="Base Action"
    )
    sequence_ip_type: Optional[OneOfSequencesSequenceIpTypeOptionsDef] = Field(
        None, alias="sequenceIpType", description="Sequence IP Type"
    )
    match: Optional[Match] = None
    actions: Optional[Union[List[Action], Actions]] = None


class Data(BaseModel):
    class Config:
        extra = Extra.forbid

    simple_flow: Optional[BooleanDefModel] = Field(None, alias="simpleFlow")
    target: Optional[Target] = Field(None, description="Target vpn and direction")
    sequences: Optional[List[Sequence]] = Field(None, description="Traffic policy sequence list", unique_items=True)


class TrafficPolicyParcelSchema(BaseModel):
    name: Optional[CgFpPpNameDef] = None
    description: Optional[str] = None
    data: Data