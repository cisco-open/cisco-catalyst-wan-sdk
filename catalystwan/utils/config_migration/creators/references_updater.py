from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Mapping, Type, Union, cast
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

    def get_target_uuid(self, origin_uuid: Union[str, UUID]) -> UUID:
        _origin_uuid: UUID = cast(UUID, UUID(origin_uuid) if type(origin_uuid) is str else origin_uuid)
        if target_uuid := self.pushed_objects_map.get(_origin_uuid):
            return target_uuid

        raise CatalystwanConverterCantConvertException(
            f"Cannot find transferred policy object based on v1 API id: {_origin_uuid}"
        )


def update_parcels_references(
    parcel: AnyParcel,
    pushed_objects_map: Dict[UUID, UUID],
    updaters_map: Mapping[Type[AnyParcel], Type[ReferencesUpdater]],
) -> None:
    if ref_updater := updaters_map.get(type(parcel)):
        ref_updater(parcel, pushed_objects_map=pushed_objects_map).update_references()
