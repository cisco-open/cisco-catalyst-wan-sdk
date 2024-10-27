# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.fxs_port import (
    FxsPortPolicy,
    FxsPortPolicyEditPayload,
    FxsPortPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyFxsPortDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/fxsport")
    def create_policy_definition(self, payload: FxsPortPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/fxsport/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/fxsport/multiple/{id}
        ...

    @put("/template/policy/definition/fxsport/{id}")
    def edit_policy_definition(self, id: UUID, payload: FxsPortPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/fxsport", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/fxsport/{id}")
    def get_policy_definition(self, id: UUID) -> FxsPortPolicyGetResponse:
        ...

    @post("/template/policy/definition/fxsport/preview")
    def preview_policy_definition(self, payload: FxsPortPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/fxsport/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/fxsport/bulk
        ...
