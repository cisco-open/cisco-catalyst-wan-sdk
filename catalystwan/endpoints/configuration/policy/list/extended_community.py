# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.communities import (
    ExtendedCommunityList,
    ExtendedCommunityListEditPayload,
    ExtendedCommunityListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyExtendedCommunityList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/extcommunity")
    def create_policy_list(self, payload: ExtendedCommunityList) -> PolicyListId:
        ...

    @delete("/template/policy/list/extcommunity/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/extcommunity")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/extcommunity/{id}")
    def edit_policy_list(self, id: UUID, payload: ExtendedCommunityListEditPayload) -> None:
        ...

    @get("/template/policy/list/extcommunity/{id}")
    def get_lists_by_id(self, id: UUID) -> ExtendedCommunityListInfo:
        ...

    @get("/template/policy/list/extcommunity", "data")
    def get_policy_lists(self) -> DataSequence[ExtendedCommunityListInfo]:
        ...

    @get("/template/policy/list/extcommunity/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ExtendedCommunityListInfo]:
        ...

    @post("/template/policy/list/extcommunity/preview")
    def preview_policy_list(self, payload: ExtendedCommunityList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/extcommunity/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
