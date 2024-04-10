# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, get


class CloudConnector(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cloud_enabled: Optional[bool] = Field(
        default=False, serialization_alias="cloudEnabled", validation_alias="cloudEnabled"
    )
    client_id: Optional[str] = Field(default=None, serialization_alias="clientId", validation_alias="clientId")
    client_secret: Optional[str] = Field(
        default=None, serialization_alias="clientSecret", validation_alias="clientSecret"
    )
    org_name: Optional[str] = Field(default=None, serialization_alias="orgName", validation_alias="orgName")
    affinity: Optional[str] = None
    telemetry_enabled: Optional[bool] = Field(
        default=None, serialization_alias="telemetryEnabled", validation_alias="telemetryEnabled"
    )


class SDAVCCloudConnector(APIEndpoints):
    def disable_cloud_connector(self):
        # PUT /sdavc/cloudconnector
        ...

    def enable_cloud_connector(self):
        # POST /sdavc/cloudconnector
        ...

    @get("/sdavc/cloudconnector")
    def get_cloud_connector(self) -> CloudConnector:
        ...

    def get_cloud_connector_status(self):
        # GET /sdavc/cloudconnector/status
        ...
