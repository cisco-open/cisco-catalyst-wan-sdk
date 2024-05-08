# Copyright 2024 Cisco Systems, Inc. and its affiliates

from itertools import chain
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import PolicyModeType, WebCategory, WebReputation
from catalystwan.models.policy import URLAllowListInfo, URLBlockListInfo
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
)


class SslDecryptionUtdProfileDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    decrypt_categories: List[WebCategory] = Field(
        default=[], validation_alias="decryptCategories", serialization_alias="decryptCategories"
    )
    never_decrypt_categories: List[WebCategory] = Field(
        default=[], validation_alias="neverDecryptCategories", serialization_alias="neverDecryptCategories"
    )

    skip_decrypt_categories: List[WebCategory] = Field(
        default=[], validation_alias="skipDecryptCategories", serialization_alias="skipDecryptCategories"
    )

    reputation: bool = False
    fail_decrypt: bool = Field(default=False, validation_alias="failDecrypt", serialization_alias="failDecrypt")
    decrypt_threshold: Optional[WebReputation] = Field(
        default=None, validation_alias="decryptThreshold", serialization_alias="decryptThreshold"
    )

    filtered_url_white_list: List[URLAllowListInfo] = Field(
        default=[], validation_alias="filteredUrlWhiteList", serialization_alias="filteredUrlWhiteList"
    )
    filtered_url_black_list: List[URLBlockListInfo] = Field(
        default=[], validation_alias="filteredUrlBlackList", serialization_alias="filteredUrlBlackList"
    )

    url_white_list: Optional[Reference] = Field(
        default=None, validation_alias="urlWhiteList", serialization_alias="urlWhiteList"
    )

    url_black_list: Optional[Reference] = Field(
        default=None, validation_alias="urlBlackList", serialization_alias="urlBlackList"
    )

    def add_never_decrypt_category(self, category: WebCategory):
        self._check_category_already_added(category)
        self.never_decrypt_categories.append(category)

    def add_skip_decrypt_category(self, category: WebCategory):
        self._check_category_already_added(category)
        self.skip_decrypt_categories.append(category)

    def add_decrypt_category(self, category: WebCategory):
        self._check_category_already_added(category)
        self.decrypt_categories.append(category)

    def add_decrypt_domain_list(self, black_list: URLBlockListInfo):
        self.url_black_list = Reference(ref=black_list.list_id)

    def add_no_decrypt_domain_list(self, white_list: URLAllowListInfo):
        self.url_white_list = Reference(ref=white_list.list_id)

    def _check_category_already_added(self, category: WebCategory):
        if category in chain(self.decrypt_categories, self.never_decrypt_categories, self.skip_decrypt_categories):
            raise ValueError(f"Category: '{category}' already added to one of categories list.")


class SslDecryptionUtdProfilePolicy(PolicyDefinitionBase):
    type: Literal["sslUtdDecryptProfile"] = "sslUtdDecryptProfile"
    mode: PolicyModeType = "security"
    definition: SslDecryptionUtdProfileDefinition


class SslDecryptionUtdProfilePolicyEditPayload(SslDecryptionUtdProfilePolicy, PolicyDefinitionId):
    pass


class SslDecryptionUtdProfilePolicyGetResponse(SslDecryptionUtdProfilePolicy, PolicyDefinitionGetResponse):
    pass
