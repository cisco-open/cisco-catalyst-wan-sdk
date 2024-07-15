# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field, field_validator

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

Privilage = Literal["1", "15"]
AuthenticationOrder = Literal["local", "radius", "tacacs"]
TacacsAuthType = Literal["pap", "ascii"]
TaskPermission = Literal["read", "write"]
DefaultAction = Literal["accept", "deny"]
TaskMode = Literal["system", "interface", "policy", "routing", "security"]


class Command(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    command: str = Field(description="Define command", json_schema_extra={"vmanage_key": "command"})


class Task(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    name: str = Field(description="The name of the user", json_schema_extra={"vmanage_key": "name"})
    config_default_action: DefaultAction = Field(
        json_schema_extra={
            "vmanage_key": "default-action",
            "data_path": ["config"],
        },
        description="Define config default action",
    )
    oper_exec_default_action: DefaultAction = Field(
        json_schema_extra={
            "vmanage_key": "default-action",
            "data_path": ["oper-exec"],
        },
        description="Define oper-exec default action",
    )
    oper_exec_accept_action: Optional[List[Command]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "accept",
            "data_path": ["oper-exec"],
        },
        description="List of oper-exec commands to allow",
    )
    oper_exec_deny_action: Optional[List[Command]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "deny",
            "data_path": ["oper-exec"],
        },
        description="List of oper-exec commands to deny",
    )
    config_accept_action: Optional[List[Command]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "accept",
            "data_path": ["config"],
        },
        description="List of config commands to allow",
    )
    config_deny_action: Optional[List[Command]] = Field(
        default=None,
        json_schema_extra={
            "vmanage_key": "deny",
            "data_path": ["config"],
        },
        description="List of config commands to deny",
    )

    password: Optional[str] = Field(default=None, description="The password for the user")
    secret: Optional[str] = Field(default=None, description="The secret for the user")
    privilege: Optional[Privilage] = Field(default="15", description="The privilege level for the user")


class PubkeyChain(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    usertag: str = Field(
        description="User Tag",
        json_schema_extra={"vmanage_key": "usertag"},
    )
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
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    name: str = Field(description="The name of the user")
    password: Optional[str] = Field(default=None, description="The password for the user")
    secret: Optional[str] = Field(default=None, description="The secret for the user")
    description: Optional[str] = Field(default=None, description="Add a description of the user")
    group: Optional[List[str]] = Field(default=None, description="Configure the groups that the user is part of")
    pubkey_chain: Optional[List[PubkeyChain]] = Field(
        default=None,
        description="List of public keys for the user",
        json_schema_extra={"vmanage_key": "pubkey-chain"},
    )


class RadiusServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    address: str = Field(description="The IP address or hostname of the RADIUS server")
    auth_port: Optional[int] = Field(
        default=1812,
        json_schema_extra={"vmanage_key": "auth-port"},
        description="The authentication port for the RADIUS server",
    )
    tag: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "tag"},
        description="Reference tag/name for the server",
    )
    acct_port: Optional[int] = Field(
        default=1813,
        json_schema_extra={"vmanage_key": "acct-port"},
        description="The accounting port for the RADIUS server",
    )
    vpn: Optional[str] = Field(
        default=0,
        json_schema_extra={"vmanage_key": "vpn"},
        description="Set VPN in which RADIUS server is located",
    )
    source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "source-interface"},
        description="Set interface to use to reach RADIUS server",
    )
    key: Optional[str] = Field(default=None, description="Set the password to access the RADIUS server")
    secret_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "secret-key"},
        description="Set the AES encrypted key to access the RADIUS server",
    )
    priority: int = Field(default=0, description="RADIUS server priority <0..7>")


class TacacsServer(FeatureTemplateValidator):
    model_config = ConfigDict(populate_by_name=True, coerce_numbers_to_str=True)

    address: str = Field(description="The IP address or hostname of the TACACS+ server")
    auth_port: Optional[int] = Field(
        default=49,
        json_schema_extra={"vmanage_key": "auth-port"},
        description="The authentication port for the TACACS+ server",
    )
    vpn: Optional[str] = Field(
        default=0,
        json_schema_extra={"vmanage_key": "vpn"},
        description="Set VPN in which TACACS+ server is located",
    )
    source_interface: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "source-interface"},
        description="Set interface to use to reach TACACS+ server",
    )
    key: Optional[str] = Field(default=None, description="Set the password to access the TACACS+ server")
    secret_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "secret-key"},
        description="Set the AES encrypted key to access the TACACS+ server",
    )
    priority: int = Field(default=0, description="TACACS+ server priority <0..7>")


class TaskPermissions(FeatureTemplateValidator):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    mode: TaskMode = Field(
        json_schema_extra={"vmanage_key": "mode"},
        description="Select the task to set privileges for",
    )
    permission: List[TaskPermission] = Field(
        default="pap",
        json_schema_extra={
            "vmanage_key": "permission",
        },
        description="Set read or write permission for the task",
    )

    @field_validator("permission")
    def convert_permission_field(cls, val: List[TaskPermission]) -> List:
        permission_list = []
        for value in val:
            permission_list.append({"vipType": "constant", "vipValue": f"{value}", "vipObjectType": "object"})
        return permission_list


class UserGroup(FeatureTemplateValidator):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str = Field(
        json_schema_extra={"vmanage_key": "name"},
        description="Set name of user group",
    )
    task: List[TaskPermissions] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "task", "priority_order": ["mode", "permission"]},
        description="Set the user group's tasks and task privileges. Skipping tasks sets all as read and write",
    )


class AAAModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "AAA Feature Template configuration"

    auth_order: Optional[List[AuthenticationOrder]] = Field(
        validate_default=True,
        default=["local", "radius", "tacacs"],
        json_schema_extra={"vmanage_key": "auth-order", "data_path": ["aaa"]},
        description="ServerGroups authentication order to user access",
    )

    @field_validator("auth_order")
    def convert_to_auth_order_field(cls, val: Optional[List[AuthenticationOrder]]) -> List:
        auth_order_list = []
        if val:
            for value in val:
                auth_order_list.append({"vipType": "constant", "vipValue": f"{value}", "vipObjectType": "object"})
        return auth_order_list

    auth_fallback: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "auth-fallback",
        },
        description="Authenticate admin user as per auth-order",
    )
    admin_auth_order: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "admin-auth-order",
        },
        description="Fall back if higher-priority authentication fails",
    )
    netconf_disable: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["aaa", "logs"],
            "vmanage_key": "netconf-disable",
        },
        description="Disable Netconf logs",
    )
    audit_disable: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["aaa", "logs"],
            "vmanage_key": "audit-disable",
        },
        description="Disable audit logs",
    )
    radius_server_list: Optional[List[str]] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "radius-servers", "data_path": ["aaa"]},
        description="Designate radius servers for authentication and accounting",
    )
    task: Optional[List[Task]] = Field(
        default=None,
        frozen=True,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "audit-disable",
            "priority_order": ["name"],
        },
        description="Set the user group's tasks and task privileges.",
    )
    accounting: Optional[BoolStr] = Field(
        default=False,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "accounting",
        },
        description="Enable/disable user accounting",
    )
    usergroup: Optional[List[UserGroup]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "usergroup",
            "priority_order": ["name"],
        },
        description="Create groupings of users with the same authorization privileges. "
        "When used, overrides existing groups(netadmin, basic, operator)",
    )
    user: Optional[List[User]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "user",
        },
        description="List of local user configurations. When used, overrides existing users",
    )
    cisco_tac_ro_user: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "ciscotacro-user",
        },
        description="Cisco Tac Enable Read only",
    )
    cisco_tac_rw_user: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={
            "data_path": ["aaa"],
            "vmanage_key": "ciscotacrw-user",
        },
        description="Cisco Tac Enable Read and Write",
    )
    tacacs_timeout: Optional[int] = Field(
        default=5,
        json_schema_extra={
            "data_path": ["tacacs"],
            "vmanage_key": "timeout",
        },
        description="The timeout period in seconds for the TACACS+ server",
    )
    tacacs_authentication: Optional[TacacsAuthType] = Field(
        default="pap",
        json_schema_extra={
            "data_path": ["tacacs"],
            "vmanage_key": "authentication",
        },
        description="TACACS authentication type",
    )
    tacacs_server: Optional[List[TacacsServer]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["tacacs"],
            "priority_order": ["address", "auth-port", "vpn", "source-interface", "secret-key", "priority"],
            "vmanage_key": "server",
        },
        description="The list of TACACS+ servers",
    )
    radius_timeout: Optional[int] = Field(
        default=5,
        json_schema_extra={
            "data_path": ["radius"],
            "vmanage_key": "timeout",
        },
        description="The timeout period in seconds for the RADIUS server",
    )
    radius_retransmit: Optional[int] = Field(
        default=3,
        json_schema_extra={
            "data_path": ["radius"],
            "vmanage_key": "retransmit",
        },
        description="The number of retransmit attempts for the RADIUS server",
    )
    radius_server: Optional[List[RadiusServer]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["radius"],
            "priority_order": [
                "address",
                "auth-port",
                "vpn",
                "source-interface",
                "key",
                "secret-key",
                "priority",
                "tag",
                "acct-port",
            ],
            "vmanage_key": "server",
        },
        description="The list of RADIUS servers",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "aaa"
