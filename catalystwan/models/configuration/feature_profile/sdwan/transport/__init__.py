# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.acl import AnyAclParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.route_policy import RoutePolicyParcel

from .cellular_controller import CellularControllerParcel
from .cellular_profile import CellularProfileParcel
from .gps import GpsParcel
from .management.ethernet import InterfaceEthernetParcel as ManagementInterfaceEthernetParcel
from .t1e1controller import T1E1ControllerParcel
from .vpn import ManagementVpnParcel, TransportVpnParcel
from .wan.interface.cellular import InterfaceCellularParcel
from .wan.interface.ethernet import InterfaceEthernetParcel
from .wan.interface.gre import InterfaceGreParcel
from .wan.interface.ipsec import InterfaceIpsecParcel
from .wan.interface.multilink import InterfaceMultilinkParcel
from .wan.interface.protocol_over import (
    InterfaceDslIPoEParcel,
    InterfaceDslPPPoAParcel,
    InterfaceDslPPPoEParcel,
    InterfaceEthPPPoEParcel,
)
from .wan.interface.t1e1serial import T1E1SerialParcel

AnyTransportVpnSubParcel = Annotated[
    Union[
        T1E1SerialParcel,
        InterfaceEthPPPoEParcel,
        InterfaceDslPPPoEParcel,
        InterfaceDslPPPoAParcel,
        InterfaceDslIPoEParcel,
        InterfaceGreParcel,
        InterfaceIpsecParcel,
        InterfaceEthernetParcel,
        InterfaceMultilinkParcel,
        InterfaceCellularParcel,
        # Add wan interfaces here
    ],
    Field(discriminator="type_"),
]
AnyTransportVpnParcel = Annotated[Union[ManagementVpnParcel, TransportVpnParcel], Field(discriminator="type_")]
AnyTransportSuperParcel = Annotated[
    Union[
        T1E1ControllerParcel,
        CellularControllerParcel,
        CellularProfileParcel,
        T1E1ControllerParcel,
        GpsParcel,
    ],
    Field(discriminator="type_"),
]
AnyManagementVpnSubParcel = Annotated[
    Union[ManagementInterfaceEthernetParcel],
    Field(discriminator="type_"),
]

AnyTransportParcel = Annotated[
    Union[
        AnyAclParcel,
        AnyTransportSuperParcel,
        AnyTransportVpnParcel,
        AnyTransportVpnSubParcel,
        AnyManagementVpnSubParcel,
        RoutePolicyParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = [
    "RoutingBgpParcel",
    "CellularControllerParcel",
    "ManagementVpnParcel",
    "TransportVpnParcel",
    "AnyTransportParcel",
    "AnyTransportSuperParcel",
    "AnyTransportVpnSubParcel",
    "AnyManagementVpnSubParcel",
    "T1E1ControllerParcel",
    "T1E1SerialParcel",
    "InterfaceDslPPPoAParcel",
    "InterfaceDslPPPoEParcel",
    "InterfaceEthPPPoEParcel",
    "InterfaceIpsecParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
