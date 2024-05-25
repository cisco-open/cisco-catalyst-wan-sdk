from typing import Any, Callable, Dict, Mapping, Type, Union

from pydantic import Field
from typing_extensions import Annotated

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

Input = AnyPolicyDefinition
Output = Annotated[
    Union[CustomControlParcel, HubSpokeParcel, MeshParcel, Ipv4AclParcel, Ipv6AclParcel], Field(discriminator="type_")
]


def _get_parcel_name_desc(policy_definition: AnyPolicyDefinition) -> Dict[str, Any]:
    return dict(parcel_name=policy_definition.name, parcel_description=policy_definition.description)


def control(in_: ControlPolicy, context) -> CustomControlParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {ControlPolicy.__name__}")
    out = CustomControlParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def hubspoke(in_: HubAndSpokePolicy, context) -> HubSpokeParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {HubAndSpokePolicy.__name__}")
    out = HubSpokeParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def ipv4acl(in_: AclPolicy, context) -> Ipv4AclParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {Ipv4AclParcel.__name__}")
    out = Ipv4AclParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def ipv6acl(in_: AclIPv6Policy, context) -> Ipv6AclParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {Ipv6AclParcel.__name__}")
    out = Ipv6AclParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def mesh(in_: MeshPolicy, context) -> MeshParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {MeshPolicy.__name__}")
    out = MeshParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    AclPolicy: ipv4acl,
    AclIPv6Policy: ipv6acl,
    ControlPolicy: control,
    HubAndSpokePolicy: hubspoke,
    MeshPolicy: mesh,
}


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    raise CatalystwanConverterCantConvertException(f"No converter found for {type(in_).__name__}")


def convert(in_: Input, context) -> Output:
    result = _find_converter(in_)(in_, context)
    result.model_validate(result)
    return result
