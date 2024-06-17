# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global, as_optional_global
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

    @classmethod
    def create(
        cls,
        local_domain_bypass_enabled: bool,
        uid: str,
        umbrella_default: bool,
        vpns: List[str],
        dns_server_ip: Optional[str] = None,
    ) -> Self:
        return cls(
            dns_server_ip=as_optional_global(dns_server_ip),
            local_domain_bypass_enabled=as_global(local_domain_bypass_enabled),
            uid=as_global(str(uid)),
            umbrella_default=as_global(umbrella_default),
            vpns=as_global([vpn for vpn in vpns]),
        )


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

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        dns_crypt: bool,
        match_all_vpn: bool,
        dns_server_ip: Optional[str],
        child_org_id: Optional[int],
        umbrella_default: Optional[bool],
        local_domain_bypass_enabled: Optional[bool],
        local_domain_bypass_list: Optional[UUID],
        target_vpns: Optional[List[TargetVpns]] = None,
    ) -> Self:
        _child_org_id = as_global(str(child_org_id)) if child_org_id is not None else None
        _dns_server_ip = as_global(dns_server_ip) if dns_server_ip else None
        _local_domain_bypass_list = RefIdItem.from_uuid(local_domain_bypass_list) if local_domain_bypass_list else None

        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            local_domain_bypass_enabled=as_optional_global(local_domain_bypass_enabled),
            local_domain_bypass_list=_local_domain_bypass_list,
            dns_crypt=as_global(dns_crypt),
            match_all_vpn=as_global(match_all_vpn),
            umbrella_default=as_optional_global(umbrella_default),
            child_org_id=_child_org_id,
            dns_server_ip=_dns_server_ip,
            target_vpns=target_vpns,
        )
