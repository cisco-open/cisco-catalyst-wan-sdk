# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from typing import List, cast
from uuid import uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import TransformedParcel, TransformHeader, UX1Config, UX2Config
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    MulticastBasicAttributes,
    MulticastParcel,
)
from catalystwan.utils.config_migration.converters.feature_template.parcel_factory import create_parcel_from_template
from catalystwan.utils.config_migration.steps.constants import (
    NO_SUBSTITUTE_ERROR,
    VPN_ADDITIONAL_TEMPLATES,
    VPN_MANAGEMENT,
    VPN_SERVICE,
    VPN_TEMPLATE_MAPPINGS,
    VPN_TRANSPORT,
)

logger = logging.getLogger(__name__)


def _merge_to_multicast(ux2: UX2Config, vpn: TransformedParcel) -> None:
    transformed_sub_parcel_list: List[TransformedParcel] = []
    for sub_parcel_uuid in vpn.header.subelements:
        for parcel in ux2.profile_parcels:
            if parcel.header.origin == sub_parcel_uuid and parcel.header.type == "routing/multicast":
                transformed_sub_parcel_list.append(parcel)

    if len(transformed_sub_parcel_list) <= 1:
        # Nothing to merge
        return

    basic = MulticastBasicAttributes()
    igmp = None
    pim = None

    for transformed_parcel in transformed_sub_parcel_list:
        # Remove the subelements from the VPN
        vpn.header.subelements.remove(transformed_parcel.header.origin)
        mp = cast(MulticastParcel, transformed_parcel.parcel)
        if mp.igmp is None and mp.pim is None:
            # If Multicast parcel has no IGMP or PIM,
            # it was converted from Multicast Feature Template
            basic = mp.basic
        elif mp.igmp is not None:
            igmp = mp.igmp
        elif mp.pim is not None:
            pim = mp.pim

    parcel_description = (
        f"Merged from: {', '.join(sorted([tp.parcel.parcel_name for tp in transformed_sub_parcel_list]))}"
    )
    new_origin_uuid = uuid4()
    transformed_parcel = TransformedParcel(
        header=TransformHeader(
            type="routing/multicast",
            origin=new_origin_uuid,
        ),
        parcel=MulticastParcel(
            parcel_name="Merged_Service_Multicast",
            parcel_description=parcel_description,
            basic=basic,
            igmp=igmp,
            pim=pim,
        ),
    )
    # Add the merged parcel uuid to the VPN
    vpn.header.subelements.add(new_origin_uuid)
    ux2.profile_parcels.append(transformed_parcel)


def merge_parcels(ux2: UX2Config) -> UX2Config:
    """There is inconsitency between Feature Templates and Parcels.
    There is many to one relation occuring.

    For now this function covers Feature Template merges:
    -  Multicast, PIM, IGMP -> Parcel Multicast (Subelements of VPN Service parcel)
    """

    vpns = [
        parcel
        for parcel in ux2.profile_parcels
        if parcel.header.type == "lan/vpn" and len(parcel.header.subelements) > 0
    ]
    for vpn in vpns:
        _merge_to_multicast(ux2, vpn)
    return ux2


def resolve_template_type(cisco_vpn_template: GeneralTemplate, ux1_config: UX1Config):
    """
    Resolve Cisco VPN template type and its sub-elements.
    """
    # Find the target feature template based on the provided template ID
    target_feature_template = next(
        (t for t in ux1_config.templates.feature_templates if t.id == cisco_vpn_template.templateId), None
    )

    if not target_feature_template:
        logger.error(f"Cisco VPN template {cisco_vpn_template.templateId} not found in Feature Templates list.")
        return

    # Determine the VPN type based on the VPN ID
    vpn_id = create_parcel_from_template(target_feature_template).vpn_id.value  # type: ignore
    if vpn_id == 0:
        cisco_vpn_template.templateType = VPN_TRANSPORT
    elif vpn_id == 512:
        cisco_vpn_template.templateType = VPN_MANAGEMENT
    else:
        cisco_vpn_template.templateType = VPN_SERVICE

    logger.debug(
        f"Resolved Cisco VPN {target_feature_template.name} template to type {cisco_vpn_template.templateType}"
    )

    if not cisco_vpn_template.subTemplates:
        # No additional templates on VPN, nothing to cast
        return

    # Get templates that need casting
    subtemplates_uuids = [
        st.templateId for st in cisco_vpn_template.subTemplates if st.templateType in VPN_ADDITIONAL_TEMPLATES
    ]
    feature_templates_to_differentiate = [
        t for t in ux1_config.templates.feature_templates if t.id in subtemplates_uuids
    ]

    if not feature_templates_to_differentiate:
        # No additional templates that can be casted
        return

    for ft in feature_templates_to_differentiate:
        new_id = str(uuid4())
        new_name = f"{ft.name}{VPN_TEMPLATE_MAPPINGS[cisco_vpn_template.templateType]['suffix']}"
        new_type = VPN_TEMPLATE_MAPPINGS[cisco_vpn_template.templateType]["mapping"][ft.template_type]  # type: ignore

        if NO_SUBSTITUTE_ERROR in new_type:
            logger.error(new_type)
            continue

        logger.debug(
            f"Copied feature template and casted type from: {ft.name}[{ft.template_type}] to {new_name}[{new_type}]"
        )

        ft_copy = ft.model_copy(deep=True)
        ft_copy.template_type = new_type
        ft_copy.id = new_id
        ft_copy.name = new_name

        ux1_config.templates.feature_templates.append(ft_copy)
        cisco_vpn_template.subTemplates.append(
            GeneralTemplate(
                templateId=new_id,
                templateType=ft_copy.template_type,
                name=new_name,
                subTemplates=[],
            )
        )

    # Remove old GeneralTemplates
    cisco_vpn_template.subTemplates = [
        st for st in cisco_vpn_template.subTemplates if st.templateType not in VPN_ADDITIONAL_TEMPLATES
    ]
