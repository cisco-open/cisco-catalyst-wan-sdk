# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.fxs_did_port import (
    FxsDidPortPolicy,
    FxsDidPortPolicyEditPayload,
    FxsDidPortPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyFxsDidPortDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/fxsdidport")
    def create_policy_definition(self, payload: FxsDidPortPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/fxsdidport/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/fxsdidport/multiple/{id}
        ...

    @put("/template/policy/definition/fxsdidport/{id}")
    def edit_policy_definition(self, id: UUID, payload: FxsDidPortPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/fxsdidport", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/fxsdidport/{id}")
    def get_policy_definition(self, id: UUID) -> FxsDidPortPolicyGetResponse:
        ...

    @post("/template/policy/definition/fxsdidport/preview")
    def preview_policy_definition(self, payload: FxsDidPortPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/fxsdidport/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/fxsdidport/bulk
        ...
