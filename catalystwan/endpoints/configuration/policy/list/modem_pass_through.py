# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.modem_pass_through import (
    ModemPassThroughList,
    ModemPassThroughListEditPayload,
    ModemPassThroughListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyModemPassThroughList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/modempassthrough")
    def create_policy_list(self, payload: ModemPassThroughList) -> PolicyListId:
        ...

    @delete("/template/policy/list/modempassthrough/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/modempassthrough")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/modempassthrough/{id}")
    def edit_policy_list(self, id: UUID, payload: ModemPassThroughListEditPayload) -> None:
        ...

    @get("/template/policy/list/modempassthrough/{id}")
    def get_lists_by_id(self, id: UUID) -> ModemPassThroughListInfo:
        ...

    @get("/template/policy/list/modempassthrough", "data")
    def get_policy_lists(self) -> DataSequence[ModemPassThroughListInfo]:
        ...

    @get("/template/policy/list/modempassthrough/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ModemPassThroughListInfo]:
        ...

    @post("/template/policy/list/modempassthrough/preview")
    def preview_policy_list(self, payload: ModemPassThroughList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/modempassthrough/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
