# Copyright 2023 Cisco Systems, Inc. and its affiliates
from functools import lru_cache
from typing import Generic, List, Literal, Sequence, TypeVar, Union, cast
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.application_priority import AnyApplicationPriorityParcel
from catalystwan.models.configuration.feature_profile.sdwan.cli import AnyCliParcel
from catalystwan.models.configuration.feature_profile.sdwan.dns_security import AnyDnsSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.embedded_security import AnyEmbeddedSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.other import AnyOtherParcel
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing import AnyRoutingParcel
from catalystwan.models.configuration.feature_profile.sdwan.service import AnyServiceParcel
from catalystwan.models.configuration.feature_profile.sdwan.sig_security import AnySIGSecurityParcel
from catalystwan.models.configuration.feature_profile.sdwan.system import AnySystemParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology import AnyTopologyParcel
from catalystwan.models.configuration.feature_profile.sdwan.transport import AnyTransportParcel
from catalystwan.utils.model import resolve_nested_base_model_unions

ParcelType = Literal[
    "aaa",
    "app-list",
    "app-probe",
    "appqoe",
    "as-path",
    "banner",
    "basic",
    "bfd",
    "bgp",
    "cellular-controller",
    "class",
    "color",
    "config",
    "custom-control",
    "data-ipv6-prefix",
    "data-prefix",
    "dhcp-server",
    "dns",
    "expanded-community",
    "ext-community",
    "global",
    "gps",
    "hubspoke",
    "ipv4-acl",
    "ipv6-acl",
    "ipv6-prefix",
    "lan/vpn",
    "lan/vpn/interface/ethernet",
    "lan/vpn/interface/gre",
    "lan/vpn/interface/ipsec",
    "lan/vpn/interface/multilink",
    "lan/vpn/interface/svi",
    "logging",
    "management/vpn",
    "management/vpn/interface/ethernet",
    "mesh",
    "mirror",
    "mrf",
    "ntp",
    "omp",
    "policer",
    "policy-settings",
    "preferred-color-group",
    "prefix",
    "qos-policy",
    "routing/bgp",
    "routing/eigrp",
    "routing/multicast",
    "routing/ospf",
    "routing/ospfv3/ipv4",
    "routing/ospfv3/ipv6",
    "security-fqdn",
    "security-geolocation",
    "security-ipssignature",
    "security-localapp",
    "security-localdomain",
    "security-port",
    "security-protocolname",
    "security-urllist",
    "security-zone",
    "security",
    "sig",
    "sla-class",
    "snmp",
    "standard-community",
    "switchport",
    "tloc",
    "tracker",
    "trackergroup",
    "unified/advanced-inspection-profile",
    "unified/advanced-malware-protection",
    "unified/intrusion-prevention",
    "unified/ssl-decryption-profile",
    "unified/ssl-decryption",
    "unified/url-filtering",
    "wan/vpn",
    "wan/vpn/interface/cellular",
    "wan/vpn/interface/dsl-ipoe",
    "wan/vpn/interface/dsl-pppoa",
    "wan/vpn/interface/dsl-pppoe",
    "wan/vpn/interface/ethernet",
    "wan/vpn/interface/gre",
    "wan/vpn/interface/multilink",
    "traffic-policy",
    "wan/vpn/interface/serial",
    "wirelesslan",
    "cellular-profile",
    "wan/vpn/interface/ethpppoe",
    "unified/ngfirewall",
    "policy",
]


AnyParcel = Annotated[
    Union[
        AnySystemParcel,
        AnyPolicyObjectParcel,
        AnyServiceParcel,
        AnyOtherParcel,
        AnyTransportParcel,
        AnyEmbeddedSecurityParcel,
        AnyCliParcel,
        AnyDnsSecurityParcel,
        AnySIGSecurityParcel,
        AnyApplicationPriorityParcel,
        AnyTopologyParcel,
        AnyRoutingParcel,
    ],
    Field(discriminator="type_"),
]

T = TypeVar("T", bound=AnyParcel)


class Parcel(BaseModel, Generic[T]):
    parcel_id: Union[str, UUID] = Field(alias="parcelId")
    parcel_type: ParcelType = Field(alias="parcelType")
    created_by: str = Field(alias="createdBy")
    last_updated_by: str = Field(alias="lastUpdatedBy")
    created_on: int = Field(alias="createdOn")
    last_updated_on: int = Field(alias="lastUpdatedOn")
    payload: T

    @model_validator(mode="before")
    def validate_payload(cls, data):
        if not isinstance(data, dict):
            return data
        data["payload"]["type_"] = data["parcelType"]
        return data


class Header(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    generated_on: int = Field(alias="generatedOn")


class ParcelInfo(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class ParcelSequence(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    header: Header
    data: List[Parcel[T]]


class ParcelCreationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(serialization_alias="parcelId", validation_alias="parcelId")


class ParcelAssociationPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    parcel_id: UUID = Field(serialization_alias="parcelId", validation_alias="parcelId")


class ParcelId(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: UUID = Field(serialization_alias="parcelId", validation_alias="parcelId")


@lru_cache
def list_types(any_union: T) -> Sequence[T]:
    return cast(Sequence[T], resolve_nested_base_model_unions(any_union))


@lru_cache
def find_type(name: str, any_union: T) -> T:
    parcel_types = list_types(any_union)
    parcel_type = next(t for t in parcel_types if t._get_parcel_type() == name)
    return cast(T, parcel_type)
