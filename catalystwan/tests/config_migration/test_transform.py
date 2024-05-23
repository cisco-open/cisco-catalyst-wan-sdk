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
    interface_ethernet,
    interface_gre,
    interface_ipsec,
    malformed,
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
    transport_vpn_parcel = next(p for p in ux2_config.profile_parcels if p.parcel.parcel_name == vpn_0_transport.name)
    service_vpn_parcel = next(p for p in ux2_config.profile_parcels if p.parcel.parcel_name == vpn_1_service.name)
    management_vpn_parcel = next(
        p for p in ux2_config.profile_parcels if p.parcel.parcel_name == vpn_512_management.name
    )

    # Find the required VPN sub-elements
    transport_gre = find_subelement_parcel(
        ux2_config.profile_parcels, transport_vpn_parcel, interface_gre.name, "_TRANSPORT"
    )
    transport_ethernet = find_subelement_parcel(
        ux2_config.profile_parcels, transport_vpn_parcel, interface_ethernet.name, "_TRANSPORT"
    )
    service_gre = find_subelement_parcel(ux2_config.profile_parcels, service_vpn_parcel, interface_gre.name, "_SERVICE")
    service_ethernet = find_subelement_parcel(
        ux2_config.profile_parcels, service_vpn_parcel, interface_ethernet.name, "_SERVICE"
    )
    service_ipsec = find_subelement_parcel(
        ux2_config.profile_parcels, service_vpn_parcel, interface_ipsec.name, "_SERVICE"
    )
    management_ethernet = find_subelement_parcel(
        ux2_config.profile_parcels, management_vpn_parcel, interface_ethernet.name, "_MANAGEMENT"
    )
    # Assert

    # Assert Feature Profiles have correct VPNs
    assert service_profile is not None
    assert service_profile.header.subelements == {UUID(vpn_1_service.id)}
    assert transport_and_management_profile is not None
    assert transport_and_management_profile.header.subelements == {
        UUID(vpn_0_transport.id),
        UUID(vpn_512_management.id),
    }

    # Assert VPNs have correct interfaces
    assert transport_gre is not None
    assert transport_ethernet is not None
    assert service_gre is not None
    assert service_ethernet is not None
    assert service_ipsec is not None
    assert management_ethernet is not None


def test_when_one_feature_template_with_invalid_payload_expect_one_failed_item_in_conversion_result():
    # Arrange
    vpn_0_transport, malformed_logging = deepcopy_models(vpn_transport, malformed)
    malformed_logging.template_type = "cisco_logging"
    malformed_logging.name = "Malformed"

    ux1_config = UX1Config(
        templates=UX1Templates(
            feature_templates=[malformed_logging, vpn_0_transport],
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
                            name=malformed_logging.name,
                            templateId=str(malformed_logging.id),
                            templateType=malformed_logging.template_type,
                            subTemplates=[],
                        ),
                        GeneralTemplate(
                            name=vpn_0_transport.name,
                            templateId=str(vpn_0_transport.id),
                            templateType=vpn_0_transport.template_type,
                            subTemplates=[],
                        ),
                    ],
                )
            ],
        )
    )
    # Act
    transform_result = transform(ux1_config, add_suffix=False)
    # Assert
    assert len(transform_result.failed_items) == 1
    assert transform_result.failed_items[0].feature_template == malformed_logging
    assert len(transform_result.ux2_config.profile_parcels) == 1
