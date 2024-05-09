# Copyright 2023 Cisco Systems, Inc. and its affiliates
from datetime import datetime
from uuid import uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import DeviceTemplateWithInfo, UX1Config, UX1Templates
from catalystwan.models.templates import FeatureTemplateInformation
from catalystwan.workflows.config_migration import transform


def test_when_many_cisco_vpn_feature_templates_expect_assign_to_correct_feature_profile():
    """Cisco VPN Feature Template can represent Serivce, Transport, or Security VPNs,
    but there is only one templateType for all of them. This test will check if the
    transformed templates are assigned to the correct feature profiles: Service or
    Transport and Management (Transport and Management are one profile).
    """

    # Arrange
    # Create a ux1 config with Service VPN, Transport VPN, and Security VPN templates
    # and a one Device Template that uses them
    vpn_512_uuid = uuid4()
    vpn_0_uuid = uuid4()
    vpn_1_uuid = uuid4()
    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[
                FeatureTemplateInformation(
                    last_updated_by="",
                    id=str(vpn_512_uuid),
                    factory_default=True,
                    name="Factory_Default_Cisco_VPN_512_Template",
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
                    name="Factory_Default_Cisco_VPN_0_Template",
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
                    name="Default_VPN_1_Cisco_V01",
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
                            name="Factory_Default_Cisco_VPN_512_Template",
                            templateId=str(vpn_512_uuid),
                            templateType="cisco_vpn",
                            subTemplates=[],
                        ),
                        GeneralTemplate(
                            name="Factory_Default_Cisco_VPN_0_Template",
                            templateId=str(vpn_0_uuid),
                            templateType="cisco_vpn",
                            subTemplates=[],
                        ),
                        GeneralTemplate(
                            name="Default_VPN_1_Cisco_V01",
                            templateId=str(vpn_1_uuid),
                            templateType="cisco_vpn",
                            subTemplates=[],
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
    # Assert
    assert service_profile.header.subelements == set([vpn_1_uuid])
    assert transport_and_management_profile.header.subelements == set([vpn_0_uuid, vpn_512_uuid])
