from ipaddress import IPv4Address
from typing import Any, Dict, List, Literal, Optional, overload
from uuid import UUID

from pydantic import (
    AliasPath,
    BaseModel,
    ConfigDict,
    Field,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    model_serializer,
    model_validator,
)
from typing_extensions import Annotated

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, as_global
from catalystwan.models.common import (
    AcceptRejectActionType,
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
    VersionedField,
    check_fields_exclusive,
)
from catalystwan.models.configuration.feature_profile.common import RefIdItem

Level = Literal[
    "REGION",
    "SITE",
    "SUB_REGION",
]

ControlSequenceType = Literal[
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
    level: Annotated[Optional[Global[Level]], VersionedField(versions="<20.15", forbidden=True)] = Field(default=None)
    outbound_regions: Optional[List[Region]] = Field(
        default=None, validation_alias="outboundRegions", serialization_alias="outboundRegions"
    )
    outbound_sites: Optional[Global[List[str]]] = Field(
        default=None, validation_alias="outboundSites", serialization_alias="outboundSites"
    )
    vpn: Optional[Global[List[str]]] = Field(default=None)

    @model_serializer(mode="wrap", when_used="json")
    def serialize(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> Dict[str, Any]:
        return VersionedField.dump(self.model_fields, handler(self), info)


class Tloc(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    color: Optional[Global[TLOCColor]] = Field(default=None)
    encap: Optional[Global[EncapType]] = Field(default=None)
    ip: Optional[Global[str]] = Field(default=None)

    @staticmethod
    def from_params(color: TLOCColor, encap: EncapType, ip: IPv4Address) -> "Tloc":
        _color = as_global(color, TLOCColor)
        _encap = as_global(encap, EncapType)
        _ip = as_global(str(ip))
        return Tloc(color=_color, encap=_encap, ip=_ip)


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
    actions: Optional[List[Actions]] = Field(default_factory=list)
    base_action: Optional[Global[AcceptRejectActionType]] = Field(
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
    sequence_type: Optional[Global[ControlSequenceType]] = Field(
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

    @property
    def _action(self) -> Actions:
        if not self.actions:
            self.actions = [Actions()]
        return self.actions[0]

    @property
    def _action_set(self) -> ActionSet:
        action = self._action
        if action.set is None:
            action.set = [ActionSet()]
        return action.set[0]

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

    def associate_affinitty_action(self, affinity: int) -> None:
        self._action_set.affinity = as_global(affinity)

    def associate_community_additive_action(self, additive: bool) -> None:
        self._action_set.community_additive = as_global(additive)

    def associate_community_action(self, community: str) -> None:
        self._action_set.community = as_global(community)

    def associate_omp_tag_action(self, omp_tag: int) -> None:
        self._action_set.omp_tag = as_global(omp_tag)

    def associate_preference_action(self, preference: int) -> None:
        self._action_set.preference = as_global(preference)

    @overload
    def associate_service_action(self, service_type: ServiceType, vpn: Optional[int], *, tloc_list_id: UUID) -> None:
        ...

    @overload
    def associate_service_action(
        self, service_type: ServiceType, vpn: Optional[int], *, ip: IPv4Address, color: TLOCColor, encap: EncapType
    ) -> None:
        ...

    def associate_service_action(
        self, service_type=ServiceType, vpn=Optional[int], *, tloc_list_id=None, ip=None, color=None, encap=None
    ) -> None:
        _vpn = as_global(vpn) if vpn is not None else None
        _service_type = as_global(service_type, ServiceType)
        if tloc_list_id is not None:
            service = Service(
                tloc_list=RefIdItem(ref_id=as_global(str(tloc_list_id))),
                type=_service_type,
                vpn=_vpn,
            )
        else:
            _tloc = Tloc.from_params(color=color, encap=encap, ip=ip)
            service = Service(tloc=_tloc, type=_service_type, vpn=_vpn)
        self._action_set.service = service

    def associate_tloc(self, color: TLOCColor, encap: EncapType, ip: IPv4Address) -> None:
        self._action_set.tloc = Tloc.from_params(color=color, encap=encap, ip=ip)

    def associate_tloc_action(self, tloc_action_type: TLOCActionType) -> None:
        self._action_set.tloc_action = as_global(tloc_action_type, TLOCActionType)

    def associate_tloc_list(self, tloc_list_id: UUID) -> None:
        self._action_set.tloc_list = RefIdItem(ref_id=as_global(str(tloc_list_id)))


class CustomControlParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["custom-control"] = Field(default="custom-control", exclude=True)
    default_action: Optional[Global[AcceptRejectActionType]] = Field(
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

    def set_default_action(self, action: AcceptRejectActionType = "reject"):
        self.default_action = as_global(action, AcceptRejectActionType)

    def assign_target_sites(
        self,
        inbound_sites: List[str],
        outbound_sites: List[str],
        _dummy_vpns: Optional[
            List[str]
        ],  # mitigate a bug (vpn is not used but value needs to be provided for server to accept the message)
    ) -> Target:
        self.target = Target(
            vpn=Global[List[str]](value=_dummy_vpns) if _dummy_vpns is not None else None,
            level=as_global("SITE", Level),
            inbound_sites=as_global(inbound_sites) if inbound_sites else None,
            outbound_sites=as_global(outbound_sites) if outbound_sites else None,
        )
        return self.target

    def add_sequence(
        self,
        name: str,
        id_: int,
        type_: ControlSequenceType,
        ip_type: SequenceIpType,
        base_action: AcceptRejectActionType,
    ) -> Sequence:
        seq = Sequence(
            base_action=as_global(base_action, AcceptRejectActionType),
            sequence_id=as_global(id_),
            sequence_ip_type=as_global(ip_type, SequenceIpType),
            sequence_name=as_global(name),
            sequence_type=as_global(type_, ControlSequenceType),
        )
        if self.sequences is None:
            self.sequences = [seq]
        else:
            self.sequences.append(seq)
        return seq
