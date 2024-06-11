# Copyright 2023 Cisco Systems, Inc. and its affiliates
from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .bgp import RoutingBgpParcel
from .ospf import RoutingOspfParcel
from .ospfv3 import RoutingOspfv3IPv4Parcel, RoutingOspfv3IPv6Parcel

AnyRoutingParcel = Annotated[
    Union[RoutingBgpParcel, RoutingOspfParcel, RoutingOspfv3IPv6Parcel, RoutingOspfv3IPv4Parcel],
    Field(discriminator="type_"),
]

__all__ = [
    "RoutingBgpParcel",
    "RoutingOspfParcel",
    "RoutingOspfv3IPv4Parcel",
    "RoutingOspfv3IPv6Parcel",
    "AnyRoutingParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
