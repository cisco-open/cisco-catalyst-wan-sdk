import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Mapping, Optional, Type, cast
from uuid import UUID

from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import PushContext, UX2Config, UX2ConfigPushResult
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, RefIdItem
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel, Parcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AdvancedInspectionProfileParcel,
    AnyPolicyObjectParcel,
    IntrusionPreventionParcel,
    SslDecryptionProfileParcel,
    UrlFilteringParcel,
)
from catalystwan.session import ManagerSession
from catalystwan.typed_list import DataSequence
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

logger = logging.getLogger(__name__)


@dataclass
class ReferencesUpdater(ABC):
    parcel: AnyPolicyObjectParcel
    pushed_objects_map: Dict[UUID, UUID]

    @abstractmethod
    def update_references(self):
        pass

    def get_target_uuid(self, origin_uuid: UUID) -> UUID:
        if v2_uuid := self.pushed_objects_map.get(origin_uuid):
            return v2_uuid

        raise CatalystwanConverterCantConvertException(
            f"Cannot find transferred policy object based on v1 API id: {origin_uuid}"
        )


class UrlFilteringReferencesUpdater(ReferencesUpdater):
    def update_references(self):
        if allowed_list := self.parcel.url_allowed_list:
            v2_uuid = self.get_target_uuid(UUID(allowed_list.ref_id.value))
            self.parcel.url_allowed_list = RefIdItem.from_uuid(v2_uuid)

        if blocked_list := self.parcel.url_blocked_list:
            v2_uuid = self.get_target_uuid(UUID(blocked_list.ref_id.value))
            self.parcel.url_blocked_list = RefIdItem.from_uuid(v2_uuid)


class SslProfileReferencesUpdater(ReferencesUpdater):
    def update_references(self):
        if allowed_list := self.parcel.url_allowed_list:
            v2_uuid = self.get_target_uuid(UUID(allowed_list.ref_id.value))
            self.parcel.url_allowed_list = RefIdItem.from_uuid(v2_uuid)

        if blocked_list := self.parcel.url_blocked_list:
            v2_uuid = self.get_target_uuid(UUID(blocked_list.ref_id.value))
            self.parcel.url_blocked_list = RefIdItem.from_uuid(v2_uuid)


class IntrusionPreventionReferencesUpdater(ReferencesUpdater):
    def update_references(self):
        if allowed_list := self.parcel.signature_allowed_list:
            v2_uuid = self.get_target_uuid(UUID(allowed_list.ref_id.value))
            self.parcel.signature_allowed_list = RefIdItem.from_uuid(v2_uuid)


class AdvancedInspectionProfileReferencesUpdater(ReferencesUpdater):
    def update_references(self):
        if advanced_malware_protection := self.parcel.advanced_malware_protection:
            v2_uuid = self.get_target_uuid(UUID(advanced_malware_protection.ref_id.value))
            self.parcel.advanced_malware_protection = RefIdItem.from_uuid(v2_uuid)

        if intrusion_prevention := self.parcel.intrusion_prevention:
            v2_uuid = self.get_target_uuid(UUID(intrusion_prevention.ref_id.value))
            self.parcel.intrusion_prevention = RefIdItem.from_uuid(v2_uuid)

        if ssl_decryption_profile := self.parcel.ssl_decryption_profile:
            v2_uuid = self.get_target_uuid(UUID(ssl_decryption_profile.ref_id.value))
            self.parcel.ssl_decryption_profile = RefIdItem.from_uuid(v2_uuid)

        if url_filtering := self.parcel.url_filtering:
            v2_uuid = self.get_target_uuid(UUID(url_filtering.ref_id.value))
            self.parcel.url_filtering = RefIdItem.from_uuid(v2_uuid)


REFERENCES_UPDATER_MAPPING: Mapping[type, Type[ReferencesUpdater]] = {
    UrlFilteringParcel: UrlFilteringReferencesUpdater,
    SslDecryptionProfileParcel: SslProfileReferencesUpdater,
    IntrusionPreventionParcel: IntrusionPreventionReferencesUpdater,
    AdvancedInspectionProfileParcel: AdvancedInspectionProfileReferencesUpdater,
}

POLICY_OBJECTS_PUSH_ORDER: Mapping[Type[AnyParcel], int] = {
    UrlFilteringParcel: 1,
    SslDecryptionProfileParcel: 1,
    IntrusionPreventionParcel: 1,
    AdvancedInspectionProfileParcel: 2,
}


def get_parcel_ordering_value(parcel: Type[AnyParcel]) -> int:
    return POLICY_OBJECTS_PUSH_ORDER.get(parcel, 0)


def update_parcels_references(parcel: AnyPolicyObjectParcel, pushed_objects_map: Dict[UUID, UUID]) -> None:
    if ref_updater := REFERENCES_UPDATER_MAPPING.get(type(parcel)):
        ref_updater(parcel, pushed_objects_map=pushed_objects_map).update_references()


class PolicyObjectPusher:
    def __init__(
        self,
        ux2_config: UX2Config,
        session: ManagerSession,
        push_result: UX2ConfigPushResult,
        push_context: PushContext,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._ux2_config = ux2_config
        self._policy_object_api: PolicyObjectFeatureProfileAPI = session.api.sdwan_feature_profiles.policy_object
        self._push_result: UX2ConfigPushResult = push_result
        self._progress: Callable[[str, int, int], None] = progress
        self.push_context = push_context

    def push(self):
        profile_id = self.get_or_create_default_policy_object_profile()
        self.push_context.default_policy_object_profile_id = profile_id
        self.push_groups_of_interests_objects()

    def push_groups_of_interests_objects(self):
        default_profile_id = self.push_context.default_policy_object_profile_id
        if default_profile_id is None:
            logger.error("Cannot create Groups of Interest without Default Policy Object Profile")
            return

        def cast_(parcel: AnyParcel) -> AnyPolicyObjectParcel:
            return parcel  # type: ignore

        profile_rollback = self._push_result.rollback.add_default_policy_object_profile_id(default_profile_id)

        # will hold system created parcels id by type and name when detected
        system_created_parcels: Dict[Type[AnyPolicyObjectParcel], Dict[str, UUID]] = {}

        transformed_parcels = sorted(
            [
                transformed_parcel
                for transformed_parcel in self._ux2_config.profile_parcels
                if type(transformed_parcel.parcel) in list_types(AnyPolicyObjectParcel)
            ],
            key=lambda x: get_parcel_ordering_value(type(x.parcel)),  # sorter
        )

        for i, transformed_parcel in enumerate(transformed_parcels):
            parcel = cast_(transformed_parcel.parcel)
            header = transformed_parcel.header
            parcel_type = type(parcel)

            # update existing system created parcels
            if not system_created_parcels.get(parcel_type):
                system_created_parcels[parcel_type] = {}
                exsisting_parcel_list = cast(
                    DataSequence[Parcel[AnyPolicyObjectParcel]],
                    self._policy_object_api.get(default_profile_id, parcel_type).filter(  # type: ignore [arg-type]
                        created_by="system"
                    ),
                )
                for ep in exsisting_parcel_list:
                    id_ = UUID(ep.parcel_id) if not isinstance(ep.parcel_id, UUID) else ep.parcel_id
                    system_created_parcels[parcel_type][ep.payload.parcel_name] = id_

            # if parcel with given name exists we skip it
            if system_created_parcels[parcel_type].get(header.origname or ""):
                continue

            try:
                update_parcels_references(parcel, self.push_context.id_lookup)

                parcel_id = self._policy_object_api.create(profile_id=default_profile_id, payload=parcel).id
                profile_rollback.add_parcel(parcel.type_, parcel_id)
                self._push_result.report.groups_of_interest.add_created(parcel.parcel_name, parcel_id)
                self.push_context.id_lookup[transformed_parcel.header.origin] = parcel_id

                self._progress(
                    f"Creating Policy Object Parcel: {parcel.parcel_name}",
                    i + 1,
                    len(transformed_parcels),
                )
            except ManagerHTTPError as e:
                logger.error(f"Error occured during config group creation: {e.info}")
                self._push_result.report.groups_of_interest.add_failed(parcel, e)

    def get_or_create_default_policy_object_profile(self) -> Optional[UUID]:
        profiles = self._policy_object_api.get_profiles()
        if len(profiles) >= 1:
            return profiles[0].profile_id
        try:
            profile_id = self._policy_object_api.create_profile(
                FeatureProfileCreationPayload(
                    name="Policy_Profile_Global", description="Policy_Profile_Global_description"
                )
            ).id
        except ManagerHTTPError:
            profile_id = None
        return profile_id
