from ipaddress import IPv4Address, IPv4Interface
from typing import List, Literal, Optional, Tuple, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_global, as_variable
from catalystwan.models.common import AcceptDropActionType
from catalystwan.models.configuration.feature_profile.common import RefIdItem

IcmpIPv4Messages = Literal[
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
    destination_ip_prefix: Union[Variable, Global[str]] = Field(
        validation_alias="destinationIpPrefix", serialization_alias="destinationIpPrefix"
    )


class DestinationPorts(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    destination_port: Union[Global[str], Global[int], None] = Field(
        default=None, validation_alias="destinationPort", serialization_alias="destinationPort"
    )


class MatchEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
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
    icmp_msg: Optional[Global[List[IcmpIPv4Messages]]] = Field(
        default=None, validation_alias="icmpMsg", serialization_alias="icmpMsg"
    )
    packet_length: Union[Global[str], Global[int], None] = Field(
        default=None, validation_alias="packetLength", serialization_alias="packetLength"
    )
    protocol: Optional[Global[List[int]]] = Field(default=None)
    source_data_prefix: Union[SourceDataPrefix, SourceDataPrefixList, None] = Field(
        default=None, validation_alias="sourceDataPrefix", serialization_alias="sourceDataPrefix"
    )
    source_ports: Optional[List[SourcePorts]] = Field(
        default=None,
        validation_alias="sourcePorts",
        serialization_alias="sourcePorts",
        description="Source Port List",
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
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
    accept: Accept = Field(description="Accept Action")


class Drop(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    counter_name: Optional[Global[str]] = Field(
        default=None, validation_alias="counterName", serialization_alias="counterName"
    )
    log: Optional[Union[Global[bool], Default[bool]]] = Field(default=None)


class DropAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
    drop: Drop = Field(description="Drop Action")


class Sequence(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
    actions: Optional[List[Union[AcceptAction, DropAction]]] = Field(
        default=None, description="Define list of actions", max_length=1, min_length=1
    )
    base_action: Optional[Union[Global[AcceptDropActionType], Default[Literal["accept"]]]] = Field(
        default=None, validation_alias="baseAction", serialization_alias="baseAction"
    )
    match_entries: Optional[List[MatchEntry]] = Field(
        default=None,
        validation_alias="matchEntries",
        serialization_alias="matchEntries",
        description="Define match conditions",
        max_length=1,
        min_length=1,
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

    def match_destination_data_prefix(self, prefix: IPv4Interface):
        value = as_global(str(prefix))
        self._entry.destination_data_prefix = DestinationDataPrefix(destination_ip_prefix=value)

    def match_destination_data_prefix_variable(self, prefix: str):
        value = as_variable(prefix)
        self._entry.destination_data_prefix = DestinationDataPrefix(destination_ip_prefix=value)

    def match_destination_data_prefix_list(self, prefix: UUID):
        self._entry.destination_data_prefix = DestinationDataPrefixList(
            destination_data_prefix_list=RefIdItem.from_uuid(prefix)
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

    def match_dscp(self, dscp: List[int]):
        self._entry.dscp = as_global(dscp)

    def match_icmp_msg(self, icmp: List[IcmpIPv4Messages]):
        self._entry.icmp_msg = Global[List[IcmpIPv4Messages]](value=icmp)

    def match_packet_length(self, len: Union[int, Tuple[int, int]]):
        if isinstance(len, int):
            value = as_global(len)
        else:
            value = as_global(f"{len[0]}-{len[1]}")
        self._entry.packet_length = value

    def match_protocol(self, protocols: List[int]):
        self._entry.protocol = as_global(protocols)

    def match_source_data_prefix(self, prefix: IPv4Interface):
        value = as_global(str(prefix))
        self._entry.source_data_prefix = SourceDataPrefix(source_ip_prefix=value)

    def match_source_data_prefix_variable(self, prefix: str):
        value = as_variable(prefix)
        self._entry.source_data_prefix = SourceDataPrefix(source_ip_prefix=value)

    def match_source_data_prefix_list(self, prefix: UUID):
        self._entry.source_data_prefix = SourceDataPrefixList(source_data_prefix_list=RefIdItem.from_uuid(prefix))

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

    def associate_set_dscp_action(self, dscp: int):
        self._accept_action.set_dscp = as_global(dscp)

    def associate_set_next_hop_action(self, next_hop: IPv4Address):
        self._accept_action.set_next_hop = as_global(str(next_hop))


class Ipv4AclParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
    type_: Literal["ipv4-acl"] = Field(default="ipv4-acl", exclude=True)
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
