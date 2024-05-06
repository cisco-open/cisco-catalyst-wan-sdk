# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .bgp import WanRoutingBgpParcel as BGPParcel
from .cellular_controller import CellularControllerParcel
from .t1e1controller import T1E1ControllerParcel
from .vpn import ManagementVpnParcel, TransportVpnParcel

AnyTransportVpnSubParcel = Annotated[Union[T1E1ControllerParcel, BGPParcel], Field(discriminator="type_")]

AnyTransportParcel = Annotated[
    Union[CellularControllerParcel, ManagementVpnParcel, TransportVpnParcel, AnyTransportVpnSubParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "BGPParcel",
    "CellularControllerParcel",
    "ManagementVpnParcel",
    "TransportVpnParcel",
    "AnyTransportParcel",
    "AnyTransportVpnSubParcel",
    "T1E1ControllerParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
