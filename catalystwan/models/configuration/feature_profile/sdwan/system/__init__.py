from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from .aaa import AAAParcel
from .banner import BannerParcel
from .basic import BasicParcel
from .bfd import BFDParcel
from .device_access import DeviceAccessIPv4Parcel
from .device_access_ipv6 import DeviceAccessIPv6Parcel
from .global_parcel import GlobalParcel
from .logging_parcel import LoggingParcel
from .mrf import MRFParcel
from .ntp import NtpParcel
from .omp import OMPParcel
from .security import SecurityParcel
from .snmp import SNMPParcel

AnySystemParcel = Annotated[
    Union[
        AAAParcel,
        BFDParcel,
        LoggingParcel,
        BannerParcel,
        BasicParcel,
        DeviceAccessIPv4Parcel,
        DeviceAccessIPv6Parcel,
        GlobalParcel,
        NtpParcel,
        MRFParcel,
        OMPParcel,
        SecurityParcel,
        SNMPParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = [
    "AAAParcel",
    "BFDParcel",
    "LoggingParcel",
    "BannerParcel",
    "BasicParcel",
    "DeviceAccessIPv4Parcel",
    "DeviceAccessIPv6Parcel",
    "GlobalParcel",
    "NtpParcel",
    "MRFParcel",
    "OMPParcel",
    "SecurityParcel",
    "SNMPParcel",
    "AnySystemParcel",
]


def __dir__() -> "List[str]":
    return list(__all__)
