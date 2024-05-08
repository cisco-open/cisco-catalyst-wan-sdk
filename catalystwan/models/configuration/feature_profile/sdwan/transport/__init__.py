# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .bgp import WanRoutingBgpParcel as BGPParcel
from .cellular_controller import CellularControllerParcel
from .t1e1controller import T1E1ControllerParcel
from .vpn import ManagementVpnParcel, TransportVpnParcel
from .wan.interface.t1e1serial import T1E1SerialParcel

AnyTransportVpnSubParcel = Annotated[
    Union[
        T1E1SerialParcel
        # Add wan interfaces here
    ],
    Field(discriminator="type_"),
]
AnyTransportVpnParcel = Annotated[Union[ManagementVpnParcel, TransportVpnParcel], Field(discriminator="type_")]
AnyTransportSuperParcel = Annotated[
    Union[T1E1ControllerParcel, CellularControllerParcel, BGPParcel, T1E1ControllerParcel], Field(discriminator="type_")
]
AnyTransportParcel = Annotated[
    Union[AnyTransportSuperParcel, AnyTransportVpnParcel, AnyTransportVpnSubParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "BGPParcel",
    "CellularControllerParcel",
    "ManagementVpnParcel",
    "TransportVpnParcel",
    "AnyTransportParcel",
    "AnyTransportSuperParcel",
    "AnyTransportVpnSubParcel" "T1E1ControllerParcel",
    "T1E1SerialParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
