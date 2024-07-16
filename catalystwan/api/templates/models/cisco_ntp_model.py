# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class Server(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(description="The hostname or IP address of the NTP server")
    key: Optional[int] = Field(default=None, description="The identifier for the authentication key")
    vpn: Optional[int] = Field(default=None, description="The VPN ID associated with the NTP server")
    version: Optional[int] = Field(default=None, description="The NTP version used")
    source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "source-interface"},
        description="The source interface for NTP messages",
    )
    prefer: Optional[BoolStr] = Field(default=None, description="Whether this server is preferred over others")


class Authentication(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    number: int = Field(description="The authentication key number")
    md5: str = Field(description="The MD5 hash used for authentication")


class CiscoNTPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco NTP Feature Template configuration"

    server: List[Server] = Field(default=[], description="List of NTP servers")
    authentication: Optional[List[Authentication]] = Field(
        default=None, json_schema_extra={"data_path": ["keys"]}, description="List of authentication keys"
    )
    trusted: Optional[List[int]] = Field(
        default=None, json_schema_extra={"data_path": ["keys"]}, description="List of trusted key numbers"
    )
    enable: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"data_path": ["master"]}, description="Whether the device is an NTP master"
    )
    stratum: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["master"]},
        description="The stratum level if the device is an NTP master",
    )
    source: Optional[str] = Field(
        default=None,
        json_schema_extra={"data_path": ["master"]},
        description="The source interface for NTP messages if the device is an NTP master",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_ntp"
