# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.route_policy import (
    RoutePolicy,
    RoutePolicyEditPayload,
    RoutePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyRouteDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/vedgeroute")
    def create_policy_definition(self, payload: RoutePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/vedgeroute/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/vedgeroute/{id}")
    def edit_policy_definition(self, id: UUID, payload: RoutePolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/vedgeroute", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/vedgeroute/{id}")
    def get_policy_definition(self, id: UUID) -> RoutePolicyGetResponse:
        ...

    @post("/template/policy/definition/vedgeroute/preview")
    def preview_policy_definition(self, payload: RoutePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/vedgeroute/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
