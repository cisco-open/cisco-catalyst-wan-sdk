# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.models.templates import FeatureTemplateDefinition, FeatureTemplateInformation
from catalystwan.typed_list import DataSequence

FeatureType = Literal["all", "vmanage-default", "network-design", "cloud-dock", "lawful-interception"]


class FeatureQueryParams(BaseModel):
    summary: bool = Field(default=False)
    offset: Optional[int] = Field(default=None)
    limit: Optional[int] = Field(default=None)


class ConfigurationGeneralTemplate(APIEndpoints):
    @get("/template/feature", "data")
    def get_feature_template_list(
        self, params: FeatureQueryParams = FeatureQueryParams()
    ) -> DataSequence[FeatureTemplateInformation]:
        ...

    @get("/template/feature/object/{template_id}")
    def get_template_definition(self, template_id: UUID) -> DataSequence[FeatureTemplateDefinition]:
        ...
