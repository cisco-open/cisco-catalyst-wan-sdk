# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.threat_grid_api_key import (
    ThreatGridApiKeyList,
    ThreatGridApiKeyListEditPayload,
    ThreatGridApiKeyListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyThreatGridApiKeyList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/tgapikey")
    def create_policy_list(self, payload: ThreatGridApiKeyList) -> PolicyListId:
        ...

    @delete("/template/policy/list/tgapikey/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/tgapikey")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/tgapikey/{id}")
    def edit_policy_list(self, id: UUID, payload: ThreatGridApiKeyListEditPayload) -> None:
        ...

    @get("/template/policy/list/tgapikey/{id}")
    def get_lists_by_id(self, id: UUID) -> ThreatGridApiKeyListInfo:
        ...

    @get("/template/policy/list/tgapikey", "data")
    def get_policy_lists(self) -> DataSequence[ThreatGridApiKeyListInfo]:
        ...

    @get("/template/policy/list/tgapikey/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[ThreatGridApiKeyListInfo]:
        ...

    @post("/template/policy/list/tgapikey/preview")
    def preview_policy_list(self, payload: ThreatGridApiKeyList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/tgapikey/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
