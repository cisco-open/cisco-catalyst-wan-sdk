# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.fax_protocol import FaxProtocolList, FaxProtocolListEditPayload, FaxProtocolListInfo
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyFaxProtocolList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/faxprotocol")
    def create_policy_list(self, payload: FaxProtocolList) -> PolicyListId:
        ...

    @delete("/template/policy/list/faxprotocol/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/faxprotocol")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/faxprotocol/{id}")
    def edit_policy_list(self, id: UUID, payload: FaxProtocolListEditPayload) -> None:
        ...

    @get("/template/policy/list/faxprotocol/{id}")
    def get_lists_by_id(self, id: UUID) -> FaxProtocolListInfo:
        ...

    @get("/template/policy/list/faxprotocol", "data")
    def get_policy_lists(self) -> DataSequence[FaxProtocolListInfo]:
        ...

    @get("/template/policy/list/faxprotocol/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[FaxProtocolListInfo]:
        ...

    @post("/template/policy/list/faxprotocol/preview")
    def preview_policy_list(self, payload: FaxProtocolList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/faxprotocol/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
