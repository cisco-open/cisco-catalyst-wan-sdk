# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import JSON, APIEndpoints, get, post
from catalystwan.typed_list import DataSequence

FeatureType = Literal["all", "vmanage-default", "network-design", "cloud-dock", "lawful-interception"]


TemplateType = Literal["file", "template"]  # file == cli, template == feature


class TemplateID(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    template_id: UUID = Field(serialization_alias="templateId", validation_alias="templateId")


class FeatureQueryParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    feature: FeatureType = Field(default="all")


class DeviceTemplateInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    device_type: str = Field(serialization_alias="deviceType", validation_alias="deviceType")
    last_updated_on: datetime.datetime = Field(serialization_alias="lastUpdatedOn", validation_alias="lastUpdatedOn")
    resource_group: Optional[str] = Field(
        default=None, serialization_alias="resourceGroup", validation_alias="resourceGroup"
    )
    device_role: Optional[str] = Field(default=None, serialization_alias="deviceRole", validation_alias="deviceRole")
    template_class: str = Field(serialization_alias="templateClass", validation_alias="templateClass")
    config_type: TemplateType = Field(serialization_alias="configType", validation_alias="configType")
    template_attached: int = Field(serialization_alias="templateAttached", validation_alias="templateAttached")
    draft_mode: Optional[str] = Field(default=None, serialization_alias="draftMode", validation_alias="draftMode")
    last_updated_by: str = Field(serialization_alias="lastUpdatedBy", validation_alias="lastUpdatedBy")
    id: str = Field(serialization_alias="templateId", validation_alias="templateId")
    factory_default: bool = Field(serialization_alias="factoryDefault", validation_alias="factoryDefault")
    name: str = Field(serialization_alias="templateName", validation_alias="templateName")
    devices_attached: int = Field(serialization_alias="devicesAttached", validation_alias="devicesAttached")
    description: str = Field(serialization_alias="templateDescription", validation_alias="templateDescription")


class ConfigurationTemplateMaster(APIEndpoints):
    @get("/template/device", "data")
    def get_device_template_list(
        self, params: FeatureQueryParams = FeatureQueryParams()
    ) -> DataSequence[DeviceTemplateInfo]:
        ...

    @post("/template/device/feature")
    def create_device_template_from_feature_templates(self, payload: JSON) -> TemplateID:
        ...
