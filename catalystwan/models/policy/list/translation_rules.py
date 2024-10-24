# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class TranslationRulesEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rule_num: IntStr = Field(ge=1, validation_alias="ruleNum", serialization_alias="ruleNum")
    match: str = Field(pattern=r"^/.*/$")
    replace: str = Field(pattern=r"^/.*/$|^reject$")


class TranslationRulesList(PolicyListBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["translationRules", "translationrules"] = "translationRules"
    entries: List[TranslationRulesEntry] = Field(default_factory=list)


class TranslationRulesListEditPayload(TranslationRulesList, PolicyListId):
    pass


class TranslationRulesListInfo(TranslationRulesList, PolicyListInfo):
    pass
