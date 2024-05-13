# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyDefinitionEndpoints
from catalystwan.models.policy.definition.dns_security import (
    DnsSecurityPolicy,
    DnsSecurityPolicyEditPayload,
    DnsSecurityPolicyGetResponse,
)
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionEditResponse,
    PolicyDefinitionId,
    PolicyDefinitionInfo,
    PolicyDefinitionPreview,
)
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyDnsSecurityDefinition(APIEndpoints, PolicyDefinitionEndpoints):
    @post("/template/policy/definition/dnssecurity")
    def create_policy_definition(self, payload: DnsSecurityPolicy) -> PolicyDefinitionId:
        ...

    @delete("/template/policy/definition/dnssecurity/{id}")
    def delete_policy_definition(self, id: UUID) -> None:
        ...

    @put("/template/policy/definition/dnssecurity/{id}")
    def edit_policy_definition(self, id: UUID, payload: DnsSecurityPolicyEditPayload) -> PolicyDefinitionEditResponse:
        ...

    @get("/template/policy/definition/dnssecurity", "data")
    def get_definitions(self) -> DataSequence[PolicyDefinitionInfo]:
        ...

    @get("/template/policy/definition/dnssecurity/{id}")
    def get_policy_definition(self, id: UUID) -> DnsSecurityPolicyGetResponse:
        ...

    @post("/template/policy/definition/dnssecurity/preview")
    def preview_policy_definition(self, payload: DnsSecurityPolicy) -> PolicyDefinitionPreview:
        ...

    @get("/template/policy/definition/dnssecurity/preview/{id}")
    def preview_policy_definition_by_id(self, id: UUID) -> PolicyDefinitionPreview:
        ...
