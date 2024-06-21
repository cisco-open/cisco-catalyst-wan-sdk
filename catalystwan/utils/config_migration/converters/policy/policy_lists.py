from logging import getLogger
from re import match
from typing import Any, Callable, Dict, List, Mapping, Type, TypeVar, cast

from pydantic import ValidationError

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
    IPSSignatureParcel,
    IPv6DataPrefixParcel,
    IPv6PrefixListParcel,
    LocalDomainParcel,
    MirrorParcel,
    PolicerParcel,
    PreferredColorGroupParcel,
    PrefixListParcel,
    ProtocolListParcel,
    SecurityPortParcel,
    SecurityZoneListParcel,
    SLAClassParcel,
    StandardCommunityParcel,
    TlocParcel,
    URLAllowParcel,
    URLBlockParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.sla_class import SLAClassCriteria
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
from catalystwan.models.policy.list.region import RegionList, RegionListInfo
from catalystwan.models.policy.list.site import SiteList, SiteListInfo
from catalystwan.models.policy.list.vpn import VPNList, VPNListInfo

logger = getLogger(__name__)


def _get_parcel_name_desc(policy_list: AnyPolicyList) -> Dict[str, Any]:
    return dict(parcel_name=policy_list.name, parcel_description=policy_list.description)


def app_probe(in_: AppProbeClassList, context) -> ConvertResult[AppProbeParcel]:
    out = AppProbeParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_fowarding_class(entry.forwarding_class)
    return ConvertResult[AppProbeParcel](output=out, status="complete")


def app_list(in_: AppList, context) -> ConvertResult[ApplicationListParcel]:
    out = ApplicationListParcel(**_get_parcel_name_desc(in_))
    for app in set(in_.list_all_app()):
        out.add_application(app)
    for app_family in set(in_.list_all_app_family()):
        out.add_application_family(app_family)
    return ConvertResult[ApplicationListParcel](output=out, status="complete")


def as_path(in_: ASPathList, context) -> ConvertResult[AsPathParcel]:
    out = AsPathParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_as_path(entry.as_path)
    return ConvertResult[AsPathParcel](output=out, status="complete")


def class_map(in_: ClassMapList, context) -> ConvertResult[FowardingClassParcel]:
    out = FowardingClassParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_queue(entry.queue)
    return ConvertResult[FowardingClassParcel](output=out, status="complete")


def color(in_: ColorList, context) -> ConvertResult[ColorParcel]:
    out = ColorParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_color(entry.color)
    return ConvertResult[ColorParcel](output=out, status="complete")


def community(in_: CommunityList, context) -> ConvertResult[StandardCommunityParcel]:
    out = StandardCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_community(entry.community)
    return ConvertResult[StandardCommunityParcel](output=out, status="complete")


def data_prefix_ipv6(in_: DataIPv6PrefixList, context) -> ConvertResult[IPv6DataPrefixParcel]:
    out = IPv6DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ipv6_prefix)
    return ConvertResult[IPv6DataPrefixParcel](output=out, status="complete")


def data_prefix(in_: DataPrefixList, context) -> ConvertResult[DataPrefixParcel]:
    out = DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_data_prefix(entry.ip_prefix)
    return ConvertResult[DataPrefixParcel](output=out, status="complete")


def expanded_community(in_: ExpandedCommunityList, context) -> ConvertResult[ExpandedCommunityParcel]:
    out = ExpandedCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_community(entry.community)
    return ConvertResult[ExpandedCommunityParcel](output=out, status="complete")


def extended_community(in_: ExtendedCommunityList, context) -> ConvertResult[ExtendedCommunityParcel]:
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


def fqdn(in_: FQDNList, context) -> ConvertResult[FQDNDomainParcel]:
    out = FQDNDomainParcel(**_get_parcel_name_desc(in_))
    out.from_fqdns([entry.pattern for entry in in_.entries])
    return ConvertResult[FQDNDomainParcel](output=out, status="complete")


def mirror(in_: MirrorList, context) -> ConvertResult[MirrorParcel]:
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


def geo_location(in_: GeoLocationList, context) -> ConvertResult[GeoLocationListParcel]:
    out = GeoLocationListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.country is not None:
            out.add_country(entry.country)
        if entry.continent is not None:
            out.add_continent(entry.continent)
    return ConvertResult[GeoLocationListParcel](output=out, status="complete")


def ips_signature(in_: IPSSignatureList, context) -> ConvertResult[IPSSignatureParcel]:
    out = IPSSignatureParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_signature(f"{entry.generator_id}:{entry.signature_id}")
    return ConvertResult[IPSSignatureParcel](output=out, status="complete")


def prefix_ipv6(in_: IPv6PrefixList, context) -> ConvertResult[IPv6PrefixListParcel]:
    out = IPv6PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(ipv6_network=entry.ipv6_prefix, ge=entry.ge, le=entry.le)
    return ConvertResult[IPv6PrefixListParcel](output=out, status="complete")


# TODO: def local_app(in_: LocalAppList):
def local_domain(in_: LocalDomainList, context) -> ConvertResult[LocalDomainParcel]:
    out = LocalDomainParcel(**_get_parcel_name_desc(in_))
    out.from_local_domains([entry.name_server for entry in in_.entries])
    return ConvertResult[LocalDomainParcel](output=out, status="complete")


# TODO: def mirror_list(in_: MirrorList):
def policer(in_: PolicerList, context) -> ConvertResult[PolicerParcel]:
    out = PolicerParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_entry(burst=entry.burst, exceed=entry.exceed, rate=entry.rate)
    return ConvertResult[PolicerParcel](output=out, status="complete")


def port(in_: PortList, context) -> ConvertResult[SecurityPortParcel]:
    out = SecurityPortParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_port(int_range_serializer(entry.port))
    return ConvertResult[SecurityPortParcel](output=out, status="complete")


def preferred_color_group(in_: PreferredColorGroupList, context) -> ConvertResult[PreferredColorGroupParcel]:
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


def prefix(in_: PrefixList, context) -> ConvertResult[PrefixListParcel]:
    out = PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ip_prefix)
    return ConvertResult[PrefixListParcel](output=out, status="complete")


def protocol(in_: ProtocolNameList, context) -> ConvertResult[ProtocolListParcel]:
    out = ProtocolListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_protocol(entry.protocol_name)
    return ConvertResult[ProtocolListParcel](output=out, status="complete")


def region(in_: RegionListInfo, context: PolicyConvertContext) -> ConvertResult[None]:
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


def site(in_: SiteListInfo, context: PolicyConvertContext) -> ConvertResult[None]:
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


def sla_class(in_: SLAClassList, context) -> ConvertResult[SLAClassParcel]:
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


def tloc(in_: TLOCList, context) -> ConvertResult[TlocParcel]:
    out = TlocParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        _preference = str(entry.preference) if entry.preference is not None else None
        out.add_entry(tloc=entry.tloc, color=entry.color, encapsulation=entry.encap, preference=_preference)
    return ConvertResult[TlocParcel](output=out, status="complete")


def url_allow(in_: URLAllowList, context) -> ConvertResult[URLAllowParcel]:
    out = URLAllowParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return ConvertResult[URLAllowParcel](output=out, status="complete")


def url_block(in_: URLBlockList, context) -> ConvertResult[URLBlockParcel]:
    out = URLBlockParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return ConvertResult[URLBlockParcel](output=out, status="complete")


def vpn(in_: VPNListInfo, context: PolicyConvertContext) -> ConvertResult[None]:
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


def zone(in_: ZoneList, context) -> ConvertResult[SecurityZoneListParcel]:
    out = SecurityZoneListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.interface is not None:
            out.add_interface(entry.interface)
        if entry.vpn is not None:
            out.add_vpn(int_range_serializer(entry.vpn))
    return ConvertResult[SecurityZoneListParcel](output=out, status="complete")


OPL = TypeVar("OPL", AnyPolicyObjectParcel, None)
Input = AnyPolicyList
Output = ConvertResult[OPL]


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AppProbeClassList: app_probe,
    AppList: app_list,
    #  ASPathList: as_path,
    ClassMapList: class_map,
    ColorList: color,
    CommunityList: community,
    DataIPv6PrefixList: data_prefix_ipv6,
    DataPrefixList: data_prefix,
    ExpandedCommunityList: expanded_community,
    FQDNList: fqdn,
    GeoLocationList: geo_location,
    IPSSignatureList: ips_signature,
    IPv6PrefixList: prefix_ipv6,
    LocalDomainList: local_domain,
    PolicerList: policer,
    PortList: port,
    PreferredColorGroupList: preferred_color_group,
    PrefixList: prefix,
    ProtocolNameList: protocol,
    RegionList: region,
    SiteList: site,
    SLAClassList: sla_class,
    TLOCList: tloc,
    URLAllowList: url_allow,
    URLBlockList: url_block,
    VPNList: vpn,
    ZoneList: zone,
    MirrorList: mirror,
    ExtendedCommunityList: extended_community,
}


def _not_supported(in_: Input, *args, **kwargs) -> ConvertResult[None]:
    logger.warning(f"Not Supported Conversion of Policy List: '{in_.type}' '{in_.name}'")
    return ConvertResult[None](status="unsupported")


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    return _not_supported


def convert(in_: Input, context: PolicyConvertContext) -> Output:
    result = _find_converter(in_)(in_, context)
    if result.output is not None:
        try:
            result.output.model_validate(result.output)
        except ValidationError as e:
            result.status = "failed"
            result.info.append(str(e))
    return result
