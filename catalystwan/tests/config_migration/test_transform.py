# Copyright 2023 Cisco Systems, Inc. and its affiliates
from typing import List, Optional, TypeVar
from uuid import UUID, uuid4

from catalystwan.api.configuration_groups.parcel import _ParcelBase
from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import (
    DeviceTemplateWithInfo,
    TransformedParcel,
    UX1Config,
    UX1Templates,
)
from catalystwan.models.templates import FeatureTemplateInformation
from catalystwan.tests.config_migration.test_data import (
    dhcp_server,
    interface_ethernet,
    interface_gre,
    interface_ipsec,
    interface_multilink,
    ospfv3,
    vpn_management,
    vpn_service,
    vpn_transport,
)
from catalystwan.workflows.config_migration import transform

T = TypeVar("T", FeatureTemplateInformation, _ParcelBase)


def deepcopy_models(*models: T) -> List[T]:
    """During testing, models can be modified."""
    return [model.model_copy(deep=True) for model in models]


def find_subelement_parcel(
    parcels: List[TransformedParcel],
    parent_parcel: TransformedParcel,
    subelement_name: str,
    subelement_name_suffix: str,
) -> Optional[TransformedParcel]:
    subelement_parcel = next(
        (
            p
            for p in parcels
            if p.header.origin in parent_parcel.header.subelements
            and p.parcel.parcel_name.startswith(subelement_name)
            and p.parcel.parcel_name.endswith(subelement_name_suffix)
        ),
        None,
    )
    return subelement_parcel


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

    vpn_512_management, vpn_0_transport, vpn_1_service = deepcopy_models(vpn_management, vpn_transport, vpn_service)
    gre, ethernet, ipsec = deepcopy_models(interface_gre, interface_ethernet, interface_ipsec)

    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[
                vpn_512_management,
                vpn_0_transport,
                vpn_1_service,
                gre,
                ethernet,
                ipsec,
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
                            name=vpn_management.name,
                            templateId=vpn_management.id,
                            templateType=vpn_management.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=ethernet.name,
                                    templateId=ethernet.id,
                                    templateType=ethernet.template_type,
                                ),
                            ],
                        ),
                        GeneralTemplate(
                            name=vpn_0_transport.name,
                            templateId=vpn_0_transport.id,
                            templateType=vpn_0_transport.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=gre.name,
                                    templateId=gre.id,
                                    templateType=gre.template_type,
                                ),
                                GeneralTemplate(
                                    name=ethernet.name,
                                    templateId=ethernet.id,
                                    templateType=ethernet.template_type,
                                ),
                            ],
                        ),
                        GeneralTemplate(
                            name=vpn_1_service.name,
                            templateId=vpn_1_service.id,
                            templateType=vpn_1_service.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=gre.name,
                                    templateId=gre.id,
                                    templateType=gre.template_type,
                                ),
                                GeneralTemplate(
                                    name=ethernet.name,
                                    templateId=ethernet.id,
                                    templateType=ethernet.template_type,
                                ),
                                GeneralTemplate(
                                    name=ipsec.name,
                                    templateId=ipsec.id,
                                    templateType=ipsec.template_type,
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    )
    # Act
    ux2_config = transform(ux1_config, add_suffix=False).ux2_config
    # There must be feature profiles named DeviceTemplate_service and DeviceTemplate_transport_and_management
    service_profile = None
    transport_and_management_profile = None
    for profile in ux2_config.feature_profiles:
        if profile.feature_profile.name == "DeviceTemplate_service":
            service_profile = profile
        elif profile.feature_profile.name == "DeviceTemplate_transport_and_management":
            transport_and_management_profile = profile

    # Find the transformed VPN parcels
    transport_vpn_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if p.header.origin in transport_and_management_profile.header.subelements
        and vpn_0_transport.name in p.parcel.parcel_name
    )
    service_vpn_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if p.header.origin in service_profile.header.subelements and vpn_1_service.name in p.parcel.parcel_name
    )
    management_vpn_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if p.header.origin in transport_and_management_profile.header.subelements
        and vpn_management.name in p.parcel.parcel_name
    )

    # Find the required VPN sub-elements
    transport_gre = find_subelement_parcel(
        ux2_config.profile_parcels,
        transport_vpn_parcel,
        interface_gre.name,
        "_TRANSPORT",
    )
    transport_ethernet = find_subelement_parcel(
        ux2_config.profile_parcels,
        transport_vpn_parcel,
        interface_ethernet.name,
        "_TRANSPORT",
    )
    service_gre = find_subelement_parcel(ux2_config.profile_parcels, service_vpn_parcel, interface_gre.name, "_SERVICE")
    service_ethernet = find_subelement_parcel(
        ux2_config.profile_parcels,
        service_vpn_parcel,
        interface_ethernet.name,
        "_SERVICE",
    )
    service_ipsec = find_subelement_parcel(
        ux2_config.profile_parcels, service_vpn_parcel, interface_ipsec.name, "_SERVICE"
    )
    management_ethernet = find_subelement_parcel(
        ux2_config.profile_parcels,
        management_vpn_parcel,
        interface_ethernet.name,
        "_MANAGEMENT",
    )
    # Assert

    # Assert Feature Profiles have correct VPNs
    assert service_profile is not None
    assert service_profile.header.subelements == {service_vpn_parcel.header.origin}
    assert transport_and_management_profile is not None
    assert transport_and_management_profile.header.subelements == {
        transport_vpn_parcel.header.origin,
        management_vpn_parcel.header.origin,
    }

    # Assert VPNs have correct interfaces
    assert transport_gre is not None
    assert transport_ethernet is not None
    assert service_gre is not None
    assert service_ethernet is not None
    assert service_ipsec is not None
    assert management_ethernet is not None


def test_when_ospfv3_feature_template_expect_two_parcels_assigin_to_correct_profile():
    """Ospfv3 feature template have data that can create two parcels, one for the ospfv3_ipv4
    and another for the ospfv3_ipv6. This test checks if the transformed template produce two
    parcels and if they are correctly assigned to the appropriate feature profiles after
    the transformation from UX1 to UX2."""

    # Arrange
    vpn_service_, vpn_0_transport, ospfv3_ft_1, ospfv3_ft_2 = deepcopy_models(
        vpn_service, vpn_transport, ospfv3, ospfv3
    )

    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[ospfv3_ft_1, ospfv3_ft_2, vpn_0_transport, vpn_service_],
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
                            name=vpn_0_transport.name,
                            templateId=str(vpn_0_transport.id),
                            templateType=vpn_0_transport.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=ospfv3_ft_1.name,
                                    templateId=ospfv3_ft_1.id,
                                    templateType=ospfv3_ft_1.template_type,
                                    subTemplates=[],
                                ),
                            ],
                        ),
                        GeneralTemplate(
                            name=vpn_service_.name,
                            templateId=str(vpn_service_.id),
                            templateType=vpn_service_.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=ospfv3_ft_2.name,
                                    templateId=ospfv3_ft_2.id,
                                    templateType=ospfv3_ft_2.template_type,
                                    subTemplates=[],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    )
    # Act
    ux2_config = transform(ux1_config, add_suffix=False).ux2_config
    service_profile = None
    transport_and_management_profile = None
    for profile in ux2_config.feature_profiles:
        if profile.feature_profile.name == "DeviceTemplate_service":
            service_profile = profile
        elif profile.feature_profile.name == "DeviceTemplate_transport_and_management":
            transport_and_management_profile = profile

    # Find the transformed VPN parcels
    transport_vpn_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if p.header.origin in transport_and_management_profile.header.subelements
        and vpn_0_transport.name in p.parcel.parcel_name
    )
    service_vpn_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if p.header.origin in service_profile.header.subelements and vpn_service_.name in p.parcel.parcel_name
    )
    # Find the required VPN sub-elements that are created from the OSPFv3 template
    t_ospfv3_ipv4_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if "_TRANSPORT_IPV4" in p.parcel.parcel_name and p.header.type == "routing/ospfv3/ipv4"
    )
    t_ospfv3_ipv6_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if "_TRANSPORT_IPV6" in p.parcel.parcel_name and p.header.type == "routing/ospfv3/ipv6"
    )

    s_ospfv3_ipv4_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if "_SERVICE_IPV4" in p.parcel.parcel_name and p.header.type == "routing/ospfv3/ipv4"
    )
    s_ospfv3_ipv6_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if "_SERVICE_IPV6" in p.parcel.parcel_name and p.header.type == "routing/ospfv3/ipv6"
    )
    # Assert
    assert transport_vpn_parcel is not None
    assert transport_vpn_parcel.header.subelements == {
        t_ospfv3_ipv4_parcel.header.origin,
        t_ospfv3_ipv6_parcel.header.origin,
    }
    assert service_vpn_parcel is not None
    assert service_vpn_parcel.header.subelements == {
        s_ospfv3_ipv4_parcel.header.origin,
        s_ospfv3_ipv6_parcel.header.origin,
    }


def test_when_nested_feature_templates_with_interfaces_and_dhcp_servers_expect_correct_subelements_for_interfaces():
    """This checks if two levels nested templates are correctly assigned to the correct parent template.

    VPN can have interfaces and interfaces can have DHCP servers."""

    # Arrange
    vpn_service_, ethernet, multilink, dhcp = deepcopy_models(
        vpn_service, interface_ethernet, interface_multilink, dhcp_server
    )

    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[vpn_service_, ethernet, multilink, dhcp],
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
                            name=vpn_service_.name,
                            templateId=vpn_service_.id,
                            templateType=vpn_service_.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=ethernet.name,
                                    templateId=ethernet.id,
                                    templateType=ethernet.template_type,
                                    subTemplates=[
                                        GeneralTemplate(
                                            name=dhcp.name,
                                            templateId=dhcp.id,
                                            templateType=dhcp.template_type,
                                        ),
                                    ],
                                ),
                                GeneralTemplate(
                                    name=multilink.name,
                                    templateId=multilink.id,
                                    templateType=multilink.template_type,
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    )
    # Act
    ux2_config = transform(ux1_config).ux2_config
    # Find the transformed Ethernet parcel
    ethernet_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if "_SERVICE" in p.parcel.parcel_name and p.header.type == "lan/vpn/interface/ethernet"
    )
    multilink_parcel = next(
        p
        for p in ux2_config.profile_parcels
        if "_SERVICE" in p.parcel.parcel_name and p.header.type == "lan/vpn/interface/multilink"
    )
    # Assert
    assert ethernet_parcel is not None
    assert ethernet_parcel.header.subelements == {UUID(dhcp.id)}
    assert multilink_parcel is not None
    assert multilink_parcel.header.subelements == set()


def test_when_transform_expect_removed_copies():
    """During transform we create copies of the templates,
    but we need to remove the original templates from the list,
    to clean list of templates that will not be pushed to UX2.0.

    Also remove standalone templates that are not used in any device template.
    """

    # Arrange

    #
    # Original Service VPN should be deleted and not converted becouse
    # it is used in the two Device Templates and each of them
    # has its own copy of the Service VPN template.
    #
    # Original Management VPN should be deleted and not converted becouse
    # it is not used in any Device Template.
    #
    # Original Ethernet interface should be deleted and not converted
    # becouse it is used in the two Device Templates and each of them
    # has its own copy of the Ethernet interface template.
    #
    vpn_service_, vpn_standalone, ethernet = deepcopy_models(vpn_service, vpn_management, interface_ethernet)
    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[vpn_service_, vpn_standalone, ethernet],
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
                            name=vpn_service_.name,
                            templateId=vpn_service_.id,
                            templateType=vpn_service_.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=ethernet.name,
                                    templateId=ethernet.id,
                                    templateType=ethernet.template_type,
                                ),
                            ],
                        ),
                    ],
                ),
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
                            name=vpn_service_.name,
                            templateId=vpn_service_.id,
                            templateType=vpn_service_.template_type,
                            subTemplates=[
                                GeneralTemplate(
                                    name=ethernet.name,
                                    templateId=ethernet.id,
                                    templateType=ethernet.template_type,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    )
    # Act
    ux2_config = transform(ux1_config).ux2_config
    removed_vpn_service = next(
        (p for p in ux2_config.profile_parcels if p.parcel.parcel_name == vpn_service_.name), None
    )
    removed_vpn_standalone = next(
        (p for p in ux2_config.profile_parcels if p.parcel.parcel_name == vpn_standalone.name), None
    )
    removed_ethernet = next((p for p in ux2_config.profile_parcels if p.parcel.parcel_name == ethernet.name), None)
    # Assert
    assert removed_vpn_service is None
    assert removed_vpn_standalone is None
    assert removed_ethernet is None
