# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
import datetime
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, get
from catalystwan.typed_list import DataSequence

FeatureType = Literal["all", "vmanage-default", "network-design", "cloud-dock", "lawful-interception"]


class FeatureQueryParams(BaseModel):
    summary: bool = Field(default=False)
    offset: Optional[int] = Field(default=None)
    limit: Optional[int] = Field(default=None)


class FeatureTemplateInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(serialization_alias="templateId", validation_alias="templateId")
    name: str = Field(serialization_alias="templateName", validation_alias="templateName")
    description: str = Field(serialization_alias="templateDescription", validation_alias="templateDescription")
    template_type: str = Field(serialization_alias="templateType", validation_alias="templateType")
    device_type: List[str] = Field(serialization_alias="deviceType", validation_alias="deviceType")
    last_updated_by: str = Field(serialization_alias="lastUpdatedBy", validation_alias="lastUpdatedBy")
    last_updated_on: datetime.datetime = Field(serialization_alias="lastUpdatedOn", validation_alias="lastUpdatedOn")
    factory_default: bool = Field(serialization_alias="factoryDefault", validation_alias="factoryDefault")
    devices_attached: int = Field(serialization_alias="devicesAttached", validation_alias="devicesAttached")
    attached_masters_count: Optional[str] = Field(
        default=None, serialization_alias="attachedMasterCount", validation_alias="attachedMasterCount"
    )
    version: str = Field(serialization_alias="templateMinVersion", validation_alias="templateMinVersion")
    config_type: str = Field(serialization_alias="configType", validation_alias="configType")
    created_by: Optional[str] = Field(default=None, serialization_alias="createdBy", validation_alias="createdBy")
    created_on: Optional[int] = Field(default=None, serialization_alias="createdOn", validation_alias="createdOn")
    resource_group: Optional[str] = Field(
        default=None, serialization_alias="resourceGroup", validation_alias="resourceGroup"
    )
    template_definition: Optional[str] = Field(
        default=None, serialization_alias="templateDefinition", validation_alias="templateDefinition"
    )


class FeatureTemplateDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    template_type: str = Field(serialization_alias="templateType", validation_alias="templateType")
    version: str = Field(serialization_alias="templateMinVersion", validation_alias="templateMinVersion")
    device_type: List[str] = Field(serialization_alias="deviceType", validation_alias="deviceType")
    last_updated_by: str = Field(serialization_alias="lastUpdatedBy", validation_alias="lastUpdatedBy")
    edited_template_definition: Optional[dict] = Field(
        serialization_alias="editedTemplateDefinition", validation_alias="editedTemplateDefinition"
    )
    templateDefinition: Optional[dict] = Field(
        serialization_alias="templateDefinition", validation_alias="templateDefinition"
    )
    config_type: str = Field(serialization_alias="configType", validation_alias="configType")
    attached_masters_count: Optional[str] = Field(
        default=None, serialization_alias="attachedMasterCount", validation_alias="attachedMasterCount"
    )
    name: str = Field(serialization_alias="templateName", validation_alias="templateName")
    id: str = Field(serialization_alias="templateId", validation_alias="templateId")
    factory_default: bool = Field(serialization_alias="factoryDefault", validation_alias="factoryDefault")
    feature: FeatureType
    created_on: Optional[int] = Field(default=None, serialization_alias="createdOn", validation_alias="createdOn")
    created_by: Optional[str] = Field(default=None, serialization_alias="createdBy", validation_alias="createdBy")
    devices_attached: int = Field(serialization_alias="devicesAttached", validation_alias="devicesAttached")
    description: str = Field(serialization_alias="templateDescription", validation_alias="templateDescription")
    last_updated_on: datetime.datetime = Field(serialization_alias="lastUpdatedOn", validation_alias="lastUpdatedOn")


class ConfigurationGeneralTemplate(APIEndpoints):
    @get("/template/feature", "data")
    def get_feature_template_list(
        self, params: FeatureQueryParams = FeatureQueryParams()
    ) -> DataSequence[FeatureTemplateInfo]:
        ...

    @get("/template/feature/object/{template_id}")
    def get_template_definition(self, template_id: UUID) -> DataSequence[FeatureTemplateDefinition]:
        ...
