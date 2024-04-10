# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address, IPv6Interface
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase, as_default

Action = Literal["drop", "accept"]
Icmp6Msg = Literal[
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
IcmpMsg = Literal[
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
Tcp = Literal["syn"]


class ReferenceId(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    ref_id: Global[UUID] = Field(..., serialization_alias="refId", validation_alias="refId")


class SourceDataPrefixListReference(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    source_data_prefix_list: ReferenceId = Field(
        ...,
        serialization_alias="sourceDataPrefixList",
        validation_alias="sourceDataPrefixList",
        description="Source Data Prefix Parcel",
    )


class SourceDataPrefixIp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    source_ip_prefix: Global[str] = Field(
        ...,
        serialization_alias="sourceIpPrefix",
        validation_alias="sourceIpPrefix",
        description="Source Data IP Prefix",
    )


class SourcePort(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    source_port: Union[Global[int], Global[str]] = Field(
        ...,
        serialization_alias="sourcePort",
        validation_alias="sourcePort",
        description="source port range or individual port number",
    )


class DestinationDataPrefixListReference(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    destination_data_prefix_list: ReferenceId = Field(
        ...,
        serialization_alias="destinationDataPrefixList",
        validation_alias="destinationDataPrefixList",
        description="Destination Data Prefix Parcel",
    )


class DestinationDataPrefixIp(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    destination_ip_prefix: Global[IPv6Interface] = Field(
        ...,
        serialization_alias="destinationIpPrefix",
        validation_alias="destinationIpPrefix",
        description="Destination Data IP Prefix",
    )


class DestinationPort(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    destination_port: Union[Global[int], Global[str]] = Field(
        ...,
        serialization_alias="destinationPort",
        validation_alias="destinationPort",
        description="destination port range or individual port number",
    )


class Ipv4MatchEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    dscp: Optional[Global[List[int]]] = Field(default=None, description="DSCP number")
    packet_length: Optional[Union[Global[int], Global[str]]] = Field(
        default=None, serialization_alias="packetLength", validation_alias="packetLength", description="Packet Length"
    )
    protocol: Optional[Global[List[int]]] = Field(
        default=None, description="protocol number list with at least one item"
    )
    icmp_msg: Optional[IcmpMsg] = Field(
        default=None, serialization_alias="icmpMsg", validation_alias="icmpMsg", description="ICMP Message"
    )
    source_data_prefix: Optional[Union[SourceDataPrefixListReference, SourceDataPrefixIp]] = Field(
        default=None, serialization_alias="sourceDataPrefix", validation_alias="sourceDataPrefix"
    )
    source_ports: Optional[List[SourcePort]] = Field(
        default=None, serialization_alias="sourcePorts", validation_alias="sourcePorts", description="Source Port List"
    )
    destination_data_prefix: Optional[Union[DestinationDataPrefixListReference, DestinationDataPrefixIp]] = Field(
        default=None, serialization_alias="destinationDataPrefix", validation_alias="destinationDataPrefix"
    )
    destination_ports: Optional[List[DestinationPort]] = Field(
        default=None,
        serialization_alias="destinationPorts",
        validation_alias="destinationPorts",
        description="Destination Port List",
    )
    tcp: Optional[Tcp] = Field(default=None, description="TCP States")


class Ipv6MatchEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    next_header: Optional[Global[int]] = Field(
        default=None, serialization_alias="nextHeader", validation_alias="nextHeader", description="next header number"
    )
    packet_length: Optional[Union[Global[int], Global[str]]] = Field(
        default=None, serialization_alias="packetLength", validation_alias="packetLength", description="Packet Length"
    )
    source_data_prefix: Optional[Union[SourceDataPrefixListReference, SourceDataPrefixIp]] = Field(
        default=None, serialization_alias="sourceDataPrefix", validation_alias="sourceDataPrefix"
    )
    source_ports: Optional[List[SourcePort]] = Field(
        default=None, serialization_alias="sourcePorts", validation_alias="sourcePorts", description="Source Port List"
    )
    destination_data_prefix: Optional[Union[DestinationDataPrefixListReference, DestinationDataPrefixIp]] = Field(
        default=None, serialization_alias="destinationDataPrefix", validation_alias="destinationDataPrefix"
    )
    destination_ports: Optional[List[DestinationPort]] = Field(
        default=None,
        serialization_alias="destinationPorts",
        validation_alias="destinationPorts",
        description="Destination Port List",
    )
    tcp: Optional[Global[Tcp]] = Field(default=None, description="TCP States")
    traffic_class: Optional[Global[List[int]]] = Field(
        default=None,
        serialization_alias="trafficClass",
        validation_alias="trafficClass",
        description="Select Traffic Class",
    )
    icmp6_msg: Optional[Global[List[Icmp6Msg]]] = Field(
        default=None, serialization_alias="icmp6Msg", validation_alias="icmp6Msg", description="ICMP6 Message"
    )


class Ipv4AcceptAction(BaseModel):
    """
    Accept Action
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    set_dscp: Optional[Global[int]] = Field(
        default=None, serialization_alias="setDscp", validation_alias="setDscp", description="DSCP number"
    )
    counter_name: Optional[Global[str]] = Field(
        default=None, serialization_alias="counterName", validation_alias="counterName", description="Counter Name"
    )
    log: Union[Global[bool], Default[bool]] = Field(default=as_default(False), description="Enable log")
    set_next_hop: Optional[Global[IPv4Address]] = Field(
        default=None,
        serialization_alias="setNextHop",
        validation_alias="setNextHop",
        description="Set Next Hop (IPV4 address)",
    )
    mirror: Optional[ReferenceId] = Field(default=None, description="Select a Mirror Parcel UUID")
    policer: Optional[ReferenceId] = Field(default=None, description="Select a Policer Parcel")


class Ipv6AcceptAction(BaseModel):
    """
    Accept Action
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    counter_name: Optional[Global[str]] = Field(
        default=None, serialization_alias="counterName", validation_alias="counterName", description="Counter Name"
    )
    log: Union[Global[bool], Default[bool]] = Field(default=as_default(False), description="Enable log")
    set_next_hop: Optional[Global[IPv6Address]] = Field(
        default=None,
        serialization_alias="setNextHop",
        validation_alias="setNextHop",
        description="Set Next Hop (IPV6 address)",
    )
    set_traffic_class: Optional[Global[int]] = Field(
        default=None,
        serialization_alias="setTrafficClass",
        validation_alias="setTrafficClass",
        description="set traffic class number",
    )
    mirror: Optional[ReferenceId] = Field(default=None, description="Select a Mirror Parcel UUID")
    policer: Optional[ReferenceId] = Field(default=None, description="Select a Policer Parcel")


class Ipv4AcceptActions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    accept: Ipv4AcceptAction = Field(..., description="Accept Action")


class Ipv6AcceptActions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    accept: Ipv6AcceptAction = Field(..., description="Accept Action")


class DropAction(BaseModel):
    """
    Drop Action
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    counter_name: Optional[Global[str]] = Field(
        default=None, serialization_alias="counterName", validation_alias="counterName", description="Counter Name"
    )
    log: Union[Global[bool], Default[bool]] = Field(default=as_default(False), description="Enable log")


class DropActions(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    drop: DropAction = Field(..., description="Drop Action")


class Sequences(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    sequence_id: Global[int] = Field(
        ..., serialization_alias="sequenceId", validation_alias="sequenceId", description="Sequence Id"
    )
    sequence_name: Global[str] = Field(
        ..., serialization_alias="sequenceName", validation_alias="sequenceName", description="Sequence Name"
    )
    base_action: Optional[Union[Global[Action], Default[Action]]] = Field(
        default=None, serialization_alias="baseAction", validation_alias="baseAction", description="Base Action"
    )
    match_entries: Optional[List[Ipv6MatchEntry]] = Field(
        default=None,
        serialization_alias="matchEntries",
        validation_alias="matchEntries",
        description="Define match conditions",
        max_length=1,
        min_length=1,
    )

    @model_validator(mode="after")
    def check_fields_at_least_one_assigned(self):
        """There are two Sequence models in schema,
        one with set base_action and empty actions,
        and one with set actions and empty base_action,
        so we combine two models into one model with check if
        at least one field assigned
        """
        if self.base_action is None and self.actions is None:
            self.base_action = as_default("accept", Action)


class Ipv6Sequences(Sequences):
    actions: Optional[List[Union[Ipv6AcceptActions, DropActions]]] = Field(
        default=None, description="Define list of actions", max_length=1, min_length=1
    )


class Ipv4Sequences(Sequences):
    actions: Optional[List[Union[Ipv4AcceptActions, DropActions]]] = Field(
        default=None, description="Define list of actions", max_length=1, min_length=1
    )


class Ipv4AclParcel(_ParcelBase):
    type_: Literal["ipv4-acl"] = Field(default="ipv4-acl", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    default_action: Union[Global[Action], Global[Action]] = Field(
        as_default("drop", Action),
        validation_alias=AliasPath("data", "defaultAction"),
        description="Default Action",
    )
    sequences: List[Union[Ipv4Sequences]] = Field(
        default_factory=list, validation_alias=AliasPath("data", "sequences"), description="Access Control List"
    )


class Ipv6AclParcel(_ParcelBase):
    type_: Literal["ipv6-acl"] = Field(default="ipv6-acl", exclude=True)
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    default_action: Union[Global[Action], Global[Action]] = Field(
        as_default("drop", Action),
        validation_alias=AliasPath("data", "defaultAction"),
        description="Default Action",
    )
    sequences: List[Union[Ipv6Sequences]] = Field(
        default_factory=list, validation_alias=AliasPath("data", "sequences"), description="Access Control List"
    )
