from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

BaseAction = Literal[
    "accept",
    "drop",
]


Value = Literal[
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


class SourceDataPrefixList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    source_data_prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )


class SourceDataPrefix(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    source_ip_prefix: Union[Variable, Global[str]] = Field(
        validation_alias="sourceIpPrefix", serialization_alias="sourceIpPrefix"
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
    destination_ip_prefix: Union[Variable, Global[str]] = Field(
        validation_alias="destinationIpPrefix", serialization_alias="destinationIpPrefix"
    )


class DestinationPorts(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    destination_port: Optional[Global[Union[str, int]]] = Field(
        default=None, validation_alias="destinationPort", serialization_alias="destinationPort"
    )


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
    dscp: Optional[Global[List[int]]] = Field(default=None)
    icmp_msg: Optional[Global[List[Value]]] = Field(
        default=None, validation_alias="icmpMsg", serialization_alias="icmpMsg"
    )
    packet_length: Optional[Global[Union[str, int]]] = Field(
        default=None, validation_alias="packetLength", serialization_alias="packetLength"
    )
    protocol: Optional[Global[List[int]]] = Field(default=None)
    source_data_prefix: Union[SourceDataPrefix, SourceDataPrefixList, None] = Field(
        default=None, validation_alias="sourceDataPrefix", serialization_alias="sourceDataPrefix"
    )
    source_ports: Optional[List[SourcePorts]] = Field(
        default=None, validation_alias="sourcePorts", serialization_alias="sourcePorts", description="Source Port List"
    )
    tcp: Optional[Global[Literal["syn"]]] = Field(default=None)


class Accept(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    counter_name: Optional[Global[str]] = Field(
        default=None, validation_alias="counterName", serialization_alias="counterName"
    )
    log: Optional[Union[Global[bool], Default[bool]]] = Field(default=None)
    mirror: Optional[RefIdItem] = Field(default=None)
    policer: Optional[RefIdItem] = Field(default=None)
    set_dscp: Optional[Global[int]] = Field(default=None, validation_alias="setDscp", serialization_alias="setDscp")
    set_next_hop: Optional[Global[str]] = Field(
        default=None, validation_alias="setNextHop", serialization_alias="setNextHop"
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


class Ipv4AclParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["ipv4-acl"] = Field(default="ipv4-acl", exclude=True)
    default_action: Union[Global[BaseAction], Default[Literal["drop"]]] = Field(
        default=Default[Literal["drop"]](value="drop"), validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: List[Sequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Access Control List"
    )
