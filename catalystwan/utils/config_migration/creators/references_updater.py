from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Mapping, Type
from uuid import UUID

from catalystwan.models.configuration.feature_profile.parcel import AnyParcel
from catalystwan.utils.config_migration.converters.exceptions import CatalystwanConverterCantConvertException


@dataclass
class ReferencesUpdater(ABC):
    parcel: AnyParcel
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


def update_parcels_references(
    parcel: AnyParcel,
    pushed_objects_map: Dict[UUID, UUID],
    updaters_map: Mapping[Type[AnyParcel], Type[ReferencesUpdater]],
) -> None:
    if ref_updater := updaters_map.get(type(parcel)):
        ref_updater(parcel, pushed_objects_map=pushed_objects_map).update_references()
