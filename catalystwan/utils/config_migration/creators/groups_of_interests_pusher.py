import logging
from typing import Dict, Mapping, Optional, Type, cast
from uuid import UUID

from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel, Parcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import (
    AdvancedInspectionProfileParcel,
    AnyPolicyObjectParcel,
    IntrusionPreventionParcel,
    SslDecryptionProfileParcel,
    UrlFilteringParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.app_probe import AppProbeParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.sla_class import SLAClassParcel
from catalystwan.typed_list import DataSequence
from catalystwan.utils.config_migration.creators.pusher import Pusher, PusherConfig

from .references_updater import update_parcel_references

logger = logging.getLogger(__name__)

POLICY_OBJECTS_PUSH_ORDER: Mapping[Type[AnyParcel], int] = {
    UrlFilteringParcel: 1,
    SslDecryptionProfileParcel: 1,
    IntrusionPreventionParcel: 1,
    AppProbeParcel: 1,
    AdvancedInspectionProfileParcel: 2,
    SLAClassParcel: 2,
}


def get_parcel_ordering_value(parcel: Type[AnyParcel]) -> int:
    return POLICY_OBJECTS_PUSH_ORDER.get(parcel, 0)


class GroupsOfInterestPusher(Pusher):
    def __init__(
        self,
        config: PusherConfig,
    ) -> None:
        self.load_config(config)
        self.dns = self._session.api.sdwan_feature_profiles.dns_security
        self._policy_object_api = self._session.api.sdwan_feature_profiles.policy_object

    def cast_(self, parcel: AnyParcel) -> AnyPolicyObjectParcel:
        return parcel  # type: ignore

    def push(self) -> None:
        profile_id = self.get_or_create_default_policy_object_profile()
        self._push_context.default_policy_object_profile_id = profile_id

        if profile_id is None:
            logger.error("Cannot create Groups of Interest without Default Policy Object Profile")
            return

        profile_rollback = self._push_result.rollback.add_default_policy_object_profile_id(profile_id)

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
            parcel = self.cast_(transformed_parcel.parcel)
            header = transformed_parcel.header
            parcel_type = type(parcel)

            # update existing system created parcels
            if not system_created_parcels.get(parcel_type):
                system_created_parcels[parcel_type] = {}
                exsisting_parcel_list = cast(
                    DataSequence[Parcel[AnyPolicyObjectParcel]],
                    self._policy_object_api.get(profile_id, parcel_type).filter(  # type: ignore [arg-type]
                        created_by="system"
                    ),
                )
                for ep in exsisting_parcel_list:
                    system_created_parcels[parcel_type][ep.payload.parcel_name] = ep.parcel_id

            # if parcel with given name exists we skip it
            if system_created_parcels[parcel_type].get(header.origname or ""):
                continue

            try:
                self._progress(
                    f"Creating Policy Object Parcel: {parcel.parcel_name}",
                    i + 1,
                    len(transformed_parcels),
                )
                parcel = update_parcel_references(parcel, self._push_context.id_lookup)
                parcel_id = self._policy_object_api.create_parcel(profile_id=profile_id, payload=parcel).id
                profile_rollback.add_parcel(parcel.type_, parcel_id)
                self._push_result.report.groups_of_interest.add_created(parcel.parcel_name, parcel_id)
                self._push_context.id_lookup[transformed_parcel.header.origin] = parcel_id

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
