# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv6Interface
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_global, as_variable
from catalystwan.models.common import AcceptDropActionType, DeviceAccessProtocolPort
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class SourceDataPrefix(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    source_data_prefix_list: RefIdItem = Field(
        validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )


class SourceIPPrefix(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    source_ip_prefix_list: Union[Global[List[IPv6Interface]], Variable] = Field(
        validation_alias="sourceIpPrefixList", serialization_alias="sourceIpPrefixList"
    )


class DestinationDataPrefix(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    destination_data_prefix_list: RefIdItem = Field(
        validation_alias="destinationDataPrefixList", serialization_alias="destinationDataPrefixList"
    )


class DestinationIPPrefix(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    destination_ip_prefix_list: Union[Global[List[IPv6Interface]], Variable] = Field(
        validation_alias="destinationIpPrefixList", serialization_alias="destinationIpPrefixList"
    )


class MatchEntries(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)

    destination_data_prefix: Optional[Union[DestinationIPPrefix, DestinationDataPrefix]] = Field(
        default=None, validation_alias="destinationDataPrefix", serialization_alias="destinationDataPrefix"
    )
    destination_port: Global[DeviceAccessProtocolPort] = Field(
        validation_alias="destinationPort", serialization_alias="destinationPort"
    )
    source_data_prefix: Optional[Union[SourceIPPrefix, SourceDataPrefix]] = Field(
        default=None, validation_alias="sourceDataPrefix", serialization_alias="sourceDataPrefix"
    )
    source_ports: Optional[Global[List[int]]] = Field(
        default=None, validation_alias="sourcePorts", serialization_alias="sourcePorts"
    )


class Sequence(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)

    base_action: Union[Global[AcceptDropActionType], Default[Literal[AcceptDropActionType]]] = Field(
        default=Default[Literal[AcceptDropActionType]](value="accept"),
        validation_alias="baseAction",
        serialization_alias="baseAction",
    )
    match_entries: MatchEntries = Field(
        validation_alias="matchEntries", serialization_alias="matchEntries", description="Define match conditions"
    )
    sequence_id: Global[int] = Field(validation_alias="sequenceId", serialization_alias="sequenceId")
    sequence_name: Global[str] = Field(validation_alias="sequenceName", serialization_alias="sequenceName")

    def set_base_action(self, base_action: AcceptDropActionType):
        self.base_action = Global[AcceptDropActionType](value=base_action)

    def match_destination_data_prefixes(self, prefixes: List[IPv6Interface]):
        self.match_entries.destination_data_prefix = DestinationIPPrefix(
            destination_ip_prefix_list=Global[List[IPv6Interface]](value=prefixes)
        )

    def match_destination_data_prefix_list(self, list_id: UUID):
        self.match_entries.destination_data_prefix = DestinationDataPrefix(
            destination_data_prefix_list=RefIdItem.from_uuid(list_id)
        )

    def match_destination_data_prefix_variable(self, variable_name: str):
        self.match_entries.destination_data_prefix = DestinationIPPrefix(
            destination_ip_prefix_list=as_variable(value=variable_name)
        )

    def match_destination_port(self, port: DeviceAccessProtocolPort):
        self.match_entries.destination_port = Global[DeviceAccessProtocolPort](value=port)

    def match_source_data_prefixes(self, prefixes: List[IPv6Interface]):
        self.match_entries.source_data_prefix = SourceIPPrefix(
            source_ip_prefix_list=Global[List[IPv6Interface]](value=prefixes)
        )

    def match_source_data_prefix_list(self, list_id: UUID):
        self.match_entries.source_data_prefix = SourceDataPrefix(source_data_prefix_list=RefIdItem.from_uuid(list_id))

    def match_source_data_prefix_variable(self, variable_name: str):
        self.match_entries.source_data_prefix = SourceIPPrefix(source_ip_prefix_list=as_variable(value=variable_name))

    def match_source_ports(self, ports: List[int]):
        self.match_entries.source_ports = Global[List[int]](value=ports)

    @classmethod
    def create(
        cls,
        sequence_id: int,
        sequence_name: str,
        base_action: AcceptDropActionType,
        match_entries: MatchEntries,
    ) -> "Sequence":
        return cls(
            base_action=Global[AcceptDropActionType](value=base_action),
            match_entries=match_entries,
            sequence_id=Global[int](value=sequence_id),
            sequence_name=Global[str](value=sequence_name),
        )


class DeviceAccessIPv6Parcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    type_: Literal["ipv6-device-access-policy"] = Field(default="ipv6-device-access-policy", exclude=True)

    default_action: Union[Global[AcceptDropActionType], Default[AcceptDropActionType]] = Field(
        default=Default[AcceptDropActionType](value="drop"), validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: List[Sequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Device Access Control List"
    )

    def set_default_action(self, default_action: AcceptDropActionType) -> None:
        self.default_action = Global[AcceptDropActionType](value=default_action)

    def add_sequence(
        self,
        id_: int,
        name: str,
        destination_port: DeviceAccessProtocolPort,
        base_action: AcceptDropActionType,
    ) -> Sequence:
        match_entries = MatchEntries(destination_port=as_global(destination_port, DeviceAccessProtocolPort))
        sequence = Sequence.create(
            sequence_id=id_,
            sequence_name=name,
            base_action=base_action,
            match_entries=match_entries,
        )
        self.sequences.append(sequence)
        return sequence
