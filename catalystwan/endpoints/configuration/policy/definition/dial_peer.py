# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.dial_peer import (
    DialPeerPolicy,
    DialPeerPolicyEditPayload,
    DialPeerPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyDialPeerDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/dialpeer")
    def create_policy_definition(self, payload: DialPeerPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/dialpeer/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/dialpeer/multiple/{id}
        ...

    @put("/template/policy/definition/dialpeer/{id}")
    def edit_policy_definition(self, id: UUID, payload: DialPeerPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/dialpeer", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/dialpeer/{id}")
    def get_policy_definition(self, id: UUID) -> DialPeerPolicyGetResponse:
        ...

    @post("/template/policy/definition/dialpeer/preview")
    def preview_policy_definition(self, payload: DialPeerPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/dialpeer/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/dialpeer/bulk
        ...