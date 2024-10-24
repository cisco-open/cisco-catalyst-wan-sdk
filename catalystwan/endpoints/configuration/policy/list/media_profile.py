# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.media_profile import (
    MediaProfileList,
    MediaProfileListEditPayload,
    MediaProfileListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyMediaProfileList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/mediaprofile")
    def create_policy_list(self, payload: MediaProfileList) -> PolicyListId:
        ...

    @delete("/template/policy/list/mediaprofile/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/mediaprofile")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/mediaprofile/{id}")
    def edit_policy_list(self, id: UUID, payload: MediaProfileListEditPayload) -> None:
        ...

    @get("/template/policy/list/mediaprofile/{id}")
    def get_lists_by_id(self, id: UUID) -> MediaProfileListInfo:
        ...

    @get("/template/policy/list/mediaprofile", "data")
    def get_policy_lists(self) -> DataSequence[MediaProfileListInfo]:
        ...

    @get("/template/policy/list/mediaprofile/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[MediaProfileListInfo]:
        ...

    @post("/template/policy/list/mediaprofile/preview")
    def preview_policy_list(self, payload: MediaProfileList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/mediaprofile/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
