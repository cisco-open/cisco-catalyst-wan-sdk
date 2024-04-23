from collections import defaultdict
from typing import Dict, List, cast
from uuid import UUID

from catalystwan.models.configuration.config_migration import TransformedParcel
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyAssociatoryParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.session import ManagerSession


class ParcelPusher:
    """
    Base class for pushing parcels to a feature profile.
    """

    def __init__(self, session: ManagerSession, profile_type: ProfileType):
        self.builder = session.api.builders.feature_profiles.create_builder(profile_type)

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> UUID:
        raise NotImplementedError


class SimpleParcelPusher(ParcelPusher):
    """
    Simple implementation of ParcelPusher that creates parcels directly.
    Includes: Other and System feature profiles.
    """

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> UUID:
        for transformed_parcel in target_parcels:
            self.builder.add_parcel(transformed_parcel.parcel)  # type: ignore
        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()


class ServiceParcelPusher(ParcelPusher):
    """
    Parcel pusher for service feature profiles.
    """

    def __init__(self, session: ManagerSession, profile_type: ProfileType):
        super().__init__(session, profile_type)
        self.subparcel_name_counter: Dict[str, int] = defaultdict(lambda: 0)

    def push(
        self,
        feature_profile: FeatureProfileCreationPayload,
        target_parcels: List[TransformedParcel],
        all_parcels: Dict[UUID, TransformedParcel],
    ) -> UUID:
        for transformed_parcel in target_parcels:
            parcel = transformed_parcel.parcel
            if not isinstance(parcel, LanVpnParcel):
                self.builder.add_parcel(parcel)  # type: ignore
            else:
                vpn_tag = self.builder.add_parcel_vpn(parcel)  # type: ignore
                for transformed_subparcel in [
                    all_parcels.get(element) for element in transformed_parcel.header.subelements
                ]:
                    parcel = self._resolve_parcel_naming(transformed_subparcel)  # type: ignore
                    self.builder.add_parcel_vpn_subparcel(vpn_tag, parcel)  # type: ignore
        self.builder.add_profile_name_and_description(feature_profile)
        return self.builder.build()

    def _resolve_parcel_naming(self, transformed_subparcel: TransformedParcel) -> AnyAssociatoryParcel:
        """This occurs when a Device Template has many VPNs and the VPNs have assigned the same subcomponent.
        In UX2 every subparcel has to be unique, so we have to rename the subparcels to avoid conflicts.
        We check if the same name exist and if it does we add a counter to the name,
        create copy and change the name with the counter value.
        """
        self.subparcel_name_counter[transformed_subparcel.parcel.parcel_name] += 1
        parcel = cast(AnyAssociatoryParcel, transformed_subparcel.parcel)
        count_value = self.subparcel_name_counter[parcel.parcel_name]
        if count_value > 1:
            parcel = parcel.model_copy(deep=True)
            parcel.parcel_name += f"_{count_value}"
        return parcel
