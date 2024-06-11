from ipaddress import IPv6Interface
from typing import Any, Dict, List, Literal, Optional, Union, overload

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem
from catalystwan.utils.type_check import is_str_uuid

BaseAction = Literal[
    "accept",
    "drop",
]
DestinationPort = Literal[161, 22]


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
    destination_port: Global[DestinationPort] = Field(
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

    base_action: Union[Global[BaseAction], Default[Literal[BaseAction]]] = Field(
        default=Default[Literal[BaseAction]](value="accept"),
        validation_alias="baseAction",
        serialization_alias="baseAction",
    )
    match_entries: MatchEntries = Field(
        validation_alias="matchEntries", serialization_alias="matchEntries", description="Define match conditions"
    )
    sequence_id: Global[int] = Field(validation_alias="sequenceId", serialization_alias="sequenceId")
    sequence_name: Global[str] = Field(validation_alias="sequenceName", serialization_alias="sequenceName")

    def set_base_action(self, base_action: BaseAction):
        self.base_action = Global[BaseAction](value=base_action)

    @overload
    def match_destination_data_prefix(self, destination_prefix: str):
        ...

    @overload
    def match_destination_data_prefix(self, destination_prefix: List[str]):
        ...

    @overload
    def match_destination_data_prefix(self, destination_prefix: List[IPv6Interface]):
        ...

    def match_destination_data_prefix(self, destination_prefix):
        if isinstance(destination_prefix, str):
            if is_str_uuid(destination_prefix):
                self.match_entries.destination_data_prefix = DestinationDataPrefix(
                    destination_data_prefix_list=RefIdItem(ref_id=Global[str](value=destination_prefix))
                )
            else:
                self.match_entries.destination_data_prefix = DestinationIPPrefix(
                    destination_ip_prefix_list=Variable(value=destination_prefix)
                )
        else:
            self.match_entries.destination_data_prefix = DestinationIPPrefix(
                destination_ip_prefix_list=Global[List[IPv6Interface]](value=destination_prefix)
            )

    @overload
    def match_source_data_prefix(self, source_prefix: str):
        ...

    @overload
    def match_source_data_prefix(self, source_prefix: List[str]):
        ...

    @overload
    def match_source_data_prefix(self, source_prefix: List[IPv6Interface]):
        ...

    def match_source_data_prefix(self, source_prefix):
        if isinstance(source_prefix, str):
            if is_str_uuid(source_prefix):
                self.match_entries.source_data_prefix = SourceDataPrefix(
                    source_data_prefix_list=RefIdItem(ref_id=Global[str](value=source_prefix))
                )
            else:
                self.match_entries.source_data_prefix = SourceIPPrefix(
                    source_ip_prefix_list=Variable(value=source_prefix)
                )
        else:
            self.match_entries.source_data_prefix = SourceIPPrefix(
                source_ip_prefix_list=Global[List[IPv6Interface]](value=source_prefix)
            )

    def match_source_ports(self, ports: List[int]):
        self.match_entries.source_ports = Global[List[int]](value=ports)


class DeviceAccessIPv6Parcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    type_: Literal["ipv6-device-access-policy"] = Field(default="ipv6-device-access-policy", exclude=True)

    default_action: Union[Global[BaseAction], Default[BaseAction]] = Field(
        default=Default[BaseAction](value="drop"), validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: List[Sequence] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Device Access Control List"
    )

    def set_default_action(self, default_action: BaseAction) -> None:
        self.default_action = Global[BaseAction](value=default_action)

    def add_sequence(
        self,
        sequence_id: int,
        sequence_name: str,
        destination_port: DestinationPort,
        base_action: Optional[BaseAction] = None,
    ) -> Sequence:
        payload: Dict[str, Any] = {
            "sequence_id": Global[int](value=sequence_id),
            "sequence_name": Global[str](value=sequence_name),
            "match_entries": MatchEntries(destination_port=Global[DestinationPort](value=destination_port)),
        }
        if base_action is not None:
            payload["base_action"] = Global[BaseAction](value=base_action)

        sequences = Sequence(**payload)
        self.sequences.append(sequences)
        return sequences
