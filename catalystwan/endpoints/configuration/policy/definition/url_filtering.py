# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.url_filtering import (
    UrlFilteringPolicy,
    UrlFilteringPolicyEditPayload,
    UrlFilteringPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyUrlFilteringDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/urlfiltering")
    def create_policy_definition(self, payload: UrlFilteringPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/urlfiltering/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/urlfiltering/{id}")
    def edit_policy_definition(self, id: UUID, payload: UrlFilteringPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/urlfiltering", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/urlfiltering/{id}")
    def get_policy_definition(self, id: UUID) -> UrlFilteringPolicyGetResponse:
        ...

    @post("/template/policy/definition/urlfiltering/preview")
    def preview_policy_definition(self, payload: UrlFilteringPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/urlfiltering/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
