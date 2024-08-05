# Copyright 2023 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv4Address, IPv4Network, IPv6Network
from typing import List, Literal, Optional, Set, Tuple, Union, overload
from uuid import UUID

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import (
    AcceptDropActionType,
    DestinationRegion,
    DNSEntryType,
    EncapType,
    IcmpMsgType,
    SequenceIpType,
    ServiceChainNumber,
    ServiceType,
    TLOCColor,
    TrafficTargetType,
)
from catalystwan.models.policy.policy_definition import (
    ActionSet,
    AppListEntry,
    CFlowDAction,
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
    DNSTypeEntryType,
    DREOptimizationAction,
    DSCPEntry,
    FallBackToRoutingAction,
    ForwardingClassEntry,
    ICMPMessageEntry,
    LocalTLOCListEntry,
    LocalTLOCListEntryValue,
    LogAction,
    LossProtectionAction,
    LossProtectionFECAction,
    LossProtectionPacketDuplicationAction,
    LossProtectionType,
    Match,
    NATAction,
    NextHopActionEntry,
    NextHopLooseEntry,
    PacketLengthEntry,
    PLPEntry,
    PLPEntryType,
    PolicerListEntry,
    PolicyAcceptDropAction,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    PrefferedColorGroupListEntry,
    ProtocolEntry,
    RedirectDNSAction,
    SecureInternetGatewayAction,
    ServiceChainEntry,
    ServiceChainEntryValue,
    ServiceEntry,
    ServiceEntryValue,
    ServiceNodeGroupAction,
    SourceDataIPv6PrefixListEntry,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourceIPv6Entry,
    SourcePortEntry,
    TCPEntry,
    TCPOptimizationAction,
    TLOCEntry,
    TLOCEntryValue,
    TLOCListEntry,
    TrafficToEntry,
    VPNEntry,
    accept_action,
)

TrafficDataPolicySequenceEntry = Annotated[
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
        ICMPMessageEntry,
        PacketLengthEntry,
        PLPEntry,
        ProtocolEntry,
        SourceDataIPv6PrefixListEntry,
        SourceDataPrefixListEntry,
        SourceIPEntry,
        SourceIPv6Entry,
        SourcePortEntry,
        TCPEntry,
        TrafficToEntry,
    ],
    Field(discriminator="field"),
]

TrafficDataPolicySequenceActionEntry = Annotated[
    Union[
        ActionSet,
        CFlowDAction,
        CountAction,
        DREOptimizationAction,
        FallBackToRoutingAction,
        LogAction,
        LossProtectionAction,
        LossProtectionFECAction,
        LossProtectionPacketDuplicationAction,
        NATAction,
        RedirectDNSAction,
        SecureInternetGatewayAction,
        ServiceNodeGroupAction,
        TCPOptimizationAction,
    ],
    Field(discriminator="type"),
]


class TrafficDataPolicyHeader(PolicyDefinitionBase):
    type: Literal["data"] = "data"


class TrafficDataPolicySequenceMatch(Match):
    entries: List[TrafficDataPolicySequenceEntry] = []


class TrafficDataPolicySequence(PolicyDefinitionSequenceBase):
    sequence_type: Literal["applicationFirewall", "qos", "serviceChaining", "trafficEngineering", "data"] = Field(
        default="data", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: AcceptDropActionType = Field(serialization_alias="baseAction", validation_alias="baseAction")
    match: TrafficDataPolicySequenceMatch = TrafficDataPolicySequenceMatch()
    actions: List[TrafficDataPolicySequenceActionEntry] = []
    model_config = ConfigDict(populate_by_name=True)

    def match_app_list(self, app_list_id: UUID) -> None:
        self._insert_match(AppListEntry(ref=[app_list_id]))

    def match_dns_app_list(self, dns_app_list_id: UUID) -> None:
        self._insert_match(DNSAppListEntry(ref=dns_app_list_id))

    def match_dns(self, dns: DNSEntryType) -> None:
        self._insert_match(DNSEntry(value=dns))

    def match_dscp(self, dscp: List[int]) -> None:
        self._insert_match(DSCPEntry(value=dscp))

    def match_icmp(self, icmp_message_types: List[IcmpMsgType]) -> None:
        self._insert_match(ICMPMessageEntry(value=icmp_message_types))

    def match_packet_length(self, packet_lengths: Tuple[int, int]) -> None:
        self._insert_match(PacketLengthEntry.from_range(packet_lengths))

    def match_plp(self, plp: PLPEntryType) -> None:
        self._insert_match(PLPEntry(value=plp))

    def match_protocols(self, protocols: Set[int]) -> None:
        self._insert_match(ProtocolEntry.from_protocol_set(protocols))

    def match_source_data_prefix_list(self, data_prefix_list_id: UUID) -> None:
        self._insert_match(SourceDataPrefixListEntry(ref=[data_prefix_list_id]))

    def match_source_ip(self, networks: List[IPv4Network]) -> None:
        self._insert_match(SourceIPEntry.from_ipv4_networks(networks))

    def match_source_ipv6(self, networks: List[IPv6Network]) -> None:
        self._insert_match(SourceIPv6Entry.from_ipv6_networks(networks))

    def match_source_port(self, ports: Set[int] = set(), port_ranges: List[Tuple[int, int]] = []) -> None:
        self._insert_match(SourcePortEntry.from_port_set_and_ranges(ports, port_ranges))

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

    def match_tcp(self) -> None:
        self._insert_match(TCPEntry())

    def match_traffic_to(self, traffic_to: TrafficTargetType) -> None:
        self._insert_match(TrafficToEntry(value=traffic_to))

    def associate_count_action(self, counter_name: str) -> None:
        self._insert_action(CountAction(parameter=counter_name))

    def associate_log_action(self) -> None:
        self._insert_action(LogAction())

    @accept_action
    def associate_dscp_action(self, dscp: int) -> None:
        self._insert_action_in_set(DSCPEntry(value=[dscp]))

    @accept_action
    def associate_forwarding_class_action(self, fwclass: str) -> None:
        self._insert_action_in_set(ForwardingClassEntry(value=fwclass))

    @accept_action
    def associate_local_tloc_action(self, color: List[TLOCColor], encap: EncapType, restrict: bool = False) -> None:
        tloc_entry = LocalTLOCListEntry(
            value=LocalTLOCListEntryValue(
                color=color,
                encap=encap,
                restrict="" if restrict else None,
            )
        )
        self._insert_action_in_set(tloc_entry)

    @accept_action
    def associate_preffered_color_group(self, color_group_list_id: UUID, restrict: bool = False) -> None:
        self._insert_action_in_set(PrefferedColorGroupListEntry(ref=color_group_list_id, color_restrict=restrict))

    @accept_action
    def associate_cflowd_action(self) -> None:
        self._insert_action(CFlowDAction())

    @overload
    def associate_nat_action(self, *, nat_pool: int = 0) -> None:
        ...

    @overload
    def associate_nat_action(
        self,
        *,
        use_vpn: int = 0,
        fallback: bool = False,
        bypass: bool = False,
        dia_pool: List[int] = [],
        dia_interface: List[str] = []
    ) -> None:
        ...

    @accept_action
    def associate_nat_action(
        self,
        *,
        nat_pool: Optional[int] = None,
        use_vpn: int = 0,
        fallback: bool = False,
        bypass: bool = False,
        dia_pool: List[int] = [],
        dia_interface: List[str] = []
    ) -> None:
        if nat_pool:
            nat_action = NATAction.from_nat_pool(nat_pool=nat_pool)
        else:
            nat_action = NATAction.from_nat_vpn(
                use_vpn=use_vpn, fallback=fallback, bypass=bypass, dia_pool=dia_pool, dia_interface=dia_interface
            )
        self._insert_action(nat_action)

    @accept_action
    def associate_next_hop_action(self, next_hop: IPv4Address, loose: bool = False) -> None:
        self._insert_action_in_set(NextHopActionEntry(value=next_hop))
        self._insert_action_in_set(NextHopLooseEntry(value=loose))

    @accept_action
    def associate_policer_list_action(self, policer_list_id: UUID) -> None:
        self._insert_action_in_set(PolicerListEntry(ref=policer_list_id))

    @overload
    def associate_redirect_dns_action(self, *, ip: IPv4Address) -> None:
        ...

    @overload
    def associate_redirect_dns_action(self, *, dns_type: DNSTypeEntryType = "host") -> None:
        ...

    @accept_action
    def associate_redirect_dns_action(self, *, ip=None, dns_type=None) -> None:
        if ip:
            redirect_dns_action = RedirectDNSAction.from_ip_address(ip)
        else:
            redirect_dns_action = RedirectDNSAction.from_dns_type(dns_type)
        self._insert_action(redirect_dns_action)

    @accept_action
    def associate_local_service_chain_action(
        self, sc_type: ServiceChainNumber, vpn: int, restrict: bool = False
    ) -> None:
        self._insert_action_in_set(
            ServiceChainEntry(
                value=ServiceChainEntryValue(
                    type=sc_type,
                    vpn=str(vpn),
                    restrict="" if restrict else None,
                    local="",
                )
            )
        )

    @accept_action
    def associate_remote_service_chain_action(
        self,
        sc_type: ServiceChainNumber,
        vpn: int,
        ip: IPv4Address,
        color: TLOCColor,
        encap: EncapType,
        restrict: bool = False,
    ) -> None:
        self._insert_action_in_set(
            ServiceChainEntry(
                value=ServiceChainEntryValue(
                    type=sc_type,
                    vpn=str(vpn),
                    restrict="" if restrict else None,
                    tloc=TLOCEntryValue(
                        ip=ip,
                        color=color,
                        encap=encap,
                    ),
                )
            )
        )

    @accept_action
    def associate_app_qoe_optimization_action(
        self, tcp: bool = False, dre: bool = False, service_node_group: Optional[str] = None
    ) -> None:
        if tcp:
            self._insert_action(TCPOptimizationAction())
        else:
            self._remove_action(TCPOptimizationAction().type)
        if dre:
            self._insert_action(DREOptimizationAction())
        else:
            self._remove_action(DREOptimizationAction().type)
        if service_node_group is not None:
            self._insert_action(ServiceNodeGroupAction(parameter=service_node_group))
        else:
            self._remove_action(ServiceNodeGroupAction().type)

    @accept_action
    def associate_loss_correction_fec_action(self, adaptive: bool = False, threshold: Optional[int] = None) -> None:
        self._remove_action(LossProtectionPacketDuplicationAction().type)
        fec_type: LossProtectionType = "fecAdaptive" if adaptive else "fecAlways"
        fec_value = str(threshold) if adaptive and threshold is not None else None
        self._insert_action(LossProtectionAction(parameter=fec_type))
        self._insert_action(LossProtectionFECAction(parameter=fec_type, value=fec_value))

    @accept_action
    def associate_loss_correction_packet_duplication_action(self) -> None:
        self._remove_action(LossProtectionFECAction().type)
        self._insert_action(LossProtectionAction(parameter="packetDuplication"))
        self._insert_action(LossProtectionPacketDuplicationAction())

    @accept_action
    def associate_vpn_action(self, vpn: int) -> None:
        # TLOC or Next Hop is mandatory when configuring VPN. Please populate Action > TLOC or Action > Next Hop
        self._insert_action_in_set(VPNEntry(value=str(vpn)))

    @overload
    def associate_tloc_action(self, *, tloc_list_id: UUID) -> None:
        ...

    @overload
    def associate_tloc_action(self, *, ip: IPv4Address, color: TLOCColor, encap: EncapType) -> None:
        ...

    @accept_action
    def associate_tloc_action(self, *, tloc_list_id=None, ip=None, color=None, encap=None) -> None:
        # VPN is mandatory when configuring TLOC. Please populate Action > VPN.
        if tloc_list_id is not None:
            self._insert_action_in_set(TLOCListEntry(ref=tloc_list_id))
        else:
            self._insert_action_in_set(
                TLOCEntry(
                    value=TLOCEntryValue(
                        ip=ip,
                        color=color,
                        encap=encap,
                    )
                )
            )

    @accept_action
    def associate_secure_internet_gateway_action(self, fallback_to_routing: bool = False) -> None:
        # Secure Internet Gateway cannot be enabled with NAT Pool or NAT VPN or Next Hop.
        self._insert_action(SecureInternetGatewayAction())
        if fallback_to_routing:
            self._insert_action(FallBackToRoutingAction())
        else:
            self._remove_action(FallBackToRoutingAction().type)

    @overload
    def associate_service_action(
        self,
        service_type: ServiceType,
        vpn: Optional[int] = None,
        *,
        tloc_list_id: UUID,
        local: bool = False,
        restrict: bool = False
    ) -> None:
        ...

    @overload
    def associate_service_action(
        self,
        service_type: ServiceType,
        vpn: int,
        *,
        ip: IPv4Address,
        color: TLOCColor,
        encap: EncapType,
        local: bool = False,
        restrict: bool = False
    ) -> None:
        ...

    @accept_action
    def associate_service_action(
        self,
        service_type=None,
        vpn=None,
        *,
        tloc_list_id=None,
        ip=None,
        color=None,
        encap=None,
        local=None,
        restrict=None
    ) -> None:
        if tloc_list_id is None:
            tloc_entry = TLOCEntryValue(ip=ip, color=color, encap=encap)
            tloc_list_entry = None
        else:
            tloc_entry = None
            tloc_list_entry = TLOCListEntry(ref=tloc_list_id)
        _local = "" if local else None
        _restrict = "" if restrict else None
        service_value = ServiceEntryValue(
            type=service_type, vpn=vpn, tloc=tloc_entry, tloc_list=tloc_list_entry, local=_local, restrict=_restrict
        )
        self._insert_action_in_set(ServiceEntry(value=service_value))


class TrafficDataPolicy(TrafficDataPolicyHeader, DefinitionWithSequencesCommonBase):
    sequences: List[TrafficDataPolicySequence] = []
    default_action: PolicyAcceptDropAction = Field(
        default=PolicyAcceptDropAction(type="drop"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )
    model_config = ConfigDict(populate_by_name=True)

    def add_sequence(
        self,
        name: str = "Custom",
        base_action: AcceptDropActionType = "drop",
        sequence_ip_type: SequenceIpType = "ipv4",
    ) -> TrafficDataPolicySequence:
        seq = TrafficDataPolicySequence(
            sequence_name=name,
            base_action=base_action,
            sequence_ip_type=sequence_ip_type,
        )
        self.add(seq)
        return seq


class TrafficDataPolicyEditPayload(TrafficDataPolicy, PolicyDefinitionId):
    pass


class TrafficDataPolicyGetResponse(TrafficDataPolicy, PolicyDefinitionGetResponse):
    pass
