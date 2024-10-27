# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.fxo_port import (
    FxoPortPolicy,
    FxoPortPolicyEditPayload,
    FxoPortPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyFxoPortDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/fxoport")
    def create_policy_definition(self, payload: FxoPortPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/fxoport/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/fxoport/multiple/{id}
        ...

    @put("/template/policy/definition/fxoport/{id}")
    def edit_policy_definition(self, id: UUID, payload: FxoPortPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/fxoport", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/fxoport/{id}")
    def get_policy_definition(self, id: UUID) -> FxoPortPolicyGetResponse:
        ...

    @post("/template/policy/definition/fxoport/preview")
    def preview_policy_definition(self, payload: FxoPortPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/fxoport/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/fxoport/bulk
        ...
