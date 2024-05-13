# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class UmbrellaDataListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    api_key: str = Field(validation_alias="apiKey", serialization_alias="apiKey")
    secret: str
    token: str
    umb_org_id: str = Field(validation_alias="umbOrgId", serialization_alias="umbOrgId")


class UmbrellaDataList(PolicyListBase):
    type: Literal["umbrellaData"] = "umbrellaData"
    entries: List[UmbrellaDataListEntry] = []


class UmbrellaDataListEditPayload(UmbrellaDataList, PolicyListId):
    pass


class UmbrellaDataListInfo(UmbrellaDataList, PolicyListInfo):
    pass
