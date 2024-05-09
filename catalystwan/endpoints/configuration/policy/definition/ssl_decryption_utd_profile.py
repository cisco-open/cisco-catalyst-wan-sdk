# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.ssl_decryption_utd_profile import (
    SslDecryptionUtdProfilePolicy,
    SslDecryptionUtdProfilePolicyEditPayload,
    SslDecryptionUtdProfilePolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationSslDecryptionUtdProfileDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/sslutdprofile")
    def create_policy_definition(self, payload: SslDecryptionUtdProfilePolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/sslutdprofile/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/sslutdprofile/{id}")
    def edit_policy_definition(
        self, id: UUID, payload: SslDecryptionUtdProfilePolicyEditPayload
    ) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/sslutdprofile", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/sslutdprofile/{id}")
    def get_policy_definition(self, id: UUID) -> SslDecryptionUtdProfilePolicyGetResponse:
        ...

    @post("/template/policy/definition/sslutdprofile/preview")
    def preview_policy_definition(self, payload: SslDecryptionUtdProfilePolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/sslutdprofile/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
