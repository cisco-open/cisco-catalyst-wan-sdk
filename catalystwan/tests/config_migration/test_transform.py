# Copyright 2023 Cisco Systems, Inc. and its affiliates
from datetime import datetime
from uuid import uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo, UX1Config, UX1Templates
from catalystwan.models.templates import FeatureTemplateInformation
from catalystwan.workflows.config_migration import transform


def test_when_many_cisco_vpn_feature_templates_expect_assign_to_correct_feature_profile():
    """Cisco VPN Feature Template can represent Serivce, Transport, or Security VPNs,
    but there is only one templateType for all of them. Also the additional templates for
    cisco_vpn ("cisco_vpn_interface", "cisco_vpn_interface_gre", "cisco_vpn_interface_ipsec",
    "vpn-interface-svi") can be shared in UX1 bettwen all VPNs. In UX2.0 every VPN has its own
    endpoint and model. We need to somehow differentiate between them,
    assigin them to the correct feature profile and create correct Parcel.

    This test will check if the transformed templates are assigned to the correct feature profiles:
    Service or Transport and Management (Transport and Management are one profile).
    """

    # Arrange

    # Create a ux1 config with Service VPN, Transport VPN, and Security VPN templates
    # and a one Device Template that uses them, also there are interface templates
    # that are used by the VPN templates

    vpn_512_uuid = uuid4()
    vpn_0_uuid = uuid4()
    vpn_1_uuid = uuid4()

    vpn_0_1_shared_gre_uuid = uuid4()

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
                                )
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
    with open("test_dump.json", "w") as f:
        f.write(ux2_config.model_dump_json(indent=2, by_alias=True, exclude_none=True))

    service_profile = None
    transport_and_management_profile = None
    for profile in ux2_config.feature_profiles:
        if profile.feature_profile.name == "DeviceTemplate_service":
            service_profile = profile
        elif profile.feature_profile.name == "DeviceTemplate_transport_and_management":
            transport_and_management_profile = profile

    # There must be a Gre Interface assigned to the Service VPN and Transport VPN
    transport_vpn_transformed_parcel = next(
        filter(lambda p: p.parcel.parcel_name == "Transport_VPN", ux2_config.profile_parcels)
    )
    service_vpn_transformed_parcel = next(
        filter(lambda p: p.parcel.parcel_name == "Service_VPN", ux2_config.profile_parcels)
    )

    t_vpn_subelements = transport_vpn_transformed_parcel.header.subelements
    transport_gre = next(filter(lambda p: p.header.origin in t_vpn_subelements, ux2_config.profile_parcels))

    s_vpn_subelements = service_vpn_transformed_parcel.header.subelements
    service_gre = next(filter(lambda p: p.header.origin in s_vpn_subelements, ux2_config.profile_parcels))

    # Assert

    # Assert feature profile have correct VPNs
    assert service_profile.header.subelements == set([vpn_1_uuid])
    assert transport_and_management_profile.header.subelements == set([vpn_0_uuid, vpn_512_uuid])

    # Assert VPNs have correct interfaces
    assert transport_gre.parcel.parcel_name == "GREVPN_TRANSPORT"
    assert service_gre.parcel.parcel_name == "GREVPN_SERVICE"
