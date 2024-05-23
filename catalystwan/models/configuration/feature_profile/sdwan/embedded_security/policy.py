# Copyright 2023 Cisco Systems, Inc. and its affiliates
# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

PredefinedZone = Literal["self", "default", "untrusted"]
SettingOn = Literal["on"]
FailureMode = Literal["close", "open"]


class AppHosting(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    nat: Union[Global[bool], Variable]
    database_url: Union[Global[bool], Variable] = Field(validation_alias="databaseUrl")
    resource_profile: Union[Global[bool], Variable] = Field(validation_alias="resourceProfile")


class NetworkSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    option_type: str = Field(default="network-settings", validation_alias="optionType")
    value: bool


class PolicySettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    tcp_syn_flood_limit: Global[str] = Field(default=None, validation_alias="tcpSynFloodLimit")
    max_incomplete_tcp_limit: Global[str] = Field(default=None, validation_alias="maxIncompleteTcpLimit")
    max_incomplete_udp_limit: Global[str] = Field(default=None, validation_alias="maxIncompleteUdpLimit")

    max_incomplete_icmp_limit: Global[str] = Field(default=None, validation_alias="maxIncompleteIcmpLimit")
    audit_trail: Global[SettingOn] = Field(default=None, validation_alias="auditTrail")
    unified_logging: Global[SettingOn] = Field(default=None, validation_alias="unifiedLogging")
    session_reclassify_allow: Global[SettingOn] = Field(default=None, validation_alias="sessionReclassifyAllow")
    icmp_unreachable_allow: Global[SettingOn] = Field(default=None, validation_alias="icmpUnreachableAllow")
    failure_mode: Global[FailureMode] = Field(default=None, validation_alias="failureMode")
    security_logging: NetworkSettings = Field(default=None, validation_alias="securityLogging")


class NgFirewallEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    src_zone: Union[RefIdItem, Global[PredefinedZone]] = Field(
        validation_alias="srcZone", serialization_alias="srcZone"
    )
    dst_zone: Union[RefIdItem, Global[PredefinedZone]] = Field(
        validation_alias="dstZone", serialization_alias="dstZone"
    )


class NgFirewall(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ref_id: Union[Global[UUID], Global[str]] = Field(validation_alias="refId", serialization_alias="refId")
    entries: List[NgFirewallEntry] = Field(validation_alias="entries", min_length=1)


class NgFirewallContainer(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ngfirewall: NgFirewall = Field(validation_alias="ngfirewall", serialization_alias="ngfirewall")


class SslDecryption(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ssl_decryption: RefIdItem = Field(validation_alias="sslDecryption", serialization_alias="sslDecryption")


class AdvancedInspectionProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    advanced_inspection_profile: RefIdItem = Field(validation_alias="advancedInspectionProfile")


class PolicyParcel(_ParcelBase):
    type_: Literal["policy"] = Field(default="policy", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    assembly: List[Union[NgFirewallContainer, SslDecryption, AdvancedInspectionProfile]] = Field(
        validation_alias=AliasPath("data", "assembly"), min_length=1
    )
    settings: PolicySettings = Field(default=None, validation_alias=AliasPath("data", "settings"))
    app_hosting: AppHosting = Field(default=None, validation_alias=AliasPath("data", "appHosting"))
