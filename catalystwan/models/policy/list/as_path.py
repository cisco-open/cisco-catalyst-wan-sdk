# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class ASPathListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    as_path: str = Field(serialization_alias="asPath", validation_alias="asPath")


class ASPathList(PolicyListBase):
    type: Literal["asPath"] = "asPath"
    entries: List[ASPathListEntry] = []

    def add_as_path(self, as_path: str):
        as_path_entry = ASPathListEntry(as_path=as_path)
        self._add_entry(entry=as_path_entry)


class ASPathListEditPayload(ASPathList, PolicyListId):
    pass


class ASPathListInfo(ASPathList, PolicyListInfo):
    pass
