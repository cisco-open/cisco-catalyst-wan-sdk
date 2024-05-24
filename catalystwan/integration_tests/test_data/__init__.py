# Copyright 2023 Cisco Systems, Inc. and its affiliates
from ipaddress import IPv4Address
from typing import List, Literal

from catalystwan.api.configuration_groups.parcel import Default, Global, as_global
from catalystwan.models.configuration.feature_profile.sdwan.routing.bgp import RoutingBgpParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospf import RoutingOspfParcel
from catalystwan.models.configuration.feature_profile.sdwan.routing.ospfv3 import (
    Ospfv3InterfaceParametres,
    Ospfv3IPv4Area,
    Ospfv3IPv6Area,
    RoutingOspfv3IPv4Parcel,
    RoutingOspfv3IPv6Parcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_controller import (
    CellularControllerParcel,
    ControllerConfig,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.cellular_profile import (
    Authentication,
    CellularProfileParcel,
    NeedAuthentication,
    ProfileConfig,
    ProfileInfo,
)
from catalystwan.models.configuration.feature_profile.sdwan.transport.gps import GpsParcel

cellular_controller_parcel = CellularControllerParcel(
    parcel_name="CellularControllerParcel",
    parcel_description="Description",
    controller_config=ControllerConfig(
        id=as_global("0/2/0"),
        slot=as_global(1),
        max_retry=as_global(3),
        failover_timer=as_global(4),
        auto_sim=as_global(True),
    ),
)

cellular_profile_parcel = CellularProfileParcel(
    parcel_name="CellularProfileParcel",
    parcel_description="Description",
    profile_config=ProfileConfig(
        id=Global[int](value=2),
        profile_info=ProfileInfo(
            apn=Global[str](value="KvqJrCD"),
            authentication=Authentication(
                need_authentication=NeedAuthentication(
                    password=Global[str](value="HfBBBHZlFH"),
                    type=Global[Literal["chap", "pap", "pap_chap"]](value="chap"),
                    username=Global[str](value="BABBBBBBV"),
                )
            ),
            no_overwrite=Global[bool](value=False),
            pdn_type=Global[Literal["ipv4", "ipv4v6", "ipv6"]](value="ipv4"),
        ),
    ),
    config_type=Default[Literal["non-eSim"]](value="non-eSim"),
)

gps_parcel = GpsParcel(
    parcel_name="GpsParcel",
    parcel_description="Description",
    destination_address=Global[IPv4Address](value=IPv4Address("66.22.1.2")),
    destination_port=Global[int](value=266),
    enable=Global[bool](value=True),
    mode=Global[Literal["ms-based", "standalone"]](value="standalone"),
    nmea=Global[bool](value=True),
    source_address=Global[IPv4Address](value=IPv4Address("76.22.3.9")),
)


ospf_parcel = RoutingOspfParcel(
    parcel_name="TestRoutingOspfParcel",
    parcel_description="Test Ospf Parcel",
)
ospfv3ipv4_parcel = RoutingOspfv3IPv4Parcel(
    parcel_name="TestOspfv3ipv4",
    parcel_description="Test Ospfv3ipv4 Parcel",
    area=[
        Ospfv3IPv4Area(
            area_number=as_global(5),
            interfaces=[Ospfv3InterfaceParametres(name=as_global("GigabitEthernet0/0/0"))],
        )
    ],
)
ospfv3ipv6_parcel = RoutingOspfv3IPv6Parcel(
    parcel_name="TestOspfv3ipv6",
    parcel_description="Test Ospfv3ipv6 Parcel",
    area=[
        Ospfv3IPv6Area(
            area_number=as_global(7),
            interfaces=[Ospfv3InterfaceParametres(name=as_global("GigabitEthernet0/0/0"))],
        )
    ],
)

bgp_parcel = RoutingBgpParcel(
    parcel_name="TestRoutingBgpParcel",
    parcel_description="Test Bgp Parcel",
    as_num=as_global(30),
)


__all__ = [
    "cellular_controller_parcel",
    "cellular_profile_parcel",
    "gps_parcel",
    "ospf_parcel",
    "ospfv3ipv4_parcel",
    "ospfv3ipv6_parcel",
    "bgp_parcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
