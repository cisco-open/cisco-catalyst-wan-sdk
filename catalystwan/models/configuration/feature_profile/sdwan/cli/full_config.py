from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class FullConfigParcel(_ParcelBase):
    type_: Literal["full-config"] = Field(default="full-config", exclude=True)
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    fullconfig: str = Field(validation_alias=AliasPath("data", "fullconfig"))
    documentation: Any = None
