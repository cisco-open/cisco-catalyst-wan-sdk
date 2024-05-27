import logging
from ipaddress import IPv4Interface
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Type, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.common import int_range_str_validator
from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.policy import AnyPolicyDefinition
from catalystwan.models.policy.definition.access_control_list import AclPolicy
from catalystwan.models.policy.definition.access_control_list_ipv6 import AclIPv6Policy
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException
from catalystwan.utils.config_migration.converters.utils import convert_varname

logger = logging.getLogger(__name__)

Input = AnyPolicyDefinition
Output = Optional[
    Annotated[
        Union[CustomControlParcel, HubSpokeParcel, MeshParcel, Ipv4AclParcel, Ipv6AclParcel],
        Field(discriminator="type_"),
    ]
]


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
            num_list.append((hi, low))
    return num_list


def control(in_: ControlPolicy, context) -> CustomControlParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {ControlPolicy.__name__}")
    out = CustomControlParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def hubspoke(in_: HubAndSpokePolicy, context: PolicyConvertContext) -> HubSpokeParcel:
    target_vpns = context.lan_vpns_by_list_id[in_.definition.vpn_list]
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
    return out


def ipv4acl(in_: AclPolicy, context) -> Ipv4AclParcel:
    out = Ipv4AclParcel(**_get_parcel_name_desc(in_))
    out.set_default_action(in_.default_action.type)
    for in_seq in in_.sequences:
        out_seq = out.add_sequence(name=in_seq.sequence_name, id_=in_seq.sequence_id, base_action=in_seq.base_action)
        for in_entry in in_seq.match.entries:
            if "destinationDataPrefixList" == in_entry.field and in_entry.ref:
                out_seq.match_destination_data_prefix_list(in_entry.ref[0])

            elif "destinationIp" == in_entry.field:
                if in_entry.vipVariableName is not None:
                    varname = convert_varname(in_entry.vipVariableName)
                    out_seq.match_destination_data_prefix_variable(varname)
                elif in_entry.value is not None:
                    out_seq.match_destination_data_prefix(IPv4Interface(in_entry.value))

            elif "destinationPort" == in_entry.field:
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif "dscp" == in_entry.field:
                out_seq.match_dscp([int(s) for s in in_entry.value.split()])

            elif "packetLength" == in_entry.field:
                low, hi = int_range_str_validator(in_entry.value, False)
                if hi is None:
                    out_seq.match_packet_length(low)
                else:
                    out_seq.match_packet_length((low, hi))

            elif "plp" == in_entry.field:
                logger.warning(
                    f"{Ipv4AclParcel.__name__} has no field matching plp found in {AclPolicy.__name__}: {in_.name}"
                )

            elif "protocol" == in_entry.field:
                protocols: List[int] = []
                for val in in_entry.value.split():
                    low, hi = int_range_str_validator(val, False)
                    if hi is None:
                        protocols.append(low)
                    else:
                        protocols.extend(range(low, hi + 1))
                out_seq.match_protocol(protocols)

            elif "sourceDataPrefixList" == in_entry.field and in_entry.ref:
                out_seq.match_destination_data_prefix_list(in_entry.ref[0])

            elif "sourceIp" == in_entry.field:
                if in_entry.vipVariableName is not None:
                    varname = convert_varname(in_entry.vipVariableName)
                    out_seq.match_source_data_prefix_variable(varname)
                elif in_entry.value is not None:
                    out_seq.match_source_data_prefix(IPv4Interface(in_entry.value))

            elif "sourcePort" == in_entry.field:
                portlist = as_num_ranges_list(in_entry.value)
                out_seq.match_destination_ports(portlist)

            elif "tcp" == in_entry.field:
                out_seq.match_tcp()

    return out


def ipv6acl(in_: AclIPv6Policy, context) -> Ipv6AclParcel:
    out = Ipv6AclParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def mesh(in_: MeshPolicy, context: PolicyConvertContext) -> MeshParcel:
    target_vpns = context.lan_vpns_by_list_id[in_.definition.vpn_list]
    mesh_sites: List[str] = []
    for region in in_.definition.regions:
        for site_list in region.site_lists:
            mesh_sites.extend(context.sites_by_list_id[site_list])
    out = MeshParcel(**_get_parcel_name_desc(in_))
    out.target.vpn.value = target_vpns
    out.sites.value = mesh_sites
    return out


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AclPolicy: ipv4acl,
    AclIPv6Policy: ipv6acl,
    ControlPolicy: control,
    HubAndSpokePolicy: hubspoke,
    MeshPolicy: mesh,
}


def _not_supported(in_: Input, *args, **kwargs) -> None:
    logger.warning(f"Not Supported Conversion of Policy Definition: '{in_.type}' '{in_.name}'")


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
