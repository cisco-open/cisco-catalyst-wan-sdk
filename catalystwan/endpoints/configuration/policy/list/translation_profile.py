# Copyright 2024 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from uuid import UUID

from catalystwan.endpoints import APIEndpoints, delete, get, post, put
from catalystwan.endpoints.configuration.policy.abstractions import PolicyListEndpoints
from catalystwan.models.policy.list.translation_profile import (
    TranslationProfileList,
    TranslationProfileListEditPayload,
    TranslationProfileListInfo,
)
from catalystwan.models.policy.policy_list import InfoTag, PolicyListId, PolicyListPreview
from catalystwan.typed_list import DataSequence


class ConfigurationPolicyTranslationProfileList(APIEndpoints, PolicyListEndpoints):
    @post("/template/policy/list/translationprofile")
    def create_policy_list(self, payload: TranslationProfileList) -> PolicyListId:
        ...

    @delete("/template/policy/list/translationprofile/{id}")
    def delete_policy_list(self, id: UUID) -> None:
        ...

    @delete("/template/policy/list/translationprofile")
    def delete_policy_lists_with_info_tag(self, params: InfoTag) -> None:
        ...

    @put("/template/policy/list/translationprofile/{id}")
    def edit_policy_list(self, id: UUID, payload: TranslationProfileListEditPayload) -> None:
        ...

    @get("/template/policy/list/translationprofile/{id}")
    def get_lists_by_id(self, id: UUID) -> TranslationProfileListInfo:
        ...

    @get("/template/policy/list/translationprofile", "data")
    def get_policy_lists(self) -> DataSequence[TranslationProfileListInfo]:
        ...

    @get("/template/policy/list/translationprofile/filtered", "data")
    def get_policy_lists_with_info_tag(self, params: InfoTag) -> DataSequence[TranslationProfileListInfo]:
        ...

    @post("/template/policy/list/translationprofile/preview")
    def preview_policy_list(self, payload: TranslationProfileList) -> PolicyListPreview:
        ...

    @get("/template/policy/list/translationprofile/preview/{id}")
    def preview_policy_list_by_id(self, id: UUID) -> PolicyListPreview:
        ...
