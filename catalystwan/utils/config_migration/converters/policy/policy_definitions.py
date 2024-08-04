# Copyright 2024 Cisco Systems, Inc. and its affiliates
import logging
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Type, TypeVar, Union, cast
from uuid import UUID

from packaging.version import Version  # type: ignore
from pydantic import Field, ValidationError
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.common import (
    AcceptDropActionType,
    AcceptRejectActionType,
    DeviceAccessProtocolPort,
    LossProtectionType,
    int_range_str_validator,
)
from catalystwan.models.configuration.config_migration import (
    ConvertResult,
    PolicyConvertContext,
    QoSMapResidues,
    SslDecryptioneResidues,
    SslProfileResidues,
)
from catalystwan.models.configuration.feature_profile.common import RefIdItem
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.qos_policy import QosPolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.traffic_policy import (
    TrafficPolicyParcel,
    TrafficPolicyTarget,
)
from catalystwan.models.configuration.feature_profile.sdwan.dns_security.dns import DnsParcel, TargetVpns
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import AnyEmbeddedSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.aip import (
    AdvancedInspectionProfileParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.amp import (
    AdvancedMalwareProtectionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.intrusion_prevention import (
    IntrusionPreventionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption import (
    CaCertBundle,
    SslDecryptionParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption_profile import (
    SslDecryptionProfileParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.url_filtering import (
    BlockPageAction,
    UrlFilteringParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import (
    Criteria,
    Origin,
    Protocol,
    RoutePolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access import DeviceAccessIPv4Parcel
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import DeviceAccessIPv6Parcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.configuration.network_hierarchy.cflowd import CflowdParcel
from catalystwan.models.policy import AnyPolicyDefinition
from catalystwan.models.policy.centralized import TrafficDataDirection
from catalystwan.models.policy.definition.access_control_list import AclPolicy
from catalystwan.models.policy.definition.access_control_list_ipv6 import AclIPv6Policy
from catalystwan.models.policy.definition.aip import AdvancedInspectionProfilePolicy
from catalystwan.models.policy.definition.amp import AdvancedMalwareProtectionPolicy
from catalystwan.models.policy.definition.cflowd import CflowdPolicy
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.device_access import DeviceAccessPolicy
from catalystwan.models.policy.definition.device_access_ipv6 import DeviceAccessIPv6Policy
from catalystwan.models.policy.definition.dns_security import DnsSecurityPolicy, TargetVpn
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.intrusion_prevention import IntrusionPreventionPolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy
from catalystwan.models.policy.definition.qos_map import QoSMapPolicy
from catalystwan.models.policy.definition.route_policy import RoutePolicy
from catalystwan.models.policy.definition.ssl_decryption import SslDecryptionPolicy
from catalystwan.models.policy.definition.ssl_decryption_utd_profile import SslDecryptionUtdProfilePolicy
from catalystwan.models.policy.definition.traffic_data import TrafficDataPolicy
from catalystwan.models.policy.definition.url_filtering import UrlFilteringPolicy
from catalystwan.models.policy.definition.zone_based_firewall import ZoneBasedFWPolicy
from catalystwan.utils.config_migration.converters.utils import convert_varname

from .zone_based_firewall import zone_based_fw

logger = logging.getLogger(__name__)


Input = AnyPolicyDefinition
OutputItem = Optional[
    Annotated[
        Union[
            CustomControlParcel,
            HubSpokeParcel,
            MeshParcel,
            Ipv4AclParcel,
            Ipv6AclParcel,
            AdvancedInspectionProfileParcel,
            AdvancedMalwareProtectionParcel,
            IntrusionPreventionParcel,
            SslDecryptionParcel,
            SslDecryptionProfileParcel,
            UrlFilteringParcel,
            DnsParcel,
            DeviceAccessIPv6Parcel,
            DeviceAccessIPv4Parcel,
            RoutePolicyParcel,
            AnyEmbeddedSecurityParcel,
        ],
        Field(discriminator="type_"),
    ]
]
OPD = TypeVar("OPD", OutputItem, None)
Output = ConvertResult[OPD]


def _get_parcel_name_desc(policy_definition: AnyPolicyDefinition) -> Dict[str, Any]:
    return dict(parcel_name=policy_definition.name, parcel_description=policy_definition.description)


def as_num_ranges_list(p: str) -> List[Union[int, Tuple[int, int]]]:
    """
    applicable to acl source/destination port list
    "1 2-5 6 7 20-22" -> [1 (2,5) 6 7 (20,22)]

    """
    num_list: List[Union[int, Tuple[int, int]]] = []
    for val in p.split():
        low, hi = int_range_str_validator(val, False)
        if hi is None:
            num_list.append(low)
        else:
            num_list.append((low, hi))
    return num_list


def as_num_list(ports_list: List[Union[int, Tuple[int, int]]]) -> List[int]:
    """
    applicable to device access port list
    [(30, 35), 80] -> [30 31 32 33 34 35 80]
    """
    num_list: List[int] = []
    for val in ports_list:
        if isinstance(val, int):
            num_list.append(val)
        elif isinstance(val, tuple):
            num_list.extend(range(min(val), max(val) + 1))
    num_list = sorted(list(set(num_list)))
    return num_list


def conditional_split(s: str, seps: List[str]) -> List[str]:
    """
    split s by first sep in seps
    """
    for sep in seps:
        if sep in s:
            return s.split(sep)
    return [s]


def advanced_malware_protection(
    in_: AdvancedMalwareProtectionPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[AdvancedMalwareProtectionParcel]:
    if vpn_list := in_.definition.target_vpns:
        context.amp_target_vpns_id[uuid] = vpn_list
    if not in_.definition.file_reputation_alert:
        return ConvertResult[AdvancedMalwareProtectionParcel](
            status="failed", info=["AMP file reputation alert shall not be an empty str."]
        )
    definition_dump = in_.definition.model_dump(exclude={"target_vpns"})
    return ConvertResult[AdvancedMalwareProtectionParcel](
        output=AdvancedMalwareProtectionParcel.create(**_get_parcel_name_desc(in_), **definition_dump)
    )


def control(in_: ControlPolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[CustomControlParcel]:
    result = ConvertResult[CustomControlParcel](output=None)
    out = CustomControlParcel(
        **_get_parcel_name_desc(in_), default_action=as_global(in_.default_action.type, AcceptRejectActionType)
    )
    for in_seq in in_.sequences:
        ip_type = in_seq.sequence_ip_type
        if not ip_type:
            ip_type = "ipv4"
        out_seq = out.add_sequence(
            id_=in_seq.sequence_id,
            name=in_seq.sequence_name,
            type_=in_seq.sequence_type,
            ip_type=ip_type,
            base_action=in_seq.base_action,
        )
        for in_match in in_seq.match.entries:
            if in_match.field == "carrier":
                out_seq.match_carrier(in_match.value)
            elif in_match.field == "colorList":
                out_seq.match_color_list(in_match.ref)
            elif in_match.field == "community":
                out_seq.match_community(in_match.ref)
            elif in_match.field == "domainId":
                out_seq.match_domain_id(int(in_match.value))
            elif in_match.field == "expandedCommunity":
                out_seq.match_expanded_community(in_match.ref)
            elif in_match.field == "groupId":
                out_seq.match_group_id(int(in_match.value))
            elif in_match.field == "ompTag":
                out_seq.match_omp_tag(int(in_match.value))
            elif in_match.field == "origin":
                out_seq.match_origin(in_match.value)
            elif in_match.field == "originator":
                out_seq.match_originator(in_match.value)
            elif in_match.field == "pathType":
                out_seq.match_path_type(in_match.value)
            elif in_match.field == "preference":
                out_seq.match_preference(int(in_match.value))
            elif in_match.field == "prefixList":
                out_seq.match_prefix_list(in_match.ref)
            elif in_match.field == "regionId":
                out_seq.match_region(in_match.value)
            elif in_match.field == "regionList":
                regions = context.regions_by_list_id.get(in_match.ref, [])
                if regions:
                    for region in regions:
                        out_seq.match_region(region=region)
                else:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains region list which is not matching any defined region "
                        f"{in_match.field} = {in_match.ref}",
                    )
            elif in_match.field == "role":
                out_seq.match_role(in_match.value)
            elif in_match.field == "siteId":
                out_seq.match_sites([in_match.value])
            elif in_match.field == "siteList":
                sites = context.sites_by_list_id.get(in_match.ref, [])
                if sites:
                    out_seq.match_sites(sites=sites)
                else:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains site list which is not matching any defined site "
                        f"{in_match.field} = {in_match.ref}",
                    )
            elif in_match.field == "tloc":
                out_seq.match_tloc(ip=in_match.value.ip, color=in_match.value.color, encap=in_match.value.encap)
            elif in_match.field == "tlocList":
                out_seq.match_tloc_list(in_match.ref)
            elif in_match.field == "vpnList":
                vpns = context.lan_vpns_by_list_id.get(in_match.ref, [])
                if vpns:
                    out_seq.match_vpns(vpns=vpns)
                else:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains vpn list which is not matching any defined vpn "
                        f"{in_match.field} = {in_match.ref}",
                    )
        for in_action in in_seq.actions:
            if in_action.type == "set":
                for param in in_action.parameter:
                    if param.field == "affinity":
                        out_seq.associate_affinitty_action(affinity=int(param.value))
                    elif param.field == "community" and param.value is not None:
                        out_seq.associate_community_action(community=param.value)
                    elif param.field == "communityAdditive":
                        out_seq.associate_community_additive_action(additive=True)
                    elif param.field == "service":
                        if param.value.tloc_list is not None:
                            out_seq.associate_service_action(
                                service_type=param.value.type,
                                vpn=param.value.vpn,
                                tloc_list_id=param.value.tloc_list.ref,
                            )
                        elif param.value.tloc is not None:
                            out_seq.associate_service_action(
                                service_type=param.value.type,
                                vpn=param.value.vpn,
                                ip=param.value.tloc.ip,
                                color=param.value.tloc.color,
                                encap=param.value.tloc.encap,
                            )
                    elif param.field == "tloc":
                        out_seq.associate_tloc(color=param.value.color, encap=param.value.encap, ip=param.value.ip)
                    elif param.field == "tlocAction":
                        out_seq.associate_tloc_action(tloc_action_type=param.value)
                    elif param.field == "tlocList":
                        out_seq.associate_tloc_list(tloc_list_id=param.ref)
    result.output = out
    return result


def traffic_data(
    in_: TrafficDataPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[TrafficPolicyParcel]:
    result = ConvertResult[TrafficPolicyParcel](output=None)
    out = TrafficPolicyParcel(
        **_get_parcel_name_desc(in_),
        data_default_action=as_global(in_.default_action.type, AcceptDropActionType),
        target=TrafficPolicyTarget(direction=as_global("tunnel", TrafficDataDirection), vpn=as_global([";dummy-vpn"])),
    )  # centralized policy converter will replace target and make copies when neccessary

    result.output = out
    for in_seq in in_.sequences:
        ip_type = in_seq.sequence_ip_type if in_seq.sequence_ip_type is not None else "ipv4"
        out_seq = out.add_sequence(
            name=in_seq.sequence_name,
            id_=in_seq.sequence_id,
            ip_type=ip_type,
            base_action=in_seq.base_action,
        )
        for in_match in in_seq.match.entries:
            if in_match.field == "appList":
                out_seq.match_app_list(in_match.ref[0])
            elif in_match.field == "destinationDataIpv6PrefixList":
                out_seq.match_destination_data_ipv6_prefix_list(in_match.ref[0])
            elif in_match.field == "destinationDataPrefixList":
                out_seq.match_destination_data_prefix_list(in_match.ref[0])
            elif in_match.field == "destinationIp":
                if in_match.value is not None:
                    out_seq.match_destination_ip(in_match.as_ipv4_networks()[0])
                    if len(in_match.value) > 1:
                        result.update_status(
                            "partial",
                            f"sequence[{in_seq.sequence_id}] contains multiple ip prefixes "
                            f"{in_match.field} = {in_match.value} only first is converted",
                        )
                elif in_match.vip_variable_name is not None:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] variable name as ip prefix is not supported "
                        f"{in_match.field} = {in_match.value}",
                    )
            elif in_match.field == "destinationIpv6":
                out_seq.match_destination_ipv6(in_match.as_ipv6_networks()[0])
                if len(in_match.value) > 1:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains multiple ipv6 prefixes "
                        f"{in_match.field} = {in_match.value} only first is converted",
                    )
            elif in_match.field == "destinationPort":
                out_seq.match_destination_ports(in_match.value.split())
            elif in_match.field == "destinationRegion":
                out_seq.match_destination_region(in_match.value)
            elif in_match.field == "dns":
                out_seq.match_dns(in_match.value)
            elif in_match.field == "dnsAppList":
                out_seq.match_dns_app_list(in_match.ref)
            elif in_match.field == "dscp":
                out_seq.match_dscp(in_match.value)
            elif in_match.field == "icmpMessage":
                out_seq.match_icmp_messages(in_match.value)
            elif in_match.field == "packetLength":
                out_seq.match_packet_length(in_match.value)
            elif in_match.field == "plp":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains entry "
                    f"{in_match.field} = {in_match.value} which cannot be converted",
                )
            elif in_match.field == "protocol":
                _protocols = [str(n) for n in as_num_list(as_num_ranges_list(in_match.value))]
                out_seq.match_protocols(_protocols)
            elif in_match.field == "sourceDataIpv6PrefixList":
                out_seq.match_source_data_ipv6_prefix_list(in_match.ref[0])
            elif in_match.field == "sourceDataPrefixList":
                out_seq.match_source_data_prefix_list(in_match.ref[0])
            elif in_match.field == "sourceIp":
                if in_match.value is not None:
                    out_seq.match_source_ip(in_match.as_ipv4_networks()[0])
                    if len(in_match.value) > 1:
                        result.update_status(
                            "partial",
                            f"sequence[{in_seq.sequence_id}] contains multiple ip prefixes "
                            f"{in_match.field} = {in_match.value} only first is converted",
                        )
                elif in_match.vip_variable_name is not None:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] variable name as ip prefix is not supported "
                        f"{in_match.field} = {in_match.value}",
                    )
            elif in_match.field == "sourceIpv6":
                out_seq.match_source_ipv6(in_match.as_ipv6_networks()[0])
                if len(in_match.value) > 1:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains multiple ipv6 prefixes "
                        f"{in_match.field} = {in_match.value} only first is converted",
                    )
            elif in_match.field == "sourcePort":
                out_seq.match_source_ports(in_match.value.split())
            elif in_match.field == "tcp":
                out_seq.match_tcp()
            elif in_match.field == "trafficTo":
                out_seq.match_traffic_to(in_match.value)

        appqoe_dre = False
        appqoe_tcp = False
        appqoe_sv_grp = None
        loss_prot: Optional[LossProtectionType] = None
        loss_prot_fec: Optional[int] = None

        for in_action in in_seq.actions:
            if in_action.type == "set":
                for in_param in in_action.parameter:
                    if in_param.field == "dscp":
                        out_seq.associate_dscp_action(in_param.value[0])
                    elif in_param.field == "forwardingClass":
                        _fwcid = context.fwclass_id_by_name.get(in_param.value)
                        if _fwcid is not None:
                            out_seq.associate_forwarding_class_action(_fwcid)
                    elif in_param.field == "localTlocList":
                        _ltloc = in_param.value
                        out_seq.associate_local_tloc_list_action(
                            color=_ltloc.color,
                            encap=_ltloc.encap,
                            restrict=True if _ltloc.restrict is not None else False,
                        )
                    elif in_param.field == "preferredColorGroup":
                        out_seq.associate_preferred_color_group_action(in_param.ref)
                    elif in_param.field == "nextHop":
                        if isinstance(in_param.value, IPv4Address):
                            out_seq.associate_next_hop_action(in_param.value)
                        elif isinstance(in_param.value, IPv6Address):
                            out_seq.associate_next_hop_ipv6_action(in_param.value)
                    elif in_param.field == "nextHopLoose":
                        out_seq.associate_next_hop_loose_action(in_param.value)
                    elif in_param.field == "policer":
                        out_seq.associate_policer_action(in_param.ref)
                    elif in_param.field == "service":
                        _vpn = in_param.value.vpn
                        if _vpn is None:
                            _vpn = 65530  # insert dummy vpn (vpn in parcel is required)
                        if in_param.value.tloc_list is not None:
                            out_seq.associate_service_action(
                                service_type=in_param.value.type,
                                vpn=_vpn,
                                tloc_list_id=in_param.value.tloc_list.ref,
                            )
                        elif in_param.value.tloc is not None:
                            out_seq.associate_service_action(
                                service_type=in_param.value.type,
                                vpn=_vpn,
                                ip=in_param.value.tloc.ip,
                                color=[in_param.value.tloc.color],
                                encap=in_param.value.tloc.encap,
                            )
                    elif in_param.field == "serviceChain":
                        result.update_status(
                            "partial",
                            f"sequence[{in_seq.sequence_id}] contains unsupported entry "
                            f"{in_param.field} = {in_param.value} which cannot be converted",
                        )  # >=20.15
                    elif in_param.field == "vpn":
                        out_seq.associate_vpn_action(int(in_param.value))
                    elif in_param.field == "tloc":
                        out_seq.associate_tloc_action(
                            ip=in_param.value.ip,
                            color=[in_param.value.color],
                            encap=in_param.value.encap,
                        )
                    elif in_param.field == "tlocList":
                        out_seq.associate_tloc_list_action(in_param.ref)

            elif in_action.type == "count":
                out_seq.associate_count_action(in_action.parameter)
            elif in_action.type == "log":
                out_seq.associate_log_action(True)
            elif in_action.type == "cflowd":
                out_seq.associate_cflowd_action(True)
            elif in_action.type == "nat":
                if in_action.nat_pool is not None:
                    out_seq.associate_nat_pool_action(in_action.nat_pool)
                elif in_action.nat_vpn is not None:
                    _nat = in_action.nat_vpn
                    out_seq.associate_nat_action(
                        bypass=_nat.bypass,
                        dia_interface=_nat.dia_interface,
                        dia_pool=_nat.dia_pool,
                        fallback=_nat.fallback,
                        use_vpn=True if _nat.vpn is not None else False,
                    )
            elif in_action.type == "redirectDns":
                _rdns = in_action.parameter
                if _rdns.field == "ipAddress":
                    out_seq.associate_redirect_dns_action_with_ip(_rdns.value)
                elif _rdns.field == "dnsType":
                    out_seq.associate_redirect_dns_action_with_dns_type(_rdns.value)
            elif in_action.type == "tcpOptimization":
                appqoe_tcp = True
            elif in_action.type == "dreOptimization":
                appqoe_dre = True
            elif in_action.type == "serviceNodeGroup":
                appqoe_sv_grp = in_action.parameter
            elif in_action.type == "lossProtect":
                if context.platform_version < Version("20.14"):
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] "
                        f"{in_action.type} = {in_action.parameter} cannot be converted",
                    )
                else:
                    loss_prot = in_action.parameter
            elif in_action.type == "lossProtectFec":
                if context.platform_version < Version("20.14"):
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] "
                        f"{in_action.type} = {in_action.parameter} cannot be converted",
                    )
                else:
                    _fec = in_action.value
                    loss_prot = in_action.parameter
                    loss_prot_fec = int(_fec) if _fec else None
            elif in_action.type == "lossProtectPktDup":
                if context.platform_version < Version("20.14"):
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] "
                        f"{in_action.type} = {in_action.parameter} cannot be converted",
                    )
                else:
                    loss_prot = in_action.parameter
            elif in_action.type == "fallbackToRouting":
                out_seq.associate_fallback_to_routing_action()
            elif in_action.type == "sig":
                out_seq.associate_sig_action()
        if appqoe_sv_grp is not None:
            out_seq.associate_appqoe_optimization_action(
                dre_optimization=appqoe_dre, service_node_group=appqoe_sv_grp, tcp_optimization=appqoe_tcp
            )
        if loss_prot is not None:
            out_seq.associate_loss_correction_action(type=loss_prot, fec=loss_prot_fec)
    return result


def dns_security(in_: DnsSecurityPolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[DnsParcel]:
    errors: List[str] = []

    def target_vpn_convert(target_vpn: TargetVpn, vpn_id_to_map: Dict[Union[str, int], List[str]]) -> TargetVpns:
        vpn_names = []
        for vpn in target_vpn.vpns:
            if not (mapped_name := vpn_id_to_map.get(vpn)):
                errors.append(f"Cannot find TargetVPN with id: {vpn}")
            else:
                vpn_names.extend(mapped_name)
        return TargetVpns.create(**target_vpn.model_dump(exclude={"vpns"}), vpns=vpn_names)

    vpn_id_to_map = context.get_vpn_id_to_vpn_name_map()

    if umbrella_data := in_.definition.umbrella_data:
        context.dns_security_umbrella_data[uuid] = umbrella_data.ref

    _target_vpns = (
        [target_vpn_convert(target_vpn, vpn_id_to_map) for target_vpn in in_.definition.target_vpns]
        if in_.definition.target_vpns
        else None
    )

    _local_domain_bypass_list = (
        in_.definition.local_domain_bypass_list.ref if in_.definition.local_domain_bypass_list else None
    )

    result = ConvertResult[DnsParcel](
        output=DnsParcel.create(
            **_get_parcel_name_desc(in_),
            **in_.definition.model_dump(exclude={"local_domain_bypass_list", "umbrella_data", "target_vpns"}),
            target_vpns=_target_vpns,
            local_domain_bypass_list=_local_domain_bypass_list,
        ),
        info=errors,
        status="failed" if errors else "complete",
    )
    return result


def hubspoke(in_: HubAndSpokePolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[HubSpokeParcel]:
    target_vpns = context.lan_vpns_by_list_id[in_.definition.vpn_list]
    if not target_vpns:
        return ConvertResult[HubSpokeParcel](status="failed", info=["No VPNs found matching VPN list assignment"])
    out = HubSpokeParcel(**_get_parcel_name_desc(in_))
    out.target.vpn.value.extend(target_vpns)
    for isubdef in in_.definition.sub_definitions:
        osites: List[str] = []
        ohubs: List[str] = []
        for ispoke in isubdef.spokes:
            osites.extend(context.sites_by_list_id[ispoke.site_list])
            for ihub in ispoke.hubs:
                ohubs.extend(context.sites_by_list_id[ihub.site_list])
        ospoke = out.add_spoke(isubdef.name, list(set(osites)))
        ospoke.add_hub_site(list(set(ohubs)), 1)
        out.selected_hubs.value = list(set(ohubs))
    return ConvertResult[HubSpokeParcel](output=out)


def ipv4acl(in_: AclPolicy, uuid: UUID, context) -> ConvertResult[Ipv4AclParcel]:
    out = Ipv4AclParcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    result = ConvertResult[Ipv4AclParcel](output=out)
    for in_seq in in_.sequences:
        out_seq = out.add_sequence(name=in_seq.sequence_name, id_=in_seq.sequence_id, base_action=in_seq.base_action)
        for in_entry in in_seq.match.entries:
            if in_entry.field == "class":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains entry "
                    f"{in_entry.field} = {in_entry.ref} which cannot be converted",
                )

            if in_entry.field == "destinationDataPrefixList" and in_entry.ref:
                out_seq.match_destination_data_prefix_list(in_entry.ref[0])

            elif in_entry.field == "destinationIp":
                if in_entry.vip_variable_name is not None:
                    varname = convert_varname(in_entry.vip_variable_name)
                    out_seq.match_destination_data_prefix_variable(varname)
                elif in_entry.value is not None:
                    out_seq.match_destination_data_prefix(prefix=in_entry.value[0])
                    if len(in_entry.value) > 1:
                        result.update_status(
                            "partial",
                            f"sequence[{in_seq.sequence_id}] contains multiple ip prefixes "
                            f"{in_entry.field} = {in_entry.value} only first is converted",
                        )

            elif in_entry.field == "destinationPort":
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif in_entry.field == "dscp":
                out_seq.match_dscp(in_entry.value)

            elif in_entry.field == "packetLength":
                low, hi = int_range_str_validator(in_entry.value, False)
                if hi is None:
                    out_seq.match_packet_length(low)
                else:
                    out_seq.match_packet_length((low, hi))

            elif in_entry.field == "plp":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains entry "
                    f"{in_entry.field} = {in_entry.value} which cannot be converted",
                )

            elif in_entry.field == "protocol":
                protocols: List[int] = []
                for val in in_entry.value.split():
                    low, hi = int_range_str_validator(val, False)
                    if hi is None:
                        protocols.append(low)
                    else:
                        protocols.extend(range(low, hi + 1))
                out_seq.match_protocol(protocols)

            elif in_entry.field == "sourceDataPrefixList" and in_entry.ref:
                out_seq.match_source_data_prefix_list(in_entry.ref[0])

            elif in_entry.field == "sourceIp":
                if in_entry.vip_variable_name is not None:
                    varname = convert_varname(in_entry.vip_variable_name)
                    out_seq.match_source_data_prefix_variable(varname)
                elif in_entry.value is not None:
                    out_seq.match_source_data_prefix(in_entry.value[0])
                    if len(in_entry.value) > 1:
                        result.update_status(
                            "partial",
                            f"sequence[{in_seq.sequence_id}] contains multiple ip prefixes "
                            f"{in_entry.field} = {in_entry.value} only first is converted",
                        )

            elif in_entry.field == "sourcePort":
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif in_entry.field == "tcp":
                out_seq.match_tcp()

        for in_action in in_seq.actions:
            if in_action.type == "set":
                for param in in_action.parameter:
                    if param.field == "dscp":
                        out_seq.associate_set_dscp_action(dscp=int(param.value[0]))
                    elif param.field == "nextHop":
                        out_seq.associate_set_next_hop_action(next_hop=cast(IPv4Address, param.value))
            elif in_action.type == "count":
                out_seq.associate_counter_action(name=in_action.parameter)
            elif in_action.type == "class":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains action "
                    f"{in_action.type} = {in_action.parameter} which cannot be converted",
                )
            elif in_action.type == "log":
                out_seq.associate_log_action()
            elif in_action.type == "mirror":
                out_seq.associate_mirror_action(mirror=in_action.parameter.ref)
            elif in_action.type == "policer":
                out_seq.associate_policer_action(in_action.parameter.ref)

    return result


def ipv6acl(in_: AclIPv6Policy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[Ipv6AclParcel]:
    out = Ipv6AclParcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    result = ConvertResult[Ipv6AclParcel](output=out)
    for in_seq in in_.sequences:
        out_seq = out.add_sequence(name=in_seq.sequence_name, id_=in_seq.sequence_id, base_action=in_seq.base_action)
        for in_entry in in_seq.match.entries:
            if in_entry.field == "class":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains entry "
                    f"{in_entry.field} = {in_entry.ref} which cannot be converted",
                )

            if in_entry.field == "destinationDataIpv6PrefixList" and in_entry.ref:
                out_seq.match_destination_data_prefix_list(in_entry.ref[0])

            elif in_entry.field == "destinationIpv6":
                out_seq.match_destination_data_prefix(in_entry.value[0])
                if len(in_entry.value) > 1:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains multiple ipv6 prefixes "
                        f"{in_entry.field} = {in_entry.value} only first is converted",
                    )

            elif in_entry.field == "destinationPort":
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif in_entry.field == "nextHeader":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains entry "
                    f"{in_entry.field} = {in_entry.value} which cannot be converted",
                )

            elif in_entry.field == "packetLength":
                low, hi = int_range_str_validator(in_entry.value, False)
                if hi is None:
                    out_seq.match_packet_length(low)
                else:
                    out_seq.match_packet_length((low, hi))

            elif in_entry.field == "plp":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains entry "
                    f"{in_entry.field} = {in_entry.value} which cannot be converted",
                )

            elif in_entry.field == "sourceDataIpv6PrefixList" and in_entry.ref:
                out_seq.match_source_data_prefix_list(in_entry.ref[0])

            elif in_entry.field == "sourceIpv6":
                out_seq.match_source_data_prefix(in_entry.value[0])
                if len(in_entry.value) > 1:
                    result.update_status(
                        "partial",
                        f"sequence[{in_seq.sequence_id}] contains multiple ipv6 prefixes "
                        f"{in_entry.field} = {in_entry.value} only first is converted",
                    )

            elif in_entry.field == "sourcePort":
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif in_entry.field == "tcp":
                out_seq.match_tcp()

            elif in_entry.field == "trafficClass":
                out_seq.match_traffic_class(classes=list(map(int, in_entry.value.split())))

        for in_action in in_seq.actions:
            if in_action.type == "set":
                for param in in_action.parameter:
                    if param.field == "nextHop":
                        out_seq.associate_set_next_hop_action(next_hop=cast(IPv6Address, param.value))
                    elif param.field == "trafficClass":
                        out_seq.associate_set_traffic_class_action(traffic_class=int(param.value))
            elif in_action.type == "count":
                out_seq.associate_counter_action(name=in_action.parameter)
            elif in_action.type == "class":
                result.update_status(
                    "partial",
                    f"sequence[{in_seq.sequence_id}] contains action "
                    f"{in_action.type} = {in_action.parameter} which cannot be converted",
                )
            elif in_action.type == "log":
                out_seq.associate_log_action()
            elif in_action.type == "mirror":
                out_seq.associate_mirror_action(mirror=in_action.parameter.ref)
            elif in_action.type == "policer":
                out_seq.associate_policer_action(in_action.parameter.ref)

    return result


def device_access_ipv6(
    in_: DeviceAccessIPv6Policy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[DeviceAccessIPv6Parcel]:
    out = DeviceAccessIPv6Parcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        port_str = next(e.value for e in in_seq.match.entries if e.field == "destinationPort")
        port = cast(DeviceAccessProtocolPort, int(port_str))
        seq = out.add_sequence(
            id_=in_seq.sequence_id,
            name=in_seq.sequence_name,
            destination_port=port,
            base_action=in_seq.base_action,
        )
        for in_entry in in_seq.match.entries:
            if in_entry.field == "destinationDataIpv6PrefixList":
                if in_entry.ref:
                    seq.match_destination_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "destinationIpv6":
                seq.match_destination_data_prefixes(in_entry.value)
            elif in_entry.field == "destinationPort":
                destination_port = cast(DeviceAccessProtocolPort, int(in_entry.value))
                seq.match_destination_port(destination_port)
            elif in_entry.field == "sourceDataIpv6PrefixList":
                if in_entry.ref:
                    seq.match_source_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "sourceIpv6":
                seq.match_source_data_prefixes(in_entry.value)
            elif in_entry.field == "sourcePort":
                seq.match_source_ports(as_num_list(as_num_ranges_list(in_entry.value)))
    return ConvertResult[DeviceAccessIPv6Parcel](output=out)


def device_access_ipv4(
    in_: DeviceAccessPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[DeviceAccessIPv4Parcel]:
    out = DeviceAccessIPv4Parcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        port_str = next(e.value for e in in_seq.match.entries if e.field == "destinationPort")
        port = cast(DeviceAccessProtocolPort, int(port_str))
        seq = out.add_sequence(
            id_=in_seq.sequence_id,
            name=in_seq.sequence_name,
            destination_port=port,
            base_action=in_seq.base_action,
        )
        for in_entry in in_seq.match.entries:
            if in_entry.field == "destinationDataPrefixList":
                if in_entry.ref:
                    seq.match_destination_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "destinationIp":
                if in_entry.value is not None:
                    seq.match_destination_data_prefixes(prefixes=in_entry.value)
                elif in_entry.vip_variable_name is not None:
                    seq.match_destination_data_prefix_variable(convert_varname(in_entry.vip_variable_name))
            elif in_entry.field == "sourceDataPrefixList":
                if in_entry.ref:
                    seq.match_source_data_prefix_list(in_entry.ref[0])
            elif in_entry.field == "sourceIp":
                if in_entry.value is not None:
                    seq.match_source_data_prefixes(prefixes=in_entry.value)
                elif in_entry.vip_variable_name is not None:
                    seq.match_source_data_prefix_variable(convert_varname(in_entry.vip_variable_name))
            elif in_entry.field == "sourcePort":
                seq.match_source_ports(as_num_list(as_num_ranges_list(in_entry.value)))
    return ConvertResult[DeviceAccessIPv4Parcel](output=out)


def qos_map(in_: QoSMapPolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[QosPolicyParcel]:
    result = ConvertResult[QosPolicyParcel]()

    try:
        context.qos_map_residues[uuid] = []
        out = QosPolicyParcel.create(**_get_parcel_name_desc(in_))
        result.output = out

        # add target
        # out.set_variable_target("Interface_1")  # for tests

        for scheduler in in_.definition.qos_schedulers:
            out.add_scheduler(
                queue=str(scheduler.queue),
                class_map_ref=scheduler.class_map_ref,
                bandwidth_percent=str(scheduler.bandwidth_percent),
                drops=scheduler.drops,
                scheduling=scheduler.scheduling,
            )

            context.qos_map_residues[uuid].append(
                QoSMapResidues(
                    buffer_percent=scheduler.buffer_percent,
                    burst=scheduler.burst,
                    temp_key_values=scheduler.temp_key_values,
                )
            )
    except ValidationError as e:
        result.update_status("failed", f"Cannot convert QOS Map: {e}")

    return result


def route(in_: RoutePolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[RoutePolicyParcel]:
    out = RoutePolicyParcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    result = ConvertResult[RoutePolicyParcel](output=out)
    for in_seq in in_.sequences:
        sequence_ip_type = in_seq.sequence_ip_type
        if sequence_ip_type is not None:
            protocol = "BOTH" if sequence_ip_type == "all" else sequence_ip_type.upper()
        out_seq = out.add_sequence(
            id_=in_seq.sequence_id,
            name=in_seq.sequence_name,
            base_action=in_seq.base_action,
            protocol=cast(Protocol, protocol),
        )

        for in_entry in in_seq.match.entries:
            if in_entry.field == "asPath":
                out_seq.match_as_path_list(in_entry.ref)
            elif in_entry.field == "expandedCommunity":
                out_seq.match_community_list(expanded_community_list=in_entry.ref)
            elif in_entry.field == "advancedCommunity":
                # Advanced matches to standard, because it has a list of UUIDs and a match flag
                out_seq.match_community_list(
                    standard_community_list=in_entry.refs, criteria=cast(Criteria, in_entry.match_flag.upper())
                )
            elif in_entry.field == "extCommunity":
                out_seq.match_ext_community_list(in_entry.ref)
            elif in_entry.field == "localPreference":
                # Local preference is matches to bgp
                out_seq.match_bgp_local_preference(in_entry.value)
            elif in_entry.field == "metric":
                out_seq.match_metric(in_entry.value)
            elif in_entry.field == "ompTag":
                out_seq.match_omp_tag(in_entry.value)
            elif in_entry.field == "ospfTag":
                out_seq.match_ospf_tag(in_entry.value)
            elif in_entry.field == "address":
                if sequence_ip_type == "ipv4":
                    out_seq.match_ipv4_address(in_entry.ref)
                elif sequence_ip_type == "ipv6":
                    out_seq.match_ipv6_address(in_entry.ref)
            elif in_entry.field == "nextHop":
                if sequence_ip_type == "ipv4":
                    out_seq.match_ipv4_next_hop(in_entry.ref)
                elif sequence_ip_type == "ipv6":
                    out_seq.match_ipv6_next_hop(in_entry.ref)

        if in_seq.base_action == "accept":
            for in_action in in_seq.actions:
                community_additive = any(
                    [action.value for action in in_action.parameter if action.field == "communityAdditive"]
                )
                for in_param in in_action.parameter:
                    if in_param.field == "asPath":
                        if in_param.value.prepend is not None:
                            out_seq.associate_as_path_action(in_param.value.prepend)
                        if in_param.value.exclude is not None:
                            result.update_status(
                                "partial",
                                f"sequence[{in_seq.sequence_id}] contains action parameter "
                                f"{in_param.field}.exclude = {in_param.value.exclude} which cannot be converted",
                            )
                    elif in_param.field == "community":
                        if in_param.value:
                            out_seq.associate_community_action(community_additive, in_param.value)
                        if in_param.vip_variable_name:
                            out_seq.associate_community_variable_action(
                                community_additive, convert_varname(in_param.vip_variable_name)
                            )
                    elif in_param.field == "localPreference":
                        out_seq.associate_local_preference_action(in_param.value)
                    elif in_param.field == "metric":
                        out_seq.associate_metric_action(in_param.value)
                    elif in_param.field == "metricType":
                        out_seq.associate_metric_type_action(in_param.value)
                    elif in_param.field == "ospfTag":
                        out_seq.associate_ospf_tag_action(in_param.value)
                    elif in_param.field == "origin":
                        origin = "Incomplete" if in_param.value == "incomplete" else in_param.value.upper()
                        out_seq.associate_origin_action(cast(Origin, origin))
                    elif in_param.field == "ompTag":
                        out_seq.associate_omp_tag_action(in_param.value)
                    elif in_param.field == "weight":
                        out_seq.associate_weight_action(in_param.value)
                    elif in_param.field == "nextHop":
                        if isinstance(in_param.value, IPv4Address):
                            out_seq.associate_ipv4_next_hop_action(in_param.value)
                        if isinstance(in_param.value, IPv6Address):
                            out_seq.associate_ipv6_next_hop_action(in_param.value)
    return result


def mesh(in_: MeshPolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[MeshParcel]:
    target_vpns = context.lan_vpns_by_list_id[in_.definition.vpn_list]
    if not target_vpns:
        return ConvertResult[MeshParcel](status="failed", info=["No VPNs found matching VPN list assignment"])
    mesh_sites: List[str] = []
    for region in in_.definition.regions:
        for site_list in region.site_lists:
            mesh_sites.extend(context.sites_by_list_id[site_list])
    if not mesh_sites:
        return ConvertResult[MeshParcel](status="failed", info=["No Sites found matching Site list assignment"])
    out = MeshParcel(**_get_parcel_name_desc(in_))
    out.target.vpn.value = target_vpns
    out.sites.value = mesh_sites
    return ConvertResult[MeshParcel](output=out)


def ssl_decryption(
    in_: SslDecryptionPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[SslDecryptionParcel]:
    definition_dump = in_.definition.settings.model_dump(
        exclude={"certificate_lifetime", "ca_cert_bundle", "unknown_status"}
    )
    certificate_lifetime = str(in_.definition.settings.certificate_lifetime)
    ca_cert_bundle = CaCertBundle.create(**in_.definition.settings.ca_cert_bundle.model_dump())
    unknown_status = (
        in_.definition.settings.unknown_status
        if in_.definition.settings.certificate_revocation_status != "none"
        else None
    )

    if in_.definition.sequences or in_.definition.profiles:
        context.ssl_decryption_residues[uuid] = SslDecryptioneResidues(
            sequences=in_.definition.sequences, profiles=in_.definition.profiles
        )

    out = SslDecryptionParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        ca_cert_bundle=ca_cert_bundle,
        certificate_lifetime=certificate_lifetime,
        unknown_status=unknown_status,
    )
    return ConvertResult[SslDecryptionParcel](output=out)


def ssl_profile(
    in_: SslDecryptionUtdProfilePolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[SslDecryptionProfileParcel]:
    definition_dump = in_.definition.model_dump(
        exclude={"filtered_url_white_list", "filtered_url_black_list", "url_white_list", "url_black_list"}
    )

    url_allowed_list = in_.definition.url_white_list.ref if in_.definition.url_white_list else None
    url_blocked_list = in_.definition.url_black_list.ref if in_.definition.url_black_list else None

    if in_.definition.filtered_url_black_list or in_.definition.filtered_url_white_list:
        context.ssl_profile_residues[uuid] = SslProfileResidues(
            filtered_url_black_list=in_.definition.filtered_url_black_list,
            filtered_url_white_list=in_.definition.filtered_url_white_list,
        )

    out = SslDecryptionProfileParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        url_allowed_list=url_allowed_list,
        url_blocked_list=url_blocked_list,
    )
    return ConvertResult[SslDecryptionProfileParcel](output=out)


def advanced_inspection_profile(
    in_: AdvancedInspectionProfilePolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[AdvancedInspectionProfileParcel]:
    intrusion_prevention_ref = in_.definition.intrusion_prevention.ref if in_.definition.intrusion_prevention else None
    url_filtering_ref = in_.definition.url_filtering.ref if in_.definition.url_filtering else None
    advanced_malware_protection_ref = (
        in_.definition.advanced_malware_protection.ref if in_.definition.advanced_malware_protection else None
    )
    ssl_decryption_profile_ref = (
        in_.definition.ssl_utd_decrypt_profile.ref if in_.definition.ssl_utd_decrypt_profile else None
    )

    out = AdvancedInspectionProfileParcel.create(
        **_get_parcel_name_desc(in_),
        tls_decryption_action=in_.definition.tls_decryption_action,
        intrusion_prevention=intrusion_prevention_ref,
        url_filtering=url_filtering_ref,
        advanced_malware_protection=advanced_malware_protection_ref,
        ssl_decryption_profile=ssl_decryption_profile_ref,
    )
    return ConvertResult[AdvancedInspectionProfileParcel](output=out)


def url_filtering(
    in_: UrlFilteringPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[UrlFilteringParcel]:
    block_page_action_map: Dict[str, BlockPageAction] = {"text": "text", "redirectUrl": "redirect-url"}
    definition_dump = in_.definition.model_dump(
        exclude={"target_vpns", "url_white_list", "url_black_list", "logging", "block_page_action"}
    )

    if vpns := in_.definition.target_vpns:
        context.url_filtering_target_vpns[uuid] = vpns

    block_page_action = block_page_action_map[in_.definition.block_page_action]
    # below references are a references to v1 objects,
    # during push the references shall be transformed to point v2 objects
    url_allowed_list = (
        RefIdItem(ref_id=as_global(str(in_.definition.url_white_list.ref))) if in_.definition.url_white_list else None
    )
    url_blocked_list = (
        RefIdItem(ref_id=as_global(str(in_.definition.url_black_list.ref))) if in_.definition.url_black_list else None
    )

    out = UrlFilteringParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        block_page_action=block_page_action,
        url_allowed_list=url_allowed_list,
        url_blocked_list=url_blocked_list,
    )
    return ConvertResult[UrlFilteringParcel](output=out)


def intrusion_prevention(
    in_: IntrusionPreventionPolicy, uuid: UUID, context: PolicyConvertContext
) -> ConvertResult[IntrusionPreventionParcel]:
    if vpn_list := in_.definition.target_vpns:
        context.intrusion_prevention_target_vpns_id[uuid] = vpn_list

    definition_dump = in_.definition.model_dump(exclude={"target_vpns", "logging"})
    signature_white_list = definition_dump.pop("signature_white_list", None)
    signature_allowed_list = signature_white_list.get("ref") if signature_white_list else None

    out = IntrusionPreventionParcel.create(
        **_get_parcel_name_desc(in_),
        **definition_dump,
        signature_allowed_list=signature_allowed_list,
    )
    return ConvertResult[IntrusionPreventionParcel](output=out)


def cflowd(in_: CflowdPolicy, uuid: UUID, context: PolicyConvertContext) -> ConvertResult[None]:
    """Only Cflowd from activated centralized policy is converted,
    because it there is only one cflowd parcel in the Network Hierarchy global node."""
    if uuid not in context.activated_centralized_policy_item_ids:
        logger.debug(
            f"Skipping CflowdPolicy: {uuid} conversion, because the parent centralized policy is not activated."
        )
        return ConvertResult[None]()
    out = CflowdParcel()
    definition = in_.definition
    customized = definition.customized_ipv4_record_fields
    out.set_customized_ipv4_record_fields(
        collect_dscp_output=customized.collect_dscp_output,
        collect_tos=customized.collect_tos,
    )
    out.set_flow(
        active_timeout=definition.flow_active_timeout,
        inactive_timeout=definition.flow_inactive_timeout,
        refresh_time=definition.template_refresh,
        sampling_interval=definition.flow_sampling_interval,
    )
    out.set_protocol(definition.protocol)
    for col in definition.collectors:
        out.add_collector(
            address=col.address,
            udp_port=col.port,
            vpn_id=col.vpn,
            export_spread=col.export_spread is not None,
            bfd_metrics_export=col.bfd_metrics_export is not None,
            export_interval=col.export_interval,
            # col.transport
        )
    context.cflowd = out
    return ConvertResult[None]()


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AclIPv6Policy: ipv6acl,
    AclPolicy: ipv4acl,
    AdvancedInspectionProfilePolicy: advanced_inspection_profile,
    AdvancedMalwareProtectionPolicy: advanced_malware_protection,
    CflowdPolicy: cflowd,
    ControlPolicy: control,
    DeviceAccessIPv6Policy: device_access_ipv6,
    DeviceAccessPolicy: device_access_ipv4,
    DnsSecurityPolicy: dns_security,
    HubAndSpokePolicy: hubspoke,
    IntrusionPreventionPolicy: intrusion_prevention,
    MeshPolicy: mesh,
    QoSMapPolicy: qos_map,
    RoutePolicy: route,
    SslDecryptionPolicy: ssl_decryption,
    SslDecryptionUtdProfilePolicy: ssl_profile,
    TrafficDataPolicy: traffic_data,
    UrlFilteringPolicy: url_filtering,
    ZoneBasedFWPolicy: zone_based_fw,
}


def _not_supported(in_: Input, *args, **kwargs) -> ConvertResult[None]:
    logger.warning(f"Not Supported Conversion of Policy Definition: '{in_.type}' '{in_.name}'")
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
