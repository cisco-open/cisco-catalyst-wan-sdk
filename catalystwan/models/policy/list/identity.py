# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class IdentityListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user: str = Field(default=None)
    user_group: str = Field(default=None, validation_alias="userGroup", serialization_alias="userGroup")


class IdentityList(PolicyListBase):
    type: Literal["identity"] = "identity"
    entries: List[IdentityListEntry] = Field(default_factory=list)

    def add_entry(self, user: str, user_group: str) -> None:
        self._add_entry(IdentityListEntry(user=user, user_group=user_group))


class IdentityListEditPayload(IdentityList, PolicyListId):
    pass


class IdentityListInfo(IdentityList, PolicyListInfo):
    pass
