# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_logging_model import CiscoLoggingModel, Ipv6Server, Server, TlsProfile

cisco_logging_complex = CiscoLoggingModel(
    template_name="cisco_logging_complex",
    template_description="cisco_logging_complex",
    enable=True,
    size=20,
    rotate=5,
    tls_profile=[
        TlsProfile(
            profile="default_tls_profile",
            version="TLSv1.2",
            auth_type="Server",
            ciphersuite_list=["ECDHE-ECDSA-AES256-GCM-SHA384", "ECDHE-RSA-AES256-GCM-SHA384"],
        ),
        TlsProfile(
            profile="secure_tls_profile",
            version="TLSv1.2",
            auth_type="Mutual",
            ciphersuite_list=["ECDHE-ECDSA-CHACHA20-POLY1305", "ECDHE-RSA-CHACHA20-POLY1305"],
        ),
    ],
    server=[
        Server(
            name="1.1.1.1",
            vpn=10,
            source_interface="GigabitEthernet0/0",
            priority="debugging",
            enable_tls=True,
            custom_profile=True,
            profile="default_tls_profile",
        ),
        Server(
            name="log_server_2",
            vpn=20,
            source_interface="GigabitEthernet0/1",
            priority="error",
            enable_tls=False,
            custom_profile=False,
            profile=None,
        ),
    ],
    ipv6_server=[
        Ipv6Server(
            name="ipv6_log_server_1",
            vpn=10,
            source_interface="GigabitEthernet0/2",
            priority="critical",
            enable_tls=True,
            custom_profile=True,
            profile="secure_tls_profile",
        ),
        Ipv6Server(
            name="ipv6_log_server_2",
            vpn=30,
            source_interface="GigabitEthernet0/3",
            priority="emergency",
            enable_tls=False,
            custom_profile=False,
            profile=None,
        ),
    ],
)
