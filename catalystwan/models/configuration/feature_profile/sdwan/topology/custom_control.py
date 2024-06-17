from ipaddress import IPv4Address
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
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

BaseAction = Literal[
    "accept",
    "reject",
]

SequenceType = Literal[
    "route",
    "tloc",
]


class Region(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    region: Optional[Global[str]] = Field(default=None)
    sub_region: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="subRegion", serialization_alias="subRegion"
    )


class Target(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    inbound_regions: Optional[List[Region]] = Field(
        default=None, validation_alias="inboundRegions", serialization_alias="inboundRegions"
    )
    inbound_sites: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="inboundSites", serialization_alias="inboundSites"
    )
    level: Optional[Global[Level]] = Field(default=None)
    outbound_regions: Optional[List[Region]] = Field(
        default=None, validation_alias="outboundRegions", serialization_alias="outboundRegions"
    )
    outbound_sites: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="outboundSites", serialization_alias="outboundSites"
    )
    vpn: Optional[Global[List[str]]] = Field(default=None)


class Tloc(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    color: Optional[Global[TLOCColor]] = Field(default=None)
    encap: Optional[Global[EncapType]] = Field(default=None)
    ip: Optional[Global[str]] = Field(default=None)


class Entry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
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
    originator: Optional[Global[str]] = Field(default=None)
    path_type: Optional[Global[ControlPathType]] = Field(
        default=None, validation_alias="pathType", serialization_alias="pathType"
    )
    preference: Optional[Global[int]] = Field(default=None)
    prefix_list: Optional[RefIdItem] = Field(
        default=None, validation_alias="prefixList", serialization_alias="prefixList"
    )
    regions: Optional[List[Region]] = Field(default=None)
    role: Optional[Global[MultiRegionRole]] = Field(default=None)
    site: Optional[Global[List[str]]] = Field(default=None)
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    vpn: Optional[Global[List[str]]] = Field(default=None)


class Match(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    entries: List[Entry] = Field()


class Service(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    type: Optional[Global[ServiceType]] = Field(default=None)
    vpn: Optional[Global[int]] = Field(default=None)

    @model_validator(mode="after")
    def tloc_xor_tloc_list(self):
        check_fields_exclusive(self.__dict__, {"tloc", "tloc_list"}, True)
        return self


class ServiceChain(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    tloc: Optional[Tloc] = Field(default=None)
    tloc_list: Optional[RefIdItem] = Field(default=None, validation_alias="tlocList", serialization_alias="tlocList")
    type: Optional[Global[ServiceChainNumber]] = Field(default=None)
    vpn: Optional[Global[int]] = Field(default=None)

    @model_validator(mode="after")
    def tloc_nand_tloc_list(self):
        check_fields_exclusive(self.__dict__, {"tloc", "tloc_list"}, False)
        return self


class ActionSet(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
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
    model_config = ConfigDict(populate_by_name=True)
    export_to: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="exportTo", serialization_alias="exportTo"
    )
    set: Optional[List[ActionSet]] = Field(default=None)


class Sequence(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
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

    def _get_match(self) -> Match:
        if self.match is None:
            self.match = Match(entries=[])
        if self.match.entries is None:
            self.match.entries = []
        return self.match

    def _match(self, entry: Entry):
        self._get_match().entries.append(entry)

    def _get_regions_entry(self) -> Entry:
        entries = self._get_match().entries
        for entry in entries:
            if entry.regions is not None:
                return entry
        entry = Entry()
        entries.append(entry)
        return entry

    def match_carrier(self, carrier: CarrierType):
        entry = Entry(carrier=as_global(carrier, CarrierType))
        self._match(entry)

    def match_color_list(self, list_id: UUID):
        entry = Entry(color_list=RefIdItem(ref_id=as_global(str(list_id))))
        self._match(entry)

    def match_community(self, list_id: UUID):
        entry = Entry(community=RefIdItem(ref_id=as_global(str(list_id))))
        self._match(entry)

    def match_domain_id(self, domain_id: int):
        entry = Entry(domain_id=as_global(domain_id))
        self._match(entry)

    def match_expanded_community(self, list_id: UUID):
        entry = Entry(expanded_community=RefIdItem(ref_id=as_global(str(list_id))))
        self._match(entry)

    def match_group_id(self, group_id: int):
        entry = Entry(group_id=as_global(group_id))
        self._match(entry)

    def match_ipv6prefix_list(self, list_id: UUID):
        entry = Entry(ipv6prefix_list=RefIdItem(ref_id=as_global(str(list_id))))
        self._match(entry)

    def match_omp_tag(self, omp_tag: int):
        entry = Entry(omp_tag=as_global(omp_tag))
        self._match(entry)

    def match_origin(self, origin: OriginProtocol):
        entry = Entry(origin=as_global(origin, OriginProtocol))
        self._match(entry)

    def match_originator(self, originator: IPv4Address):
        entry = Entry(originator=as_global(str(originator)))
        self._match(entry)

    def match_path_type(self, path_type: ControlPathType):
        entry = Entry(path_type=as_global(path_type, ControlPathType))
        self._match(entry)

    def match_preference(self, preference: int):
        entry = Entry(preference=as_global(preference))
        self._match(entry)

    def match_prefix_list(self, list_id: UUID):
        entry = Entry(prefix_list=RefIdItem(ref_id=as_global(str(list_id))))
        self._match(entry)

    def match_region(self, region: str, subregions: Optional[List[str]] = None):
        _region = Region(
            region=as_global(region),
            sub_region=as_global(subregions) if subregions else None,
        )
        entry = self._get_regions_entry()
        if entry.regions:
            entry.regions.append(_region)
        else:
            entry.regions = [_region]

    def match_role(self, role: MultiRegionRole):
        entry = Entry(role=as_global(role, MultiRegionRole))
        self._match(entry)

    def match_sites(self, sites: List[str]):
        entry = Entry(site=as_global(sites))
        self._match(entry)

    def match_tloc(self, ip: IPv4Address, color: TLOCColor, encap: EncapType):
        entry = Entry(
            tloc=Tloc(color=as_global(color, TLOCColor), encap=as_global(encap, EncapType), ip=as_global(str(ip)))
        )
        self._match(entry)

    def match_tloc_list(self, list_id: UUID):
        entry = Entry(tloc_list=RefIdItem(ref_id=as_global(str(list_id))))
        self._match(entry)

    def match_vpns(self, vpns: List[str]):
        entry = Entry(vpn=as_global(vpns))
        self._match(entry)


class CustomControlParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["custom-control"] = Field(default="custom-control", exclude=True)
    default_action: Optional[Global[BaseAction]] = Field(
        default=None, validation_alias=AliasPath("data", "defaultAction")
    )
    sequences: Optional[List[Sequence]] = Field(
        default=None,
        validation_alias=AliasPath("data", "sequences"),
        description="Sequence list",
    )
    target: Optional[Target] = Field(
        default=None,
        validation_alias=AliasPath("data", "target"),
        description="Target",
    )

    def set_default_action(self, action: BaseAction = "reject"):
        self.default_action = as_global(action, BaseAction)

    def assign_target(
        self,
        vpns: List[str],
        inbound_sites: Optional[List[str]] = None,
        outbound_sites: Optional[List[str]] = None,
    ) -> Target:
        self.target = Target(
            inbound_sites=as_global(inbound_sites) if inbound_sites else None,
            outbound_sites=as_global(outbound_sites) if outbound_sites else None,
            vpn=as_global(vpns),
        )
        return self.target

    def add_sequence(
        self, name: str, id_: int, type_: SequenceType, ip_type: SequenceIpType, base_action: BaseAction
    ) -> Sequence:
        seq = Sequence(
            base_action=as_global(base_action, BaseAction),
            sequence_id=as_global(id_),
            sequence_ip_type=as_global(ip_type, SequenceIpType),
            sequence_name=as_global(name),
            sequence_type=as_global(type_, SequenceType),
        )
        if self.sequences is None:
            self.sequences = [seq]
        else:
            self.sequences.append(seq)
        return seq
