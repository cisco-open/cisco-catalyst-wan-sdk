# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.translation_rules import (
    TranslationRulesList,
    TranslationRulesListEditPayload,
    TranslationRulesListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyTranslationRulesList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/translationrules")
    def create_policy_list(self, payload: TranslationRulesList) -> PolicyListId:
        ...

    @delete("/template/policy/list/translationrules/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/translationrules")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/translationrules/{id}")
    def edit_policy_list(self, id: UUID, payload: TranslationRulesListEditPayload) -> None:
        ...

    @get("/template/policy/list/translationrules/{id}")
    def get_lists_by_id(self, id: UUID) -> TranslationRulesListInfo:
        ...

    @get("/template/policy/list/translationrules", "data")
    def get_policy_lists(self) -> DataSequence[TranslationRulesListInfo]:
        ...

    @get("/template/policy/list/translationrules/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[TranslationRulesListInfo]:
        ...

    @post("/template/policy/list/translationrules/preview")
    def preview_policy_list(self, payload: TranslationRulesList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/translationrules/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
