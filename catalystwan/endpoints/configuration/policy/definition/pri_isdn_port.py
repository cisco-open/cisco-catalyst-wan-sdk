# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.pri_isdn_port import (
    PriIsdnPortPolicy,
    PriIsdnPortPolicyEditPayload,
    PriIsdnPortPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyPriIsdnPortDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/priisdnport")
    def create_policy_definition(self, payload: PriIsdnPortPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/priisdnport/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/priisdnport/multiple/{id}
        ...

    @put("/template/policy/definition/priisdnport/{id}")
    def edit_policy_definition(self, id: UUID, payload: PriIsdnPortPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/priisdnport", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/priisdnport/{id}")
    def get_policy_definition(self, id: UUID) -> PriIsdnPortPolicyGetResponse:
        ...

    @post("/template/policy/definition/priisdnport/preview")
    def preview_policy_definition(self, payload: PriIsdnPortPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/priisdnport/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/priisdnport/bulk
        ...
