# Copyright 2023 Cisco Systems, Inc. and its affiliates
from datetime import datetime
from uuid import uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo, UX1Config, UX1Templates
from catalystwan.models.templates import FeatureTemplateInformation
from catalystwan.workflows.config_migration import transform


def test_when_many_cisco_vpn_feature_templates_expect_assign_to_correct_feature_profile():
    """Cisco VPN Feature Templates can represent Service, Transport, or Security VPNs,
    but there is only one templateType for all of them in UX1.

    Additionally, the additional templates for VPNs (Ethernet, SVI, GRE, IPSec) can be shared between all VPNs in UX1.

    In UX2.0, every VPN has its own endpoint and model. To differentiate between them,
    we need to assign them to the correct feature profile (Service or Transport and Management,
    where Transport and Management are combined into one profile) and create the correct Parcel.

    This test checks if the transformed templates are correctly assigned to the appropriate feature profiles after
    the transformation from UX1 to UX2."""

    # Arrange

    # Create a ux1 config with Service VPN, Transport VPN, and Security VPN templates
    # and a one Device Template that uses them, also there are interface templates
    # that are used by the VPN templates

    # Please look at the DeviceTemplateWithInfo and see the structure that should be
    # preserved when we transform the data from UX1.0 to UX2.0

    vpn_512_uuid = uuid4()
    vpn_0_uuid = uuid4()
    vpn_1_uuid = uuid4()

    vpn_0_1_shared_gre_uuid = uuid4()
    vpn_1_ethernet_uuid = uuid4()
    vpn_1_ethernet_ipsec = uuid4()

    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[
                FeatureTemplateInformation(
                    last_updated_by="",
                    id=str(vpn_512_uuid),
                    factory_default=True,
                    name="Management_VPN",
                    devices_attached=0,
                    description="Default Cisco Management VPN template settings",
                    last_updated_on=datetime.now(),
                    resource_group="global",
                    template_type="cisco_vpn",
                    device_type=[""],
                    version="15.0.0",
                    template_definiton='{"vpn-id":{"vipObjectType":"object","vipType":"constant","vipValue":512},'
                    '"name":{"vipObjectType":"object","vipType":"constant","vipValue":"Management VPN"},'
                    '"ecmp-hash-key":{"layer4":{"vipObjectType":"object","vipType":"ignore","vipValue":"false"}},'
                    '"host":{"vipType":"ignore","vipValue":[],"vipObjectType":"tree","vipPrimaryKey":["hostname"]}}',
                ),
                FeatureTemplateInformation(
                    last_updated_by="",
                    id=str(vpn_0_uuid),
                    factory_default=True,
                    name="Transport_VPN",
                    devices_attached=0,
                    description="Default Cisco Transport VPN template settings",
                    last_updated_on=datetime.now(),
                    resource_group="global",
                    template_type="cisco_vpn",
                    device_type=[""],
                    version="15.0.0",
                    template_definiton='{"vpn-id":{"vipObjectType":"object","vipType":"constant","vipValue":0},'
                    '"name":{"vipObjectType":"object","vipType":"constant","vipValue":"Transport VPN"},'
                    '"ecmp-hash-key":{"layer4":{"vipObjectType":"object","vipType":"ignore","vipValue":"false"}},'
                    '"host":{"vipType":"ignore","vipValue":[],"vipObjectType":"tree","vipPrimaryKey":["hostname"]}}',
                ),
                FeatureTemplateInformation(
                    last_updated_by="",
                    id=str(vpn_1_uuid),
                    factory_default=True,
                    name="Service_VPN",
                    devices_attached=0,
                    description="Factory Default template for VPN 1 Cisco",
                    last_updated_on=datetime.now(),
                    resource_group="global",
                    template_type="cisco_vpn",
                    device_type=[""],
                    version="15.0.0",
                    template_definiton='{"vpn-id":{"vipValue":1,"vipObjectType":"object",'
                    '"vipType":"constant","vipVariableName":""},"name":{"vipValue":"","vipObjectType":'
                    '"object","vipType":"ignore"},"dns":{"vipValue":[],"vipObjectType":"tree",'
                    '"vipType":"ignore","vipPrimaryKey":["dns-addr"]},"dns-ipv6":{"vipValue":[],'
                    '"vipObjectType":"tree","vipType":"ignore","vipPrimaryKey":["dns-addr"]},'
                    '"ecmp-hash-key":{"layer4":{"vipValue":"","vipObjectType":"object","vipType":"ignore"}},'
                    '"host":{"vipValue":[],"vipObjectType":"tree","vipType":"ignore","vipPrimaryKey":'
                    '["hostname"]},"ip":{"route": {"vipValue":[],"vipObjectType":"tree","vipType":"ignore",'
                    '"vipPrimaryKey":["prefix"]}}, "ipv6":{"route":{"vipValue":[],"vipObjectType":"tree",'
                    '"vipType":"ignore","vipPrimaryKey":["prefix"]}}, "omp":{"advertise":{"vipValue":[],'
                    '"vipObjectType":"tree","vipType":"ignore","vipPrimaryKey":["protocol"]},'
                    '"ipv6-advertise":{"vipValue":[],"vipObjectType":"tree","vipType":"ignore",'
                    '"vipPrimaryKey":["protocol"]}}, "nat64":{"v4":{"pool":{"vipValue":[],"vipObjectType":'
                    '"tree","vipType":"ignore","vipPrimaryKey":["name"]}}}}',
                ),
                FeatureTemplateInformation(
                    last_updated_by="admin",
                    id=str(vpn_0_1_shared_gre_uuid),
                    factory_default=False,
                    name="GREVPN",
                    devices_attached=0,
                    description="HnQSYJsm",
                    last_updated_on=1715275556625,
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
                ),
                FeatureTemplateInformation(
                    last_updated_by="admin",
                    id=str(vpn_1_ethernet_uuid),
                    factory_default=False,
                    name="EthernetVPN1",
                    devices_attached=0,
                    description="HnQSYJsm",
                    last_updated_on=1715275556625,
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
                ),
                FeatureTemplateInformation(
                    last_updated_by="admin",
                    id=str(vpn_1_ethernet_ipsec),
                    factory_default=False,
                    name="EthernetIpsecVPN1",
                    devices_attached=0,
                    description="HnQSYJsm",
                    last_updated_on=1715275556625,
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
                ),
            ],
            device_templates=[
                DeviceTemplateWithInfo(
                    template_id=str(uuid4()),
                    factory_default=False,
                    devices_attached=2,
                    template_name="DeviceTemplate",
                    template_description="DT-example",
                    device_role="None",
                    device_type="None",
                    security_policy_id="None",
                    policy_id="None",
                    generalTemplates=[
                        GeneralTemplate(
                            name="Management_VPN",
                            templateId=str(vpn_512_uuid),
                            templateType="cisco_vpn",
                            subTemplates=[],
                        ),
                        GeneralTemplate(
                            name="Transport_VPN",
                            templateId=str(vpn_0_uuid),
                            templateType="cisco_vpn",
                            subTemplates=[
                                GeneralTemplate(
                                    name="GREVPN",
                                    templateId=str(vpn_0_1_shared_gre_uuid),
                                    templateType="cisco_vpn_interface_gre",
                                )
                            ],
                        ),
                        GeneralTemplate(
                            name="Service_VPN",
                            templateId=str(vpn_1_uuid),
                            templateType="cisco_vpn",
                            subTemplates=[
                                GeneralTemplate(
                                    name="GREVPN",
                                    templateId=str(vpn_0_1_shared_gre_uuid),
                                    templateType="cisco_vpn_interface_gre",
                                ),
                                GeneralTemplate(
                                    name="EthernetVPN1",
                                    templateId=str(vpn_1_ethernet_uuid),
                                    templateType="cisco_vpn_interface",
                                ),
                                GeneralTemplate(
                                    name="EthernetIpsecVPN1",
                                    templateId=str(vpn_1_ethernet_ipsec),
                                    templateType="cisco_vpn_interface_ipsec",
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    )
    # Act
    ux2_config = transform(ux1_config)
    # There must be feature profiles named DeviceTemplate_service and DeviceTemplate_transport_and_management
    service_profile = None
    transport_and_management_profile = None
    for profile in ux2_config.feature_profiles:
        if profile.feature_profile.name == "DeviceTemplate_service":
            service_profile = profile
        elif profile.feature_profile.name == "DeviceTemplate_transport_and_management":
            transport_and_management_profile = profile

    # Find the transformed VPN parcels
    transport_vpn_parcel = next(p for p in ux2_config.profile_parcels if p.parcel.parcel_name == "Transport_VPN")
    service_vpn_parcel = next(p for p in ux2_config.profile_parcels if p.parcel.parcel_name == "Service_VPN")

    # Find the required VPN sub-elements
    transport_gre = next(
        (
            p
            for p in ux2_config.profile_parcels
            if p.header.origin in transport_vpn_parcel.header.subelements and p.parcel.parcel_name == "GREVPN_TRANSPORT"
        ),
        None,
    )
    service_gre = next(
        (
            p
            for p in ux2_config.profile_parcels
            if p.header.origin in service_vpn_parcel.header.subelements and p.parcel.parcel_name == "GREVPN_SERVICE"
        ),
        None,
    )
    service_ethernet = next(
        (
            p
            for p in ux2_config.profile_parcels
            if p.header.origin in service_vpn_parcel.header.subelements
            and p.parcel.parcel_name == "EthernetVPN1_SERVICE"
        ),
        None,
    )
    service_ethernet_ipsec = next(
        (
            p
            for p in ux2_config.profile_parcels
            if p.header.origin in service_vpn_parcel.header.subelements
            and p.parcel.parcel_name == "EthernetIpsecVPN1_SERVICE"
        ),
        None,
    )

    # Assert

    # Assert Feature Profiles have correct VPNs
    assert service_profile is not None
    assert service_profile.header.subelements == {vpn_1_uuid}
    assert transport_and_management_profile is not None
    assert transport_and_management_profile.header.subelements == {vpn_0_uuid, vpn_512_uuid}

    # Assert VPNs have correct interfaces
    assert transport_gre is not None
    assert service_gre is not None
    assert service_ethernet is not None
    assert service_ethernet_ipsec is not None
