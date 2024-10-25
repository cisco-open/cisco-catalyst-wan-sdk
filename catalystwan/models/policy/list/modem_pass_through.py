# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import ModemPassThroughCodec
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ModemPassThroughListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    protocol: ModemPassThroughCodec


class ModemPassThroughList(PolicyListBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["modemPassthrough", "modempassthrough"] = "modemPassthrough"
    entires: List[ModemPassThroughListEntry] = Field(default_factory=list, max_length=1)


class ModemPassThroughListEditPayload(ModemPassThroughList, PolicyListId):
    pass


class ModemPassThroughListInfo(ModemPassThroughList, PolicyListInfo):
    pass
