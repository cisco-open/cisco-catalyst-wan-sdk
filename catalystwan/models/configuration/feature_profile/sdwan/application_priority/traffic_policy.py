# Copyright 2024 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Address, IPv4Network, IPv6Address
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import EncapType, SequenceIpType, ServiceChainNumber, ServiceType, TLOCColor
from catalystwan.models.configuration.feature_profile.common import Icmp6Msg, IcmpMsg, RefIdItem
from catalystwan.models.policy.centralized import TrafficDataDirection
from catalystwan.models.policy.policy_definition import (
    DestinationRegion,
    DNSEntryType,
    DNSTypeEntryType,
    LossProtectionType,
    TrafficTargetType,
)

BaseAction = Literal[
    "accept",
    "drop",
]


class TrafficPolicyTarget(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    direction: Global[TrafficDataDirection]
    vpn: Global[List[str]]


ServiceAreaValue = Literal[
    "common",
    "exchange",
    "sharepoint",
    "skype",
]

TrafficCategory = Literal[
    "all",
    "optimize",
    "optimize-allow",
]

TrafficClass = Literal[
    "bronze",
    "gold-broadcast-video",
    "gold-bulk-data",
    "gold-multimedia-conferencing",
    "gold-multimedia-streaming",
    "gold-network-control",
    "gold-ops-admin-mgmt",
    "gold-real-time-interactive",
    "gold-signaling",
    "gold-transactional-data",
    "gold-voip-telephony",
    "silver",
]


class AppListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    app_list: RefIdItem = Field(default=None, validation_alias="appList", serialization_alias="appList")


class SaasAppListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    saas_app_list: RefIdItem = Field(default=None, validation_alias="saasAppList", serialization_alias="saasAppList")


class ServiceAreaMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    service_area: Global[List[ServiceAreaValue]] = Field(
        default=None, validation_alias="serviceArea", serialization_alias="serviceArea"
    )


class TrafficCategoryMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    traffic_category: Global[TrafficCategory] = Field(
        default=None, validation_alias="trafficCategory", serialization_alias="trafficCategory"
    )


class DnsAppListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    dns_app_list: RefIdItem = Field(default=None, validation_alias="dnsAppList", serialization_alias="dnsAppList")


class TrafficClassMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    traffic_class: Global[TrafficClass] = Field(
        default=None, validation_alias="trafficClass", serialization_alias="trafficClass"
    )


class DscpMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    dscp: Global[int] = Field(default=None, ge=0, le=63)


class PacketLengthMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    packet_length: Global[str] = Field(
        default=None, validation_alias="packetLength", serialization_alias="packetLength"
    )


class ProtocolMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    protocol: Global[List[str]] = Field(default=None)


class IcmpMessageMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    icmp_message: Global[List[IcmpMsg]] = Field(
        default=None, validation_alias="icmpMessage", serialization_alias="icmpMessage"
    )


class Icmp6MessageMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    icmp6_message: Global[List[Icmp6Msg]] = Field(
        default=None, validation_alias="icmp6Message", serialization_alias="icmp6Message"
    )


class SourceDataPrefixListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_data_prefix_list: RefIdItem = Field(
        default=None, validation_alias="sourceDataPrefixList", serialization_alias="sourceDataPrefixList"
    )


class SourceDataIpv6PrefixListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_data_ipv6_prefix_list: RefIdItem = Field(
        default=None, validation_alias="sourceDataIpv6PrefixList", serialization_alias="sourceDataIpv6PrefixList"
    )


class SourceIpMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_ip: Global[IPv4Network] = Field(default=None, validation_alias="sourceIp", serialization_alias="sourceIp")


class SourceIpv6Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_ipv6: Global[str] = Field(default=None, validation_alias="sourceIpv6", serialization_alias="sourceIpv6")


class SourcePortMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    source_port: Global[List[str]] = Field(
        default=None, validation_alias="sourcePort", serialization_alias="sourcePort"
    )


class DestinationDataPrefixListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_data_prefix_list: RefIdItem = Field(
        default=None, validation_alias="destinationDataPrefixList", serialization_alias="destinationDataPrefixList"
    )


class DestinationDataIpv6PrefixListMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_data_ipv6_prefix_list: RefIdItem = Field(
        default=None,
        validation_alias="destinationDataIpv6PrefixList",
        serialization_alias="destinationDataIpv6PrefixList",
    )


class DestinationIpMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_ip: Global[IPv4Network] = Field(
        default=None, validation_alias="destinationIp", serialization_alias="destinationIp"
    )


class DestinationIpv6Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_ipv6: Global[str] = Field(
        default=None, validation_alias="destinationIpv6", serialization_alias="destinationIpv6"
    )


class DestinationPortMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_port: Global[List[str]] = Field(
        default=None, validation_alias="destinationPort", serialization_alias="destinationPort"
    )


class TcpMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    tcp: Global[Literal["syn"]] = Field(default=Global[Literal["syn"]](value="syn"))


class DestinationRegionMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    destination_region: Global[DestinationRegion] = Field(
        default=None, validation_alias="destinationRegion", serialization_alias="destinationRegion"
    )


class TrafficToMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    traffic_to: Global[TrafficTargetType] = Field(
        default=None, validation_alias="trafficTo", serialization_alias="trafficTo"
    )


class DnsMatch(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    dns: Global[DNSEntryType] = Field(default=None)


Entries = Union[
    AppListMatch,
    SaasAppListMatch,
    ServiceAreaMatch,
    TrafficCategoryMatch,
    DnsAppListMatch,
    TrafficClassMatch,
    DscpMatch,
    PacketLengthMatch,
    ProtocolMatch,
    IcmpMessageMatch,
    Icmp6Msg,
    SourceDataPrefixListMatch,
    SourceDataIpv6PrefixListMatch,
    SourceIpMatch,
    SourceIpv6Match,
    SourcePortMatch,
    DestinationDataPrefixListMatch,
    DestinationDataIpv6PrefixListMatch,
    DestinationIpMatch,
    DestinationIpv6Match,
    DestinationPortMatch,
    TcpMatch,
    DestinationRegionMatch,
    TrafficToMatch,
    DnsMatch,
]


class Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    entries: List[Entries]


class SlaClass(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    fallback_to_best_path: Optional[Global[bool]] = Field(
        default=None, validation_alias="fallbackToBestPath", serialization_alias="fallbackToBestPath"
    )
    preferred_color: Optional[Global[List[TLOCColor]]] = Field(
        default=None, validation_alias="preferredColor", serialization_alias="preferredColor"
    )
    preferred_color_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="preferredColorGroup", serialization_alias="preferredColorGroup"
    )
    preferred_remote_color: Optional[Global[List[TLOCColor]]] = Field(
        default=None, validation_alias="preferredRemoteColor", serialization_alias="preferredRemoteColor"
    )
    remote_color_restrict: Optional[Global[bool]] = Field(
        default=None, validation_alias="remoteColorRestrict", serialization_alias="remoteColorRestrict"
    )
    sla_name: Optional[RefIdItem] = Field(default=None, validation_alias="slaName", serialization_alias="slaName")
    strict: Optional[Global[bool]] = Field(default=None)


class LocalTlocList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    color: Global[List[TLOCColor]] = Field(default=None)
    encap: Optional[Global[EncapType]] = Field(default=None)
    restrict: Optional[Global[Global[bool]]] = Field(default=None)


class PreferredRemoteColor(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    color: Global[List[TLOCColor]] = Field(default=None)
    remote_color_restrict: Optional[Global[Global[bool]]] = Field(
        default=None, validation_alias="remoteColorRestrict", serialization_alias="remoteColorRestrict"
    )


class Tloc(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    color: Global[List[TLOCColor]] = Field(default=None)
    encap: Global[EncapType] = Field(default=None)
    ip: Global[IPv4Address] = Field(default=None)


class ServiceTloc(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    tloc: Tloc = Field()
    type: Global[ServiceType] = Field(default=None)
    vpn: Global[int] = Field(default=None)


class ServiceTlocList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    type: Optional[Global[ServiceType]] = Field(default=None)
    vpn: Optional[Global[int]] = Field(default=None)


class ServiceChain(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    local: Global[bool] = Field(default=None)
    restrict: Global[bool] = Field(default=None)
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    type: Global[ServiceChainNumber] = Field(default=None)
    vpn: Optional[Global[int]] = Field(default=None)


class SetDscp(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    dscp: Optional[Global[int]] = Field(default=None)


class SetForwardingClass(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    forwarding_class: Optional[RefIdItem] = Field(
        default=None, validation_alias="forwardingClass", serialization_alias="forwardingClass"
    )


class SetLocalTlocList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    local_tloc_list: Optional[LocalTlocList] = Field(
        default=None, validation_alias="localTlocList", serialization_alias="localTlocList"
    )


class SetNextHop(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    next_hop: Optional[Global[IPv4Address]] = Field(
        default=None, validation_alias="nextHop", serialization_alias="nextHop"
    )


class SetNextHopIpv6(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    next_hop_ipv6: Optional[Global[IPv6Address]] = Field(
        default=None, validation_alias="nextHopIpv6", serialization_alias="nextHopIpv6"
    )


class SetNextHopLoose(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    next_hop_loose: Optional[Global[bool]] = Field(
        default=None, validation_alias="nextHopLoose", serialization_alias="nextHopLoose"
    )


class SetPolicer(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    policer: Optional[RefIdItem] = Field(default=None)


class SetPreferredColorGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    preferred_color_group: Optional[RefIdItem] = Field(
        default=None, validation_alias="preferredColorGroup", serialization_alias="preferredColorGroup"
    )


class SetPreferredRemoteColor(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    preferred_remote_color: Optional[PreferredRemoteColor] = Field(
        default=None, validation_alias="preferredRemoteColor", serialization_alias="preferredRemoteColor"
    )


class SetService(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    service: Optional[Union[ServiceTloc, ServiceTlocList]] = Field(default=None)


class SetServiceChain(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    service_chain: Optional[ServiceChain] = Field(
        default=None, validation_alias="serviceChain", serialization_alias="serviceChain"
    )


class SetTloc(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    tloc: Optional[Tloc] = Field(default=None)


class SetTlocList(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")


class SetVpn(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    vpn: Optional[Global[int]] = Field(default=None)


Set = Union[
    SetVpn,
    SetTlocList,
    SetDscp,
    SetTloc,
    SetForwardingClass,
    SetLocalTlocList,
    SetNextHop,
    SetNextHopIpv6,
    SetNextHopLoose,
    SetPolicer,
    SetPreferredColorGroup,
    SetPreferredRemoteColor,
    SetService,
    SetServiceChain,
]

RedirectDnsType = Literal[
    "dnsHost",
    "ipAddress",
]


class RedirectDns(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    field: Optional[Global[RedirectDnsType]] = Field(default=None)
    value: Optional[Global[Union[DNSTypeEntryType, str]]] = Field(default=None)


class AppqoeOptimization(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    dre_optimization: Optional[Global[bool]] = Field(
        default=None, validation_alias="dreOptimization", serialization_alias="dreOptimization"
    )
    service_node_group: Global[str] = Field(
        default=None, validation_alias="serviceNodeGroup", serialization_alias="serviceNodeGroup"
    )
    tcp_optimization: Optional[Global[bool]] = Field(
        default=None, validation_alias="tcpOptimization", serialization_alias="tcpOptimization"
    )

    @field_validator("service_node_group")
    @classmethod
    def check_service_node_group(cls, service_node_group: Global[str]):
        assert service_node_group.value.startswith("SNG-APPQOE")
        return service_node_group


class LossCorrection(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    loss_correct_fec: Optional[Global[int]] = Field(
        default=None, validation_alias="lossCorrectFec", serialization_alias="lossCorrectFec"
    )
    loss_correction_type: Global[LossProtectionType] = Field(
        default=None, validation_alias="lossCorrectionType", serialization_alias="lossCorrectionType"
    )


class Nat(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    bypass: Optional[Global[bool]] = Field(default=None)
    dia_interface: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="diaInterface", serialization_alias="diaInterface"
    )
    dia_pool: Optional[Global[List[int]]] = Field(
        default=None, validation_alias="diaPool", serialization_alias="diaPool"
    )
    fallback: Optional[Global[bool]] = Field(default=None)
    use_vpn: Global[bool] = Field(default=None, validation_alias="useVpn", serialization_alias="useVpn")


SecureServiceEdgeInstance = Literal[
    "Cisco-Secure-Access",
    "zScaler",
]


class Sse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    secure_service_edge: Global[Global[bool]] = Field(
        default=None, validation_alias="secureServiceEdge", serialization_alias="secureServiceEdge"
    )
    secure_service_edge_instance: Global[SecureServiceEdgeInstance] = Field(
        default=None, validation_alias="secureServiceEdgeInstance", serialization_alias="secureServiceEdgeInstance"
    )


class SlaClassAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    sla_class: Optional[List[SlaClass]] = Field(
        default=None, validation_alias="slaClass", serialization_alias="slaClass", description="slaClass"
    )


class BackupSlaPreferredColorAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    backup_sla_preferred_color: Global[List[TLOCColor]] = Field(
        default=None, validation_alias="backupSlaPreferredColor", serialization_alias="backupSlaPreferredColor"
    )


class SetAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    set: List[Set] = Field(default=None)


class RedirectDnsAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    redirect_dns: RedirectDns = Field(default=None, validation_alias="redirectDns", serialization_alias="redirectDns")


class AppqoeOptimizationAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    appqoe_optimization: AppqoeOptimization = Field(
        default=None, validation_alias="appqoeOptimization", serialization_alias="appqoeOptimization"
    )


class LossCorrectionAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    loss_correction: LossCorrection = Field(
        default=None, validation_alias="lossCorrection", serialization_alias="lossCorrection"
    )


class CountAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    count: Global[str] = Field(default=None)


class LogAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    log: Global[bool] = Field(default=None)


class CloudSaasAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    cloud_saas: Global[bool] = Field(default=None, validation_alias="cloudSaas", serialization_alias="cloudSaas")


class CloudProbeAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    cloud_probe: Global[bool] = Field(default=None, validation_alias="cloudProbe", serialization_alias="cloudProbe")


class CflowdAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    cflowd: Global[bool] = Field(default=None)


class NatPoolAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    nat_pool: Global[int] = Field(default=None, validation_alias="natPool", serialization_alias="natPool")


class NatAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    nat: Nat = Field(default=None)


class SigAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    sig: Global[bool] = Field(default=None)


class FallbackToRoutingAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    fallback_to_routing: Global[bool] = Field(
        default=None, validation_alias="fallbackToRouting", serialization_alias="fallbackToRouting"
    )


class SseAction(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    sse: Sse = Field(default=None)


Actions = Union[
    SlaClassAction,
    BackupSlaPreferredColorAction,
    SetAction,
    RedirectDnsAction,
    AppqoeOptimizationAction,
    LossCorrectionAction,
    CountAction,
    LogAction,
    CloudSaasAction,
    CloudProbeAction,
    CflowdAction,
    NatPoolAction,
    NatAction,
    SigAction,
    FallbackToRoutingAction,
    SseAction,
]


class Sequences(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    actions: Optional[List[Actions]] = Field(default=None)
    base_action: Optional[Global[BaseAction]] = Field(
        default=None, validation_alias="baseAction", serialization_alias="baseAction"
    )
    match: Optional[Match] = Field(default=None)
    sequence_id: Optional[Global[int]] = Field(
        default=None, validation_alias="sequenceId", serialization_alias="sequenceId"
    )
    sequence_ip_type: Global[SequenceIpType] = Field(
        default=None, validation_alias="sequenceIpType", serialization_alias="sequenceIpType"
    )
    sequence_name: Optional[Global[str]] = Field(
        default=None, validation_alias="sequenceName", serialization_alias="sequenceName"
    )


class TrafficPolicyParcel(_ParcelBase):
    type_: Literal["traffic-policy"] = Field(default="traffic-policy", exclude=True)
    data_default_action: Optional[Global[BaseAction]] = Field(
        default=None, validation_alias=AliasPath("data", "dataDefaultAction")
    )
    has_cor_via_sig: Optional[Global[bool]] = Field(default=None, validation_alias=AliasPath("data", "hasCorViaSig"))
    sequences: List[Sequences] = Field(default=[], validation_alias=AliasPath("data", "sequences"))
    simple_flow: Optional[Global[bool]] = Field(default=None, validation_alias=AliasPath("data", "simpleFlow"))
    target: TrafficPolicyTarget = Field(validation_alias=AliasPath("data", "target"))
