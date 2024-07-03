import logging
from typing import Callable, Dict, List, Tuple, Union, cast
from uuid import UUID

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.api.builders.feature_profiles.report import FeatureProfileBuildReport
from catalystwan.endpoints.configuration_group import ConfigGroup
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import (
    PushContext,
    TransformedParcel,
    UX2Config,
    UX2ConfigPushResult,
)
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv4acl import Ipv4AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.acl.ipv6acl import Ipv6AclParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access import DeviceAccessIPv4Parcel
from catalystwan.models.configuration.feature_profile.sdwan.system.device_access_ipv6 import DeviceAccessIPv6Parcel
from catalystwan.models.configuration.profile_type import ProfileType
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.creators.references_updater import update_parcel_references

LOCALIZED_POLICY_PARCEL_TYPES = [
    "ipv4-device-access-policy",
    "ipv6-device-access-policy",
    "ipv4-acl",
    "ipv6-acl",
    "route",
]
AnyDeviceAccessParcel = Annotated[
    Union[DeviceAccessIPv4Parcel, DeviceAccessIPv6Parcel],
    Field(discriminator="type_"),
]
AnyAclParcel = Annotated[
    Union[Ipv4AclParcel, Ipv6AclParcel],
    Field(discriminator="type_"),
]

ProfileInfo = Tuple[ProfileType, UUID, str, List[TransformedParcel]]

logger = logging.getLogger(__name__)


class LocalizedPolicyPusher:
    """
    1. Associate selected Config Group with Default_Policy_Object_Profile
    2. Update selected Feature Profiles with Parcels originating from Localized Policy items (eg. acl, route)
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
        self._fp_api = session.api.sdwan_feature_profiles
        self._cg_api = session.api.config_group
        self._system_api = self._fp_api.system
        self._transport_api = self._fp_api.transport
        self._service_api = self._fp_api.service
        self.dns = session.api.sdwan_feature_profiles.dns_security
        self._push_result: UX2ConfigPushResult = push_result
        self._progress: Callable[[str, int, int], None] = progress
        self.push_context = push_context
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
                updated_id = self.push_context.id_lookup[transformed_cg.header.origin]
                result.append(updated_id)
        return result

    def _get_config_group_contents(self, cg_ids: List[UUID]) -> Dict[UUID, ConfigGroup]:
        result: Dict[UUID, ConfigGroup] = dict()
        for cg_id in cg_ids:
            cg = self._cg_api.get(cg_id)
            result[cg_id] = cg
        return result

    def _find_profiles_to_update(self) -> List[ProfileInfo]:
        profiles: List[ProfileInfo] = list()
        for transformed_profile in self._ux2_config.feature_profiles:
            if transformed_profile.header.localized_policy_subelements is not None:
                profile_type = cast(ProfileType, transformed_profile.header.type)
                name = transformed_profile.feature_profile.name
                updated_id = self.push_context.id_lookup[transformed_profile.header.origin]
                parcels = self._get_parcels_to_push(list(transformed_profile.header.localized_policy_subelements))
                profiles.append((profile_type, updated_id, name, parcels))
        return profiles

    def update_system_profile(
        self, profile_id: UUID, device_access: AnyDeviceAccessParcel, report: FeatureProfileBuildReport
    ):
        try:
            parcel_id = self._system_api.create_parcel(
                profile_id=profile_id, payload=update_parcel_references(device_access, self.push_context.id_lookup)
            ).id
            report.add_created_parcel(parcel_name=device_access.parcel_name, parcel_uuid=parcel_id)
        except ManagerHTTPError as e:
            logger.error(f"Error occured during creation of {device_access.type_} {device_access.parcel_name}: {e}")
            report.add_failed_parcel(
                parcel_name=device_access.parcel_name, parcel_type=device_access.type_, error_info=e.info
            )

    def associate_config_groups_with_default_policy_object_profile(self):
        for cg_id, cg in self._get_config_group_contents(self._find_config_groups_to_update()).items():
            profile_ids = [p.id for p in cg.profiles]
            profile_ids.append(self.push_context.default_policy_object_profile_id)
            try:
                self._cg_api.edit(
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
                parcel = transformed_parcel.parcel
                if profile_type == "system" and isinstance(parcel, (DeviceAccessIPv4Parcel, DeviceAccessIPv6Parcel)):
                    self.update_system_profile(
                        profile_id=profile_id, device_access=parcel, report=profile_reports[profile_id]
                    )
                elif profile_type == "service" and isinstance(parcel, RoutePolicyParcel):
                    logger.warning(f"not implemented: adding {parcel.parcel_name} parcel to profile: {profile_id}")
                elif profile_type == "transport" and isinstance(parcel, (Ipv4AclParcel, Ipv6AclParcel)):
                    logger.warning(f"not implemented: adding {parcel.parcel_name} parcel to profile: {profile_id}")
                else:
                    logger.warning(f"Unexpected profile type {profile_type} to add Localized Policy items, skipping")
