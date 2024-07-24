# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.identity import IdentityList, IdentityListEditPayload, IdentityListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyIdentityList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/identity")
    def create_policy_list(self, payload: IdentityList) -> PolicyListId:
        ...

    @delete("/template/policy/list/identity/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/identity")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/identity/{id}")
    def edit_policy_list(self, id: UUID, payload: IdentityListEditPayload) -> None:
        ...

    @get("/template/policy/list/identity/{id}")
    def get_lists_by_id(self, id: UUID) -> IdentityListInfo:
        ...

    @get("/template/policy/list/identity", "data")
    def get_policy_lists(self) -> DataSequence[IdentityListInfo]:
        ...

    @get("/template/policy/list/identity/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[IdentityListInfo]:
        ...

    @post("/template/policy/list/identity/preview")
    def preview_policy_list(self, payload: IdentityList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/identity/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
