from typing import Any, Callable, Dict, Mapping, Type, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.policy import AnyPolicyDefinition
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

Input = AnyPolicyDefinition
Output = Annotated[Union[CustomControlParcel, HubSpokeParcel, MeshParcel], Field(discriminator="type_")]


def _get_parcel_name_desc(policy_definition: AnyPolicyDefinition) -> Dict[str, Any]:
    return dict(parcel_name=policy_definition.name, parcel_description=policy_definition.description)


def control(in_: ControlPolicy, **context) -> CustomControlParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {MeshPolicy.__name__}")
    out = CustomControlParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def hubspoke(in_: HubAndSpokePolicy, **context) -> HubSpokeParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {MeshPolicy.__name__}")
    out = HubSpokeParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


def mesh(in_: MeshPolicy, **context) -> MeshParcel:
    if not context:
        raise CatalystwanConverterCantConvertException(f"Additional context required for {MeshPolicy.__name__}")
    out = MeshParcel(**_get_parcel_name_desc(in_))
    # TODO: convert definition
    return out


CONVERTERS: Mapping[Type[Input], Callable[..., Output]] = {
    ControlPolicy: control,
    HubAndSpokePolicy: hubspoke,
    MeshPolicy: mesh,
}


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    raise CatalystwanConverterCantConvertException(f"No converter found for {type(in_).__name__}")


def convert(in_: Input, **context) -> Output:
    return _find_converter(in_)(in_, **context)
