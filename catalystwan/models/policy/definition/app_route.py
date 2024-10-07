from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import SequenceIpType
from catalystwan.models.policy.policy_definition import (
    AppListEntry,
    BackupSlaPrefferedColorAction,
    CloudSaaSAction,
    CountAction,
    DefinitionWithSequencesCommonBase,
    DestinationDataIPv6PrefixListEntry,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationIPv6Entry,
    DestinationPortEntry,
    DestinationRegionEntry,
    DNSAppListEntry,
    DNSEntry,
    DSCPEntry,
    LogAction,
    Match,
    PLPEntry,
    PolicyActionBase,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    ProtocolEntry,
    SaaSAppListEntry,
    SlaClassAction,
    SourceDataIPv6PrefixListEntry,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourceIPv6Entry,
    SourcePortEntry,
    TrafficToEntry,
)

AppRoutePolicySequenceEntry = Annotated[
    Union[
        AppListEntry,
        DestinationDataIPv6PrefixListEntry,
        DestinationDataPrefixListEntry,
        DestinationIPEntry,
        DestinationIPv6Entry,
        DestinationPortEntry,
        DestinationRegionEntry,
        DNSAppListEntry,
        DNSEntry,
        DSCPEntry,
        PLPEntry,
        ProtocolEntry,
        SaaSAppListEntry,
        SourceDataIPv6PrefixListEntry,
        SourceDataPrefixListEntry,
        SourceIPEntry,
        SourceIPv6Entry,
        SourcePortEntry,
        TrafficToEntry,
    ],
    Field(discriminator="field"),
]

AppRoutePolicySequenceActionEntry = Annotated[
    Union[
        BackupSlaPrefferedColorAction,
        CloudSaaSAction,
        CountAction,
        LogAction,
        SlaClassAction,
    ],
    Field(discriminator="type"),
]


class AppRoutePolicySequenceMatch(Match):
    entries: List[AppRoutePolicySequenceEntry] = []


class AppRoutePolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["appRoute"] = Field(
        default="appRoute", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    match: AppRoutePolicySequenceMatch = AppRoutePolicySequenceMatch()
    actions: List[AppRoutePolicySequenceActionEntry] = []
    model_config = ConfigDict(populate_by_name=True)


class AppRouteDefaultAction(PolicyActionBase):
    type: Literal["slaClass"] = "slaClass"
    ref: UUID


class AppRoutePolicyHeader(PolicyDefinitionBase):
    type: Literal["appRoute"] = "appRoute"


class AppRoutePolicy(AppRoutePolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[AppRoutePolicySequence] = []
    default_action: Optional[AppRouteDefaultAction] = Field(
        default=None, serialization_alias="defaultAction", validation_alias="defaultAction"
    )
    model_config = ConfigDict(populate_by_name=True)

    def add_sequence(
        self,
        name: str = "Custom",
        sequence_ip_type: SequenceIpType = "ipv4",
    ) -> AppRoutePolicySequence:
        seq = AppRoutePolicySequence(
            sequence_name=name,
            sequence_ip_type=sequence_ip_type,
        )
        self.add(seq)
        return seq


class AppRoutePolicyEditPayload(AppRoutePolicy, PolicyDefinitionId):
    pass


class AppRoutePolicyGetResponse(AppRoutePolicy, PolicyDefinitionGetResponse):
    pass
