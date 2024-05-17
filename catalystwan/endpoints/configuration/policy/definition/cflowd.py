# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.cflowd import CflowdPolicy, CflowdPolicyEditPayload, CflowdPolicyGetResponse
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyCflowdDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/cflowd/")
    def create_policy_definition(self, payload: CflowdPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/cflowd/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/cflowd/{id}")
    def edit_policy_definition(self, id: UUID, payload: CflowdPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/cflowd", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/cflowd/{id}")
    def get_policy_definition(self, id: UUID) -> CflowdPolicyGetResponse:
        ...

    @post("/template/policy/definition/cflowd/preview")
    def preview_policy_definition(self, payload: CflowdPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/cflowd/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
