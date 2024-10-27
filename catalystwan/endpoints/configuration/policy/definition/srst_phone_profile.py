# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.srst_phone_profile import (
    SrstPhoneProfilePolicy,
    SrstPhoneProfilePolicyEditPayload,
    SrstPhoneProfilePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicySrstPhoneProfileDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/srstphoneprofile")
    def create_policy_definition(self, payload: SrstPhoneProfilePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/srstphoneprofile/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    def edit_multiple_policy_definition(self):
        # PUT /template/policy/definition/srstphoneprofile/multiple/{id}
        ...

    @put("/template/policy/definition/srstphoneprofile/{id}")
    def edit_policy_definition(
        self, id: UUID, payload: SrstPhoneProfilePolicyEditPayload
    ) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/srstphoneprofile", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/srstphoneprofile/{id}")
    def get_policy_definition(self, id: UUID) -> SrstPhoneProfilePolicyGetResponse:
        ...

    @post("/template/policy/definition/srstphoneprofile/preview")
    def preview_policy_definition(self, payload: SrstPhoneProfilePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/srstphoneprofile/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...

    def save_policy_definition_in_bulk(self):
        # PUT /template/policy/definition/srstphoneprofile/bulk
        ...
