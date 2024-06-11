# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class TargetVpns(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    dns_server_ip: Optional[Global[str]] = Field(
        default=None, validation_alias="dnsServerIP", serialization_alias="dnsServerIP"
    )
    local_domain_bypass_enabled: Global[bool] = Field(
        validation_alias="localDomainBypassEnabled", serialization_alias="localDomainBypassEnabled"
    )
    uid: Global[str]
    umbrella_default: Global[bool] = Field(validation_alias="umbrellaDefault", serialization_alias="umbrellaDefault")
    vpns: Global[List[str]]


class DnsParcel(_ParcelBase):
    type_: Literal["dns"] = Field(default="dns", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    child_org_id: Optional[Global[str]] = Field(default=None, validation_alias=AliasPath("data", "childOrgId"))
    dns_crypt: Global[bool] = Field(validation_alias=AliasPath("data", "dnsCrypt"))
    dns_server_ip: Optional[Global[str]] = Field(default=None, validation_alias=AliasPath("data", "dnsServerIP"))
    local_domain_bypass_enabled: Optional[Global[bool]] = Field(
        default=None, validation_alias=AliasPath("data", "localDomainBypassEnabled")
    )
    local_domain_bypass_list: Optional[RefIdItem] = Field(
        default=None, validation_alias=AliasPath("data", "localDomainBypassList")
    )
    match_all_vpn: Global[bool] = Field(validation_alias=AliasPath("data", "matchAllVpn"))
    target_vpns: Optional[List[TargetVpns]] = Field(
        default=None,
        validation_alias=AliasPath("data", "targetVpns"),
        description="Will be under data field only if matchAllVpn is false,"
        " if matchAllVpn is true field should not be in payload",
    )
    umbrella_default: Optional[Global[bool]] = Field(
        default=None, validation_alias=AliasPath("data", "umbrellaDefault")
    )

    @model_validator(mode="after")
    def check_target_vpns(self):
        if self.match_all_vpn == Global[bool](value=True) and self.target_vpns is not None:
            raise ValueError("if match_all_vpn is true field target_vpns should not be in payload")
        elif self.match_all_vpn == Global[bool](value=False) and self.target_vpns is None:
            raise ValueError("if match_all_vpn is false field target_vpns should be in payload")
        return self
