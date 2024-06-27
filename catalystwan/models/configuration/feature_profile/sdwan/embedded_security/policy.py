# Copyright 2023 Cisco Systems, Inc. and its affiliates
# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase, as_global, as_optional_global
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
    tcp_syn_flood_limit: Optional[Global[str]] = Field(
        default=None, validation_alias="tcpSynFloodLimit", serialization_alias="tcpSynFloodLimit"
    )
    max_incomplete_tcp_limit: Optional[Global[str]] = Field(
        default=None, validation_alias="maxIncompleteTcpLimit", serialization_alias="maxIncompleteTcpLimit"
    )
    max_incomplete_udp_limit: Optional[Global[str]] = Field(
        default=None, validation_alias="maxIncompleteUdpLimit", serialization_alias="maxIncompleteUdpLimit"
    )
    max_incomplete_icmp_limit: Optional[Global[str]] = Field(
        default=None, validation_alias="maxIncompleteIcmpLimit", serialization_alias="maxIncompleteIcmpLimit"
    )
    audit_trail: Optional[Global[SettingOn]] = Field(
        default=None, validation_alias="auditTrail", serialization_alias="auditTrail"
    )
    unified_logging: Optional[Global[SettingOn]] = Field(
        default=None, validation_alias="unifiedLogging", serialization_alias="unifiedLogging"
    )
    session_reclassify_allow: Optional[Global[SettingOn]] = Field(
        default=None, validation_alias="sessionReclassifyAllow", serialization_alias="sessionReclassifyAllow"
    )
    icmp_unreachable_allow: Optional[Global[SettingOn]] = Field(
        default=None, validation_alias="icmpUnreachableAllow", serialization_alias="icmpUnreachableAllow"
    )
    failure_mode: Optional[Global[FailureMode]] = Field(
        default=None, validation_alias="failureMode", serialization_alias="failureMode"
    )
    security_logging: Optional[NetworkSettings] = Field(
        default=None, validation_alias="securityLogging", serialization_alias="securityLogging"
    )

    @classmethod
    def create(
        cls,
        tcp_syn_flood_limit: Optional[str] = None,
        max_incomplete_tcp_limit: Optional[str] = None,
        max_incomplete_udp_limit: Optional[str] = None,
        max_incomplete_icmp_limit: Optional[str] = None,
        unified_logging: Optional[SettingOn] = None,
        session_reclassify_allow: Optional[SettingOn] = None,
        failure_mode: Optional[FailureMode] = None,
        audit_trail: Optional[SettingOn] = None,
        icmp_unreachable_allow: Optional[SettingOn] = None,
    ) -> Self:
        return cls(
            tcp_syn_flood_limit=as_optional_global(tcp_syn_flood_limit),
            max_incomplete_tcp_limit=as_optional_global(max_incomplete_tcp_limit),
            max_incomplete_udp_limit=as_optional_global(max_incomplete_udp_limit),
            max_incomplete_icmp_limit=as_optional_global(max_incomplete_icmp_limit),
            unified_logging=as_optional_global(unified_logging, SettingOn),
            session_reclassify_allow=as_optional_global(session_reclassify_allow, SettingOn),
            failure_mode=as_optional_global(failure_mode, FailureMode),
            audit_trail=as_optional_global(audit_trail, SettingOn),
            icmp_unreachable_allow=as_optional_global(icmp_unreachable_allow, SettingOn),
        )


class NgFirewallEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    src_zone: Union[RefIdItem, Global[PredefinedZone]] = Field(
        validation_alias="srcZone", serialization_alias="srcZone"
    )
    dst_zone: Union[RefIdItem, Global[PredefinedZone]] = Field(
        validation_alias="dstZone", serialization_alias="dstZone"
    )

    @classmethod
    def create(cls, src_zone: Union[UUID, PredefinedZone], dst_zone: Union[UUID, PredefinedZone]) -> Self:
        if type(src_zone) is UUID:
            _src_zone = RefIdItem.from_uuid(src_zone)
        else:
            _src_zone = as_global(src_zone, PredefinedZone)

        if type(dst_zone) is UUID:
            _dst_zone = RefIdItem.from_uuid(dst_zone)
        else:
            _dst_zone = as_global(dst_zone, PredefinedZone)

        return cls(
            src_zone=_src_zone,
            dst_zone=_dst_zone,
        )


class NgFirewall(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ref_id: Union[Global[UUID], Global[str]] = Field(validation_alias="refId", serialization_alias="refId")
    entries: List[NgFirewallEntry] = Field(validation_alias="entries", min_length=1)


class NgFirewallContainer(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ng_firewall: NgFirewall = Field(validation_alias="ngfirewall", serialization_alias="ngfirewall")


class SslDecryption(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    ssl_decryption: RefIdItem = Field(validation_alias="sslDecryption", serialization_alias="sslDecryption")

    @classmethod
    def from_uuid(cls, uuid: UUID) -> Self:
        return cls(ssl_decryption=RefIdItem.from_uuid(uuid))


class AdvancedInspectionProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    advanced_inspection_profile: RefIdItem = Field(validation_alias="advancedInspectionProfile")

    @classmethod
    def from_uuid(cls, uuid: UUID) -> Self:
        return cls(advanced_inspection_profile=RefIdItem.from_uuid(uuid))


class PolicyParcel(_ParcelBase):
    type_: Literal["policy"] = Field(default="policy", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    assembly: List[Union[NgFirewallContainer, SslDecryption, AdvancedInspectionProfile]] = Field(
        default=[], validation_alias=AliasPath("data", "assembly")
    )

    settings: Optional[PolicySettings] = Field(default=None, validation_alias=AliasPath("data", "settings"))
    app_hosting: Optional[AppHosting] = Field(default=None, validation_alias=AliasPath("data", "appHosting"))

    def add_ng_firewall_assembly(self, ng_firewall_id: UUID, entries: List[NgFirewallEntry] = []) -> None:
        self.assembly.append(
            NgFirewallContainer(ng_firewall=NgFirewall(ref_id=as_global(ng_firewall_id), entries=entries))
        )

    def add_ssl_decryption_assembly(self, ssl_decryption_profile_id: UUID) -> None:
        self.assembly.append(SslDecryption.from_uuid(ssl_decryption_profile_id))

    def add_advanced_inspection_profile_assembly(self, aip_id: UUID) -> None:
        self.assembly.append(AdvancedInspectionProfile.from_uuid(aip_id))
