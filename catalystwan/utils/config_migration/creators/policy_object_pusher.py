import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, Mapping, Type, cast
from uuid import UUID

from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.config_migration import TransformedParcel, UX2Config, UX2ConfigPushResult
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, RefIdItem
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel, Parcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AnyPolicyObjectParcel,
    UrlFilteringParcel,
)
from catalystwan.session import ManagerSession
from catalystwan.typed_list import DataSequence
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException

logger = logging.getLogger(__name__)


@dataclass
class ReferencesUpdater(ABC):
    transformed_parcel: TransformedParcel
    pushed_objects_map: Dict[UUID, UUID]

    def get_parcel(self) -> AnyParcel:
        return self.transformed_parcel.parcel

    @abstractmethod
    def update_references(self):
        pass

    @abstractmethod
    def are_references_update_required(self) -> bool:
        pass

    def get_v2_uuid_of_transferred_v1_policy(self, v1_uuid: UUID) -> UUID:
        if v2_uuid := self.pushed_objects_map.get(v1_uuid):
            return v2_uuid

        raise CatalystwanConverterCantConvertException(
            f"Cannot find transferred policy object based on v1 API id: {v1_uuid}"
        )


class DummyReferencesUpdater(ReferencesUpdater):
    def update_references(self):
        return

    def are_references_update_required(self) -> bool:
        return False


class UrlFilteringReferencesUpdater(ReferencesUpdater):
    def are_references_update_required(self) -> bool:
        url_filtering = cast(UrlFilteringParcel, self.transformed_parcel.parcel)
        return bool(url_filtering.url_blocked_list or url_filtering.url_allowed_list)

    def update_references(self):
        if not self.are_references_update_required():
            return

        if allowed_list := self.transformed_parcel.parcel.url_allowed_list:
            v2_uuid = self.get_v2_uuid_of_transferred_v1_policy(UUID(allowed_list.ref_id.value))
            self.transformed_parcel.parcel.url_allowed_list = RefIdItem.from_uuid(v2_uuid)

        if blocked_list := self.transformed_parcel.parcel.url_blocked_list:
            v2_uuid = self.get_v2_uuid_of_transferred_v1_policy(UUID(blocked_list.ref_id.value))
            self.transformed_parcel.parcel.url_blocked_list = RefIdItem.from_uuid(v2_uuid)


REFERENCES_UPDATER_MAPPING: Mapping[str, Callable] = {"UrlFilteringParcel": UrlFilteringReferencesUpdater}


def create_references_updater(
    transformed_parcel: TransformedParcel,
    pushed_objects_map: Dict[UUID, UUID],
) -> ReferencesUpdater:
    type_name = type(transformed_parcel.parcel).__name__
    return REFERENCES_UPDATER_MAPPING.get(type_name, DummyReferencesUpdater)(
        transformed_parcel=transformed_parcel,
        pushed_objects_map=pushed_objects_map,
    )


class PolicyObjectPusher:
    def __init__(
        self,
        ux2_config: UX2Config,
        session: ManagerSession,
        push_result: UX2ConfigPushResult,
        progress: Callable[[str, int, int], None],
    ) -> None:
        self._ux2_config = ux2_config
        self._policy_object_api: PolicyObjectFeatureProfileAPI = session.api.sdwan_feature_profiles.policy_object
        self._push_result: UX2ConfigPushResult = push_result
        self._progress: Callable[[str, int, int], None] = progress
        self._pushed_objects_map: Dict[UUID, UUID] = {}

    def push(self):
        default_profile_id = self.get_or_create_default_policy_object_profile()
        self.push_groups_of_interests_objects(default_profile_id)

    def push_groups_of_interests_objects(self, default_profile_id: UUID):
        # TODO: fix typing issues in this method, probably we need literal containig AnyPolicyObjectType type_
        def cast_(parcel: AnyParcel) -> AnyPolicyObjectParcel:
            return parcel  # type: ignore

        profile_rollback = self._push_result.rollback.add_default_policy_object_profile(default_profile_id)

        # will hold system created parcels id by type and name when detected
        system_created_parcels: Dict[Type[AnyPolicyObjectParcel], Dict[str, UUID]] = {}

        transormed_policies_ref_updaters = [
            create_references_updater(transformed_parcel, self._pushed_objects_map)
            for transformed_parcel in self._ux2_config.profile_parcels
            if type(transformed_parcel.parcel) in list_types(AnyPolicyObjectParcel)
        ]

        for i, transormed_policy_ref_updater in enumerate(transormed_policies_ref_updaters):
            parcel = cast_(transormed_policy_ref_updater.get_parcel())
            header = transormed_policy_ref_updater.transformed_parcel.header
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
            if system_created_parcels[parcel_type].get(header.origname or ""):  # changed
                continue

            try:
                transormed_policy_ref_updater.update_references()
                parcel_id = self._policy_object_api.create(profile_id=default_profile_id, payload=parcel).id
                profile_rollback.add_parcel(parcel.type_, parcel_id)
                self._push_result.report.groups_of_interest.add_created(parcel.parcel_name, parcel_id)
                self._pushed_objects_map[transormed_policy_ref_updater.transformed_parcel.header.origin] = parcel_id

                self._progress(
                    f"Creating Policy Object Parcel: {parcel.parcel_name}",
                    i + 1,
                    len(transormed_policies_ref_updaters),
                )
            except ManagerHTTPError as e:
                logger.error(f"Error occured during config group creation: {e.info}")
                self._push_result.report.groups_of_interest.add_failed(parcel, e)

    def get_or_create_default_policy_object_profile(self) -> UUID:
        profiles = self._policy_object_api.get_profiles()
        if len(profiles) >= 1:
            return profiles[0].profile_id
        profile_id = self._policy_object_api.create_profile(
            FeatureProfileCreationPayload(name="Policy_Profile_Global", description="Policy_Profile_Global_description")
        ).id
        return profile_id
