# Copyright 2023 Cisco Systems, Inc. and its affiliates
from typing import Dict, Union

VPN_MANAGEMENT = "cisco_vpn_management"
VPN_TRANSPORT = "cisco_vpn_transport"
VPN_SERVICE = "cisco_vpn_service"


"""Atrificial constants to diffrientiate between Additional Cisco VPN 0 Templates,
Additional Cisco VPN 512 Templates and Additional Cisco VPN Templates. They all use the
same feature templates in ux1.0 but in ux2.0 every additional VPN parcel has a diferent
endpoint and model!
"""
VPN_ADDITIONAL_TEMPLATES = [
    "cisco_vpn_interface_gre",
    "cisco_vpn_interface_ipsec",
    "vpn-interface-svi",
    "cisco_vpn_interface",
    "vpn-vedge-interface-gre",
    "vpn-vsmart-interface",
    "vpn-vedge-interface",
    "vpn-vmanage-interface",
    "vpn-vedge-interface-ipsec",
    "vpn-cedge-interface-multilink-controller",
    "cisco_bgp",
    "bgp",
    "cisco_ospfv3",
    "cisco_ospf",
]

NO_SUBSTITUTE_ERROR = "NO_SUBSTITUTE_ERROR"
NO_SUBSTITUTE_VPN_MANAGEMENT_SVI = (
    "NO_SUBSTITUTE_ERROR: UX1.0 -> We can attach SVI to vpn 512, UX2.0 -> There is no SVI parcel for vpn 512"
)

MANAGEMENT_VPN_ETHERNET = "management/vpn/interface/ethernet"

WAN_BGP = "WAN_BGP"
WAN_OSPF = "WAN_OSPF"
WAN_OSPFV3 = "WAN_OSPFV3"
WAN_VPN_GRE = "wan/vpn/interface/gre"
WAN_VPN_IPSEC = "wan/vpn/interface/ipsec"
WAN_VPN_SVI = "wan/vpn/interface/svi"
WAN_VPN_ETHERNET = "wan/vpn/interface/ethernet"
WAN_VPN_MULTILINK = "wan/vpn/interface/multilink"

LAN_BGP = "LAN_BGP"
LAN_OSPF = "LAN_OSPF"
LAN_OSPFV3 = "LAN_OSPFV3"
LAN_VPN_GRE = "lan/vpn/interface/gre"
LAN_VPN_IPSEC = "lan/vpn/interface/ipsec"
LAN_VPN_SVI = "lan/vpn/interface/svi"
LAN_VPN_ETHERNET = "lan/vpn/interface/ethernet"
LAN_VPN_MULTILINK = "lan/vpn/interface/multilink"

VPN_TEMPLATE_MAPPINGS: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {
    VPN_MANAGEMENT: {
        "mapping": {
            "vpn-interface-svi": NO_SUBSTITUTE_VPN_MANAGEMENT_SVI,
            "cisco_vpn_interface": MANAGEMENT_VPN_ETHERNET,
            "vpn-vsmart-interface": MANAGEMENT_VPN_ETHERNET,
            "vpn-vedge-interface": MANAGEMENT_VPN_ETHERNET,
            "vpn-vmanage-interface": MANAGEMENT_VPN_ETHERNET,
        },
        "suffix": "_MANAGEMENT",
    },
    VPN_TRANSPORT: {
        "mapping": {
            "cisco_bgp": WAN_BGP,
            "bgp": WAN_BGP,
            "cisco_ospf": WAN_OSPF,
            "cisco_ospfv3": WAN_OSPFV3,
            "vpn-vedge-interface-gre": WAN_VPN_GRE,
            "cisco_vpn_interface_gre": WAN_VPN_GRE,
            "cisco_vpn_interface_ipsec": WAN_VPN_IPSEC,
            "vpn-interface-svi": WAN_VPN_SVI,
            "cisco_vpn_interface": WAN_VPN_ETHERNET,
            "vpn-vsmart-interface": WAN_VPN_ETHERNET,
            "vpn-vedge-interface": WAN_VPN_ETHERNET,
            "vpn-vmanage-interface": WAN_VPN_ETHERNET,
            "vpn-cedge-interface-multilink-controller": WAN_VPN_MULTILINK,
        },
        "suffix": "_TRANSPORT",
    },
    VPN_SERVICE: {
        "mapping": {
            "cisco_bgp": LAN_BGP,
            "bgp": LAN_BGP,
            "cisco_ospf": LAN_OSPF,
            "cisco_ospfv3": LAN_OSPFV3,
            "vpn-vedge-interface-gre": LAN_VPN_GRE,
            "cisco_vpn_interface": LAN_VPN_ETHERNET,
            "vpn-vsmart-interface": LAN_VPN_ETHERNET,
            "vpn-vedge-interface": LAN_VPN_ETHERNET,
            "vpn-vmanage-interface": LAN_VPN_ETHERNET,
            "cisco_vpn_interface_gre": LAN_VPN_GRE,
            "cisco_vpn_interface_ipsec": LAN_VPN_IPSEC,
            "vpn-interface-svi": LAN_VPN_SVI,
            "vpn-vedge-interface-ipsec": LAN_VPN_IPSEC,
            "vpn-cedge-interface-multilink-controller": LAN_VPN_MULTILINK,
        },
        "suffix": "_SERVICE",
    },
}

MULTI_PARCEL_FEATURE_TEMPLATES = [WAN_OSPFV3, LAN_OSPFV3]
