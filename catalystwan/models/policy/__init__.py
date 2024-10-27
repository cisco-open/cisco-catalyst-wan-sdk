# Copyright 2024 Cisco Systems, Inc. and its affiliates

# This stub provide top-level "public" policy models to be used with PolicyAPI()
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.policy.definition.app_route import AppRoutePolicy, AppRoutePolicyGetResponse
from catalystwan.models.policy.definition.dial_peer import DialPeerPolicy, DialPeerPolicyGetResponse
from catalystwan.models.policy.definition.fxo_port import FxoPortPolicy, FxoPortPolicyGetResponse
from catalystwan.models.policy.definition.fxs_did_port import FxsDidPortPolicy, FxsDidPortPolicyGetResponse
from catalystwan.models.policy.definition.fxs_port import FxsPortPolicy, FxsPortPolicyGetResponse
from catalystwan.models.policy.definition.pri_isdn_port import PriIsdnPortPolicy, PriIsdnPortPolicyGetResponse
from catalystwan.models.policy.definition.srst_phone_profile import (
    SrstPhoneProfilePolicy,
    SrstPhoneProfilePolicyGetResponse,
)
from catalystwan.models.policy.list.app import AppList, AppListInfo
from catalystwan.models.policy.list.app_probe import AppProbeClassList, AppProbeClassListInfo
from catalystwan.models.policy.list.as_path import ASPathList, ASPathListInfo
from catalystwan.models.policy.list.class_map import ClassMapList, ClassMapListInfo
from catalystwan.models.policy.list.color import ColorList, ColorListInfo
from catalystwan.models.policy.list.communities import (
    CommunityList,
    CommunityListInfo,
    ExpandedCommunityList,
    ExpandedCommunityListInfo,
    ExtendedCommunityList,
    ExtendedCommunityListInfo,
)
from catalystwan.models.policy.list.data_ipv6_prefix import DataIPv6PrefixList, DataIPv6PrefixListInfo
from catalystwan.models.policy.list.data_prefix import DataPrefixList, DataPrefixListInfo
from catalystwan.models.policy.list.fax_protocol import FaxProtocolList, FaxProtocolListInfo
from catalystwan.models.policy.list.fqdn import FQDNList, FQDNListInfo
from catalystwan.models.policy.list.geo_location import GeoLocationList, GeoLocationListInfo
from catalystwan.models.policy.list.identity import IdentityList, IdentityListInfo
from catalystwan.models.policy.list.ips_signature import IPSSignatureList, IPSSignatureListInfo
from catalystwan.models.policy.list.ipv6_prefix import IPv6PrefixList, IPv6PrefixListInfo
from catalystwan.models.policy.list.local_app import LocalAppList, LocalAppListInfo
from catalystwan.models.policy.list.local_domain import LocalDomainList, LocalDomainListInfo
from catalystwan.models.policy.list.media_profile import MediaProfileList, MediaProfileListInfo
from catalystwan.models.policy.list.mirror import MirrorList, MirrorListInfo
from catalystwan.models.policy.list.modem_pass_through import ModemPassThroughList, ModemPassThroughListInfo
from catalystwan.models.policy.list.policer import PolicerList, PolicerListInfo
from catalystwan.models.policy.list.port import PortList, PortListInfo
from catalystwan.models.policy.list.preferred_color_group import PreferredColorGroupList, PreferredColorGroupListInfo
from catalystwan.models.policy.list.prefix import PrefixList, PrefixListInfo
from catalystwan.models.policy.list.protocol_name import ProtocolNameList, ProtocolNameListInfo
from catalystwan.models.policy.list.region import RegionList, RegionListInfo
from catalystwan.models.policy.list.scalable_group_tag import ScalableGroupTagList, ScalableGroupTagListInfo
from catalystwan.models.policy.list.site import SiteList, SiteListInfo
from catalystwan.models.policy.list.sla import SLAClassList, SLAClassListInfo
from catalystwan.models.policy.list.supervisory_disconnect import (
    SupervisoryDisconnectList,
    SupervisoryDisconnectListInfo,
)
from catalystwan.models.policy.list.threat_grid_api_key import ThreatGridApiKeyList, ThreatGridApiKeyListInfo
from catalystwan.models.policy.list.tloc import TLOCList, TLOCListInfo
from catalystwan.models.policy.list.translation_profile import TranslationProfileList, TranslationProfileListInfo
from catalystwan.models.policy.list.translation_rules import TranslationRulesList, TranslationRulesListInfo
from catalystwan.models.policy.list.trunkgroup import TrunkGroupList, TrunkGroupListInfo
from catalystwan.models.policy.list.umbrella_data import UmbrellaDataList, UmbrellaDataListInfo
from catalystwan.models.policy.list.url import URLAllowList, URLAllowListInfo, URLBlockList, URLBlockListInfo
from catalystwan.models.policy.list.vpn import VPNList, VPNListInfo
from catalystwan.models.policy.list.zone import ZoneList, ZoneListInfo

from .centralized import CentralizedPolicy, TrafficDataDirection
from .definition.access_control_list import AclPolicy, AclPolicyGetResponse
from .definition.access_control_list_ipv6 import AclIPv6Policy, AclIPv6PolicyGetResponse
from .definition.aip import AdvancedInspectionProfilePolicy, AdvancedInspectionProfilePolicyGetResponse
from .definition.amp import AdvancedMalwareProtectionPolicy, AdvancedMalwareProtectionPolicyGetResponse
from .definition.cflowd import CflowdPolicy, CflowdPolicyGetResponse
from .definition.control import ControlPolicy, ControlPolicyGetResponse
from .definition.device_access import DeviceAccessPolicy, DeviceAccessPolicyGetResponse
from .definition.device_access_ipv6 import DeviceAccessIPv6Policy, DeviceAccessIPv6PolicyGetResponse
from .definition.dns_security import DnsSecurityPolicy, DnsSecurityPolicyGetResponse
from .definition.hub_and_spoke import HubAndSpokePolicy, HubAndSpokePolicyGetResponse
from .definition.intrusion_prevention import IntrusionPreventionPolicy, IntrusionPreventionPolicyGetResponse
from .definition.mesh import MeshPolicy, MeshPolicyGetResponse
from .definition.qos_map import QoSDropType, QoSMapPolicy, QoSMapPolicyGetResponse
from .definition.rewrite import RewritePolicy, RewritePolicyGetResponse
from .definition.route_policy import RoutePolicy, RoutePolicyGetResponse
from .definition.rule_set import RuleSet, RuleSetGetResponse
from .definition.security_group import SecurityGroup, SecurityGroupGetResponse
from .definition.ssl_decryption import SslDecryptionPolicy, SslDecryptionPolicyGetResponse
from .definition.ssl_decryption_utd_profile import (
    SslDecryptionUtdProfilePolicy,
    SslDecryptionUtdProfilePolicyGetResponse,
)
from .definition.traffic_data import TrafficDataPolicy, TrafficDataPolicyGetResponse
from .definition.url_filtering import UrlFilteringPolicy, UrlFilteringPolicyGetResponse
from .definition.vpn_membership import VPNMembershipPolicy, VPNMembershipPolicyGetResponse
from .definition.zone_based_firewall import ZoneBasedFWPolicy, ZoneBasedFWPolicyGetResponse
from .localized import LocalizedPolicy
from .policy_definition import (
    CarrierType,
    ControlPathType,
    DNSTypeEntryType,
    MultiRegionRole,
    OriginProtocol,
    PLPEntryType,
    ServiceType,
    TLOCActionType,
)
from .security import SecurityPolicy, UnifiedSecurityPolicy

AnyPolicyDefinition = Annotated[
    Union[
        AclIPv6Policy,
        AclPolicy,
        AdvancedInspectionProfilePolicy,
        AdvancedMalwareProtectionPolicy,
        AppRoutePolicy,
        CflowdPolicy,
        ControlPolicy,
        DeviceAccessIPv6Policy,
        DeviceAccessPolicy,
        DialPeerPolicy,
        DnsSecurityPolicy,
        FxoPortPolicy,
        FxsPortPolicy,
        FxsDidPortPolicy,
        HubAndSpokePolicy,
        IntrusionPreventionPolicy,
        MeshPolicy,
        PriIsdnPortPolicy,
        QoSMapPolicy,
        RewritePolicy,
        RoutePolicy,
        RuleSet,
        SecurityGroup,
        SslDecryptionPolicy,
        SslDecryptionUtdProfilePolicy,
        SrstPhoneProfilePolicy,
        TrafficDataPolicy,
        UrlFilteringPolicy,
        VPNMembershipPolicy,
        ZoneBasedFWPolicy,
    ],
    Field(discriminator="type"),
]

AnyPolicyList = Annotated[
    Union[
        AppList,
        AppProbeClassList,
        ASPathList,
        ClassMapList,
        ColorList,
        CommunityList,
        DataIPv6PrefixList,
        DataPrefixList,
        ExpandedCommunityList,
        ExtendedCommunityList,
        FaxProtocolList,
        FQDNList,
        GeoLocationList,
        IdentityList,
        IPSSignatureList,
        IPv6PrefixList,
        LocalAppList,
        LocalDomainList,
        MediaProfileList,
        MirrorList,
        ModemPassThroughList,
        PolicerList,
        PortList,
        PreferredColorGroupList,
        PrefixList,
        ProtocolNameList,
        RegionList,
        ScalableGroupTagList,
        SiteList,
        SLAClassList,
        SupervisoryDisconnectList,
        ThreatGridApiKeyList,
        TLOCList,
        TranslationProfileList,
        TranslationRulesList,
        TrunkGroupList,
        UmbrellaDataList,
        URLAllowList,
        URLBlockList,
        VPNList,
        ZoneList,
    ],
    Field(discriminator="type"),
]

AnyPolicyListInfo = Annotated[
    Union[
        AppListInfo,
        AppProbeClassListInfo,
        ASPathListInfo,
        ClassMapListInfo,
        ColorListInfo,
        CommunityListInfo,
        DataIPv6PrefixListInfo,
        DataPrefixListInfo,
        ExpandedCommunityListInfo,
        ExtendedCommunityListInfo,
        FaxProtocolListInfo,
        FQDNListInfo,
        GeoLocationListInfo,
        IdentityListInfo,
        IPSSignatureListInfo,
        IPv6PrefixListInfo,
        LocalAppListInfo,
        LocalDomainListInfo,
        MediaProfileListInfo,
        MirrorListInfo,
        ModemPassThroughListInfo,
        PolicerListInfo,
        PortListInfo,
        PreferredColorGroupListInfo,
        PrefixListInfo,
        ProtocolNameListInfo,
        RegionListInfo,
        ScalableGroupTagListInfo,
        SiteListInfo,
        SLAClassListInfo,
        SupervisoryDisconnectListInfo,
        ThreatGridApiKeyListInfo,
        TLOCListInfo,
        TranslationProfileListInfo,
        TranslationRulesListInfo,
        TrunkGroupListInfo,
        UmbrellaDataListInfo,
        URLAllowListInfo,
        URLBlockListInfo,
        VPNListInfo,
        ZoneListInfo,
    ],
    Field(discriminator="type"),
]

AnyPolicyDefinitionInfo = Annotated[
    Union[
        AclIPv6PolicyGetResponse,
        AclPolicyGetResponse,
        AdvancedInspectionProfilePolicyGetResponse,
        AdvancedMalwareProtectionPolicyGetResponse,
        AppRoutePolicyGetResponse,
        CflowdPolicyGetResponse,
        ControlPolicyGetResponse,
        DeviceAccessIPv6PolicyGetResponse,
        DeviceAccessPolicyGetResponse,
        DialPeerPolicyGetResponse,
        DnsSecurityPolicyGetResponse,
        FxoPortPolicyGetResponse,
        FxsPortPolicyGetResponse,
        FxsDidPortPolicyGetResponse,
        HubAndSpokePolicyGetResponse,
        IntrusionPreventionPolicyGetResponse,
        MeshPolicyGetResponse,
        PriIsdnPortPolicyGetResponse,
        QoSMapPolicyGetResponse,
        RewritePolicyGetResponse,
        RoutePolicyGetResponse,
        RuleSetGetResponse,
        SecurityGroupGetResponse,
        SslDecryptionPolicyGetResponse,
        SslDecryptionUtdProfilePolicyGetResponse,
        SrstPhoneProfilePolicyGetResponse,
        TrafficDataPolicyGetResponse,
        UrlFilteringPolicyGetResponse,
        VPNMembershipPolicyGetResponse,
        ZoneBasedFWPolicyGetResponse,
    ],
    Field(discriminator="type"),
]


__all__ = (
    "AclIPv6Policy",
    "AclPolicy",
    "AdvancedInspectionProfilePolicy",
    "AdvancedMalwareProtectionPolicy",
    "AnyPolicyDefinitionInfo",
    "AnyPolicyList",
    "AppList",
    "AppProbeClassList",
    "AppRoutePolicy",
    "ASPathList",
    "CarrierType",
    "CentralizedPolicy",
    "CflowdPolicy",
    "ClassMapList",
    "ColorList",
    "CommunityList",
    "ControlPathType",
    "ControlPolicy",
    "DataIPv6PrefixList",
    "DataPrefixList",
    "DeviceAccessIPv6Policy",
    "DeviceAccessPolicy",
    "DnsSecurityPolicy",
    "DNSTypeEntryType",
    "ExpandedCommunityList",
    "ExtendedCommunityList",
    "FQDNList",
    "GeoLocationList",
    "HubAndSpokePolicy",
    "IdentityList",
    "IntrusionPreventionPolicy",
    "IPSSignatureList",
    "IPv6PrefixList",
    "LocalAppList",
    "LocalDomainList",
    "LocalizedPolicy",
    "MeshPolicy",
    "MirrorList",
    "MultiRegionRole",
    "OriginProtocol",
    "PLPEntryType",
    "PolicerList",
    "PortList",
    "PreferredColorGroupList",
    "PrefixList",
    "ProtocolNameList",
    "QoSDropType",
    "QoSMapPolicy",
    "RegionList",
    "RewritePolicy",
    "RoutePolicy",
    "RuleSet",
    "ScalableGroupTagList",
    "SecurityGroup",
    "SecurityPolicy",
    "ServiceType",
    "SiteList",
    "SLAClassList",
    "SslDecryptionPolicy",
    "SslDecryptionUtdProfilePolicy",
    "ThreatGridApiKeyList",
    "TLOCActionType",
    "TLOCList",
    "TrafficDataDirection",
    "TrafficDataPolicy",
    "TrunkGroupList",
    "UmbrellaDataList",
    "UnifiedSecurityPolicy",
    "URLAllowList",
    "URLBlockList",
    "UrlFilteringPolicy",
    "VPNList",
    "VPNMembershipPolicy",
    "ZoneBasedFWPolicy",
    "ZoneList",
)


def __dir__() -> "List[str]":
    return list(__all__)
