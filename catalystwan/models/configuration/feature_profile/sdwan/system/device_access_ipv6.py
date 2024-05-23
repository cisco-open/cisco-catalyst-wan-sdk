from ipaddress import IPv6Interface
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

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
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

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


class Sequences(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

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


class DeviceAccessIPv6Parcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    type_: Literal["ipv6-device-access-policy"] = Field(default="ipv6-device-access-policy", exclude=True)

    default_action: Union[Global[BaseAction], Default[BaseAction]] = Field(
        default=Default[BaseAction](value="drop"), validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: List[Sequences] = Field(
        default=[], validation_alias=AliasPath("data", "sequences"), description="Device Access Control List"
    )

    def add_sequences(
        self,
        sequence_id: int,
        sequence_name: str,
        match_entries: MatchEntries,
        base_action: Optional[BaseAction] = None,
    ) -> Sequences:
        payload: Dict[str, Any] = {
            "sequence_id": Global[int](value=sequence_id),
            "sequence_name": Global[str](value=sequence_name),
            "match_entries": match_entries,
        }
        if base_action is not None:
            payload["base_action"] = Global[BaseAction](value=base_action)

        sequences = Sequences(**payload)
        self.sequences.append(sequences)
        return sequences

    def create_match_entries(
        self,
        destination_port: DestinationPort,
        destination_prefix: Optional[Union[RefIdItem, List[str], List[IPv6Interface], Variable]] = None,
        source_prefix: Optional[Union[RefIdItem, List[str], List[IPv6Interface], Variable]] = None,
        source_ports: Optional[List[int]] = None,
    ) -> MatchEntries:
        def resolve_ip_prefix_list(
            prefix_list: Union[List[str], List[IPv6Interface], Variable]
        ) -> Union[Global[List[IPv6Interface]], Variable]:
            if isinstance(prefix_list, list):
                return Global[List[IPv6Interface]](value=prefix_list)  # type: ignore
            else:
                return prefix_list

        destination_data_prefix: Optional[Union[DestinationDataPrefix, DestinationIPPrefix]] = None
        if destination_prefix is not None:
            if isinstance(destination_prefix, RefIdItem):
                destination_data_prefix = DestinationDataPrefix(destination_data_prefix_list=destination_prefix)
            else:
                destination_data_prefix = DestinationIPPrefix(
                    destination_ip_prefix_list=resolve_ip_prefix_list(destination_prefix)
                )

        source_data_prefix: Optional[Union[SourceDataPrefix, SourceIPPrefix]] = None
        if source_prefix is not None:
            if isinstance(source_prefix, RefIdItem):
                source_data_prefix = SourceDataPrefix(source_data_prefix_list=source_prefix)
            else:
                source_data_prefix = SourceIPPrefix(source_ip_prefix_list=resolve_ip_prefix_list(source_prefix))

        return MatchEntries(
            destination_port=Global[DestinationPort](value=destination_port),
            destination_data_prefix=destination_data_prefix,
            source_data_prefix=source_data_prefix,
            source_ports=Global[List[int]](value=source_ports) if source_ports is not None else None,
        )
