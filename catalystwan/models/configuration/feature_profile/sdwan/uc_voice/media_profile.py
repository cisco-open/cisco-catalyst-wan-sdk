# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase
from catalystwan.models.common import MpDtmf, MpVoiceCodec


class Codec(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    value: Union[Variable, Global[MpVoiceCodec]] = Field()
    pref_num: Optional[str] = Field(
        default=None, validation_alias="prefNum", serialization_alias="prefNum", description="Preference number"
    )


class MediaProfileParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["media-profile"] = Field(default="media-profile", exclude=True)
    codec: List[Codec] = Field(validation_alias=AliasPath("data", "codec"))
    dtmf: Union[Variable, Global[MpDtmf]] = Field(validation_alias=AliasPath("data", "dtmf"))
    media_profile_number: Union[Variable, Global[int]] = Field(validation_alias=AliasPath("data", "mediaProfileNumber"))
