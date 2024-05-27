from typing import Any, Callable, Dict, List, Mapping, Optional, Type, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.amp import (
    AdvancedMalwareProtectionParcel,
    FileAnalysisAlert,
    FileAnalysisFileTypes,
    FileAnalysisServer,
    FileReputationServer,
)
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.policy import AnyPolicyDefinition
from catalystwan.models.policy.definition.amp import AdvancedMalwareProtectionPolicy
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

Input = AnyPolicyDefinition
Output = Annotated[
    Union[CustomControlParcel, HubSpokeParcel, MeshParcel, AdvancedMalwareProtectionParcel],
    Field(discriminator="type_"),
]


def _get_parcel_name_desc(policy_definition: AnyPolicyDefinition) -> Dict[str, Any]:
    return dict(parcel_name=policy_definition.name, parcel_description=policy_definition.description)


def advanced_malware_protection(in_: AdvancedMalwareProtectionPolicy, **context) -> AdvancedMalwareProtectionParcel:
    raise CatalystwanConverterCantConvertException("TODO: vpn id")

    if not in_.definition.file_reputation_alert:
        raise CatalystwanConverterCantConvertException("AMP file reputation alert shall not be an empty str.")

    _file_analysis_alert = in_.definition.file_analysis_alert if in_.definition.file_analysis_alert else None
    _file_analysis_cloud_server = (
        in_.definition.file_analysis_cloud_server if in_.definition.file_analysis_cloud_server else None
    )

    out = AdvancedMalwareProtectionParcel(
        file_reputation_cloud_server=Global[FileReputationServer](value=in_.definition.file_reputation_cloud_server),
        file_reputation_est_server=Global[FileReputationServer](value=in_.definition.file_reputation_est_server),
        match_all_vpn=as_global(in_.definition.match_all_vpn),
        file_analysis_enabled=as_global(in_.definition.file_analysis_enabled),
        file_analysis_file_types=Global[List[FileAnalysisFileTypes]](value=in_.definition.file_analysis_file_types),
        file_analysis_alert=Global[Optional[FileAnalysisAlert]](value=_file_analysis_alert),
        file_analysis_cloud_server=Global[Optional[FileAnalysisServer]](value=_file_analysis_cloud_server),
        **_get_parcel_name_desc(in_),
    )
    # varget vpns is no available
    return out


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
    AdvancedMalwareProtectionPolicy: advanced_malware_protection,  # todo VPN id
}


def _find_converter(in_: Input) -> Callable[..., Output]:
    for key in CONVERTERS.keys():
        if isinstance(in_, key):
            return CONVERTERS[key]
    raise CatalystwanConverterCantConvertException(f"No converter found for {type(in_).__name__}")


def convert(in_: Input, **context) -> Output:
    return _find_converter(in_)(in_, **context)
