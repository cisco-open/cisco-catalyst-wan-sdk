from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .acl import Ipv4AclParcel, Ipv6AclParcel
from .appqoe import AppqoeParcel
from .dhcp_server import LanVpnDhcpServerParcel
from .eigrp import EigrpParcel
from .lan.ethernet import InterfaceEthernetParcel
from .lan.gre import InterfaceGreParcel
from .lan.ipsec import InterfaceIpsecParcel
from .lan.svi import InterfaceSviParcel
from .lan.vpn import LanVpnParcel
from .multicast import MulticastParcel
from .ospf import OspfParcel
from .ospfv3 import Ospfv3IPv4Parcel, Ospfv3IPv6Parcel
from .route_policy import RoutePolicyParcel
from .switchport import SwitchportParcel
from .wireless_lan import WirelessLanParcel

AnyTopLevelServiceParcel = Annotated[
    Union[
        LanVpnDhcpServerParcel,
        AppqoeParcel,
        LanVpnParcel,
        OspfParcel,
        Ospfv3IPv4Parcel,
        Ospfv3IPv6Parcel,
        RoutePolicyParcel,
        EigrpParcel,
        SwitchportParcel,
        Ipv6AclParcel,
        Ipv4AclParcel,
        WirelessLanParcel,
        MulticastParcel,
        # TrackerGroupData,
        # WirelessLanData,
        # SwitchportData
    ],
    Field(discriminator="type_"),
]

AnyLanVpnInterfaceParcel = Annotated[
    Union[
        InterfaceEthernetParcel,
        InterfaceGreParcel,
        InterfaceIpsecParcel,
        InterfaceSviParcel,
    ],
    Field(discriminator="type_"),
]

AnyAssociatoryParcel = Annotated[
    Union[
        MulticastParcel,
        # DHCP
    ],
    Field(discriminator="type_"),
]

AnyServiceParcel = Annotated[
    Union[AnyTopLevelServiceParcel, AnyLanVpnInterfaceParcel],
    Field(discriminator="type_"),
]

__all__ = [
    "LanVpnDhcpServerParcel",
    "AppqoeParcel",
    "LanVpnParcel",
    "OspfParcel",
    "RoutePolicyParcel",
    "Ospfv3IPv4Parcel",
    "Ospfv3IPv6Parcel",
    "Ipv6AclParcel",
    "Ipv4AclParcel",
    "SwitchportParcel",
    "InterfaceSviParcel",
    "InterfaceGreParcel",
    "WirelessLanParcel",
    "MulticastParcel",
    "AnyServiceParcel",
    "AnyTopLevelServiceParcel",
    "AnyLanVpnInterfaceParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
