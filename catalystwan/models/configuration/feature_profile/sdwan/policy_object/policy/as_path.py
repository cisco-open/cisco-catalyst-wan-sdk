# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global


class AsPathEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    as_path: Global[str] = Field(validation_alias="asPath", serialization_alias="asPath")


class AsPathParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["as-path"] = Field(default="as-path", exclude=True)
    as_path_list_num: Global[int] = Field(validation_alias=AliasPath("data", "asPathListNum"))
    entries: List[AsPathEntry] = Field(default=[], validation_alias=AliasPath("data", "entries"))

    def add_as_path(self, as_path: str):
        self.entries.append(AsPathEntry(as_path=as_global(as_path)))
