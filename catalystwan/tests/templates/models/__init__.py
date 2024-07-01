# Copyright 2024 Cisco Systems, Inc. and its affiliates

#  type: ignore
from catalystwan.tests.templates.models.aaa import aaa_basic, aaa_complex_template
from catalystwan.tests.templates.models.cisco_aaa import cisco_aaa, cisco_aaa_complex
from catalystwan.tests.templates.models.cisco_banner import cisco_banner
from catalystwan.tests.templates.models.cisco_bfd import cisco_bfd
from catalystwan.tests.templates.models.cisco_logging import cisco_logging_complex
from catalystwan.tests.templates.models.cisco_ntp import cisco_ntp_complex
from catalystwan.tests.templates.models.cisco_omp import cisco_omp_complex
from catalystwan.tests.templates.models.cisco_ospf import cisco_ospf_complex
from catalystwan.tests.templates.models.cisco_secure_internet_gateway import cisco_sig
from catalystwan.tests.templates.models.cisco_snmp import cisco_snmp_complex
from catalystwan.tests.templates.models.cisco_system import cisco_system_complex
from catalystwan.tests.templates.models.cisco_vpn import cisco_vpn_basic, cisco_vpn_complex
from catalystwan.tests.templates.models.cisco_vpn_interface import cisco_vpn_interface_complex
from catalystwan.tests.templates.models.omp_vsmart import omp_vsmart_1, omp_vsmart_2, omp_vsmart_3, omp_vsmart_complex
from catalystwan.tests.templates.models.security_vsmart import security_vsmart_complex
from catalystwan.tests.templates.models.system_vsmart import system_vsmart_complex
from catalystwan.tests.templates.models.vpn_vsmart import vpn_vsmart_basic, vpn_vsmart_complex
from catalystwan.tests.templates.models.vpn_vsmart_interface import (
    vpn_vsmart_interface_basic,
    vpn_vsmart_interface_complex,
)

__all__ = [
    "aaa_basic",
    "aaa_complex_template",
    "cisco_aaa",
    "cisco_aaa_complex",
    "cisco_banner",
    "cisco_bfd",
    "cisco_logging_complex",
    "cisco_ntp_complex",
    "cisco_omp_complex",
    "cisco_snmp_complex",
    "cisco_ospf_complex",
    "cisco_sig",
    "cisco_system_complex",
    "cisco_vpn_interface_complex",
    "cisco_vpn_basic",
    "cisco_vpn_complex",
    "omp_vsmart_1",
    "omp_vsmart_2",
    "omp_vsmart_3",
    "omp_vsmart_complex",
    "security_vsmart_complex",
    "system_vsmart_complex",
    "vpn_vsmart_basic",
    "vpn_vsmart_complex",
    "vpn_vsmart_interface_basic",
    "vpn_vsmart_interface_complex",
]
