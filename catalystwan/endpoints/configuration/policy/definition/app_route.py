# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.app_route import (
    AppRoutePolicy,
    AppRoutePolicyEditPayload,
    AppRoutePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyAppRouteDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/approute/")
    def create_policy_definition(self, payload: AppRoutePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/approute/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/approute/{id}")
    def edit_policy_definition(self, id: UUID, payload: AppRoutePolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/approute", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/approute/{id}")
    def get_policy_definition(self, id: UUID) -> AppRoutePolicyGetResponse:
        ...

    @post("/template/policy/definition/approute/preview")
    def preview_policy_definition(self, payload: AppRoutePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/approute/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
