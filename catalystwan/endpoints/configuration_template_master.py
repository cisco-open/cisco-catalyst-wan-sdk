# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import JSON, APIEndpoints, get, post, put
from catalystwan.models.templates import DeviceTemplateInformation, FeatureType
from catalystwan.typed_list import DataSequence


class TemplateID(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    template_id: UUID = Field(serialization_alias="templateId", validation_alias="templateId")


class AttachedDevices(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    attached_devices: Optional[List] = Field(
        default=[], serialization_alias="AttachedDevices", validation_alias="AttachedDevices"
    )


class FeatureQueryParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    feature: FeatureType = Field(default="all")


class ConfigurationTemplateMaster(APIEndpoints):
    @get("/template/device", "data")
    def get_device_template_list(
        self, params: FeatureQueryParams = FeatureQueryParams()
    ) -> DataSequence[DeviceTemplateInformation]:
        ...

    @post("/template/device/feature")
    def create_device_template_from_feature_templates(self, payload: JSON) -> TemplateID:
        ...

    @put("/template/device/{template_id}", "data")
    def edit_template(self, template_id: str, payload: JSON) -> AttachedDevices:
        ...
