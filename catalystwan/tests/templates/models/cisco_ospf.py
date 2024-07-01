from ipaddress import IPv4Interface

from catalystwan.api.templates.models.cisco_ospf import (
    Area,
    CiscoOSPFModel,
    Interface,
    Range,
    Redistribute,
    RoutePolicy,
    RouterLsa,
)

cisco_ospf_complex = CiscoOSPFModel(
    template_name="cisco_ospf_complex",
    template_description="cisco_ospf_complex",
    device_models=["vedge-C8000V"],
    router_id="1.1.1.1",
    reference_bandwidth=10000,
    rfc1583=False,
    originate=True,
    always=True,
    metric=10,
    metric_type="type1",
    external=20,
    inter_area=30,
    intra_area=40,
    delay=5,
    initial_hold=10,
    max_hold=40,
    redistribute=[
        Redistribute(protocol="static", route_policy="static_policy", dia=True),
        Redistribute(protocol="bgp", route_policy="bgp_to_ospf_policy", dia=False),
    ],
    router_lsa=[RouterLsa(ad_type="administrative", time=10)],
    route_policy=[RoutePolicy(direction="in", pol_name="ospf_in_policy")],
    area=[
        Area(
            a_num=0,
            stub=False,
            nssa=True,
            interface=[
                Interface(
                    name="GigabitEthernet0/0",
                    hello_interval=10,
                    dead_interval=40,
                    retransmit_interval=5,
                    cost=1,
                    priority=1,
                    network="broadcast",
                    passive_interface=False,
                    type="simple",
                    message_digest_key=1,
                    md5="md5keystring",
                )
            ],
            range=[Range(address=IPv4Interface("192.168.1.0/24"), cost=100, no_advertise=True)],
        )
    ],
)
