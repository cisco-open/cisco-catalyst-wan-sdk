from __future__ import annotations

from typing import Literal

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import _ParcelBase


class ConfigParcel(_ParcelBase):
    type_: Literal["config"] = Field(default="config", exclude=True)
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    config: str = Field(
        validation_alias=AliasPath("data", "config"),
        description="Config content",
    )
