from typing import List, Optional

from pydantic import AliasPath, BaseModel, Field, model_validator
from typing_extensions import Literal

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.common import (
    CarrierType,
    ControlPathType,
    EncapType,
    MultiRegionRole,
    OriginProtocol,
    SequenceIpType,
    ServiceChainNumber,
    ServiceType,
    TLOCActionType,
    TLOCColor,
    check_fields_exclusive,
)
from catalystwan.models.configuration.feature_profile.common import RefIdItem

Level = Literal[
    "REGION",
    "SITE",
    "SUB_REGION",
]


class InboundRegions(BaseModel):
    region: Optional[Global[str]] = Field(default=None)
    sub_region: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="subRegion", serialization_alias="subRegion"
    )


class OutboundRegions(BaseModel):
    region: Optional[Global[str]] = Field(default=None)
    sub_region: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="subRegion", serialization_alias="subRegion"
    )


class Target(BaseModel):
    inbound_regions: Optional[List[InboundRegions]] = Field(
        default=None, validation_alias="inboundRegions", serialization_alias="inboundRegions"
    )
    inbound_sites: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="inboundSites", serialization_alias="inboundSites"
    )
    level: Optional[Global[Level]] = Field(default=None)
    outbound_regions: Optional[List[OutboundRegions]] = Field(
        default=None, validation_alias="outboundRegions", serialization_alias="outboundRegions"
    )
    outbound_sites: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="outboundSites", serialization_alias="outboundSites"
    )
    vpn: Optional[Global[List[str]]] = Field(default=None)


BaseAction = Literal[
    "accept",
    "reject",
]

SequenceType = Literal[
    "route",
    "tloc",
]


class Regions(BaseModel):
    region: Optional[Global[str]] = Field(default=None)
    sub_region: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="subRegion", serialization_alias="subRegion"
    )


class Tloc(BaseModel):
    color: Optional[Global[TLOCColor]] = Field(default=None)
    encap: Optional[Global[EncapType]] = Field(default=None)
    ip: Optional[Global[str]] = Field(default=None)


class Entries(BaseModel):
    carrier: Optional[Global[CarrierType]] = Field(default=None)
    color_list: Optional[RefIdItem] = Field(default=None, validation_alias="colorList", serialization_alias="colorList")
    community: Optional[RefIdItem] = Field(default=None)
    domain_id: Optional[Global[int]] = Field(default=None, validation_alias="domainId", serialization_alias="domainId")
    expanded_community: Optional[RefIdItem] = Field(
        default=None, validation_alias="expandedCommunity", serialization_alias="expandedCommunity"
    )
    group_id: Optional[Global[int]] = Field(default=None, validation_alias="groupId", serialization_alias="groupId")
    ipv6prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="ipv6prefixList", serialization_alias="ipv6prefixList"
    )
    omp_tag: Optional[Global[int]] = Field(default=None, validation_alias="ompTag", serialization_alias="ompTag")
    origin: Optional[Global[OriginProtocol]] = Field(default=None)
    originator: Optional[Global[Global[str]]] = Field(default=None)
    path_type: Optional[Global[ControlPathType]] = Field(
        default=None, validation_alias="pathType", serialization_alias="pathType"
    )
    preference: Optional[Global[int]] = Field(default=None)
    prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="prefixList", serialization_alias="prefixList"
    )
    regions: Optional[List[Regions]] = Field(default=None)
    role: Optional[Global[MultiRegionRole]] = Field(default=None)
    site: Optional[Global[List[str]]] = Field(default=None)
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    vpn: Optional[Global[List[str]]] = Field(default=None)


class Match(BaseModel):
    entries: List[Entries] = Field()


class Service(BaseModel):
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    type: Optional[Global[ServiceType]] = Field(default=None)
    vpn: Optional[Global[int]] = Field(default=None)

    @model_validator(mode="after")
    def tloc_xor_tloc_list(self):
        check_fields_exclusive(self.__dict__, {"tloc", "tloc_list"}, True)
        return self


class ServiceChain(BaseModel):
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    type: Optional[Global[ServiceChainNumber]] = Field(default=None)
    vpn: Optional[Global[int]] = Field(default=None)

    @model_validator(mode="after")
    def tloc_xor_tloc_list(self):
        check_fields_exclusive(self.__dict__, {"tloc", "tloc_list"}, False)
        return self


class ActionSet(BaseModel):
    affinity: Optional[Global[int]] = Field(default=None)
    community: Optional[Global[str]] = Field(default=None)
    community_additive: Optional[Global[bool]] = Field(
        default=None, validation_alias="communityAdditive", serialization_alias="communityAdditive"
    )
    omp_tag: Optional[Global[int]] = Field(default=None, validation_alias="ompTag", serialization_alias="ompTag")
    preference: Optional[Global[int]] = Field(default=None)
    service: Optional[Service] = Field(default=None)
    service_chain: Optional[ServiceChain] = Field(
        default=None, validation_alias="serviceChain", serialization_alias="serviceChain"
    )
    tloc: Optional[Tloc] = Field(default=None)
    tloc_action: Optional[Global[TLOCActionType]] = Field(
        default=None, validation_alias="tlocAction", serialization_alias="tlocAction"
    )
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")


class Actions(BaseModel):
    export_to: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="exportTo", serialization_alias="exportTo"
    )
    set: Optional[List[ActionSet]] = Field(default=None)


class Sequences(BaseModel):
    actions: Optional[List[Actions]] = Field(default=None)
    base_action: Optional[Global[BaseAction]] = Field(
        default=None, validation_alias="baseAction", serialization_alias="baseAction"
    )
    match: Optional[Match] = Field(default=None)
    sequence_id: Optional[Global[int]] = Field(
        default=None, validation_alias="sequenceId", serialization_alias="sequenceId"
    )
    sequence_ip_type: Optional[Global[SequenceIpType]] = Field(
        default=None, validation_alias="sequenceIpType", serialization_alias="sequenceIpType"
    )
    sequence_name: Optional[Global[str]] = Field(
        default=None, validation_alias="sequenceName", serialization_alias="sequenceName"
    )
    sequence_type: Optional[Global[SequenceType]] = Field(
        default=None, validation_alias="sequenceType", serialization_alias="sequenceType"
    )


class CustomControlParcel(_ParcelBase):
    default_action: Optional[Global[BaseAction]] = Field(
        default=None, validation_alias="defaultAction", serialization_alias="defaultAction"
    )
    sequences: Optional[List[Sequences]] = Field(
        default=None,
        validation_alias=AliasPath("data", "sequences"),
        description="Sequence list",
    )
    target: Optional[Target] = Field(
        default=None,
        validation_alias=AliasPath("data", "target"),
        description="Target",
    )
