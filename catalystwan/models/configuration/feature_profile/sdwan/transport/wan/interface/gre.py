# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address
from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import AddressWithMask, AdvancedGre, TunnelSourceType


class Basic(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    address: AddressWithMask = Field()
    if_name: Union[Variable, Global[str]] = Field(validation_alias="ifName", serialization_alias="ifName")
    tunnel_destination: Union[Variable, Global[IPv4Address]] = Field(
        validation_alias="tunnelDestination", serialization_alias="tunnelDestination"
    )
    clear_dont_fragment: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(
        default=None, validation_alias="clearDontFragment", serialization_alias="clearDontFragment"
    )
    description: Optional[Union[Variable, Global[str], Default[None]]] = Field(default=None)
    mtu: Optional[Union[Variable, Default[int], Global[int]]] = Field(default=None)
    shutdown: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    tcp_mss_adjust: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None, validation_alias="tcpMssAdjust", serialization_alias="tcpMssAdjust"
    )
    tunnel_source_type: Optional[TunnelSourceType] = Field(
        default=None, validation_alias="tunnelSourceType", serialization_alias="tunnelSourceType"
    )


class InterfaceGreParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["wan/vpn/interface/gre"] = Field(default="wan/vpn/interface/gre", frozen=True, exclude=True)
    basic: Basic = Field(validation_alias=AliasPath("data", "basic"), description="basic configuration")
    advanced: Optional[AdvancedGre] = Field(
        default=None, validation_alias=AliasPath("data", "advanced"), description="advanced"
    )
