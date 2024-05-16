# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.ssl_decryption import (
    SslDecryptionPolicy,
    SslDecryptionPolicyEditPayload,
    SslDecryptionPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationSslDecryptionDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/ssldecryption")
    def create_policy_definition(self, payload: SslDecryptionPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/ssldecryption/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/ssldecryption/{id}")
    def edit_policy_definition(self, id: UUID, payload: SslDecryptionPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/ssldecryption", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/ssldecryption/{id}")
    def get_policy_definition(self, id: UUID) -> SslDecryptionPolicyGetResponse:
        ...

    @post("/template/policy/definition/ssldecryption/preview")
    def preview_policy_definition(self, payload: SslDecryptionPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/ssldecryption/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
