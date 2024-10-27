# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.supervisory_disconnect import (
    SupervisoryDisconnectList,
    SupervisoryDisconnectListEditPayload,
    SupervisoryDisconnectListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicySupervisoryDisconnectList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/supervisorydisc")
    def create_policy_list(self, payload: SupervisoryDisconnectList) -> PolicyListId:
        ...

    @delete("/template/policy/list/supervisorydisc/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/supervisorydisc")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/supervisorydisc/{id}")
    def edit_policy_list(self, id: UUID, payload: SupervisoryDisconnectListEditPayload) -> None:
        ...

    @get("/template/policy/list/supervisorydisc/{id}")
    def get_lists_by_id(self, id: UUID) -> SupervisoryDisconnectListInfo:
        ...

    @get("/template/policy/list/supervisorydisc", "data")
    def get_policy_lists(self) -> DataSequence[SupervisoryDisconnectListInfo]:
        ...

    @get("/template/policy/list/supervisorydisc/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[SupervisoryDisconnectListInfo]:
        ...

    @post("/template/policy/list/supervisorydisc/preview")
    def preview_policy_list(self, payload: SupervisoryDisconnectList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/supervisorydisc/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
