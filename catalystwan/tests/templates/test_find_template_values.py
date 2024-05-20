from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.utils.feature_template.find_template_values import find_template_values


def test_find_template_values():
    input_values = {
        "vpn-id": {"vipObjectType": "object", "vipType": "constant", "vipValue": 0},
        "name": {
            "vipObjectType": "object",
            "vipType": "ignore",
            "vipVariableName": "vpn_name",
        },
        "ecmp-hash-key": {
            "layer4": {
                "vipObjectType": "object",
                "vipType": "ignore",
                "vipValue": "false",
                "vipVariableName": "vpn_layer4",
            }
        },
        "nat64-global": {"prefix": {"stateful": {}}},
        "nat64": {
            "v4": {
                "pool": {
                    "vipType": "ignore",
                    "vipValue": [],
                    "vipObjectType": "tree",
                    "vipPrimaryKey": ["name"],
                }
            }
        },
        "nat": {
            "natpool": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["name"],
            },
            "port-forward": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["source-port", "translate-port"],
            },
            "static": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["source-ip", "translate-ip"],
            },
        },
        "route-import": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["protocol"],
        },
        "route-export": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["protocol"],
        },
        "dns": {
            "vipType": "constant",
            "vipValue": [
                {
                    "role": {
                        "vipType": "constant",
                        "vipValue": "primary",
                        "vipObjectType": "object",
                    },
                    "dns-addr": {
                        "vipType": "variableName",
                        "vipValue": "",
                        "vipObjectType": "object",
                        "vipVariableName": "vpn_dns_primary",
                    },
                    "priority-order": ["dns-addr", "role"],
                },
                {
                    "role": {
                        "vipType": "constant",
                        "vipValue": "secondary",
                        "vipObjectType": "object",
                    },
                    "dns-addr": {
                        "vipType": "variableName",
                        "vipValue": "",
                        "vipObjectType": "object",
                        "vipVariableName": "vpn_dns_secondary",
                    },
                    "priority-order": ["dns-addr", "role"],
                },
            ],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["dns-addr"],
        },
        "host": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["hostname"],
        },
        "service": {
            "vipType": "ignore",
            "vipValue": [],
            "vipObjectType": "tree",
            "vipPrimaryKey": ["svc-type"],
        },
        "ip": {
            "route": {
                "vipType": "constant",
                "vipValue": [
                    {
                        "prefix": {
                            "vipObjectType": "object",
                            "vipType": "constant",
                            "vipValue": "0.0.0.0/0",
                            "vipVariableName": "vpn_ipv4_ip_prefix",
                        },
                        "next-hop": {
                            "vipType": "constant",
                            "vipValue": [
                                {
                                    "address": {
                                        "vipObjectType": "object",
                                        "vipType": "variableName",
                                        "vipValue": "",
                                        "vipVariableName": "vpn_next_hop_ip_address_0",
                                    },
                                    "distance": {
                                        "vipObjectType": "object",
                                        "vipType": "ignore",
                                        "vipValue": 1,
                                        "vipVariableName": "vpn_next_hop_ip_distance_0",
                                    },
                                    "priority-order": ["address", "distance"],
                                }
                            ],
                            "vipObjectType": "tree",
                            "vipPrimaryKey": ["address"],
                        },
                        "priority-order": ["prefix", "next-hop", "next-hop-with-track"],
                    }
                ],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["prefix"],
            },
            "gre-route": {},
            "ipsec-route": {},
            "service-route": {},
        },
        "ipv6": {},
        "omp": {
            "advertise": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["protocol"],
            },
            "ipv6-advertise": {
                "vipType": "ignore",
                "vipValue": [],
                "vipObjectType": "tree",
                "vipPrimaryKey": ["protocol"],
            },
        },
    }
    expected_values = {
        "vpn-id": 0,
        "dns": [
            {"role": "primary", "dns-addr": DeviceVariable(name="vpn_dns_primary")},
            {"role": "secondary", "dns-addr": DeviceVariable(name="vpn_dns_secondary")},
        ],
        "ip": {
            "route": [
                {
                    "prefix": "0.0.0.0/0",
                    "next-hop": [
                        {
                            "address": DeviceVariable(name="vpn_next_hop_ip_address_0"),
                        }
                    ],
                }
            ],
        },
    }
    # Act
    result = find_template_values(input_values)
    # Assert
    assert expected_values == result
