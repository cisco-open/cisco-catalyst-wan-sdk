# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

Version = Literal["TLSv1.1", "TLSv1.2"]


AuthType = Literal["Server", "Mutual"]


class TlsProfile(FeatureTemplateValidator):
    profile: str = Field(description="The name of the TLS profile")
    version: Optional[Version] = Field(
        default="TLSv1.1", json_schema_extra={"data_path": ["tls-version"]}, description="The TLS version"
    )
    auth_type: AuthType = Field(
        json_schema_extra={"vmanage_key": "auth-type"}, description="The authentication type for the TLS connection"
    )
    ciphersuite_list: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={"data_path": ["ciphersuite"], "vmanage_key": "ciphersuite-list"},
        description="The list of ciphersuites for the TLS connection",
    )
    model_config = ConfigDict(populate_by_name=True)


Priority = Literal["information", "debugging", "notice", "warn", "error", "critical", "alert", "emergency"]


class Server(FeatureTemplateValidator):
    name: str = Field(description="The hostname/IPv4 address of the server")
    vpn: Optional[int] = Field(description="The VPN ID for the server")
    source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "source-interface"},
        description="The source interface for the server",
    )
    priority: Optional[Priority] = Field(default="information", description="The priority level for logging messages")
    enable_tls: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"data_path": ["tls"], "vmanage_key": "enable-tls"},
        description="Whether to enable TLS encryption",
    )
    custom_profile: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"data_path": ["tls", "tls-properties"], "vmanage_key": "custom-profile"},
        description="Whether to use a custom TLS profile",
    )
    profile: Optional[str] = Field(
        default=None,
        json_schema_extra={"data_path": ["tls", "tls-properties"]},
        description="The custom TLS profile to use",
    )
    model_config = ConfigDict(populate_by_name=True)


class Ipv6Server(FeatureTemplateValidator):
    name: str = Field(description="The name of the IPv6 server")
    vpn: Optional[int] = Field(description="The VPN ID for the IPv6 server")
    source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "source-interface"},
        description="The source interface for the IPv6 server",
    )
    priority: Optional[Priority] = Field(
        default="information", description="The priority level for logging messages to the IPv6 server"
    )
    enable_tls: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"data_path": ["tls"], "vmanage_key": "enable-tls"},
        description="Whether to enable TLS encryption for the IPv6 server",
    )
    custom_profile: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={"data_path": ["tls", "tls-properties"], "vmanage_key": "custom-profile"},
        description="Whether to use a custom TLS profile for the IPv6 server",
    )
    profile: Optional[str] = Field(
        default=None,
        json_schema_extra={"data_path": ["tls", "tls-properties"]},
        description="The custom TLS profile to use for the IPv6 server",
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoLoggingModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco Logging Feature Template configuration"

    enable: Optional[BoolStr] = Field(
        default=None, json_schema_extra={"data_path": ["disk"]}, description="Whether logging to disk is enabled"
    )
    size: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["disk", "file"]},
        description="The maximum file size for the log file",
    )
    rotate: Optional[int] = Field(
        default=None,
        json_schema_extra={"data_path": ["disk", "file"]},
        description="The number of log files to maintain before rotating",
    )
    tls_profile: Optional[List[TlsProfile]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tls-profile"},
        description="List of TLS profiles configurations",
    )
    server: Optional[List[Server]] = Field(default=None, description="List of server configurations for logging")
    ipv6_server: Optional[List[Ipv6Server]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "ipv6-server"},
        description="List of IPv6 server configurations for logging",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_logging"
