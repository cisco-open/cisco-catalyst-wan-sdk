# Copyright 2024 Cisco Systems, Inc. and its affiliates

#  type: ignore
from catalystwan.tests.templates.models.cisco_aaa import cisco_aaa, cisco_aaa_complex
from catalystwan.tests.templates.models.cisco_banner import cisco_banner
from catalystwan.tests.templates.models.cisco_bfd import cisco_bfd

# from catalystwan.tests.templates.models.cisco_vpn import basic_cisco_vpn, complex_vpn_model
# from catalystwan.tests.templates.models.omp_vsmart import default_omp, omp_2, omp_3
from catalystwan.tests.templates.models.cisco_secure_internet_gateway import cisco_sig

__all__ = [
    "cisco_aaa",
    "cisco_aaa_complex",
    "cisco_banner",
    "cisco_bfd",
    # "default_omp",
    # "omp_2",
    # "omp_3",
    # "basic_cisco_vpn",
    # "complex_vpn_model",
    # "bfd_model",
    "cisco_sig",
]
