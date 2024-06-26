# Copyright 2024 Cisco Systems, Inc. and its affiliates
# Copyright 2023 Cisco Systems, Inc. and its affiliates
import json
import logging
from typing import Any, Callable, Dict, Optional, cast

from catalystwan.api.template_api import FeatureTemplateInformation
from catalystwan.models.configuration.config_migration import ConvertResult
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel
from catalystwan.utils.config_migration.converters.feature_template.lan.multilink import LanMultilinkConverter
from catalystwan.utils.feature_template.find_template_values import find_template_values

from .aaa import AAAConverter
from .appqoe import AppqoeConverter
from .banner import BannerConverter
from .base import FTConverter
from .basic import SystemToBasicConverter
from .bfd import BFDConverter
from .bgp import BgpRoutingConverter
from .cellular_controller import CellularControllerConverter
from .cellular_profile import CellularProfileConverter
from .cli import CliConverter
from .dhcp import DhcpConverter
from .ethernet import ManagementInterfaceEthernetConverter
from .global_ import GlobalConverter
from .gps import GpsConverter
from .lan.ethernet import LanInterfaceEthernetConverter
from .lan.gre import LanInterfaceGreConverter
from .lan.ipsec import LanInterfaceIpsecConverter
from .lan.svi import InterfaceSviConverter
from .logging_ import LoggingConverter
from .multicast import IgmpToMulticastConverter, MulticastToMulticastConverter, PimToMulticastConverter
from .normalizer import template_values_normalization
from .ntp import NtpConverter
from .omp import OMPConverter
from .ospf import OspfConverter
from .security import SecurityConverter
from .sig import SIGConverter
from .snmp import SNMPConverter
from .switchport import SwitchportConverter
from .thousandeyes import ThousandEyesConverter
from .ucse import UcseConverter
from .vpn import VpnConverter
from .wan.cellular import InterfaceCellularConverter
from .wan.ethernet import WanInterfaceEthernetConverter
from .wan.gre import WanInterfaceGreConverter
from .wan.ipsec import WanInterfaceIpsecConverter
from .wan.multilink import WanMultilinkConverter
from .wan.protocol_over import (
    InterfaceDslIPoEConverter,
    InterfaceDslPppoaConverter,
    InterfaceDslPppoeConverter,
    InterfaceEthernetPppoeConverter,
)
from .wan.t1e1serial import T1E1SerialConverter
from .wireless_lan import WirelessLanConverter

logger = logging.getLogger(__name__)

available_converters = [
    AAAConverter,
    BannerConverter,
    SecurityConverter,
    SystemToBasicConverter,
    BFDConverter,
    GlobalConverter,
    LoggingConverter,
    OMPConverter,
    NtpConverter,
    BgpRoutingConverter,
    ThousandEyesConverter,
    UcseConverter,
    DhcpConverter,
    SNMPConverter,
    AppqoeConverter,
    VpnConverter,
    LanInterfaceGreConverter,
    LanMultilinkConverter,
    InterfaceSviConverter,
    LanInterfaceEthernetConverter,
    LanInterfaceIpsecConverter,
    OspfConverter,
    SwitchportConverter,
    MulticastToMulticastConverter,
    PimToMulticastConverter,
    IgmpToMulticastConverter,
    WirelessLanConverter,
    T1E1SerialConverter,
    InterfaceEthernetPppoeConverter,
    InterfaceDslPppoeConverter,
    InterfaceDslPppoaConverter,
    InterfaceDslIPoEConverter,
    LanInterfaceGreConverter,
    WanInterfaceGreConverter,
    WanInterfaceIpsecConverter,
    InterfaceCellularConverter,
    GpsConverter,
    CellularControllerConverter,
    CellularProfileConverter,
    CliConverter,
    WanInterfaceEthernetConverter,
    SIGConverter,
    WanMultilinkConverter,
    ManagementInterfaceEthernetConverter,
]


supported_parcel_converters: Dict[Any, Any] = {
    converter.supported_template_types: converter for converter in available_converters  # type: ignore
}


def choose_parcel_converter(template_type: str) -> Optional[Callable[..., FTConverter]]:
    """
    This function is used to choose the correct parcel factory based on the template type.

    Args:
        template_type (str): The template type used to determine the correct factory.

    Returns:
        BaseFactory | None: The chosen parcel factory or None if there is no supported template type.
    """
    for key in supported_parcel_converters.keys():
        if template_type in key:
            converter = supported_parcel_converters[key]
            logger.debug(f"Choosen converter {converter} based on template type {template_type}")
            return converter
    logger.warning(f"Template type {template_type} not supported")
    return None


def unsupported_type(template_type: str) -> ConvertResult[AnyParcel]:
    return ConvertResult(status="unsupported", output=None, info=[f"Template type {template_type} not supported"])


def extract_template_values(template_definiton: str) -> Dict[str, Any]:
    """Extracts the template values from the template definition and create easy to consume dictionary."""
    template_definition_as_dict = json.loads(cast(str, template_definiton))
    template_values = find_template_values(template_definition_as_dict)
    template_values_normalized = template_values_normalization(template_values)
    return template_values_normalized


def convert(converter: FTConverter, template: FeatureTemplateInformation) -> ConvertResult[AnyParcel]:
    definition = template.template_definiton
    if definition is None:
        return ConvertResult(status="failed", output=None, info=["Template definition is empty"])
    template_values = extract_template_values(definition)
    return converter.convert(template.name, template.description, template_values)


def create_parcel_from_template(template: FeatureTemplateInformation) -> ConvertResult[AnyParcel]:
    """
    Creates a new instance of a ConvertResult[AnyParcel] based on the given template.

    Args:
        template (FeatureTemplateInformation): The template to use for creating the AnyParcel instance.

    Returns:
        ConvertResult[AnyParcel]: The convert result of the operation.
    """
    converter_class = choose_parcel_converter(template.template_type)
    if converter_class is None:
        return unsupported_type(template.template_type)
    converter = converter_class()
    return convert(converter, template)
