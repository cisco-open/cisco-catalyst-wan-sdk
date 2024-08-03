# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global, as_optional_global
from catalystwan.models.common import TLOCColor
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class AppProbeMapItem(BaseModel):
    color: Global[TLOCColor]
    dscp: Optional[Global[int]] = Field(default=None)


class AppProbeEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    map: List[AppProbeMapItem] = Field(default=[])
    forwarding_class: Union[Global[str], RefIdItem] = Field(
        validation_alias="forwardingClass",
        serialization_alias="forwardingClass",
        description="RefId option introduced in 20.14",
    )


class AppProbeParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["app-probe"] = Field(default="app-probe", exclude=True)
    entries: List[AppProbeEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def _insert_entry(self, entry: AppProbeEntry) -> None:
        if self.entries:
            self.entries[0] = entry
        else:
            self.entries.append(entry)

    def set_fowarding_class_name(self, name: str):
        self._insert_entry(
            AppProbeEntry(
                forwarding_class=as_global(name),
            )
        )

    def set_fowarding_class_id(self, id: UUID):
        # use only for version >= 20.14
        self._insert_entry(
            AppProbeEntry(
                forwarding_class=RefIdItem.from_uuid(id),
            )
        )

    def add_map(self, color: TLOCColor, dscp: Optional[int] = None):
        entry = self.entries[0]
        entry.map.append(AppProbeMapItem(color=as_global(color, TLOCColor), dscp=as_optional_global(dscp)))
