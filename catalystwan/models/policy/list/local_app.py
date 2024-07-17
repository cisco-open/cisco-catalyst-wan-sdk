# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.models.common import check_fields_exclusive
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class LocalAppListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    app_family: Optional[str] = Field(default=None, serialization_alias="appFamily", validation_alias="appFamily")
    app: Optional[str] = None

    @model_validator(mode="after")
    def check_app_xor_appfamily(self):
        check_fields_exclusive(self.__dict__, {"app", "app_family"}, True)
        return self


class LocalAppList(PolicyListBase):
    type: Literal["localApp"] = "localApp"
    entries: List[LocalAppListEntry] = []

    def add_app(self, app: str) -> None:
        self._add_entry(LocalAppListEntry(app=app))

    def add_app_family(self, app_family: str) -> None:
        self._add_entry(LocalAppListEntry(app_family=app_family))

    def list_all_app(self) -> List[str]:
        return [e.app for e in self.entries if e.app is not None]

    def list_all_app_family(self) -> List[str]:
        return [e.app_family for e in self.entries if e.app_family is not None]


class LocalAppListEditPayload(LocalAppList, PolicyListId):
    pass


class LocalAppListInfo(LocalAppList, PolicyListInfo):
    pass
