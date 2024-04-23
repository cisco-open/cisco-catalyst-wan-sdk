# Copyright 2023 Cisco Systems, Inc. and its affiliates

from enum import Enum
from pathlib import Path
from typing import ClassVar, List, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator


class User(FeatureTemplateValidator):
    name: str = Field(description="The name of the user")
    password: Optional[str] = Field(default=None, description="The password for the user")
    secret: Optional[str] = Field(default=None, description="The secret for the user")
    privilege: Optional[str] = Field(default=None, description="The privilege level for the user")
    pubkey_chain: List[str] = Field(
        default=[],
        json_schema_extra={"vmanage_key": "pubkey-chain", "vip_type": "ignore"},
        description="List of public keys for the user",
    )


class RadiusServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    address: str = Field(description="The IP address or hostname of the RADIUS server")
    auth_port: int = Field(
        default=1812,
        json_schema_extra={"vmanage_key": "auth-port"},
        description="The authentication port for the RADIUS server",
    )
    acct_port: int = Field(
        default=1813,
        json_schema_extra={"vmanage_key": "acct-port"},
        description="The accounting port for the RADIUS server",
    )
    timeout: int = Field(default=5, description="The timeout period in seconds for the RADIUS server")
    retransmit: int = Field(default=3, description="The number of retransmit attempts for the RADIUS server")
    key: str = Field(description="The key for the RADIUS server")
    secret_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "secret-key"},
        description="The secret key for the RADIUS server",
    )
    key_enum: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "key-enum"},
        description="The key enumeration for the RADIUS server",
    )
    key_type: Optional[str] = Field(
        default=None, json_schema_extra={"vmanage_key": "key-type"}, description="The key type for the RADIUS server"
    )


class RadiusGroup(FeatureTemplateValidator):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_name: str = Field(json_schema_extra={"vmanage_key": "group-name"}, description="The name of the RADIUS group")
    vpn: Optional[int] = Field(description="The VPN ID for the RADIUS group")
    source_interface: Optional[str] = Field(
        json_schema_extra={"vmanage_key": "source-interface"}, description="The source interface for the RADIUS group"
    )
    server: List[RadiusServer] = Field(default=[], description="The list of RADIUS servers for the group")


class DomainStripping(str, Enum):
    YES = "yes"
    NO = "no"
    RIGHT_TO_LEFT = "right-to-left"


class TacacsServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    address: str = Field(description="The IP address or hostname of the TACACS+ server")
    port: int = Field(default=49, description="The port for the TACACS+ server")
    timeout: int = Field(default=5, description="The timeout period in seconds for the TACACS+ server")
    key: str = Field(description="The key for the TACACS+ server")
    secret_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "secret-key"},
        description="The secret key for the TACACS+ server",
    )
    key_enum: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "key-enum"},
        description="The key enumeration for the TACACS+ server",
    )


class TacacsGroup(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    group_name: str = Field(
        json_schema_extra={"vmanage_key": "group-name"}, description="The name of the TACACS+ group"
    )
    vpn: int = Field(default=0, description="The VPN ID for the TACACS+ group")
    source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "source-interface"},
        description="The source interface for the TACACS+ group",
    )
    server: List[TacacsServer] = Field(default=[], description="The list of TACACS+ servers for the group")


class CiscoAAAModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    docs_description: str = Field(exclude=True, description="Cisco AAA Feature Template configuration.")

    user: Optional[List[User]] = Field(default=False, description="List of user configurations")
    authentication_group: bool = Field(
        default=False,
        json_schema_extra={"vmanage_key": "authentication_group"},
        description="Whether to enable the authentication group",
    )
    accounting_group: bool = Field(default=True, description="Whether to enable the accounting group")
    radius: Optional[List[RadiusGroup]] = Field(default=None, description="List of Radius group configurations")
    domain_stripping: Optional[DomainStripping] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "domain-stripping"},
        description="The domain stripping configuration",
    )
    port: int = Field(default=1700, description="The port number for AAA")
    tacacs: Optional[List[TacacsGroup]] = Field(default=None, description="List of TACACS group configurations")
    server_auth_order: str = Field(
        default="local",
        json_schema_extra={"vmanage_key": "server-auth-order"},
        description="Authentication order to user access",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cedge_aaa"
