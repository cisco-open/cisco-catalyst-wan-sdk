from ipaddress import IPv4Network, IPv6Network
from typing import List, Literal, Optional, Set, Tuple, Union, overload
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import DestinationRegion, DNSEntryType, SequenceIpType, TLOCColor, TrafficTargetType
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
    PLPEntryType,
    PolicyActionBase,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    ProtocolEntry,
    SaaSAppListEntry,
    SlaClassAction,
    SlaNotMetAction,
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

    def match_app_list(self, app_list_id: UUID) -> None:
        self._insert_match(AppListEntry(ref=[app_list_id]))

    def match_destination_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(DestinationDataPrefixListEntry(ref=[data_prefix_list_id]))

    def match_destination_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(DestinationIPEntry.from_ipv4_networks(networks))

    def match_destination_ipv6(self, networks: List[IPv6Network]) -> None:
        self._insert_match(DestinationIPv6Entry.from_ipv6_networks(networks))

    def match_destination_region(self, region: DestinationRegion) -> None:
        self._insert_match(DestinationRegionEntry(value=region))

    def match_destination_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(DestinationPortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_dns(self, dns: DNSEntryType) -> None:
        self._insert_match(DNSEntry(value=dns))

    def match_dns_app_list(self, dns_app_list_id: UUID) -> None:
        self._insert_match(DNSAppListEntry(ref=dns_app_list_id))

    def match_dscp(self, dscp: List[int]) -> None:
        self._insert_match(DSCPEntry(value=dscp))

    def match_plp(self, plp: PLPEntryType) -> None:
        self._insert_match(PLPEntry(value=plp))

    def match_protocols(self, protocols: Set[int]) -> None:
        self._insert_match(ProtocolEntry.from_protocol_set(protocols))

    def match_saas_app_list(self, saas_app_list_id: UUID) -> None:
        self._insert_match(SaaSAppListEntry(ref=saas_app_list_id))

    def match_source_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(SourceDataPrefixListEntry(ref=[data_prefix_list_id]))

    def match_source_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(SourceIPEntry.from_ipv4_networks(networks))

    def match_source_ipv6(self, networks: List[IPv6Network]) -> None:
        self._insert_match(SourceIPv6Entry.from_ipv6_networks(networks))

    def match_source_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(SourcePortEntry.from_port_set_and_ranges(ports, port_ranges))

    def match_traffic_to(self, traffic_to: TrafficTargetType) -> None:
        self._insert_match(TrafficToEntry(value=traffic_to))

    def associate_backup_sla_preferred_color_action(self, tloc_colors: List[TLOCColor]) -> None:
        self._insert_action(BackupSlaPrefferedColorAction(parameter=tloc_colors))

    def associate_cloud_saas_action(self) -> None:
        self._insert_action(CloudSaaSAction())

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))

    def associate_log_action(self) -> None:
        self._insert_action(LogAction())

    @overload
    def associate_sla_class_action(
        self, sla_class: UUID, not_met_action: Optional[SlaNotMetAction] = None, *, preferred_color: List[TLOCColor]
    ) -> None:
        ...

    @overload
    def associate_sla_class_action(
        self, sla_class: UUID, not_met_action: Optional[SlaNotMetAction] = None, *, preferred_color_group: UUID
    ) -> None:
        ...

    def associate_sla_class_action(
        self,
        sla_class: UUID,
        not_met_action: Optional[SlaNotMetAction] = None,
        *,
        preferred_color: Optional[List[TLOCColor]] = None,
        preferred_color_group: Optional[UUID] = None,
    ) -> None:
        if preferred_color is not None:
            action = SlaClassAction.from_params(
                sla_class=sla_class, not_met_action=not_met_action, preferred_color=preferred_color
            )
        elif preferred_color_group is not None:
            action = SlaClassAction.from_params(
                sla_class=sla_class, not_met_action=not_met_action, preferred_color_group=preferred_color_group
            )
        else:
            action = SlaClassAction()
        self._insert_action(action)


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

    def set_default_action(self, sla_class: Optional[UUID]) -> None:
        self.default_action = AppRouteDefaultAction(ref=sla_class) if sla_class else None

    def add_sequence(
        self,
        name: str = "App Route",
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
