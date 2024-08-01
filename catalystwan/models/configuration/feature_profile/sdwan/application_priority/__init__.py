# Copyright 2024 Cisco Systems, Inc. and its affiliates


from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .policy_settings import Cflowd, PolicySettingsParcel
from .qos_policy import QosMap, QosPolicyParcel, QosPolicyTarget, QosSchedulers
from .traffic_policy import (
    Action,
    AppListMatch,
    AppqoeOptimization,
    AppqoeOptimizationAction,
    BackupSlaPreferredColorAction,
    CflowdAction,
    CloudProbeAction,
    CloudSaasAction,
    CountAction,
    DestinationDataIpv6PrefixListMatch,
    DestinationDataPrefixListMatch,
    DestinationIpMatch,
    DestinationIpv6Match,
    DestinationPortMatch,
    DestinationRegion,
    DestinationRegionMatch,
    DnsAppListMatch,
    DNSEntryType,
    DnsMatch,
    DNSTypeEntryType,
    DscpMatch,
    EncapType,
    Entry,
    FallbackToRoutingAction,
    Icmp6MessageMatch,
    IcmpMessageMatch,
    LocalTlocList,
    LogAction,
    LossCorrection,
    LossCorrectionAction,
    LossProtectionType,
    Match,
    Nat,
    NatAction,
    NatPoolAction,
    PacketLengthMatch,
    PreferredRemoteColor,
    ProtocolMatch,
    RedirectDns,
    RedirectDnsAction,
    SaasAppListMatch,
    SecureServiceEdgeInstance,
    Sequence,
    SequenceIpType,
    ServiceAreaMatch,
    ServiceAreaValue,
    ServiceChain,
    ServiceChainNumber,
    ServiceTloc,
    ServiceTlocList,
    ServiceType,
    Set,
    SetAction,
    SetDscp,
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
    SetTloc,
    SetTlocList,
    SetVpn,
    SigAction,
    SlaClass,
    SlaClassAction,
    SourceDataIpv6PrefixListMatch,
    SourceDataPrefixListMatch,
    SourceIpMatch,
    SourceIpv6Match,
    SourcePortMatch,
    Sse,
    SseAction,
    TcpMatch,
    Tloc,
    TLOCColor,
    TrafficCategory,
    TrafficCategoryMatch,
    TrafficClass,
    TrafficClassMatch,
    TrafficDataDirection,
    TrafficPolicyParcel,
    TrafficPolicyTarget,
    TrafficTargetType,
    TrafficToMatch,
)

AnyApplicationPriorityParcel = Annotated[
    Union[
        PolicySettingsParcel,
        QosPolicyParcel,
        TrafficPolicyParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = (
    "AnyApplicationPriorityParcel",
    "PolicySettingsParcel",
    "QosPolicyParcel",
    "TrafficPolicyTarget",
    "QosMap",
    "QosSchedulers",
    "QosPolicyTarget",
    "Cflowd",
    "TrafficPolicyParcel",
    "Sequence",
    "Action",
    "SseAction",
    "FallbackToRoutingAction",
    "SigAction",
    "NatAction",
    "NatPoolAction",
    "CflowdAction",
    "CloudProbeAction",
    "CloudSaasAction",
    "LogAction",
    "CountAction",
    "LossCorrectionAction",
    "AppqoeOptimizationAction",
    "RedirectDnsAction",
    "SetAction",
    "BackupSlaPreferredColorAction",
    "SlaClassAction",
    "Sse",
    "SecureServiceEdgeInstance",
    "Nat",
    "LossCorrection",
    "LossProtectionType",
    "AppqoeOptimization",
    "RedirectDns",
    "RedirectDnsValue",
    "DNSTypeEntryType",
    "Set",
    "ServiceChain",
    "ServiceChainNumber",
    "ServiceTlocList",
    "ServiceTloc",
    "ServiceType",
    "Tloc",
    "PreferredRemoteColor",
    "LocalTlocList",
    "EncapType",
    "SlaClass",
    "TLOCColor",
    "Match",
    "Entry",
    "DnsMatch",
    "TrafficToMatch",
    "DestinationRegionMatch",
    "TcpMatch",
    "DestinationPortMatch",
    "DestinationIpv6Match",
    "DestinationIpMatch",
    "DestinationDataIpv6PrefixListMatch",
    "DestinationDataPrefixListMatch",
    "SourcePortMatch",
    "SourceIpv6Match",
    "SourceIpMatch",
    "SourceDataIpv6PrefixListMatch",
    "SourceDataPrefixListMatch",
    "Icmp6MessageMatch",
    "IcmpMessageMatch",
    "ProtocolMatch",
    "PacketLengthMatch",
    "DscpMatch",
    "TrafficClassMatch",
    "DnsAppListMatch",
    "TrafficCategoryMatch",
    "ServiceAreaMatch",
    "SaasAppListMatch",
    "AppListMatch",
    "DNSEntryType",
    "TrafficTargetType",
    "DestinationRegion",
    "Icmp6MessageValue",
    "IcmpMsg",
    "TrafficClass",
    "TrafficCategory",
    "ServiceAreaValue",
    "SequenceIpType",
    "TrafficPolicyTarget",
    "TrafficDataDirection",
    "SetVpn",
    "SetTlocList",
    "SetDscp",
    "SetTloc",
    "SetForwardingClass",
    "SetLocalTlocList",
    "SetNextHop",
    "SetNextHopIpv6",
    "SetNextHopLoose",
    "SetPolicer",
    "SetPreferredColorGroup",
    "SetPreferredRemoteColor",
    "SetService",
    "SetServiceChain",
)


def __dir__() -> "List[str]":
    return list(__all__)