# Copyright 2024 Cisco Systems, Inc. and its affiliates

from ipaddress import IPv6Address, IPv6Interface
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable
from catalystwan.models.common import VrrpTrackerAction


class VrrpTrackingObject(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    tracker_id: Union[Default[None], Global[UUID]] = Field(
        serialization_alias="trackerId", validation_alias="trackerId"
    )
    tracker_action: Union[Global[VrrpTrackerAction], Variable] = Field(
        serialization_alias="trackerAction", validation_alias="trackerAction"
    )
    decrement_value: Optional[Union[Variable, Global[int]]] = Field(
        serialization_alias="decrementValue", validation_alias="decrementValue", default=None
    )


class VrrpIPv6Address(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, extra="forbid")

    ipv6_link_local: Union[Global[str], Global[IPv6Address], Variable] = Field(
        serialization_alias="ipv6LinkLocal", validation_alias="ipv6LinkLocal"
    )
    prefix: Optional[Union[Global[str], Global[IPv6Interface], Variable, Default[None]]] = None
