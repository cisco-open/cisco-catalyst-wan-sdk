# Copyright 2024 Cisco Systems, Inc. and its affiliates
from logging import getLogger
from re import match
from typing import Any, Callable, Dict, List, Mapping, Type, TypeVar, cast
from uuid import UUID

from pydantic import ValidationError

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.endpoints.configuration_settings import CloudCredentials
from catalystwan.models.common import int_range_serializer, int_range_str_validator
from catalystwan.models.configuration.config_migration import ConvertResult, PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AnyPolicyObjectParcel,
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
    IdentityParcel,
    IPSSignatureParcel,
    IPv6DataPrefixParcel,
    IPv6PrefixListParcel,
    LocalDomainParcel,
    MirrorParcel,
    PolicerParcel,
    PreferredColorGroupParcel,
    PrefixListParcel,
    ProtocolListParcel,
    ScalableGroupTagParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    SLAClassParcel,
    StandardCommunityParcel,
    TlocParcel,
    URLAllowParcel,
    URLBlockParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.sla_class import SLAClassCriteria
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.application_list import (
    SecurityApplicationListParcel,
)
from catalystwan.models.policy import (
    AnyPolicyList,
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
    FQDNList,
    GeoLocationList,
    IPSSignatureList,
    IPv6PrefixList,
    LocalDomainList,
    MirrorList,
    PolicerList,
    PortList,
    PreferredColorGroupList,
    PrefixList,
    ProtocolNameList,
    SLAClassList,
    TLOCList,
    URLAllowList,
    URLBlockList,
    ZoneList,
)
from catalystwan.models.policy.list.identity import IdentityList
from catalystwan.models.policy.list.local_app import LocalAppList
from catalystwan.models.policy.list.region import RegionList, RegionListInfo
from catalystwan.models.policy.list.scalable_group_tag import ScalableGroupTagList
from catalystwan.models.policy.list.site import SiteList, SiteListInfo
from catalystwan.models.policy.list.threat_grid_api_key import ThreatGridApiKeyList
from catalystwan.models.policy.list.umbrella_data import UmbrellaDataList
from catalystwan.models.policy.list.vpn import VPNList, VPNListInfo
from catalystwan.models.settings import ThreatGridApi
from catalystwan.utils.config_migration.converters.utils import convert_interface_name

logger = getLogger(__name__)


def _get_parcel_name_desc(policy_list: AnyPolicyList) -> Dict[str, Any]:
    return dict(parcel_name=policy_list.name, parcel_description=policy_list.description)


def _get_sorted_unique_list(in_list: List[str]) -> List[str]:
    return sorted(list(set(in_list)))


def app_probe(in_: AppProbeClassList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[AppProbeParcel]:
    out = AppProbeParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.set_fowarding_class_name(entry.forwarding_class)
        for map in entry.map:
            out.add_map(map.color, map.dscp)
    return ConvertResult[AppProbeParcel](output=out, status="complete")


def app_list(in_: AppList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[ApplicationListParcel]:
    out = ApplicationListParcel(**_get_parcel_name_desc(in_))
    for app in _get_sorted_unique_list(in_.list_all_app()):
        out.add_application(app)
    for app_family in _get_sorted_unique_list(in_.list_all_app_family()):
        out.add_application_family(app_family)
    return ConvertResult[ApplicationListParcel](output=out, status="complete")


def as_path(in_: ASPathList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[AsPathParcel]:
    """There is a mismatch between UX1 and UX2 models:
    UX1:
    - AS Path List Name (Alphanumeric value for vEdge, or number from 1 to 500 for ISR Edge router)
    - AS Path list

    UX2:
    - Parcel name
    - Parcel description
    - AS Path List ID (Number from 1 to 500)
    - AS Path list

    The UX1 and UX2 intersection in AS Path list name and ID but only for the ISR Edge router (number 1 to 500).
    If there is number we can insert the value in as_path_list_num field otherwise we will
    generate the value and keep track of it in the context.
    """
    result = ConvertResult[AsPathParcel](output=None)
    if in_.name.isdigit():
        as_path_list_num = int(in_.name)
    else:
        as_path_list_num = context.generate_as_path_list_num_from_name(in_.name)
        result.update_status("partial", f"Mapped AS Path List Name: '{in_.name}' to ID: '{as_path_list_num}'")
    out = AsPathParcel(**_get_parcel_name_desc(in_), as_path_list_num=as_global(as_path_list_num))
    for entry in in_.entries:
        out.add_as_path(entry.as_path)
    result.output = out
    return result


def class_map(in_: ClassMapList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[FowardingClassParcel]:
    out = FowardingClassParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_queue(entry.queue)
    context.fwclass_id_by_name[in_.name] = uuid
    return ConvertResult[FowardingClassParcel](output=out, status="complete")


def color(in_: ColorList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[ColorParcel]:
    out = ColorParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_color(entry.color)
    return ConvertResult[ColorParcel](output=out, status="complete")


def community(in_: CommunityList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[StandardCommunityParcel]:
    out = StandardCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_community(entry.community)
    return ConvertResult[StandardCommunityParcel](output=out, status="complete")


def data_prefix_ipv6(
    in_: DataIPv6PrefixList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[IPv6DataPrefixParcel]:
    out = IPv6DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ipv6_prefix)
    return ConvertResult[IPv6DataPrefixParcel](output=out, status="complete")


def data_prefix(in_: DataPrefixList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[DataPrefixParcel]:
    out = DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_data_prefix(entry.ip_prefix)
    return ConvertResult[DataPrefixParcel](output=out, status="complete")


def expanded_community(
    in_: ExpandedCommunityList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[ExpandedCommunityParcel]:
    out = ExpandedCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_community(entry.community)
    return ConvertResult[ExpandedCommunityParcel](output=out, status="complete")


def extended_community(
    in_: ExtendedCommunityList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[ExtendedCommunityParcel]:
    out = ExtendedCommunityParcel(**_get_parcel_name_desc(in_))
    result = ConvertResult[ExtendedCommunityParcel](output=out, status="complete")

    # v2 models allow folowing entries:
    # soo ipv4_addr:port OR rt as_number:community_number
    #
    # v1 api allows to add str prefix before soo or rt ex. 'community rt 2:3'
    # if prefix is available it will be removed during thr conversion.
    entry_pattern = r"^.*(soo \d+\.\d+\.\d+\.\d+:\d+|rt \d+:\d+)$"

    for entry in in_.entries:
        if (pattern_match := match(entry_pattern, entry.community)) is None:
            result.status = "failed"
            result.info.append(
                f"Extended community entr: {entry.community} does not meet expected pattern: "
                "'soo ipv4:port OR rt int:int'"
            )
            return result

        out._add_community(pattern_match[1])

    return result


def fqdn(in_: FQDNList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[FQDNDomainParcel]:
    out = FQDNDomainParcel(**_get_parcel_name_desc(in_))
    out.from_fqdns([entry.pattern for entry in in_.entries])
    return ConvertResult[FQDNDomainParcel](output=out, status="complete")


def mirror(in_: MirrorList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[MirrorParcel]:
    result = ConvertResult[MirrorParcel](output=None)
    if len(in_.entries) == 0:
        result.status = "failed"
        result.info.append("Expected MirrorList has exactly one entry")
    elif len(in_.entries) >= 1:
        dst_ip = in_.entries[0].remote_dest
        src_ip = in_.entries[0].source
        result.output = MirrorParcel.create(remote_dest_ip=dst_ip, source_ip=src_ip, **_get_parcel_name_desc(in_))
        if len(in_.entries) > 1:
            result.status = "partial"
            result.info.append("Expected MirrorList has exactly one entry")
    return result


def geo_location(
    in_: GeoLocationList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[GeoLocationListParcel]:
    out = GeoLocationListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.country is not None:
            out.add_country(entry.country)
        if entry.continent is not None:
            out.add_continent(entry.continent)
    return ConvertResult[GeoLocationListParcel](output=out, status="complete")


def ips_signature(
    in_: IPSSignatureList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[IPSSignatureParcel]:
    out = IPSSignatureParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_signature(f"{entry.generator_id}:{entry.signature_id}")
    return ConvertResult[IPSSignatureParcel](output=out, status="complete")


def prefix_ipv6(in_: IPv6PrefixList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[IPv6PrefixListParcel]:
    out = IPv6PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(ipv6_network=entry.ipv6_prefix, ge=entry.ge, le=entry.le)
    return ConvertResult[IPv6PrefixListParcel](output=out, status="complete")


# TODO: def local_app(in_: LocalAppList):
def local_domain(in_: LocalDomainList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[LocalDomainParcel]:
    out = LocalDomainParcel(**_get_parcel_name_desc(in_))
    out.from_local_domains([entry.name_server for entry in in_.entries])
    return ConvertResult[LocalDomainParcel](output=out, status="complete")


# TODO: def mirror_list(in_: MirrorList):
def policer(in_: PolicerList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[PolicerParcel]:
    out = PolicerParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_entry(burst=entry.burst, exceed=entry.exceed, rate=entry.rate)
    return ConvertResult[PolicerParcel](output=out, status="complete")


def port(in_: PortList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[SecurityPortParcel]:
    out = SecurityPortParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_port(int_range_serializer(entry.port))
    return ConvertResult[SecurityPortParcel](output=out, status="complete")


def preferred_color_group(
    in_: PreferredColorGroupList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[PreferredColorGroupParcel]:
    out = PreferredColorGroupParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_primary(
            color_preference=list(entry.primary_preference.color_preference),
            path_preference=entry.primary_preference.path_preference,
        )
        if entry.secondary_preference is not None:
            out.add_secondary(
                color_preference=list(entry.secondary_preference.color_preference),
                path_preference=entry.secondary_preference.path_preference,
            )
        if entry.tertiary_preference is not None:
            out.add_tertiary(
                color_preference=list(entry.tertiary_preference.color_preference),
                path_preference=entry.tertiary_preference.path_preference,
            )
    return ConvertResult[PreferredColorGroupParcel](output=out, status="complete")


def prefix(in_: PrefixList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[PrefixListParcel]:
    out = PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ip_prefix)
    return ConvertResult[PrefixListParcel](output=out, status="complete")


def protocol(in_: ProtocolNameList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[ProtocolListParcel]:
    out = ProtocolListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_protocol(entry.protocol_name)
    return ConvertResult[ProtocolListParcel](output=out, status="complete")


def region(in_: RegionListInfo, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[None]:
    list_id = in_.list_id
    region_id_flatlist: List[int] = []
    context.regions_by_list_id[list_id] = []
    for entry in in_.entries:
        low, hi = entry.region_id
        if hi is None:
            region_id_flatlist.append(low)
        else:
            region_id_flatlist.extend(range(low, hi + 1))
    for name, num in context.region_map.items():
        if num in region_id_flatlist:
            context.regions_by_list_id[list_id].append(name)

    return ConvertResult[None](status="complete")


def site(in_: SiteListInfo, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[None]:
    list_id = in_.list_id
    site_id_flatlist: List[int] = []
    context.sites_by_list_id[list_id] = []
    for entry in in_.entries:
        low, hi = int_range_str_validator(entry.site_id, False)
        if hi is None:
            site_id_flatlist.append(low)
        else:
            site_id_flatlist.extend(range(low, hi + 1))
    for name, num in context.site_map.items():
        if num in site_id_flatlist:
            context.sites_by_list_id[list_id].append(name)

    return ConvertResult[None](status="complete")


def sla_class(in_: SLAClassList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[SLAClassParcel]:
    out = SLAClassParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        # TODO: modernize SLAClassList model (UX1)
        jitter = int(entry.jitter) if entry.jitter is not None else None
        latency = int(entry.latency) if entry.latency is not None else None
        loss = int(entry.loss) if entry.loss is not None else None
        out.add_entry(
            app_probe_class_id=entry.app_probe_class,
            loss=loss,
            jitter=jitter,
            latency=latency,
        )
        if entry.fallback_best_tunnel is not None:
            # TODO: modernize SLAClassList model (UX1)
            fallback = entry.fallback_best_tunnel
            criteria = cast(SLAClassCriteria, fallback.criteria)
            jitter = int(fallback.jitter_variance) if fallback.jitter_variance is not None else None
            latency = int(fallback.latency_variance) if fallback.latency_variance is not None else None
            loss = int(fallback.loss_variance) if fallback.loss_variance is not None else None

            out.add_fallback(
                criteria=criteria,
                jitter_variance=jitter,
                latency_variance=latency,
                loss_variance=loss,
            )
    return ConvertResult[SLAClassParcel](output=out, status="complete")


def tloc(in_: TLOCList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[TlocParcel]:
    out = TlocParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        _preference = str(entry.preference) if entry.preference is not None else None
        out.add_entry(tloc=entry.tloc, color=entry.color, encapsulation=entry.encap, preference=_preference)
    return ConvertResult[TlocParcel](output=out, status="complete")


def url_allow(in_: URLAllowList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[URLAllowParcel]:
    out = URLAllowParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return ConvertResult[URLAllowParcel](output=out, status="complete")


def url_block(in_: URLBlockList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[URLBlockParcel]:
    out = URLBlockParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return ConvertResult[URLBlockParcel](output=out, status="complete")


def vpn(in_: VPNListInfo, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[None]:
    list_id = in_.list_id
    vpn_id_flatlist: List[int] = []
    context.lan_vpns_by_list_id[list_id] = []
    for entry in in_.entries:
        low, hi = entry.vpn
        if hi is None:
            vpn_id_flatlist.append(low)
        else:
            vpn_id_flatlist.extend(range(low, hi + 1))
    for name, num in context.lan_vpn_map.items():
        if num in vpn_id_flatlist:
            context.lan_vpns_by_list_id[list_id].append(name)

    return ConvertResult[None](status="complete")


def zone(in_: ZoneList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[SecurityZoneListParcel]:
    out = SecurityZoneListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.interface is not None:
            out.add_interface(convert_interface_name(entry.interface))
        if entry.vpn is not None:
            out.add_vpn(int_range_serializer(entry.vpn))
    return ConvertResult[SecurityZoneListParcel](output=out, status="complete")


def local_app_list(
    in_: LocalAppList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[SecurityApplicationListParcel]:
    out = SecurityApplicationListParcel(**_get_parcel_name_desc(in_))
    for app in _get_sorted_unique_list(in_.list_all_app()):
        out.add_application(app)
    for app_family in _get_sorted_unique_list(in_.list_all_app_family()):
        out.add_application_family(app_family)
    return ConvertResult[SecurityApplicationListParcel](output=out, status="complete")


def threat_grid_api(in_: ThreatGridApiKeyList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[None]:
    out = ThreatGridApi()
    for entry in in_.entries:
        out.set_region_api_key(region=entry.region, apikey=entry.api_key)
    context.threat_grid_api = out
    return ConvertResult[None](status="complete")


def scalable_group_tag(
    in_: ScalableGroupTagList, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[ScalableGroupTagParcel]:
    out = ScalableGroupTagParcel(**_get_parcel_name_desc(in_))
    for e in in_.entries:
        out.add_entry(sgt_name=e.stg_name, tag=e.tag)
    return ConvertResult[ScalableGroupTagParcel](output=out)


def identity_list(in_: IdentityList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[IdentityParcel]:
    out = IdentityParcel(**_get_parcel_name_desc(in_))
    for e in in_.entries:
        out.add_entry(
            user=e.user,
            user_group=e.user_group,
        )
    return ConvertResult[IdentityParcel](output=out)


def umbrella_data(in_: UmbrellaDataList, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[None]:
    out = CloudCredentials()
    if not len(in_.entries) == 1:
        return ConvertResult[None](status="failed", info=["Expected exactly one entry in Umbrella Data List"])
    entry = in_.entries[0]
    out.umbrella_org_id = entry.umb_org_id
    if entry.api_key and entry.secret:
        out.umbrella_sig_auth_key = entry.api_key
        out.umbrella_sig_auth_secret = entry.secret
    elif entry.api_key_v2 and entry.secret_v2:
        out.umbrella_sig_auth_key = entry.api_key_v2
        out.umbrella_sig_auth_secret = entry.secret_v2
    else:
        return ConvertResult[None](status="failed", info=["Expected API Key and Secret or API Key V2 and Secret V2"])
    context.cloud_credentials = out
    return ConvertResult[None]()


OPL = TypeVar("OPL", AnyPolicyObjectParcel, None)
Input = AnyPolicyList
Output = ConvertResult[OPL]


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AppList: app_list,
    AppProbeClassList: app_probe,
    ASPathList: as_path,
    ClassMapList: class_map,
    ColorList: color,
    CommunityList: community,
    DataIPv6PrefixList: data_prefix_ipv6,
    DataPrefixList: data_prefix,
    ExpandedCommunityList: expanded_community,
    ExtendedCommunityList: extended_community,
    FQDNList: fqdn,
    GeoLocationList: geo_location,
    IdentityList: identity_list,
    IPSSignatureList: ips_signature,
    IPv6PrefixList: prefix_ipv6,
    LocalAppList: local_app_list,
    LocalDomainList: local_domain,
    MirrorList: mirror,
    PolicerList: policer,
    PortList: port,
    UmbrellaDataList: umbrella_data,
    PreferredColorGroupList: preferred_color_group,
    PrefixList: prefix,
    ProtocolNameList: protocol,
    RegionList: region,
    ScalableGroupTagList: scalable_group_tag,
    SiteList: site,
    SLAClassList: sla_class,
    TLOCList: tloc,
    ThreatGridApiKeyList: threat_grid_api,
    URLAllowList: url_allow,
    URLBlockList: url_block,
    VPNList: vpn,
    ZoneList: zone,
}


def _not_supported(in_: Input, *args, **kwargs) -> ConvertResult[None]:
    logger.warning(f"Not Supported Conversion of Policy List: '{in_.type}' '{in_.name}'")
    return ConvertResult[None](status="unsupported")


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    return _not_supported


def convert(in_: Input, uuid: UUID, context: PolicyConvertContext) -> Output:
    result = Output(status="unsupported", output=None)
    try:
        result = _find_converter(in_)(in_, uuid, context)
        if result.output is not None:
            result.output.model_validate(result.output)
    except ValidationError as e:
        result.status = "failed"
        result.info.append(str(e))
    return result
