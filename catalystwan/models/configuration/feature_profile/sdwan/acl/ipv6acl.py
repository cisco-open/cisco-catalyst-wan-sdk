from ipaddress import IPv6Address, IPv6Interface
from typing import List, Literal, Optional, Tuple, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase, as_global
from catalystwan.models.common import AcceptDropActionType
from catalystwan.models.configuration.feature_profile.common import RefIdItem


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
    source_port: Union[Global[str], Global[int], None] = Field(
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
    destination_port: Union[Global[str], Global[int], None] = Field(
        default=None, validation_alias="destinationPort", serialization_alias="destinationPort"
    )


IcmpIPv6Messages = Literal[
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


class MatchEntry(BaseModel):
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
    icmp6_msg: Optional[Global[List[IcmpIPv6Messages]]] = Field(
        default=None, validation_alias="icmp6Msg", serialization_alias="icmp6Msg"
    )
    next_header: Optional[Global[int]] = Field(
        default=None, validation_alias="nextHeader", serialization_alias="nextHeader"
    )
    packet_length: Optional[Global[Union[str, int]]] = Field(
        default=None, validation_alias="packetLength", serialization_alias="packetLength"
    )
    source_data_prefix: Union[SourceDataPrefix, SourceDataPrefixList, None] = Field(
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
    actions: Optional[List[Union[AcceptAction, DropAction]]] = Field(default=None, description="Define list of actions")
    base_action: Optional[Union[Global[AcceptDropActionType], Default[Literal["accept"]]]] = Field(
        default=None, validation_alias="baseAction", serialization_alias="baseAction"
    )
    match_entries: Optional[List[MatchEntry]] = Field(
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

    @property
    def _action(self) -> Union[AcceptAction, DropAction]:
        if self.actions is None:
            if self.base_action is None:
                self.base_action = Global[AcceptDropActionType](value="accept")
            if self.base_action.value == "accept":
                self.actions = [(AcceptAction(accept=Accept()))]
            else:
                self.actions = [(DropAction(drop=Drop()))]
        return self.actions[0]

    @property
    def _accept_action(self) -> Accept:
        action = self._action
        assert isinstance(action, AcceptAction), "Sequence action must be set to accept"
        return action.accept

    @property
    def _drop_action(self) -> Drop:
        action = self._action
        assert isinstance(action, DropAction), "Sequence action must be set to drop"
        return action.drop

    @property
    def _entry(self) -> MatchEntry:
        if self.match_entries is None:
            self.match_entries = [MatchEntry()]
        return self.match_entries[0]

    def match_destination_data_prefix(self, prefix: IPv6Interface):
        value = as_global(str(prefix))
        self._entry.destination_data_prefix = DestinationDataPrefix(destination_ip_prefix=value)

    def match_destination_data_prefix_list(self, list_id: UUID):
        value = as_global(str(list_id))
        self._entry.destination_data_prefix = DestinationDataPrefixList(
            destination_data_prefix_list=RefIdItem(ref_id=value)
        )

    def match_destination_ports(self, ports: List[Union[int, Tuple[int, int]]]):
        """
        ports argument example: [1, 3, (10,100), (50,200), 600]
        """
        destination_ports = []
        for port in ports:
            if isinstance(port, int):
                value = as_global(port)
            else:
                value = as_global(f"{port[0]}-{port[1]}")
            destination_ports.append(DestinationPorts(destination_port=value))
        self._entry.destination_ports = destination_ports

    def match_icmp_msg(self, icmp: List[IcmpIPv6Messages]):
        self._entry.icmp6_msg = Global[List[IcmpIPv6Messages]](value=icmp)

    def match_packet_length(self, len: Union[int, Tuple[int, int]]):
        if isinstance(len, int):
            value = as_global(len)
        else:
            value = as_global(f"{len[0]}-{len[1]}")
        self._entry.packet_length = value

    def match_source_data_prefix(self, prefix: IPv6Interface):
        value = as_global(str(prefix))
        self._entry.source_data_prefix = SourceDataPrefix(source_ip_prefix=value)

    def match_source_data_prefix_list(self, list_id: UUID):
        value = as_global(str(list_id))
        self._entry.source_data_prefix = SourceDataPrefixList(source_data_prefix_list=RefIdItem(ref_id=value))

    def match_source_ports(self, ports: List[Union[int, Tuple[int, int]]]):
        """
        ports argument example: [1, 3, (10,100), (50,200), 600]
        """
        source_ports = []
        for port in ports:
            if isinstance(port, int):
                value = as_global(port)
            else:
                value = as_global(f"{port[0]}-{port[1]}")
            source_ports.append(SourcePorts(source_port=value))
        self._entry.source_ports = source_ports

    def match_tcp(self):
        self._entry.tcp = as_global("syn", Literal["syn"])

    def match_traffic_class(self, classes: List[int]):
        self._entry.traffic_class = as_global(classes)

    def associate_log_action(self):
        if isinstance(self._action, DropAction):
            self._drop_action.log = as_global(True)
        else:
            self._accept_action.log = as_global(True)

    def associate_counter_action(self, name: str):
        if isinstance(self._action, DropAction):
            self._drop_action.counter_name = as_global(name)
        else:
            self._accept_action.counter_name = as_global(name)

    def associate_mirror_action(self, mirror: UUID):
        self._accept_action.mirror = RefIdItem(ref_id=as_global(str(mirror)))

    def associate_policer_action(self, policer: UUID):
        self._accept_action.policer = RefIdItem(ref_id=as_global(str(policer)))

    def associate_set_traffic_class_action(self, traffic_class: int):
        self._accept_action.set_traffic_class = as_global(traffic_class)

    def associate_set_next_hop_action(self, next_hop: IPv6Address):
        self._accept_action.set_next_hop = as_global(str(next_hop))


class Ipv6AclParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["ipv6-acl"] = Field(default="ipv6-acl", exclude=True)
    default_action: Union[Global[AcceptDropActionType], Default[Literal["drop"]]] = Field(
        default=Default[Literal["drop"]](value="drop"), validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: List[Sequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Access Control List"
    )

    def set_default_action(self, action: AcceptDropActionType):
        self.default_action = as_global(action, AcceptDropActionType)

    def add_sequence(self, name: str, id_: int, base_action: Optional[AcceptDropActionType] = None) -> Sequence:
        seq = Sequence(
            base_action=as_global(base_action, AcceptDropActionType) if base_action is not None else None,
            sequence_id=as_global(id_),
            sequence_name=as_global(name),
        )
        if self.sequences is None:
            self.sequences = [seq]
        else:
            self.sequences.append(seq)
        return seq
