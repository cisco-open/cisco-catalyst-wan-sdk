# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import IntStr, MpDtmf, MpVoiceCodec
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class CodecEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["codec"] = "codec"
    pref_num: IntStr = Field(ge=1, serialization_alias="prefNum", validation_alias="prefNum")
    value: MpVoiceCodec


class DtmfEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["dtmf"] = "dtmf"
    value: MpDtmf


AnyMediaProfileListEntry = Annotated[
    Union[
        CodecEntry,
        DtmfEntry,
    ],
    Field(discriminator="type"),
]


class MediaProfileList(PolicyListBase):
    type: Literal["mediaProfile", "mediaprofile"] = "mediaProfile"
    entries: List[AnyMediaProfileListEntry] = Field(default_factory=list)


class MediaProfileListEditPayload(MediaProfileList, PolicyListId):
    pass


class MediaProfileListInfo(MediaProfileList, PolicyListInfo):
    pass
