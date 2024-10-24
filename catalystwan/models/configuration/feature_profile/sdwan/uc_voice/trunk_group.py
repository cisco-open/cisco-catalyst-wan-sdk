# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.common import HuntSchemeChannel, HuntSchemeDirection, HuntSchemeMethod


class TrunkGroupParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["trunk-group"] = Field(default="trunk-group", exclude=True)
    hunt_scheme_method: Union[Variable, Global[HuntSchemeMethod], Default[None]] = Field(
        validation_alias=AliasPath("data", "huntSchemeMethod")
    )
    max_calls_in: Union[Variable, Global[int], Default[None]] = Field(validation_alias=AliasPath("data", "maxCallsIn"))
    max_calls_out: Union[Variable, Global[int], Default[None]] = Field(
        validation_alias=AliasPath("data", "maxCallsOut")
    )
    max_retries: Union[Variable, Global[int], Default[None]] = Field(validation_alias=AliasPath("data", "maxRetries"))
    hunt_scheme_channel: Optional[Union[Variable, Global[HuntSchemeChannel], Default[None]]] = Field(
        default=None, validation_alias=AliasPath("data", "huntSchemeChannel")
    )
    hunt_scheme_direction: Optional[Union[Global[HuntSchemeDirection], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "huntSchemeDirection")
    )
