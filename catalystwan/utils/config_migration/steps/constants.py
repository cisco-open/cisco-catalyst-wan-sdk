"""Artificial constants to represent the VPN template types"""
CISCO_VPN_TRANSPORT_AND_MANAGEMENT = "cisco_vpn_transport_and_management"
CISCO_VPN_SERVICE = "cisco_vpn_service"


"""Atrificial constants to diffrientiate between Additional Cisco VPN 0 Templates,
Additional Cisco VPN 512 Templates and Additional Cisco VPN Templates. They all use the
same feature templates in ux1.0 but in ux2.0 every additional VPN parcel has a diferent
endpoint and model!
"""
ADDITIONAL_TEMPLATES = [
    "cisco_vpn_interface_gre",
    "cisco_vpn_interface_ipsec",
    "vpn-interface-svi",
    "cisco_vpn_interface",
    "vpn-vedge-interface-gre",
    "vpn-vsmart-interface",
    "vpn-vedge-interface",
    "vpn-vmanage-interface",
    "vpn-vedge-interface-ipsec",
]

WAN_VPN_GRE = "wan/vpn/interface/gre"
WAN_VPN_IPSEC = "wan/vpn/interface/ipsec"
WAN_VPN_SVI = "wan/vpn/interface/svi"
WAN_VPN_ETHERNET = "wan/vpn/interface/ethernet"

LAN_VPN_GRE = "lan/vpn/interface/gre"
LAN_VPN_IPSEC = "lan/vpn/interface/ipsec"
LAN_VPN_SVI = "lan/vpn/interface/svi"
LAN_VPN_ETHERNET = "lan/vpn/interface/ethernet"

TRANSPORT_AND_MANAGEMENT_ADDITIONAL_TEMPLATES_MAPPING = {
    "vpn-vedge-interface-gre": WAN_VPN_GRE,
    "cisco_vpn_interface_gre": WAN_VPN_GRE,
    "cisco_vpn_interface_ipsec": WAN_VPN_IPSEC,
    "vpn-interface-svi": WAN_VPN_SVI,
    "cisco_vpn_interface": WAN_VPN_ETHERNET,
    "vpn-vsmart-interface": WAN_VPN_ETHERNET,
    "vpn-vedge-interface": WAN_VPN_ETHERNET,
    "vpn-vmanage-interface": WAN_VPN_ETHERNET,
}

SERVICE_ADDITIONAL_TEMPLATES_MAPPING = {
    "vpn-vedge-interface-gre": LAN_VPN_GRE,
    "cisco_vpn_interface": LAN_VPN_ETHERNET,
    "vpn-vsmart-interface": LAN_VPN_ETHERNET,
    "vpn-vedge-interface": LAN_VPN_ETHERNET,
    "vpn-vmanage-interface": LAN_VPN_ETHERNET,
    "cisco_vpn_interface_gre": LAN_VPN_GRE,
    "cisco_vpn_interface_ipsec": LAN_VPN_IPSEC,
    "vpn-interface-svi": LAN_VPN_SVI,
    "vpn-vedge-interface-ipsec": LAN_VPN_IPSEC,
}

CAST_TEMPLATE_TYPE = {
    CISCO_VPN_TRANSPORT_AND_MANAGEMENT: TRANSPORT_AND_MANAGEMENT_ADDITIONAL_TEMPLATES_MAPPING,
    CISCO_VPN_SERVICE: SERVICE_ADDITIONAL_TEMPLATES_MAPPING,
}

NEW_TEMPALTE_NAME_SUFFIX = {
    CISCO_VPN_TRANSPORT_AND_MANAGEMENT: "_TRANSPORT",
    CISCO_VPN_SERVICE: "_SERVICE",
}
