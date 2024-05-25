from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

BaseAction = Literal[
    "accept",
    "drop",
]


class SourceDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    source_data_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )


class SourceDataPrefix(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    source_ip_prefix: Optional[Global[str]] = Field(
        default=None, validation_alias="sourceIpPrefix", serialization_alias="sourceIpPrefix"
    )


class SourcePorts(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    source_port: Optional[Global[Union[str, int]]] = Field(
        default=None, validation_alias="sourcePort", serialization_alias="sourcePort"
    )


class DestinationDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    destination_data_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="destinationDataPrefixList", serialization_alias="destinationDataPrefixList"
    )


class DestinationDataPrefix(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    destination_ip_prefix: Optional[Global[str]] = Field(
        default=None, validation_alias="destinationIpPrefix", serialization_alias="destinationIpPrefix"
    )


class DestinationPorts(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    destination_port: Optional[Global[Union[str, int]]] = Field(
        default=None, validation_alias="destinationPort", serialization_alias="destinationPort"
    )


Value = Literal[
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


class MatchEntries(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    destination_data_prefix: Union[DestinationDataPrefix, DestinationDataPrefixList, None] = Field(
        default=None, validation_alias="destinationDataPrefix", serialization_alias="destinationDataPrefix"
    )
    destination_ports: Optional[List[DestinationPorts]] = Field(
        default=None,
        validation_alias="destinationPorts",
        serialization_alias="destinationPorts",
        description="Destination Port List",
    )
    icmp6_msg: Optional[Global[List[Value]]] = Field(
        default=None, validation_alias="icmp6Msg", serialization_alias="icmp6Msg"
    )
    next_header: Optional[Global[int]] = Field(
        default=None, validation_alias="nextHeader", serialization_alias="nextHeader"
    )
    packet_length: Optional[Global[Union[str, int]]] = Field(
        default=None, validation_alias="packetLength", serialization_alias="packetLength"
    )
    source_data_prefix: Union[SourceDataPrefix, SourceDataPrefixList] = Field(
        default=None, validation_alias="sourceDataPrefix", serialization_alias="sourceDataPrefix"
    )
    source_ports: Optional[List[SourcePorts]] = Field(
        default=None, validation_alias="sourcePorts", serialization_alias="sourcePorts", description="Source Port List"
    )
    tcp: Optional[Global[Literal["syn"]]] = Field(default=None)
    traffic_class: Optional[Global[List[int]]] = Field(
        default=None, validation_alias="trafficClass", serialization_alias="trafficClass"
    )


class Accept(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    counter_name: Optional[Global[str]] = Field(
        default=None, validation_alias="counterName", serialization_alias="counterName"
    )
    log: Optional[Union[Global[bool], Default[bool]]] = Field(default=None)
    mirror: Optional[RefIdItem] = Field(default=None)
    policer: Optional[RefIdItem] = Field(default=None)
    set_next_hop: Optional[Global[str]] = Field(
        default=None, validation_alias="setNextHop", serialization_alias="setNextHop"
    )
    set_traffic_class: Optional[Global[int]] = Field(
        default=None, validation_alias="setTrafficClass", serialization_alias="setTrafficClass"
    )


class AcceptAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    accept: Accept = Field(description="Accept Action")


class Drop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    counter_name: Optional[Global[str]] = Field(
        default=None, validation_alias="counterName", serialization_alias="counterName"
    )
    log: Optional[Union[Global[bool], Default[bool]]] = Field(default=None)


class DropAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    drop: Drop = Field(description="Drop Action")


class Sequence(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    actions: Optional[List[Union[AcceptAction, DropAction]]] = Field(description="Define list of actions")
    base_action: Optional[Union[Global[BaseAction], Default[Literal["accept"]]]] = Field(
        default=None, validation_alias="baseAction", serialization_alias="baseAction"
    )
    match_entries: Optional[List[MatchEntries]] = Field(
        default=None,
        validation_alias="matchEntries",
        serialization_alias="matchEntries",
        description="Define match conditions",
    )
    sequence_id: Optional[Global[int]] = Field(
        default=None, validation_alias="sequenceId", serialization_alias="sequenceId"
    )
    sequence_name: Optional[Global[str]] = Field(
        default=None, validation_alias="sequenceName", serialization_alias="sequenceName"
    )


class Ipv6AclParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["ipv6-acl"] = Field(default="ipv6-acl", exclude=True)
    default_action: Union[Global[BaseAction], Default[Literal["drop"]]] = Field(
        default=Default[Literal["drop"]](value="drop"), validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: List[Sequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Access Control List"
    )
