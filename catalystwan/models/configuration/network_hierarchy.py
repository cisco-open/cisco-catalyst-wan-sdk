# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.models.common import check_fields_exclusive

Label = Literal[
    "GLOBAL",
    "REGION",
    "SITE",
    "SUB_REGION",
]


class HierarchyId(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
    site_id: Optional[int] = Field(
        ge=0,
        le=4294967295,
        default=None,
        validation_alias="siteId",
        serialization_alias="siteId",
        description="Site ID",
    )
    region_id: Optional[int] = Field(
        ge=0, le=63, default=None, validation_alias="regionId", serialization_alias="regionId", description="Region ID"
    )
    sub_region_id: Optional[int] = Field(
        ge=0,
        le=63,
        default=None,
        validation_alias="subRegionId",
        serialization_alias="subRegionId",
        description="Sub Region ID",
    )

    @model_validator(mode="after")
    def one_of_site_region_subregion(self):
        check_fields_exclusive(self.__dict__, {"site_id", "region_id", "sub_region_id"}, True)
        return self


class Address(BaseModel):
    city: str
    country: str
    state: str
    street: str
    zipcode: str


class GpsLocation(BaseModel):
    latitude: int = Field(ge=-90, le=90, description="Set the site physical latitude")
    longitude: int = Field(ge=-180, le=180, description="Set the site physical longitude")


class Node(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    address: Optional[Address] = Field(default=None, description="Site Address")
    gps_location: Optional[GpsLocation] = Field(
        default=None, validation_alias="gpsLocation", serialization_alias="gpsLocation"
    )
    hierarchy_id: Optional[HierarchyId] = Field(
        default=None, validation_alias="hierarchyId", serialization_alias="hierarchyId"
    )
    is_secondary: Optional[bool] = Field(
        default=None,
        validation_alias="isSecondary",
        serialization_alias="isSecondary",
    )
    label: Optional[Label] = Field(default=None)
    parent_uuid: Optional[UUID] = Field(
        default=None, validation_alias="parentUuid", serialization_alias="parentUuid", description="Parent UUID"
    )


class NodeInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    data: Node
    description: Optional[str] = None
    direct_child_count: int = Field(validation_alias="directChildCount", serialization_alias="directChildCount")
    hierarchy_path: Optional[str] = Field(
        default=None, validation_alias="hierarchyPath", serialization_alias="hierarchyPath"
    )
    id: str
    name: str
    uuid: Optional[UUID] = None
