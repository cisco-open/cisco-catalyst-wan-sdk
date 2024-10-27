# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo

CallType = Literal["called", "calling"]


class TranslationProfileEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    translation_rule: IntStr = Field(
        ge=1, le=1073741823, validation_alias="translationRule", serialization_alias="translationRule"
    )
    call_type: CallType = Field(validation_alias="callType", serialization_alias="callType")


class TranslationProfileList(PolicyListBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["translationProfile", "translationprofile"] = "translationProfile"
    entries: List[TranslationProfileEntry] = Field(default_factory=list)


class TranslationProfileListEditPayload(TranslationProfileList, PolicyListId):
    pass


class TranslationProfileListInfo(TranslationProfileList, PolicyListInfo):
    pass
