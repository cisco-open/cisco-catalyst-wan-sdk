# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Optional

from pydantic import BaseModel, Field


class UrlMonitoringInfo(BaseModel):
    url: Optional[str] = None
    threshold: Optional[int] = None
    alarm_raised: Optional[bool] = Field(
        default=None, serialization_alias="lastUpdatedBy", validation_alias="lastUpdatedBy"
    )


class UrlMonitoringConfig(BaseModel):
    url: str = Field(..., examples=["/client/server/ready"], description="URL registered for monitoring requests.")
    threshold: int = Field(
        ge=10,
        le=100,
        title="Threshold",
        description="vManage alarm is raised after reaching the threshold. "
        "Threshold should be within a range of 10 and 100 inclusive.",
    )


class DeleteUrlMonitorRequest(BaseModel):
    url: str = Field(..., examples=["/client/server/ready"], description="URL registered for monitoring requests.")
