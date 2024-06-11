# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.networks import IPvAnyAddress

from catalystwan.models.common import IntStr, VpnId
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
)


class TargetVpn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dns_server_ip: Optional[IPvAnyAddress] = Field(
        default=None, validation_alias="dnsServerIP", serialization_alias="dnsServerIP"
    )

    local_domain_bypass_enabled: bool = Field(
        default=True, validation_alias="localDomainBypassEnabled", serialization_alias="localDomainBypassEnabled"
    )

    uid: int
    umbrella_default: bool = Field(validation_alias="umbrellaDefault", serialization_alias="umbrellaDefault")
    vpns: List[VpnId]


class DnsSecurityDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    local_domain_bypass_enabled: Optional[bool] = Field(
        default=None, validation_alias="localDomainBypassEnabled", serialization_alias="localDomainBypassEnabled"
    )

    local_domain_bypass_list: Optional[Reference] = Field(
        default=None, validation_alias="localDomainBypassList", serialization_alias="localDomainBypassList"
    )

    dns_crypt: bool = Field(default=True, validation_alias="dnsCrypt", serialization_alias="dnsCrypt")
    match_all_vpn: bool = Field(default=True, validation_alias="matchAllVpn", serialization_alias="matchAllVpn")

    umbrella_data: Reference = Field(validation_alias="umbrellaData", serialization_alias="umbrellaData")
    child_org_id: Optional[IntStr] = Field(
        default=None, validation_alias="childOrgId", serialization_alias="childOrgId"
    )

    umbrella_default: Optional[bool] = Field(
        default=None, validation_alias="umbrellaDefault", serialization_alias="umbrellaDefault"
    )
    dns_server_ip: Optional[str] = Field(  # using st, because server accepts non ip strings also
        default=None, validation_alias="dnsServerIP", serialization_alias="dnsServerIP"
    )

    target_vpns: Optional[List[TargetVpn]] = Field(
        default=None, validation_alias="targetVpns", serialization_alias="targetVpns"
    )

    @classmethod
    def create_match_all_vpns_config(
        cls,
        umbrella_default: bool,
        umbrella_data: Reference,
        dns_crypt: bool = True,
        dns_server_ip: Optional[str] = None,
        local_domain_bypass_list: Optional[Reference] = None,
        child_org_id: Optional[IntStr] = None,
    ):
        if not umbrella_default and not dns_server_ip:
            raise ValueError("When umbrella default is False, then dns_server_ip must be provided.")

        local_domain_bypass_enabled = True if local_domain_bypass_list else False

        return cls(
            match_all_vpn=True,
            dns_crypt=dns_crypt,
            dns_server_ip=dns_server_ip,
            child_org_id=child_org_id,
            local_domain_bypass_enabled=local_domain_bypass_enabled,
            local_domain_bypass_list=local_domain_bypass_list,
            umbrella_data=umbrella_data,
            umbrella_default=umbrella_default,
        )

    @classmethod
    def create_match_custom_vpns_config(
        cls,
        dns_crypt: bool,
        umbrella_data: Reference,
        target_vpns=List[TargetVpn],
        local_domain_bypass_list: Optional[Reference] = None,
        child_org_id: Optional[IntStr] = None,
    ):
        return cls(
            match_all_vpn=False,
            dns_crypt=dns_crypt,
            child_org_id=child_org_id,
            local_domain_bypass_list=local_domain_bypass_list,
            umbrella_data=umbrella_data,
            target_vpns=target_vpns,
        )

    @field_validator("local_domain_bypass_list", mode="before")
    @classmethod
    def convert_empty_dict_to_none(cls, value):
        if not value:
            return None
        return value

    @field_validator("child_org_id", mode="before")
    @classmethod
    def convert_empty_int_str_to_none(cls, value):
        if value == "":
            return None
        return value


class DnsSecurityPolicy(PolicyDefinitionBase):
    type: Literal["dnsSecurity"] = "dnsSecurity"
    definition: DnsSecurityDefinition


class DnsSecurityPolicyEditPayload(DnsSecurityPolicy, PolicyDefinitionId):
    pass


class DnsSecurityPolicyGetResponse(DnsSecurityPolicy, PolicyDefinitionGetResponse):
    pass
