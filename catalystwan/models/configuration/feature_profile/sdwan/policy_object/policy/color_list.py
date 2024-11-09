# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry, as_global
from catalystwan.models.common import TLOCColor


class ColorEntry(_ParcelEntry):
    color: Global[TLOCColor]


class ColorParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["color"] = Field(default="color", exclude=True)
    entries: List[ColorEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_color(self, color: TLOCColor):
        self.entries.append(ColorEntry(color=as_global(color, TLOCColor)))
