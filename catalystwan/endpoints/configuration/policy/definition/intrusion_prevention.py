# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.intrusion_prevention import (
    IntrusionPreventionPolicy,
    IntrusionPreventionPolicyEditPayload,
    IntrusionPreventionPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyIntrusionPreventionDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/intrusionprevention")
    def create_policy_definition(self, payload: IntrusionPreventionPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/intrusionprevention/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/intrusionprevention/{id}")
    def edit_policy_definition(
        self, id: UUID, payload: IntrusionPreventionPolicyEditPayload
    ) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/intrusionprevention", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/intrusionprevention/{id}")
    def get_policy_definition(self, id: UUID) -> IntrusionPreventionPolicyGetResponse:
        ...

    @post("/template/policy/definition/intrusionprevention/preview")
    def preview_policy_definition(self, payload: IntrusionPreventionPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/intrusionprevention/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
