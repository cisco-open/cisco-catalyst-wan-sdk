# Copyright 2023 Cisco Systems, Inc. and its affiliates

import ipaddress

from catalystwan.api.templates.models.vpn_vsmart_interface_model import Ip, VpnVsmartInterfaceModel

vpn_vsmart_interface_complex = VpnVsmartInterfaceModel(
    template_name="vpn_vsmart_interface_complex",
    template_description="vpn_vsmart_interface_complex",
    device_models=["vsmart"],
    if_name="GigabitEthernet0/0/0",
    interface_description="WAN interface",
    ipv4_address="10.10.10.1",
    dhcp_ipv4_client=False,
    dhcp_distance=1,
    ipv6_address=ipaddress.IPv6Interface("2001:db8::1/64"),
    dhcp_ipv6_client=True,
    dhcp_ipv6_distance=1,
    dhcp_rapid_commit=True,
    group=[0, 1],
    value="blue",
    carrier="carrier1",
    nat_refresh_interval=30,
    hello_interval=10,
    hello_tolerance=30,
    all=True,
    dhcp=False,
    dns=True,
    icmp=True,
    sshd=True,
    netconf=False,
    ntp=True,
    stun=False,
    flow_control="ingress",
    clear_dont_fragment=True,
    autonegotiate=True,
    pmtu=False,
    mtu=1500,
    tcp_mss_adjust=1452,
    mac_address="00:1A:2B:3C:4D:5F",
    speed="1000",
    duplex="full",
    shutdown=False,
    ip=[
        Ip(addr=ipaddress.IPv4Address("192.168.1.1"), mac="00:1A:2B:3C:4D:5E"),
    ],
)

vpn_vsmart_interface_basic = VpnVsmartInterfaceModel(
    template_name="vpn_vsmart_interface_basic",
    template_description="vpn_vsmart_interface_basic",
    device_models=["vsmart"],
    if_name="any",
)
