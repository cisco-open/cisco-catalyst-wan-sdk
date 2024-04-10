# Copyright 2023 Cisco Systems, Inc. and its affiliates

# mypy: disable-error-code="empty-body"
from datetime import datetime
from typing import Any, List, Optional

from packaging.version import Version  # type: ignore
from pydantic import BaseModel, ConfigDict, Field

from catalystwan.endpoints import APIEndpoints, get


class VersionField(Version):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        return Version(value)


class ServerInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    server: Optional[str] = None
    tenancy_mode: Optional[str] = Field(default=None, serialization_alias="tenancyMode", validation_alias="tenancyMode")
    user_mode: Optional[str] = Field(default=None, serialization_alias="userMode", validation_alias="userMode")
    vsession_id: Optional[str] = Field(default=None, serialization_alias="VSessionId", validation_alias="VSessionId")
    is_saml_user: Optional[bool] = Field(default=None, serialization_alias="isSamlUser", validation_alias="isSamlUser")
    is_rbac_vpn_user: Optional[bool] = Field(
        default=None, serialization_alias="isRbacVpnUser", validation_alias="isRbacVpnUser"
    )
    vpns: List[Any] = []
    csrf_token: Optional[str] = Field(default=None, serialization_alias="CSRFToken", validation_alias="CSRFToken")
    provider_domain: Optional[str] = Field(
        default=None, serialization_alias="providerDomain", validation_alias="providerDomain"
    )
    tenant_id: Optional[str] = Field(default=None, serialization_alias="tenantId", validation_alias="tenantId")
    provider_id: Optional[str] = Field(default=None, serialization_alias="providerId", validation_alias="providerId")
    view_mode: Optional[str] = Field(default=None, serialization_alias="viewMode", validation_alias="viewMode")
    capabilities: List[str] = []
    user: Optional[str] = None
    description: Optional[str] = None
    locale: Optional[str] = None
    roles: List[str] = []
    external_user: Optional[bool] = Field(
        default=None, serialization_alias="externalUser", validation_alias="externalUser"
    )
    platform_version: str = Field(default="", serialization_alias="platformVersion", validation_alias="platformVersion")
    general_template: Optional[bool] = Field(
        default=None, serialization_alias="generalTemplate", validation_alias="generalTemplate"
    )
    disable_full_config_push: Optional[bool] = Field(
        default=None, serialization_alias="disableFullConfigPush", validation_alias="disableFullConfigPush"
    )
    enable_server_events: Optional[bool] = Field(
        default=None, serialization_alias="enableServerEvents", validation_alias="enableServerEvents"
    )
    cloudx: Optional[str] = None
    reverseproxy: Optional[str] = None
    vmanage_mode: Optional[str] = Field(default=None, serialization_alias="vmanageMode", validation_alias="vmanageMode")


class AboutInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    title: Optional[str]
    version: str = Field(default="")
    application_version: Optional[str] = Field(
        serialization_alias="applicationVersion", validation_alias="applicationVersion"
    )
    application_server: Optional[str] = Field(
        serialization_alias="applicationServer", validation_alias="applicationServer"
    )
    copyright: Optional[str]
    time: Optional[datetime]
    time_zone: Optional[str] = Field(serialization_alias="timeZone", validation_alias="timeZone")
    logo: Optional[str]


class ServerReady(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    is_server_ready: bool = Field(serialization_alias="isServerReady", validation_alias="isServerReady")


class Client(APIEndpoints):
    @get("/client/server", "data")
    def server(self) -> ServerInfo:
        ...

    @get("/client/server/ready")
    def server_ready(self) -> ServerReady:
        ...

    @get("/client/about", "data")
    def about(self) -> AboutInfo:
        ...
