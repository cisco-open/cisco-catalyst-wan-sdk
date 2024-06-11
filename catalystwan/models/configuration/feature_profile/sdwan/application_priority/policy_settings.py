# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, _ParcelBase


class Cflowd(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    value: bool
    option_type: Literal["network-settings"] = Field(
        default="network-settings", validation_alias="optionType", serialization_alias="optionType"
    )


class PolicySettingsParcel(_ParcelBase):
    type_: Literal["policy-settings"] = Field(default="policy-settings", exclude=True)
    app_visibility: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "appVisibility")
    )
    app_visibility_ipv6: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "appVisibilityIPv6")
    )
    cflowd: Optional[Cflowd] = Field(default=None, validation_alias=AliasPath("data", "cflowd"))
    flow_visibility: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "flowVisibility")
    )
    flow_visibility_ipv6: Optional[Union[Global[bool], Default[bool]]] = Field(
        default=None, validation_alias=AliasPath("data", "flowVisibilityIPv6")
    )
