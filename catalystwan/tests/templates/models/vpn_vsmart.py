# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore

from catalystwan.api.templates.models.vpn_vsmart_model import (
    Dns,
    Host,
    NextHop,
    NextHopv6,
    Routev4,
    Routev6,
    VpnVsmartModel,
)

vpn_vsmart_basic = VpnVsmartModel(
    template_name="vpn_vsmart_basic",
    template_description="Primitive",
    device_models=["vsmart"],
    vpn_id="0",
)

vpn_vsmart_complex = VpnVsmartModel(
    template_name="vpn_vsmart_complex",
    template_description="cvpn_vsmart_complex",
    device_models=["vsmart"],
    vpn_id="0",
    name="vpn_name_x",
    route_v4=[Routev4(prefix="prefixv4", next_hop=[NextHop(address="1.1.1.1")])],
    route_v6=[Routev6(prefix="prefixv6", next_hop=[NextHopv6(address="2.2.2.2")], nat="NAT64")],
    dns=[Dns(dns_addr="1.1.1.1", role="primary"), Dns(dns_addr="2.2.2.2", role="secondary")],
    host=[Host(hostname="test_hostname", ip=["1.1.1.1"])],
)
