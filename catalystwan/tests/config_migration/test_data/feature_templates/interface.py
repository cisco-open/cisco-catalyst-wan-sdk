# Copyright 2023 Cisco Systems, Inc. and its affiliates
from datetime import datetime
from uuid import uuid4

from catalystwan.models.templates import FeatureTemplateInformation

interface_ethernet = FeatureTemplateInformation(
    last_updated_by="admin",
    id=str(uuid4()),
    factory_default=False,
    name="InterfaceEthernet",
    devices_attached=0,
    description="HnQSYJsm",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_vpn_interface",
    device_type=["vedge-C1101-4PLTEPW"],
    version="15.0.0",
    template_definiton='{"if-name":'
    '{"vipValue": "GigabitEthernet2", "vipObjectType": "object", "vipType":'
    '"constant", "vipVariableName": ""}, "description": {"vipValue": "", "vipObjectType":'
    '"object", "vipType": "ignore"}, "poe": {"vipValue": "", "vipObjectType": "object",'
    '"vipType": "ignore"}, "ip": {"address": {"vipValue": "10.1.17.15/24", "vipObjectType":'
    '"object", "vipType": "constant", "vipVariableName": ""}, "secondary-address": {"vipValue":'
    '[], "vipObjectType": "tree", "vipType": "ignore", "vipPrimaryKey": ["address"]}, "dhcp-'
    'client": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "dhcp-'
    'distance": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}}, "ipv6":'
    '{"address": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "dhcp-'
    'client": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "secondary-'
    'address": {"vipValue": [], "vipObjectType": "tree", "vipType": "ignore", "vipPrimaryKey":'
    '["address"]}, "access-list": {"vipValue": [], "vipObjectType": "tree", "vipType":'
    '"ignore", "vipPrimaryKey": ["direction"]}, "dhcp-helper-v6": {"vipValue": [],'
    '"vipObjectType": "tree", "vipType": "ignore", "vipPrimaryKey": ["address"]}}, "dhcp-'
    'helper": {"vipValue": "", "vipObjectType": "list", "vipType": "ignore"}, "tracker":'
    '{"vipValue": "", "vipObjectType": "list", "vipType": "ignore"}, "nat": {"vipValue": "",'
    '"vipObjectType": "node-only", "vipType": "ignore", "udp-timeout": {"vipValue": "",'
    '"vipObjectType": "object", "vipType": "ignore"}, "tcp-timeout": {"vipValue": "",'
    '"vipObjectType": "object", "vipType": "ignore"}, "static": {"vipValue": [],'
    '"vipObjectType": "tree", "vipType": "ignore", "vipPrimaryKey": ["source-ip", "translate-'
    'ip"]}}, "nat64": {"vipValue": "", "vipObjectType": "node-only", "vipType": "ignore"},'
    '"mtu": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "tcp-mss-adjust":'
    '{"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "tloc-extension":'
    '{"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "tloc-extension-gre-'
    'from": {"src-ip": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"},'
    '"xconnect": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}}, "mac-'
    'address": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "speed":'
    '{"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "duplex": {"vipValue":'
    '"", "vipObjectType": "object", "vipType": "ignore"}, "shutdown": {"vipValue": "false",'
    '"vipObjectType": "object", "vipType": "constant", "vipVariableName": ""}, "arp-timeout":'
    '{"vipValue": "", "vipObjectType": "object", "vipType": "ignore"}, "autonegotiate":'
    '{"vipValue": "true", "vipObjectType": "object", "vipType": "constant", "vipVariableName":'
    '""}, "ip-directed-broadcast": {"vipValue": "", "vipObjectType": "object", "vipType":'
    '"ignore"}, "icmp-redirect-disable": {"vipValue": "", "vipObjectType": "object", "vipType":'
    '"ignore"}, "shaping-rate": {"vipValue": "", "vipObjectType": "object", "vipType":'
    '"ignore"}, "qos-map": {"vipValue": "", "vipObjectType": "object", "vipType": "ignore"},'
    '"rewrite-rule": {"rule-name": {"vipValue": "", "vipObjectType": "object", "vipType":'
    '"ignore"}}, "access-list": {"vipValue": [], "vipObjectType": "tree", "vipType": "ignore",'
    '"vipPrimaryKey": ["direction"]}, "arp": {"ip": {"vipValue": [], "vipObjectType": "tree",'
    '"vipType": "ignore", "vipPrimaryKey": ["addr"]}}, "vrrp": {"vipValue": [],'
    '"vipObjectType": "tree", "vipType": "ignore", "vipPrimaryKey": ["grp-id"]}, "ipv6-vrrp":'
    '{"vipValue": [], "vipObjectType": "tree", "vipType": "ignore", "vipPrimaryKey": ["grp-'
    'id"]}}',
)

interface_gre = FeatureTemplateInformation(
    last_updated_by="admin",
    id=str(uuid4()),
    factory_default=False,
    name="InterfaceGre",
    devices_attached=0,
    description="HnQSYJsm",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_vpn_interface_gre",
    device_type=["vedge-C1101-4PLTEPW"],
    version="15.0.0",
    template_definiton='{"if-name":{"vipObjectType":"object","vipType":"constant","vipValue":'
    '"ImW32","vipVariableName":"vpn_if_name"},"description":{"vipObjectType":"object","vipType":'
    '"constant","vipValue":"AVDYACBJ","vipVariableName":"vpn_if_description"},"application":'
    '{"vipObjectType":"object","vipType":"constant","vipValue":"none","vipVariableName":'
    '"vpn_if_application"},"ip":{"address":{"vipObjectType":"object","vipType":"constant"'
    ',"vipValue":"3.4.5.6/15","vipVariableName":"vpn_if_ipv4_address"}},"shutdown":'
    '{"vipObjectType":"object","vipType":"constant","vipValue":"true","vipVariableName":'
    '"vpn_if_shutdown"},"tunnel-source-interface":{"vipObjectType":"object","vipType":'
    '"constant","vipValue":"Gre123","vipVariableName":"vpn_if_tunnel_source_interface"},'
    '"tunnel-destination":{"vipObjectType":"object","vipType":"constant","vipValue":"3.4.5.2"'
    ',"vipVariableName":"vpn_if_tunnel_destination"},"mtu":{"vipObjectType":"object","vipType"'
    ':"constant","vipValue":72,"vipVariableName":"vpn_if_ip_mtu"},"tcp-mss-adjust":'
    '{"vipObjectType":"object","vipType":"constant","vipValue":1213,"vipVariableName":'
    '"vpn_if_tcp_mss_adjust"},"rewrite-rule":{"rule-name":{"vipObjectType":"object","vipType"'
    ':"constant","vipValue":"GPqkFuGH","vipVariableName":"rewrite_rule_name"}},"access-list"'
    ':{"vipType":"constant","vipValue":[{"acl-name":{"vipObjectType":"object","vipType":'
    '"constant","vipValue":"JPlPFHcO","vipVariableName":"access_list_ingress_acl_name_ipv4"},'
    '"direction":{"vipType":"constant","vipValue":"in","vipObjectType":"object"}'
    ',"priority-order":["direction","acl-name"]},{"acl-name":{"vipObjectType":"object",'
    '"vipType":"constant","vipValue":"OICQGibD","vipVariableName":"access_list_egress_acl_name_ipv4"}'
    ',"direction":{"vipType":"constant","vipValue":"out","vipObjectType":"object"},'
    '"priority-order":["direction","acl-name"]}],"vipObjectType":"tree",'
    '"vipPrimaryKey":["direction"]},"clear-dont-fragment":{"vipObjectType":'
    '"object","vipType":"constant","vipValue":"true","vipVariableName":'
    '"vpn_gre_tunnel_tunnel_clear_dont_fragment"},"tracker":{"vipObjectType":"list","vipType"'
    ':"constant","vipValue":["JibukWQq"],"vipVariableName":"tracker"}}',
)

interface_ipsec = FeatureTemplateInformation(
    last_updated_by="admin",
    id=str(uuid4()),
    factory_default=False,
    name="InterfaceIpsec",
    devices_attached=0,
    description="HnQSYJsm",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="cisco_vpn_interface_ipsec",
    device_type=["vedge-C1101-4PLTEPW"],
    version="15.0.0",
    template_definiton='{"if-name": {"vipObjectType":'
    '"object", "vipType": "constant", "vipValue": "ipsec4",'
    '"vipVariableName": "vpn_if_name"}, "description": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipVariableName": "vpn_if_description"}, "application": {"vipObjectType":'
    '"object", "vipType": "notIgnore", "vipValue": "none", "vipVariableName":'
    '"vpn_if_application"}, "ip": {"address": {"vipObjectType": "object", "vipType":'
    '"constant", "vipValue": "2.2.2.2/16", "vipVariableName": "vpn_if_ipv4_address"}},'
    '"shutdown": {"vipObjectType": "object", "vipType": "ignore", "vipValue": "true",'
    '"vipVariableName": "vpn_if_shutdown"}, "tunnel-source": {"vipObjectType": "object",'
    '"vipType": "constant", "vipValue": "10.0.0.5", "vipVariableName": "vpn_if_tunnel_source"},'
    '"tunnel-destination": {"vipObjectType": "object", "vipType": "constant", "vipValue": "0::"'
    ', "vipVariableName": "vpn_if_tunnel_destination"}, "mtu": {"vipObjectType": "object",'
    '"vipType": "ignore", "vipValue": 1500, "vipVariableName": "vpn_if_mtu"}, "tcp-mss-adjust":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"vpn_if_tcp_mss_adjust"}, "dead-peer-detection": {"dpd-interval": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipValue": 10, "vipVariableName": "vpn_if_dpd_interval"},'
    '"dpd-retries": {"vipObjectType": "object", "vipType": "ignore", "vipValue": 3,'
    '"vipVariableName": "vpn_if_dpd_retries"}}, "ike": {"ike-version": {"vipObjectType":'
    '"object", "vipType": "constant", "vipValue": 2}, "ike-rekey-interval": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipValue": 14400, "vipVariableName":'
    '"vpn_if_ike_rekey_interval"}, "ike-ciphersuite": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipValue": "aes256-cbc-sha1", "vipVariableName": "vpn_if_ike_ciphersuite"},'
    '"ike-group": {"vipObjectType": "object", "vipType": "ignore", "vipValue": "16",'
    '"vipVariableName": "vpn_if_ike_group"}, "authentication-type": {"pre-shared-key": {"pre-'
    'shared-secret": {"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"vpn_if_pre_shared_secret"}, "ike-local-id": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipVariableName": "vpn_if_ike_local_id"}, "ike-remote-id": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipVariableName": "vpn_if_ike_remote_id"}}}}, "ipsec":'
    '{"ipsec-rekey-interval": {"vipObjectType": "object", "vipType": "ignore", "vipValue":'
    '3600, "vipVariableName": "vpn_if_ipsec_rekey_interval"}, "ipsec-replay-window":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipValue": 512, "vipVariableName":'
    '"vpn_if_ipsec_replay_window"}, "ipsec-ciphersuite": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipValue": "aes256-gcm", "vipVariableName": "vpn_if_ipsec_ciphersuite"},'
    '"perfect-forward-secrecy": {"vipObjectType": "object", "vipType": "ignore", "vipValue":'
    '"group-16", "vipVariableName": "vpn_if_ipsec_perfect_forward_secrecy"}}, "clear-dont-'
    'fragment": {"vipObjectType": "object", "vipType": "ignore", "vipValue": "false",'
    '"vipVariableName": "vpn_ipsec_tunnel_tunnel_clear_dont_fragment"}, "tracker":'
    '{"vipObjectType": "list", "vipType": "ignore", "vipVariableName": "tracker"}}',
)

interface_multilink = FeatureTemplateInformation(
    last_updated_by="admin",
    id=str(uuid4()),
    factory_default=False,
    name="InterfaceMultilink",
    devices_attached=0,
    description="HnQSYJsm",
    last_updated_on=datetime.now(),
    resource_group="global",
    template_type="vpn-cedge-interface-multilink-controller",
    device_type=["vedge-C1101-4PLTEPW"],
    version="15.0.0",
    template_definiton='{"if-name": {"vipObjectType": "object", "vipType":'
    '"constant", "vipValue": "Multilink1",'
    '"vipVariableName": "if_multilink_ctrl_if_name"}, "ppp": {"authentication": {"method":'
    '{"vipObjectType": "object", "vipType": "constant", "vipValue": "pap"}, "pap":'
    '{"vipObjectType": "node-only", "vipType": "constant", "vipValue": "false"}, "callin":'
    '{"vipObjectType": "node-only", "vipType": "notIgnore", "vipValue": "callin",'
    '"vipVariableName": "pppoa_dsl_auth-callin"}}, "pap": {"sent-username": {"username":'
    '{"username-string": {"vipObjectType": "object", "vipType": "constant", "vipValue": "test",'
    '"vipVariableName": "pppoa_dsl_pap_username_string"}, "password": {"vipObjectType": "node-'
    'only", "vipType": "constant", "vipValue": "true"}, "ppp-auth-password": {"vipObjectType":'
    '"object", "vipType": "constant", "vipValue": "test", "vipVariableName":'
    '"pppoa_dsl_pap_auth_password"}}}}, "multilink": {"group": {"vipObjectType": "object",'
    '"vipType": "constant", "vipValue": 1, "vipVariableName":'
    '"if_multilink_ctrl_multilink_group"}, "fragment": {"disable": {"vipObjectType": "node-'
    'only", "vipType": "ignore", "vipValue": "false", "vipVariableName":'
    '"if_multilink_fragment_disable_multilink_fragment_disable"}, "delay": {"delay-value":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"if_multilink_fragment_delay_value_multilink_fragment_delay_value"}}}, "interleave":'
    '{"vipObjectType": "node-only", "vipType": "ignore", "vipValue": "false",'
    '"vipVariableName": "if_multilink_interleave_multilink_interleave"}}}, "description":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"if_multilink_ctrl_description"}, "ip": {"address": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipVariableName": "if_multilink_ctrl_ip_addr"}}, "ipv6": {"address":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"if_multilink_ctrl_ipv6_address"}, "access-list": {"vipType": "ignore", "vipValue": [],'
    '"vipObjectType": "tree", "vipPrimaryKey": ["direction"]}}, "pmtu": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipValue": "false", "vipVariableName": "vpn_if_pmtu"},'
    '"mtu": {"vipObjectType": "object", "vipType": "ignore", "vipValue": 1500,'
    '"vipVariableName": "if_multilink_ctrl_mtu"}, "static-ingress-qos": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipVariableName": "vpn_if_static_ingress_qos"}, "tcp-mss-'
    'adjust": {"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"vpn_if_tcp_mss_adjust"}, "tloc-extension": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipVariableName": "vpn_if_tloc_extension"}, "shutdown": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipValue": "true", "vipVariableName":'
    '"if_multilink_ctrl_shutdown"}, "autonegotiate": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipValue": "true", "vipVariableName": "vpn_if_autonegotiate"}, "shaping-rate":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName": "qos_shaping-rate"},'
    '"qos-map": {"vipObjectType": "object", "vipType": "ignore", "vipVariableName": "qos-map"},'
    '"qos-map-vpn": {"vipObjectType": "object", "vipType": "ignore", "vipVariableName": "vpn-'
    'qos_map"}, "bandwidth-upstream": {"vipObjectType": "object", "vipType": "ignore",'
    '"vipVariableName": "if_multilink_ctrl_bandwidth_upstream"}, "bandwidth-downstream":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"if_multilink_ctrl_bandwidth_downstream"}, "rewrite-rule": {"rule-name": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipVariableName": "rewrite_rule-name"}}, "access-list":'
    '{"vipType": "ignore", "vipValue": [], "vipObjectType": "tree", "vipPrimaryKey":'
    '["direction"]}, "policer": {"vipType": "ignore", "vipValue": [], "vipObjectType": "tree",'
    '"vipPrimaryKey": ["policer-name", "direction"]}, "nat64-enable": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipValue": "false"}, "qos-adaptive": {"vipObjectType":'
    '"object", "vipType": "ignore", "vipValue": "false", "vipVariableName": "adaptive_qos"},'
    '"ip-directed-broadcast": {"vipObjectType": "object", "vipType": "ignore", "vipValue":'
    '"false", "vipVariableName": "vpn_if_ip-directed-broadcast"}, "service-provider":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipVariableName":'
    '"vpn_if_service_provider"}, "clear-dont-fragment": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipValue": "false", "vipVariableName": "vpn_if_clear_dont_fragment"},'
    '"controller": {"nim-list": {"vipType": "constant", "vipValue": [{"nim": {"vipObjectType":'
    '"object", "vipType": "constant", "vipValue": "2t", "vipVariableName":'
    '"nim_twot_list_nim"}, "if-name": {"vipObjectType": "object", "vipType": "constant",'
    '"vipValue": "serial1", "vipVariableName": "nim_twot_list_if-name"}, "description":'
    '{"vipObjectType": "object", "vipType": "ignore", "vipValue": "", "vipVariableName":'
    '"nim_twot_list_description"}, "bandwidth": {"vipObjectType": "object", "vipType":'
    '"ignore", "vipValue": "", "vipVariableName": "nim_twot_list_bandwidth"}, "DCE-mode-'
    'config": {"clock-rate": {"vipObjectType": "object", "vipType": "ignore", "vipValue": "",'
    '"vipVariableName": "nim_twot_list_clock-rate"}}}], "vipObjectType": "tree",'
    '"vipPrimaryKey": ["nim", "if-name"]}}}',
)
