import logging
from typing import Callable, Dict, List, Literal, Tuple, Union, cast
from uuid import UUID

from pydantic import Field, ValidationError
from typing_extensions import Annotated

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.endpoints.configuration_group import ConfigGroup
from catalystwan.exceptions import ManagerErrorInfo, ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    PushContext,
    TransformedParcel,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.parcel import list_types
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access import DeviceAccessIPv4Parcel
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import DeviceAccessIPv6Parcel
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.references_updater import update_parcel_references

_AnyTransportPolicyFeatureParcel = Annotated[
    Union[Ipv4AclParcel, Ipv6AclParcel, RoutePolicyParcel],
    Field(discriminator="type_"),
]
_AnyServicePolicyFeatureParcel = Annotated[
    Union[Ipv4AclParcel, Ipv6AclParcel, RoutePolicyParcel],
    Field(discriminator="type_"),
]
_AnySystemPolicyFeatureParcel = Annotated[
    Union[DeviceAccessIPv4Parcel, DeviceAccessIPv6Parcel],
    Field(discriminator="type_"),
]
_AnyLocalizedPolicyParcel = Annotated[
    Union[_AnyTransportPolicyFeatureParcel, _AnyServicePolicyFeatureParcel, _AnySystemPolicyFeatureParcel],
    Field(discriminator="type_"),
]
_LocalizedPolicyProfileTypes = Literal["transport", "service", "system"]
LOCALIZED_POLICY_PARCEL_TYPES = [t._get_parcel_type() for t in list_types(_AnyLocalizedPolicyParcel)]

_ProfileInfo = Tuple[_LocalizedPolicyProfileTypes, UUID, str, List[TransformedParcel]]

logger = logging.getLogger(__name__)


class LocalizedPolicyPusher:
    """
    1. Associate selected Config Group with Default_Policy_Object_Profile
    2. Update selected Feature Profiles by pushing Parcels originating from Localized Policy items (eg. acl, route)
    Update needs to be performed after Feature Profiles are already populated with VPN parcels
    and Default_Policy_Object_Profile is populated with Groups of Interest
    """

    def __init__(
        self,
        ux2_config: UX2Config,
        session: ManagerSession,
        push_result: UX2ConfigPushResult,
        push_context: PushContext,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._ux2_config = ux2_config
        self._session = session
        self._cg_api = session.api.config_group
        self._push_result: UX2ConfigPushResult = push_result
        self._push_context = push_context
        self._progress: Callable[[str, int, int], None] = progress
        self._parcel_by_id = self._create_parcel_by_id_lookup()

    def _create_parcel_by_id_lookup(self) -> Dict[UUID, TransformedParcel]:
        lookup: Dict[UUID, TransformedParcel] = dict()
        for transformed_parcel in self._ux2_config.profile_parcels:
            if transformed_parcel.header.type in LOCALIZED_POLICY_PARCEL_TYPES:
                lookup[transformed_parcel.header.origin] = transformed_parcel
        return lookup

    def _create_profile_report_by_id_lookup(self, profile_ids: List[UUID]) -> Dict[UUID, FeatureProfileBuildReport]:
        lookup: Dict[UUID, FeatureProfileBuildReport] = dict()
        for cg_report in self._push_result.report.config_groups:
            for fp_report in cg_report.feature_profiles:
                if fp_report.profile_uuid in profile_ids:
                    lookup[fp_report.profile_uuid] = fp_report
        return lookup

    def _get_parcels_to_push(self, parcel_ids: List[UUID]) -> List[TransformedParcel]:
        result: List[TransformedParcel] = list()
        for parcel_id in parcel_ids:
            if parcel := self._parcel_by_id.get(parcel_id):
                result.append(parcel)
        return result

    def _find_config_groups_to_update(self) -> List[UUID]:
        result: List[UUID] = list()
        for transformed_cg in self._ux2_config.config_groups:
            if transformed_cg.header.localized_policy_subelements is not None:
                updated_id = self._push_context.id_lookup[transformed_cg.header.origin]
                result.append(updated_id)
        return result

    def _get_config_group_contents(self, cg_ids: List[UUID]) -> Dict[UUID, ConfigGroup]:
        result: Dict[UUID, ConfigGroup] = dict()
        for cg_id in cg_ids:
            cg = self._cg_api.get(cg_id)
            result[cg_id] = cg
        return result

    def _find_profiles_to_update(self) -> List[_ProfileInfo]:
        profiles: List[_ProfileInfo] = list()
        for transformed_profile in self._ux2_config.feature_profiles:
            if transformed_profile.header.localized_policy_subelements is not None:
                profile_type = cast(_LocalizedPolicyProfileTypes, transformed_profile.header.type)
                name = transformed_profile.feature_profile.name
                updated_id = self._push_context.id_lookup[transformed_profile.header.origin]
                parcels = self._get_parcels_to_push(list(transformed_profile.header.localized_policy_subelements))
                profiles.append((profile_type, updated_id, name, parcels))
        return profiles

    def _update_transport_profile(
        self,
        profile_id: UUID,
        parcel: _AnyTransportPolicyFeatureParcel,
    ) -> UUID:
        api = self._session.api.sdwan_feature_profiles.transport
        parcel.parcel_name += "_transport"
        return api.create_parcel(profile_id=profile_id, payload=parcel).id

    def _update_service_profile(
        self,
        profile_id: UUID,
        parcel: _AnyServicePolicyFeatureParcel,
    ):
        api = self._session.api.sdwan_feature_profiles.service
        parcel.parcel_name += "_service"
        return api.create_parcel(profile_id=profile_id, payload=parcel).id

    def _update_system_profile(
        self,
        profile_id: UUID,
        parcel: _AnySystemPolicyFeatureParcel,
    ):
        api = self._session.api.sdwan_feature_profiles.system
        parcel.parcel_name += "_system"
        return api.create_parcel(profile_id=profile_id, payload=parcel).id

    def associate_config_groups_with_default_policy_object_profile(self):
        for cg_id, cg in self._get_config_group_contents(self._find_config_groups_to_update()).items():
            profile_ids = [p.id for p in cg.profiles]
            profile_ids.append(self._push_context.default_policy_object_profile_id)
            try:
                api = self._session.api.config_group
                api.edit(
                    cg_id=str(cg_id),
                    name=cg.name,
                    description=cg.description,
                    solution=cg.solution,
                    profile_ids=profile_ids,
                )
            except ManagerHTTPError as e:
                logger.error(f"Error occured during config group edit: {e}")

    def push(self):
        self._progress("Associating Config Groups with Default Policy Object Profile", 0, 1)
        self.associate_config_groups_with_default_policy_object_profile()
        self._progress("Associating Config Groups with Default Policy Object Profile", 1, 1)
        profile_infos = self._find_profiles_to_update()
        profile_ids = [t[1] for t in profile_infos]
        profile_reports = self._create_profile_report_by_id_lookup(profile_ids)
        for i, profile_info in enumerate(profile_infos):
            profile_type, profile_id, profile_name, transformed_parcels = profile_info
            self._progress(f"Updating {profile_name} profile with policy parcels", i + 1, len(profile_ids))
            for transformed_parcel in transformed_parcels:
                report = profile_reports[profile_id]
                error_parcel = transformed_parcel.parcel
                error_info: Union[ManagerErrorInfo, str, None] = None
                try:
                    parcel_copy = update_parcel_references(transformed_parcel.parcel, self._push_context.id_lookup)
                    error_parcel = parcel_copy
                    if profile_type == "transport":
                        parcel_id = self._update_transport_profile(profile_id=profile_id, parcel=parcel_copy)
                    elif profile_type == "service":
                        parcel_id = self._update_service_profile(profile_id=profile_id, parcel=parcel_copy)
                    elif profile_type == "system":
                        parcel_id = self._update_system_profile(profile_id=profile_id, parcel=parcel_copy)
                    report.add_created_parcel(parcel_name=parcel_copy.parcel_name, parcel_uuid=parcel_id)
                except ValidationError as validation_error:
                    error_info = str(validation_error)
                except ManagerHTTPError as http_error:
                    error_info = http_error.info
                if error_info is not None:
                    report.add_failed_parcel(
                        parcel_name=error_parcel.parcel_name, parcel_type=error_parcel.type_, error_info=error_info
                    )
