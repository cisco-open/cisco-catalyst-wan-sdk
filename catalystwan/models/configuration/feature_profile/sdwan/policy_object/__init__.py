# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .policy.app_probe import AppProbeMapItem, AppProbeParcel
from .policy.application_list import ApplicationFamilyListEntry, ApplicationListEntry, ApplicationListParcel
from .policy.as_path import AsPathParcel
from .policy.color_list import ColorEntry, ColorParcel
from .policy.data_prefix import DataPrefixEntry, DataPrefixParcel
from .policy.expanded_community_list import ExpandedCommunityParcel
from .policy.extended_community import ExtendedCommunityParcel
from .policy.fowarding_class import FowardingClassParcel, FowardingClassQueueEntry
from .policy.ipv6_data_prefix import IPv6DataPrefixEntry, IPv6DataPrefixParcel
from .policy.ipv6_prefix_list import IPv6PrefixListEntry, IPv6PrefixListParcel
from .policy.mirror import MirrorParcel
from .policy.policer import PolicerEntry, PolicerParcel
from .policy.prefered_group_color import Preference, PreferredColorGroupEntry, PreferredColorGroupParcel
from .policy.prefix_list import PrefixListEntry, PrefixListParcel
from .policy.sla_class import SLAClassListEntry, SLAClassParcel
from .policy.standard_community import StandardCommunityEntry, StandardCommunityParcel
from .policy.tloc_list import TlocEntry, TlocParcel
from .security.aip import AdvancedInspectionProfileParcel
from .security.amp import AdvancedMalwareProtectionParcel
from .security.application_list import (
    SecurityApplicationFamilyListEntry,
    SecurityApplicationListEntry,
    SecurityApplicationListParcel,
)
from .security.data_prefix import SecurityDataPrefixEntry, SecurityDataPrefixParcel
from .security.fqdn import FQDNDomainParcel, FQDNListEntry
from .security.geolocation_list import GeoLocationListEntry, GeoLocationListParcel
from .security.intrusion_prevention import IntrusionPreventionParcel
from .security.ips_signature import IPSSignatureListEntry, IPSSignatureParcel
from .security.local_domain import LocalDomainListEntry, LocalDomainParcel
from .security.protocol_list import ProtocolListEntry, ProtocolListParcel
from .security.security_port import SecurityPortListEntry, SecurityPortParcel
from .security.ssl_decryption import SslDecryptionParcel
from .security.ssl_decryption_profile import SslDecryptionProfileParcel
from .security.url import BaseURLListEntry, URLAllowParcel, URLBlockParcel, URLParcel
from .security.url_filtering import UrlFilteringParcel
from .security.zone import SecurityZoneListEntry, SecurityZoneListParcel

AnyPolicyObjectParcel = Annotated[
    Union[
        AdvancedInspectionProfileParcel,
        AdvancedMalwareProtectionParcel,
        ApplicationListParcel,
        AppProbeParcel,
        AsPathParcel,
        ColorParcel,
        DataPrefixParcel,
        ExpandedCommunityParcel,
        ExtendedCommunityParcel,
        FowardingClassParcel,
        FQDNDomainParcel,
        GeoLocationListParcel,
        IntrusionPreventionParcel,
        IPSSignatureParcel,
        IPv6DataPrefixParcel,
        IPv6PrefixListParcel,
        LocalDomainParcel,
        MirrorParcel,
        PolicerParcel,
        PreferredColorGroupParcel,
        PrefixListParcel,
        SLAClassParcel,
        TlocParcel,
        StandardCommunityParcel,
        LocalDomainParcel,
        FQDNDomainParcel,
        IPSSignatureParcel,
        SecurityPortParcel,
        ProtocolListParcel,
        GeoLocationListParcel,
        SecurityZoneListParcel,
        SecurityApplicationListParcel,
        SecurityDataPrefixParcel,
        SecurityPortParcel,
        SecurityZoneListParcel,
        SLAClassParcel,
        SslDecryptionParcel,
        SslDecryptionProfileParcel,
        StandardCommunityParcel,
        TlocParcel,
        URLParcel,
        UrlFilteringParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = (
    "AdvancedInspectionProfileParcel",
    "AdvancedMalwareProtectionParcel",
    "AnyPolicyObjectParcel",
    "ApplicationFamilyListEntry",
    "ApplicationListEntry",
    "ApplicationListParcel",
    "AppProbeEntry",
    "AppProbeMapItem",
    "AppProbeParcel",
    "AsPathParcel",
    "BaseURLListEntry",
    "ColorEntry",
    "ColorParcel",
    "DataPrefixEntry",
    "DataPrefixParcel",
    "ExpandedCommunityParcel",
    "ExtendedCommunityParcel",
    "FallbackBestTunnel",
    "FowardingClassParcel",
    "FowardingClassQueueEntry",
    "FQDNDomainParcel",
    "FQDNListEntry",
    "GeoLocationListEntry",
    "GeoLocationListParcel",
    "IntrusionPreventionParcel",
    "IPSSignatureListEntry",
    "IPSSignatureParcel",
    "IPv6DataPrefixEntry",
    "IPv6DataPrefixParcel",
    "IPv6PrefixListEntry",
    "IPv6PrefixListParcel",
    "LocalDomainListEntry",
    "LocalDomainParcel",
    "MirrorParcel",
    "PolicerEntry",
    "PolicerParcel",
    "Preference",
    "PreferredColorGroupEntry",
    "PreferredColorGroupParcel",
    "PrefixListEntry",
    "PrefixListParcel",
    "ProtocolListEntry",
    "ProtocolListParcel",
    "SecurityApplicationFamilyListEntry",
    "SecurityApplicationListEntry",
    "SecurityApplicationListParcel",
    "SecurityDataPrefixEntry",
    "SecurityDataPrefixParcel",
    "SecurityPortListEntry",
    "SecurityPortParcel",
    "SecurityZoneListEntry",
    "SecurityZoneListParcel",
    "SLAAppProbeClass",
    "SLAClassCriteria",
    "SLAClassListEntry",
    "SLAClassParcel",
    "SslDecryptionParcel",
    "SslDecryptionProfileParcel",
    "StandardCommunityEntry",
    "StandardCommunityParcel",
    "TlocEntry",
    "TlocParcel",
    "URLParcel",
    "URLAllowParcel",
    "URLBlockParcel",
)


def __dir__() -> "List[str]":
    return list(__all__)
