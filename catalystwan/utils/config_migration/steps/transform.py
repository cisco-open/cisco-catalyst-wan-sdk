# Copyright 2024 Cisco Systems, Inc. and its affiliates
# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from typing import List, Optional, Set, Tuple, cast
from uuid import UUID, uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import (
    ConfigTransformResult,
    ConvertResult,
    TransformedParcel,
    TransformHeader,
    UX1Config,
    UX2Config,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    MulticastBasicAttributes,
    MulticastParcel,
)
from catalystwan.models.templates import FeatureTemplateInformation
from catalystwan.utils.config_migration.converters.feature_template.ospfv3 import (
    Ospfv3Ipv4Converter,
    Ospfv3Ipv6Converter,
)
from catalystwan.utils.config_migration.converters.feature_template.parcel_factory import (
    convert,
    create_parcel_from_template,
)
from catalystwan.utils.config_migration.steps.constants import (
    LAN_OSPFV3,
    NO_SUBSTITUTE_ERROR,
    VPN_ADDITIONAL_TEMPLATES,
    VPN_MANAGEMENT,
    VPN_SERVICE,
    VPN_TEMPLATE_MAPPINGS,
    VPN_TRANSPORT,
    WAN_OSPFV3,
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


def resolve_vpn_and_subtemplates_type(cisco_vpn_template: GeneralTemplate, ux1_config: UX1Config) -> Set[str]:
    """
    Resolve Cisco VPN template type and its sub-elements.
    """
    used_feature_templates: Set[str] = set()
    # Find the target feature template based on the provided template ID
    target_feature_template = next(
        (t for t in ux1_config.templates.feature_templates if t.id == cisco_vpn_template.templateId), None
    )

    if not target_feature_template:
        logger.error(f"Cisco VPN template {cisco_vpn_template.templateId} not found in Feature Templates list.")
        return set()

    # Determine the VPN type based on the VPN ID
    vpn_id = create_parcel_from_template(target_feature_template).output.vpn_id.value  # type: ignore
    if vpn_id == 0:
        cisco_vpn_template.templateType = VPN_TRANSPORT
    elif vpn_id == 512:
        cisco_vpn_template.templateType = VPN_MANAGEMENT
    else:
        cisco_vpn_template.templateType = VPN_SERVICE

    new_vpn_id = str(uuid4())
    new_vpn_name = f"{target_feature_template.name}_{new_vpn_id[:5]}"
    vpn = target_feature_template.model_copy(deep=True)
    vpn.id = new_vpn_id
    vpn.name = new_vpn_name

    ux1_config.templates.feature_templates.append(vpn)
    cisco_vpn_template.templateId = new_vpn_id
    cisco_vpn_template.name = new_vpn_name

    used_feature_templates.add(vpn.id)

    logger.debug(
        f"Resolved Cisco VPN {target_feature_template.name} "
        f"template to type {cisco_vpn_template.templateType} and changed name to new name {new_vpn_name}"
    )

    # Get templates that need casting
    general_templates_from_device_template = [
        t for t in cisco_vpn_template.subTemplates if t.templateType in VPN_ADDITIONAL_TEMPLATES
    ]

    if len(general_templates_from_device_template) == 0:
        # No additional templates on VPN, nothing to cast
        return used_feature_templates

    feature_and_general_templates = create_feature_template_and_general_template_pairs(
        general_templates_from_device_template, ux1_config.templates.feature_templates
    )

    for ft, gt in feature_and_general_templates:
        new_id = str(uuid4())
        new_name = f"{ft.name}_{new_id[:5]}{VPN_TEMPLATE_MAPPINGS[cisco_vpn_template.templateType]['suffix']}"
        new_type = VPN_TEMPLATE_MAPPINGS[cisco_vpn_template.templateType]["mapping"][ft.template_type]  # type: ignore

        if NO_SUBSTITUTE_ERROR in new_type:
            cisco_vpn_template.subTemplates.remove(gt)
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

        gt.templateId = new_id
        gt.templateType = new_type
        gt.name = new_name

        used_feature_templates.add(new_id)

    return used_feature_templates


def create_feature_template_and_general_template_pairs(
    general_templates: List[GeneralTemplate], feature_templates: List[FeatureTemplateInformation]
) -> List[Tuple[FeatureTemplateInformation, GeneralTemplate]]:
    """Create pairs of Feature Template and General Template based on the provided General Templates list.

    General Templates come from Device Templates and they contain information
    about structure of a configuration and dependencies.

    Feature Templates are list of all available templates with definitions.

    We create a one to one mapping between General Template and Feature Template.
    To then be able to cast the Feature Template to a new type and change it in both places.
    """

    pairs: List[Tuple[FeatureTemplateInformation, GeneralTemplate]] = []
    for gt in general_templates:
        feature_template = next((ft for ft in feature_templates if ft.id == gt.templateId), None)

        if not feature_template:
            logger.error(f"Feature template with UUID [{gt.templateId}] not found in Feature Templates list.")
            continue

        pairs.append((feature_template, gt))
    return pairs


def add_result(
    ux2: UX2Config,
    transform_result: ConfigTransformResult,
    ft: FeatureTemplateInformation,
    result: ConvertResult,
    subtemplates_mapping: dict,
    provided_uuid: Optional[UUID] = None,
):
    ft_template_uuid = UUID(ft.id)
    if result.status == "unsupported":
        transform_result.add_unsupported_item(name=ft.name, uuid=ft_template_uuid, type=ft.template_type)
    elif result.status == "failed":
        transform_result.add_failed_conversion_parcel(
            exception_message=result.get_info(),
            feature_template=ft,
        )
    elif result.output is not None:
        parcel = result.output
        transformed_parcel = TransformedParcel(
            header=TransformHeader(
                type=parcel._get_parcel_type(),
                origin=ft_template_uuid if provided_uuid is None else provided_uuid,
                subelements=subtemplates_mapping[ft_template_uuid],
                status=result.status,
                info=result.info,
            ),
            parcel=parcel,
        )
        ux2.profile_parcels.append(transformed_parcel)


def convert_single_parcel_feature_template(
    ux2: UX2Config, transform_result: ConfigTransformResult, ft: FeatureTemplateInformation, subtemplates_mapping: dict
) -> None:
    result = create_parcel_from_template(ft)
    add_result(ux2, transform_result, ft, result, subtemplates_mapping)


def convert_multi_parcel_feature_template(
    ux2: UX2Config, transform_result: ConfigTransformResult, ft: FeatureTemplateInformation, subtemplates_mapping: dict
) -> None:
    multi_parcel_converters = {(LAN_OSPFV3, WAN_OSPFV3): (Ospfv3Ipv4Converter, Ospfv3Ipv6Converter)}
    converters = None
    for template_types, mulit_converters in multi_parcel_converters.items():
        if ft.template_type in template_types:
            converters = [c() for c in mulit_converters]
    if converters is None:
        transform_result.add_unsupported_item(ft.name, UUID(ft.id), ft.template_type)
        return

    results = [convert(converter, ft) for converter in converters]
    if any(r.status == "failed" for r in results):
        transform_result.add_failed_conversion_parcel(
            exception_message="One or more feature templates failed to convert.\n"
            f"{[r.get_info() for r in results if r.status == 'failed']}",
            feature_template=ft,
        )
        return

    parent_feature_template = next((p for p in ux2.profile_parcels if UUID(ft.id) in p.header.subelements), None)
    if not parent_feature_template:
        transform_result.add_failed_conversion_parcel(
            exception_message=f"Parent parcel for {ft.name} not found.",
            feature_template=ft,
        )
        return

    parent_feature_template.header.subelements.remove(UUID(ft.id))
    for r in results:
        generated_origin = uuid4()
        logger.debug(f"Generated origin for {ft.name} is {generated_origin}")
        add_result(ux2, transform_result, ft, r, subtemplates_mapping, provided_uuid=generated_origin)
        parent_feature_template.header.subelements.add(generated_origin)


def remove_unused_feature_templates(ux1: UX1Config, used_feature_templates: Set[str]):
    """
    Remove duplicates and all unused feature templates from UX1Config.

    This is needed because we are copying and casting routing templates to match the correct
    feature profile, and we need to remove the old ones. Also we want to remove all unused templates.

    Args:
        ux1 (UX1Config): The UX1Config object from which to remove duplicates.
        used_feature_templates (Set[str]): A set of template IDs that are used in UX2.0 migration.
    """
    # Remove routing templates
    routing_template_types = {"cisco_bgp", "bgp", "cisco_ospfv3", "cisco_ospf"}
    ux1.templates.feature_templates = [
        t for t in ux1.templates.feature_templates if t.template_type not in routing_template_types
    ]

    # Remove duplicates based on template IDs
    ux1.templates.feature_templates = [t for t in ux1.templates.feature_templates if t.id in used_feature_templates]
