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
    ADDITIONAL_TEMPLATES,
    CAST_TEMPLATE_TYPE,
    CISCO_VPN_SERVICE,
    CISCO_VPN_TRANSPORT_AND_MANAGEMENT,
    NEW_TEMPALTE_NAME_SUFFIX,
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
    """Resovle Cisco VPN template type and it's subelements"""
    target_feature_template = next(
        filter(lambda t: t.id == cisco_vpn_template.templateId, ux1_config.templates.feature_templates), None
    )
    if not target_feature_template:
        logger.error(f"Cisco VPN template {cisco_vpn_template.templateId} not found in Feature Templates list.")
        return

    vpn_id = create_parcel_from_template(target_feature_template).vpn_id.value  # type: ignore
    if vpn_id in [0, 512]:
        cisco_vpn_template.templateType = CISCO_VPN_TRANSPORT_AND_MANAGEMENT
    else:
        cisco_vpn_template.templateType = CISCO_VPN_SERVICE
    logger.debug(f"Resolved {target_feature_template.name} template to type {cisco_vpn_template.templateType}")

    if len(cisco_vpn_template.subTemplates) == 0:
        # No additional templates on VPN,
        # nothing to cast
        return

    # Get templates that need casting
    subtemplates = filter(lambda st: st.templateType in ADDITIONAL_TEMPLATES, cisco_vpn_template.subTemplates)
    subtemplates_uuids = [st.templateId for st in subtemplates]
    feature_templates_to_diffrientiate = list(
        filter(lambda t: t.id in subtemplates_uuids, ux1_config.templates.feature_templates)
    )

    if len(feature_templates_to_diffrientiate) == 0:
        return

    for ft in feature_templates_to_diffrientiate:
        new_id = str(uuid4())
        new_name = f"{ft.name}{NEW_TEMPALTE_NAME_SUFFIX[cisco_vpn_template.templateType]}"
        ft_copy = ft.model_copy(deep=True)
        ft_copy.template_type = CAST_TEMPLATE_TYPE[cisco_vpn_template.templateType][ft_copy.template_type]
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
    cisco_vpn_template.subTemplates = list(
        filter(lambda st: st.templateType not in ADDITIONAL_TEMPLATES, cisco_vpn_template.subTemplates)
    )
