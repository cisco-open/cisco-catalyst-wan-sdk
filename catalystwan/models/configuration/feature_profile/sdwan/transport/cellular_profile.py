# Copyright 2023 Cisco Systems, Inc. and its affiliates
# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

AuthenticationType = Literal[
    "chap",
    "pap",
    "pap_chap",
]


class NeedAuthentication(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    password: Union[Variable, Global[str]] = Field()
    type: Union[Variable, Global[AuthenticationType]] = Field()
    username: Union[Variable, Global[str]] = Field()


class Authentication(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    need_authentication: Optional[NeedAuthentication] = Field(
        default=None, validation_alias="needAuthentication", serialization_alias="needAuthentication"
    )
    no_authentication: Optional[Default[Literal["none"]]] = Field(
        default=None, validation_alias="noAuthentication", serialization_alias="noAuthentication"
    )

    @model_validator(mode="after")
    def validate_authentication_exclusive(self):
        if self.need_authentication and self.no_authentication:
            raise ValueError("Only one of need_authentication and no_authentication can be set")
        return self


PdnType = Literal[
    "ipv4",
    "ipv4v6",
    "ipv6",
]


class ProfileInfo(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    apn: Union[Variable, Global[str]] = Field()
    authentication: Optional[Authentication] = Field(default=None)
    no_overwrite: Optional[Union[Variable, Global[bool], Default[None]]] = Field(
        default=None, validation_alias="noOverwrite", serialization_alias="noOverwrite"
    )
    pdn_type: Optional[Union[Variable, Default[PdnType], Global[PdnType]]] = Field(
        default=None, validation_alias="pdnType", serialization_alias="pdnType"
    )


class ProfileConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    id: Union[Variable, Global[int]] = Field()
    profile_info: ProfileInfo = Field(validation_alias="profileInfo", serialization_alias="profileInfo")


class CellularProfileParcel(_ParcelBase):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    type_: Literal["cellular-profile"] = Field(default="cellular-profile", exclude=True, frozen=True)
    profile_config: ProfileConfig = Field(validation_alias=AliasPath("data", "profileConfig"))
    config_type: Optional[Default[Literal["non-eSim"]]] = Field(
        default=as_default("non-eSim"), validation_alias=AliasPath("data", "configType")
    )
