# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.aip import (
    AdvancedInspectionProfilePolicy,
    AdvancedInspectionProfilePolicyEditPayload,
    AdvancedInspectionProfilePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyAIPDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/advancedinspectionprofile")
    def create_policy_definition(self, payload: AdvancedInspectionProfilePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/advancedinspectionprofile/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/advancedinspectionprofile/{id}")
    def edit_policy_definition(
        self, id: UUID, payload: AdvancedInspectionProfilePolicyEditPayload
    ) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/advancedinspectionprofile", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/advancedinspectionprofile/{id}")
    def get_policy_definition(self, id: UUID) -> AdvancedInspectionProfilePolicyGetResponse:
        ...

    @post("/template/policy/definition/advancedinspectionprofile/preview")
    def preview_policy_definition(self, payload: AdvancedInspectionProfilePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/advancedinspectionprofile/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
