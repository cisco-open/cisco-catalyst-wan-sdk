# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.scalable_group_tag import (
    ScalableGroupTagList,
    ScalableGroupTagListEditPayload,
    ScalableGroupTagListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyScalableGroupTagList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/scalablegrouptag")
    def create_policy_list(self, payload: ScalableGroupTagList) -> PolicyListId:
        ...

    @delete("/template/policy/list/scalablegrouptag/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/scalablegrouptag")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/scalablegrouptag/{id}")
    def edit_policy_list(self, id: UUID, payload: ScalableGroupTagListEditPayload) -> None:
        ...

    @get("/template/policy/list/scalablegrouptag/{id}")
    def get_lists_by_id(self, id: UUID) -> ScalableGroupTagListInfo:
        ...

    @get("/template/policy/list/scalablegrouptag", "data")
    def get_policy_lists(self) -> DataSequence[ScalableGroupTagListInfo]:
        ...

    @get("/template/policy/list/scalablegrouptag/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ScalableGroupTagListInfo]:
        ...

    @post("/template/policy/list/scalablegrouptag/preview")
    def preview_policy_list(self, payload: ScalableGroupTagList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/scalablegrouptag/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
