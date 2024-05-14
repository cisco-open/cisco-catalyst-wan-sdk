# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from ipaddress import IPv4Address
from typing import Literal, Optional, Union

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

GpsMode = Literal[
    "ms-based",
    "standalone",
]


class GpsParcel(_ParcelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")
    type_: Literal["gps"] = Field(default="gps", frozen=True, exclude=True)
    destination_address: Optional[Union[Global[IPv4Address], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "destinationAddress")
    )
    destination_port: Optional[Union[Global[int], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "destinationPort")
    )
    enable: Union[Default[bool], Variable, Global[bool]] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "enable")
    )
    mode: Union[Default[GpsMode], Global[GpsMode], Variable] = Field(
        default=as_default("ms-based", GpsMode), validation_alias=AliasPath("data", "mode")
    )
    nmea: Union[Default[bool], Global[bool], Variable] = Field(
        default=as_default(False), validation_alias=AliasPath("data", "nmea")
    )
    source_address: Optional[Union[Global[IPv4Address], Default[None], Variable]] = Field(
        default=None, validation_alias=AliasPath("data", "sourceAddress")
    )
