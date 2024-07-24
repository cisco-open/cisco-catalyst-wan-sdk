# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class UmbrellaDataListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    api_key: Optional[str] = Field(default=None, validation_alias="apiKey", serialization_alias="apiKey")
    secret: Optional[str] = Field(default=None)
    api_key_v2: Optional[str] = Field(default=None, validation_alias="apiKeyV2", serialization_alias="apiKeyV2")
    secret_v2: Optional[str] = Field(default=None, validation_alias="secretV2", serialization_alias="secretV2")
    token: str
    umb_org_id: str = Field(validation_alias="umbOrgId", serialization_alias="umbOrgId")


class UmbrellaDataList(PolicyListBase):
    type: Literal["umbrellaData"] = "umbrellaData"
    entries: List[UmbrellaDataListEntry] = Field(default_factory=list)


class UmbrellaDataListEditPayload(UmbrellaDataList, PolicyListId):
    pass


class UmbrellaDataListInfo(UmbrellaDataList, PolicyListInfo):
    pass
