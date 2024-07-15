# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

Privilage = Literal["1", "15"]

AccountingMethod = Literal["commands", "exec", "network", "system"]

AuthorizationMethod = Literal["commands"]

DomainStripping = Literal["yes", "no", "right-to-left"]

AuthenticationType = Literal["any", "all", "session-key"]


class PubkeyChain(FeatureTemplateValidator):
    key_string: str = Field(
        description="Set the RSA key string",
        json_schema_extra={"vmanage_key": "key-string"},
    )
    key_type: Optional[str] = Field(
        default="ssh-rsa",
        description="Only RSA is supported",
        json_schema_extra={"vmanage_key": "key-type"},
    )


class User(FeatureTemplateValidator):
    name: str = Field(description="The name of the user")
    password: Optional[str] = Field(default=None, description="The password for the user")
    secret: Optional[str] = Field(default=None, description="The secret for the user")
    privilege: Optional[Privilage] = Field(default="15", description="The privilege level for the user")
    pubkey_chain: Optional[List[PubkeyChain]] = Field(
        default=None,
        description="List of public keys for the user",
        json_schema_extra={"vmanage_key": "pubkey-chain"},
    )


class AccountingRule(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    rule_id: str = Field(
        description="Accounting Rule ID",
        json_schema_extra={"vmanage_key": "rule-id"},
    )
    method: AccountingMethod = Field(
        description="Configure Accounting Method",
        json_schema_extra={"vmanage_key": "method"},
    )
    level: Optional[Privilage] = Field(
        default=None,
        description="Privilege level when method is commands",
        json_schema_extra={"vmanage_key": "level"},
    )
    start_stop: Optional[BoolStr] = Field(
        default=True,
        description="Enable Start-Stop",
        json_schema_extra={"vmanage_key": "start-stop"},
    )
    group: str = Field(
        description="List of groups.",
        json_schema_extra={"vmanage_key": "group"},
    )


class AuthorizationRules(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    rule_id: str = Field(
        description="Authorization Rule ID",
        json_schema_extra={"vmanage_key": "rule-id"},
    )
    method: AuthorizationMethod = Field(
        description="Configure Authorization Method",
        json_schema_extra={"vmanage_key": "method"},
    )
    level: Optional[Privilage] = Field(
        default=None,
        description="Privilege level when method is commands",
        json_schema_extra={"vmanage_key": "level"},
    )
    group: str = Field(
        description="List of groups.",
        json_schema_extra={"vmanage_key": "group"},
    )
    authenticated: Optional[BoolStr] = Field(
        default=False,
        description="Succeed if user has authenticated",
        json_schema_extra={"vmanage_key": "if-authenticated"},
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
        default=None,
        json_schema_extra={"vmanage_key": "key-type"},
        description="The key type for the RADIUS server",
    )


class RadiusGroup(FeatureTemplateValidator):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    group_name: str = Field(
        json_schema_extra={"vmanage_key": "group-name"},
        description="The name of the RADIUS group",
    )
    vpn: Optional[int] = Field(description="The VPN ID for the RADIUS group")
    source_interface: Optional[str] = Field(
        json_schema_extra={"vmanage_key": "source-interface"},
        description="The source interface for the RADIUS group",
    )
    server: List[RadiusServer] = Field(default=[], description="The list of RADIUS servers for the group")


class RadiusVPN(FeatureTemplateValidator):
    name: str = Field(
        description="VPN ID",
        json_schema_extra={
            "vmanage_key": "name",
        },
    )
    server_key: str = Field(
        default=None,
        description="Specify a RADIUS client server-key",
        json_schema_extra={
            "vmanage_key": "server-key",
        },
    )  # needs enryption


class RadiusClient(FeatureTemplateValidator):
    ip: str = Field(
        description="The Client IP",
        json_schema_extra={"vmanage_key": "ip"},
    )
    vpn: List[RadiusVPN] = Field(
        description="The VPN Configuration",
        json_schema_extra={"vmanage_key": "vpn"},
    )


class TacacsServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True)

    address: str = Field(description="The IP address or hostname of the TACACS+ server")
    key: str = Field(description="The key for the TACACS+ server")
    port: int = Field(default=49, description="The port for the TACACS+ server")
    timeout: int = Field(default=5, description="The timeout period in seconds for the TACACS+ server")
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
        json_schema_extra={"vmanage_key": "group-name"},
        description="The name of the TACACS+ group",
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
    _docs_description: str = "Cisco AAA Feature Template configuration"

    authentication_group: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["authentication", "dot1x", "default"],
            "vmanage_key": "authentication_group",
        },
        description="Whether to enable the authentication group, GUI equivalent: Authentication Param",
    )
    accounting_group: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["accounting", "dot1x", "default", "start-stop"],
            "vmanage_key": "accounting_group",
        },
        description="Whether to enable the accounting group, GUI equivalent: Accounting Param",
    )
    server_auth_order: str = Field(
        default="local",
        json_schema_extra={"vmanage_key": "server-auth-order"},
        description="ServerGroups authentication order to user access",
    )  # example: "local,tacacs-5,radius-4"
    user: Optional[List[User]] = Field(default=None, description="List of local user configurations")

    accounting_rules: Optional[List[AccountingRule]] = Field(
        default=None,
        description="Configure the accounting rules",
        json_schema_extra={
            "data_path": ["accounting"],
            "vmanage_key": "accounting-rule",
        },
    )

    authorization_console: Optional[BoolStr] = Field(
        default=None,
        description="For enabling console authorization",
        json_schema_extra={
            "data_path": ["authorization"],
            "vmanage_key": "authorization-console",
        },
    )
    authorization_config_commands: Optional[BoolStr] = Field(
        default=None,
        description="For configuration mode commands",
        json_schema_extra={
            "data_path": ["authorization"],
            "vmanage_key": "authorization-config-commands",
        },
    )
    authorization_rules: Optional[List[AuthorizationRules]] = Field(
        default=None,
        description="Configure the accounting rules",
        json_schema_extra={
            "data_path": ["authorization"],
            "vmanage_key": "authorization-rule",
        },
    )
    radius: Optional[List[RadiusGroup]] = Field(default=None, description="List of Radius group configurations")
    radius_client: Optional[List[RadiusClient]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["radius-dynamic-author"],
            "vmanage_key": "radius-client",
        },
        description="Specify a RADIUS client",
    )
    domain_stripping: Optional[DomainStripping] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["radius-dynamic-author"],
            "vmanage_key": "domain-stripping",
        },
        description="The domain stripping configuration",
    )
    authentication_type: Optional[AuthenticationType] = Field(
        default="any",
        json_schema_extra={
            "data_path": ["radius-dynamic-author"],
            "vmanage_key": "auth-type",
        },
        description="Authentication Type",
    )
    port: Optional[int] = Field(
        default=1700,
        json_schema_extra={
            "data_path": ["radius-dynamic-author"],
            "vmanage_key": "port",
        },
        description="Specify Radius Dynamic Author Port",
    )
    server_key_password: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["radius-dynamic-author"],
            "vmanage_key": "rda-server-key",
        },
        description="Specify a radius dynamic author server-key",
    )  # needs encryption

    cts_authorization_list: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["radius-trustsec"],
            "vmanage_key": "cts-auth-list",
        },
        description="Specify a radius dynamic author server-key",
    )
    radius_trustsec_group: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["radius-trustsec"],
            "vmanage_key": "radius-trustsec-group",
        },
        description="RADIUS trustsec group",
    )
    tacacs: Optional[List[TacacsGroup]] = Field(default=None, description="List of TACACS group configurations")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cedge_aaa"
