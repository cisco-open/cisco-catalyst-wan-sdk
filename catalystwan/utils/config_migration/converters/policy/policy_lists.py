from logging import getLogger
from re import match
from typing import Any, Callable, Dict, List, Mapping, Optional, Type, cast

from catalystwan.models.common import int_range_serializer, int_range_str_validator
from catalystwan.models.configuration.config_migration import PolicyConvertContext
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
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

logger = getLogger(__name__)


def _get_parcel_name_desc(policy_list: AnyPolicyList) -> Dict[str, Any]:
    return dict(parcel_name=policy_list.name, parcel_description=policy_list.description)


def app_probe(in_: AppProbeClassList, context) -> AppProbeParcel:
    out = AppProbeParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_fowarding_class(entry.forwarding_class)
    return out


def app_list(in_: AppList, context) -> ApplicationListParcel:
    out = ApplicationListParcel(**_get_parcel_name_desc(in_))
    for app in set(in_.list_all_app()):
        out.add_application(app)
    for app_family in set(in_.list_all_app_family()):
        out.add_application_family(app_family)
    return out


def as_path(in_: ASPathList, context) -> AsPathParcel:
    raise CatalystwanConverterCantConvertException(f"Additional context required for {ASPathList.__name__}")
    out = AsPathParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_as_path(entry.as_path)
    return out


def class_map(in_: ClassMapList, context) -> FowardingClassParcel:
    out = FowardingClassParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_queue(entry.queue)
    return out


def color(in_: ColorList, context) -> ColorParcel:
    out = ColorParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_color(entry.color)
    return out


def community(in_: CommunityList, context) -> StandardCommunityParcel:
    out = StandardCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_community(entry.community)
    return out


def data_prefix_ipv6(in_: DataIPv6PrefixList, context) -> IPv6DataPrefixParcel:
    out = IPv6DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ipv6_prefix)
    return out


def data_prefix(in_: DataPrefixList, context) -> DataPrefixParcel:
    out = DataPrefixParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_data_prefix(entry.ip_prefix)
    return out


def expanded_community(in_: ExpandedCommunityList, context) -> ExpandedCommunityParcel:
    out = ExpandedCommunityParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_community(entry.community)
    return out


def extended_community(in_: ExtendedCommunityList, context) -> ExtendedCommunityParcel:
    out = ExtendedCommunityParcel(**_get_parcel_name_desc(in_))

    # v2 models allow folowing entries:
    # soo ipv4_addr:port OR rt as_number:community_number
    #
    # v1 api allows to add str prefix before soo or rt ex. 'community rt 2:3'
    # if prefix is available it will be removed during thr conversion.
    entry_pattern = r"^.*(soo \d+\.\d+\.\d+\.\d+:\d+|rt \d+:\d+)$"

    for entry in in_.entries:
        if (pattern_match := match(entry_pattern, entry.community)) is None:
            raise CatalystwanConverterCantConvertException(
                f"Extended community entr: {entry.community} does not meet expected pattern: "
                "'soo ipv4:port OR rt int:int'"
            )

        out._add_community(pattern_match[1])

    return out


def fqdn(in_: FQDNList, context) -> FQDNDomainParcel:
    out = FQDNDomainParcel(**_get_parcel_name_desc(in_))
    out.from_fqdns([entry.pattern for entry in in_.entries])
    return out


def mirror(in_: MirrorList, context) -> MirrorParcel:
    if len(in_.entries) != 1:
        raise CatalystwanConverterCantConvertException("Mirror list shall contain exactly one entry.")

    dst_ip = in_.entries[0].remote_dest
    src_ip = in_.entries[0].source

    return MirrorParcel.create(remote_dest_ip=dst_ip, source_ip=src_ip, **_get_parcel_name_desc(in_))


def geo_location(in_: GeoLocationList, context) -> GeoLocationListParcel:
    out = GeoLocationListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.country is not None:
            out.add_country(entry.country)
        if entry.continent is not None:
            out.add_continent(entry.continent)
    return out


def ips_signature(in_: IPSSignatureList, context) -> IPSSignatureParcel:
    out = IPSSignatureParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_signature(f"{entry.generator_id}:{entry.signature_id}")
    return out


def prefix_ipv6(in_: IPv6PrefixList, context) -> IPv6PrefixListParcel:
    out = IPv6PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(ipv6_network=entry.ipv6_prefix, ge=entry.ge, le=entry.le)
    return out


# TODO: def local_app(in_: LocalAppList):
def local_domain(in_: LocalDomainList, context) -> LocalDomainParcel:
    out = LocalDomainParcel(**_get_parcel_name_desc(in_))
    out.from_local_domains([entry.name_server for entry in in_.entries])
    return out


# TODO: def mirror_list(in_: MirrorList):
def policer(in_: PolicerList, context) -> PolicerParcel:
    out = PolicerParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_entry(burst=entry.burst, exceed=entry.exceed, rate=entry.rate)
    return out


def port(in_: PortList, context) -> SecurityPortParcel:
    out = SecurityPortParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out._add_port(int_range_serializer(entry.port))
    return out


def preferred_color_group(in_: PreferredColorGroupList, context) -> PreferredColorGroupParcel:
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
    return out


def prefix(in_: PrefixList, context) -> PrefixListParcel:
    out = PrefixListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_prefix(entry.ip_prefix)
    return out


def protocol(in_: ProtocolNameList, context) -> ProtocolListParcel:
    out = ProtocolListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_protocol(entry.protocol_name)
    return out


def region(in_: RegionListInfo, context: PolicyConvertContext) -> None:
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


def site(in_: SiteListInfo, context: PolicyConvertContext) -> None:
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


def sla_class(in_: SLAClassList, context) -> SLAClassParcel:
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
    return out


def tloc(in_: TLOCList, context) -> TlocParcel:
    out = TlocParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        _preference = str(entry.preference) if entry.preference is not None else None
        out.add_entry(tloc=entry.tloc, color=entry.color, encapsulation=entry.encap, preference=_preference)
    return out


def url_allow(in_: URLAllowList, context) -> URLAllowParcel:
    out = URLAllowParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return out


def url_block(in_: URLBlockList, context) -> URLBlockParcel:
    out = URLBlockParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        out.add_url(entry.pattern)
    return out


def vpn(in_: VPNListInfo, context: PolicyConvertContext):
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


def zone(in_: ZoneList, context) -> SecurityZoneListParcel:
    out = SecurityZoneListParcel(**_get_parcel_name_desc(in_))
    for entry in in_.entries:
        if entry.interface is not None:
            out.add_interface(entry.interface)
        if entry.vpn is not None:
            out.add_vpn(int_range_serializer(entry.vpn))
    return out


Input = AnyPolicyList
Output = Optional[AnyPolicyObjectParcel]


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AppProbeClassList: app_probe,
    AppList: app_list,
    ASPathList: as_path,
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


def _not_supported(in_: Input, *args, **kwargs) -> None:
    logger.warning(f"Not Supported Conversion of Policy List: '{in_.type}' '{in_.name}'")


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    return _not_supported


def convert(in_: Input, context: PolicyConvertContext) -> Output:
    result = _find_converter(in_)(in_, context)
    if result is not None:
        result.model_validate(result)
    return result
