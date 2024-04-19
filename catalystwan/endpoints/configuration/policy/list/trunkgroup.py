# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.trunkgroup import TrunkGroupList, TrunkGroupListEditPayload, TrunkGroupListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyTrunkGroupList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/trunkgroup")
    def create_policy_list(self, payload: TrunkGroupList) -> PolicyListId:
        ...

    @delete("/template/policy/list/trunkgroup/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/trunkgroup")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/trunkgroup/{id}")
    def edit_policy_list(self, id: UUID, payload: TrunkGroupListEditPayload) -> None:
        ...

    @get("/template/policy/list/trunkgroup/{id}")
    def get_lists_by_id(self, id: UUID) -> TrunkGroupListInfo:
        ...

    @get("/template/policy/list/trunkgroup", "data")
    def get_policy_lists(self) -> DataSequence[TrunkGroupListInfo]:
        ...

    @get("/template/policy/list/trunkgroup/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[TrunkGroupListInfo]:
        ...

    @post("/template/policy/list/trunkgroup/preview")
    def preview_policy_list(self, payload: TrunkGroupList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/trunkgroup/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
