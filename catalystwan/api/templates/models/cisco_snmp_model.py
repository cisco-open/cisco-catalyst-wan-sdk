# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator

Authorization = Literal["read-only"]
SecurityLevel = Literal["no-auth-no-priv", "auth-no-priv", "auth-priv"]
Auth = Literal["md5", "sha"]
Priv = Literal["aes-cfb-128", "aes-256-cfb-128"]


class Oid(FeatureTemplateValidator):
    id: str = Field(description="The OID (Object Identifier) to include or exclude in the view")
    exclude: Optional[BoolStr] = Field(
        default=None, description="Indicates whether the OID should be excluded from the view"
    )


class View(FeatureTemplateValidator):
    name: str = Field(description="The name of the SNMP view")
    oid: Optional[List[Oid]] = Field(default=None, description="List of OIDs to include or exclude in the view")


class Community(FeatureTemplateValidator):
    name: str = Field(description="The name of the SNMP community")
    view: str = Field(description="The SNMP view associated with the community")
    authorization: Authorization = Field(description="The authorization level of the community")


class Group(FeatureTemplateValidator):
    name: str = Field(description="The name of the SNMP group")
    security_level: SecurityLevel = Field(
        description="The security level associated with the group", json_schema_extra={"vmanage_key": "security-level"}
    )
    view: str = Field(description="The SNMP view associated with the group")
    model_config = ConfigDict(populate_by_name=True)


class User(FeatureTemplateValidator):
    name: str = Field(description="The name of the SNMP user")
    auth: Optional[Auth] = Field(default=None, description="The authentication protocol used")
    auth_password: Optional[str] = Field(
        default=None, description="The password for authentication", json_schema_extra={"vmanage_key": "auth-password"}
    )
    priv: Optional[Priv] = Field(default=None, description="The privacy (encryption) protocol used")
    priv_password: Optional[str] = Field(
        default=None, description="The password for privacy", json_schema_extra={"vmanage_key": "priv-password"}
    )
    group: str = Field(description="The group to which the user belongs")
    model_config = ConfigDict(populate_by_name=True)


class Target(FeatureTemplateValidator):
    vpn_id: int = Field(
        description="The VPN ID where the SNMP target resides", json_schema_extra={"vmanage_key": "vpn-id"}
    )
    ip: str = Field(description="The IP address of the SNMP target")
    port: int = Field(description="The port number for the SNMP target")
    community_name: Optional[str] = Field(
        default=None,
        description="The community name for the SNMP target",
        json_schema_extra={"vmanage_key": "community-name"},
    )
    user: Optional[str] = Field(default=None, description="The user name for the SNMP target")
    source_interface: Optional[str] = Field(
        default=None,
        description="The source interface for sending SNMP traps",
        json_schema_extra={"vmanage_key": "source-interface"},
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoSNMPModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco SNMP Feature Template configuration"

    shutdown: Optional[BoolStr] = Field(
        default=True, description="Indicates whether SNMP is administratively shut down"
    )
    contact: Optional[str] = Field(default=None, description="The contact information for the SNMP administrator")
    location: Optional[str] = Field(default=None, description="The physical location information for the SNMP agent")
    view: Optional[List[View]] = Field(default=None, description="List of SNMP views for controlling access to OIDs")
    community: Optional[List[Community]] = Field(
        default=None, description="List of SNMP communities for different access rights"
    )
    group: Optional[List[Group]] = Field(
        default=None, description="List of SNMP groups defining security models and access rights"
    )
    user: Optional[List[User]] = Field(
        default=None, description="List of SNMP users with authentication and privacy configurations"
    )
    target: Optional[List[Target]] = Field(
        default=None, json_schema_extra={"data_path": ["trap"]}, description="List of SNMP targets for sending traps"
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_snmp"
