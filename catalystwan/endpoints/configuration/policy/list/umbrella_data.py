# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.umbrella_data import (
    UmbrellaDataList,
    UmbrellaDataListEditPayload,
    UmbrellaDataListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyUmbrellaDataList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/umbrelladata")
    def create_policy_list(self, payload: UmbrellaDataList) -> PolicyListId:
        ...

    @delete("/template/policy/list/umbrelladata/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/umbrelladata")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/umbrelladata/{id}")
    def edit_policy_list(self, id: UUID, payload: UmbrellaDataListEditPayload) -> None:
        ...

    @get("/template/policy/list/umbrelladata/{id}")
    def get_lists_by_id(self, id: UUID) -> UmbrellaDataListInfo:
        ...

    @get("/template/policy/list/umbrelladata", "data")
    def get_policy_lists(self) -> DataSequence[UmbrellaDataListInfo]:
        ...

    @get("/template/policy/list/umbrelladata/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[UmbrellaDataListInfo]:
        ...

    @post("/template/policy/list/umbrelladata/preview")
    def preview_policy_list(self, payload: UmbrellaDataList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/umbrelladata/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
