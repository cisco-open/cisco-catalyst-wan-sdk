# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.amp import (
    AdvancedMalwareProtectionPolicy,
    AdvancedMalwareProtectionPolicyEditPayload,
    AdvancedMalwareProtectionPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyAMPDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/advancedMalwareProtection")
    def create_policy_definition(self, payload: AdvancedMalwareProtectionPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/advancedMalwareProtection/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/advancedMalwareProtection/{id}")
    def edit_policy_definition(
        self, id: UUID, payload: AdvancedMalwareProtectionPolicyEditPayload
    ) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/advancedMalwareProtection", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/advancedMalwareProtection/{id}")
    def get_policy_definition(self, id: UUID) -> AdvancedMalwareProtectionPolicyGetResponse:
        ...

    @post("/template/policy/definition/advancedMalwareProtection/preview")
    def preview_policy_definition(self, payload: AdvancedMalwareProtectionPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/advancedMalwareProtection/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
