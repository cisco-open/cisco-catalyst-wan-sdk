# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.models.cisco_omp_model import CiscoOMPModel, IPv4Advertise, IPv6Advertise

cisco_omp_complex = CiscoOMPModel(
    template_name="cisco_omp_complex",
    template_description="cisco_omp_complex",
    graceful_restart=True,
    overlay_as=65000,
    send_path_limit=10,
    ecmp_limit=8,
    shutdown=False,
    omp_admin_distance_ipv4=110,
    omp_admin_distance_ipv6=115,
    advertisement_interval=30,
    graceful_restart_timer=120,
    eor_timer=300,
    holdtime=180,
    advertise=[
        IPv4Advertise(protocol="bgp", route="external"),
        IPv4Advertise(protocol="ospf", route=None),
        IPv4Advertise(protocol="connected", route=None),
        IPv4Advertise(protocol="static", route=None),
        IPv4Advertise(protocol="eigrp", route=None),
        IPv4Advertise(protocol="lisp", route=None),
    ],
    ipv6_advertise=[
        IPv6Advertise(protocol="bgp"),
        IPv6Advertise(protocol="ospf"),
        IPv6Advertise(protocol="connected"),
        IPv6Advertise(protocol="static"),
    ],
    ignore_region_path_length=True,
    transport_gateway="prefer",
    site_types=["type-1", "type-2", "cloud", "branch", "spoke"],
    auto_translate=True,
)
