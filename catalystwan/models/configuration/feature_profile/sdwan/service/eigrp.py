# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import AddressWithMask

EigrpAuthType = Literal[
    "md5",
    "hmac-sha-256",
]


RedistributeProtocol = Literal[
    "bgp",
    "connected",
    "nat-route",
    "omp",
    "ospf",
    "ospfv3",
    "static",
]


class KeychainDetails(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    key_id: Union[Global[int], Variable, Default[None]] = Field(
        default=Default[None](value=None), serialization_alias="keyId", validation_alias="keyId"
    )
    keystring: Union[Global[str], Variable, Default[None]] = Field(default=Default[None](value=None))


class EigrpAuthentication(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    auth_type: Union[Global[EigrpAuthType], Variable, Default[None]] = Default[None](value=None)
    auth_key: Optional[Union[Global[str], Variable, Default[None]]] = Field(
        serialization_alias="authKey", validation_alias="authKey", default=Default[None](value=None)
    )
    key: Optional[List[KeychainDetails]] = None


class TableMap(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Optional[Union[Default[None], Global[UUID]]] = Default[None](value=None)
    filter: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)


class SummaryAddress(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    prefix: AddressWithMask


class IPv4StaticRoute(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    name: Union[Global[str], Variable]
    shutdown: Optional[Union[Global[bool], Variable, Default[bool]]] = Default[bool](value=False)
    summary_address: List[SummaryAddress] = Field(
        serialization_alias="summaryAddress", validation_alias="summaryAddress", default_factory=list
    )


class RedistributeIntoEigrp(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    protocol: Union[Global[RedistributeProtocol], Variable]
    route_policy: Optional[Union[Default[None], Global[UUID]]] = Default[None](value=None)


class AddressFamily(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    redistribute: Optional[List[RedistributeIntoEigrp]] = None
    network: List[SummaryAddress] = Field(min_length=1)


class EigrpParcel(_ParcelBase):
    type_: Literal["routing/eigrp"] = Field(default="routing/eigrp", exclude=True)
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    as_number: Union[Global[int], Variable] = Field(validation_alias=AliasPath("data", "asNum"))
    address_family: AddressFamily = Field(validation_alias=AliasPath("data", "addressFamily"))
    hello_interval: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "helloInterval"), default=Default[int](value=5)
    )
    hold_time: Union[Global[int], Variable, Default[int]] = Field(
        validation_alias=AliasPath("data", "holdTime"), default=Default[int](value=15)
    )
    authentication: Optional[EigrpAuthentication] = Field(
        validation_alias=AliasPath("data", "authentication"), default=None
    )
    af_interface: Optional[List[IPv4StaticRoute]] = Field(
        validation_alias=AliasPath("data", "afInterface"), default=None
    )
    table_map: TableMap = Field(validation_alias=AliasPath("data", "tableMap"), default=TableMap())
