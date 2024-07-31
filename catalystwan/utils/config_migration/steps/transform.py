# Copyright 2024 Cisco Systems, Inc. and its affiliates
import json
import logging
from typing import Dict, List, Optional, Set, Tuple, cast
from uuid import UUID, uuid4

from catalystwan.api.templates.device_template.device_template import GeneralTemplate
from catalystwan.models.configuration.config_migration import (
    ConfigTransformResult,
    ConvertResult,
    DeviceTemplateWithInfo,
    TransformedParcel,
    TransformedPolicyGroup,
    TransformHeader,
    UX1Config,
    UX2Config,
)
from catalystwan.models.configuration.feature_profile.sdwan.service.multicast import (
    MulticastBasicAttributes,
    MulticastParcel,
)
from catalystwan.models.configuration.policy_group import PolicyGroup
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


def get_vpn_id_or_none(template: FeatureTemplateInformation) -> Optional[int]:
    """Applies only to cisco_vpn template type. Get VPN Id safely from the template definition."""
    if template.template_definition is None:
        return None
    definition = json.loads(template.template_definition)
    return definition.get("vpn-id", {}).get("vipValue")


def resolve_vpn_and_subtemplates_type(cisco_vpn_template: GeneralTemplate, ux1_config: UX1Config) -> Set[str]:
    """
    Resolve Cisco VPN template type and its sub-elements.
    """

    # Find the target feature template based on the provided template ID
    target_feature_template = next(
        (t for t in ux1_config.templates.feature_templates if t.id == cisco_vpn_template.template_id), None
    )

    if not target_feature_template:
        logger.error(f"Cisco VPN template {cisco_vpn_template.template_id} not found in Feature Templates list.")
        logger.error(
            "All items depended on this template will NOT be converted:"
            f"{[sub.template_id for sub in cisco_vpn_template.sub_templates]}"
        )
        return set()

    # Determine the VPN type based on the VPN ID
    vpn_id = get_vpn_id_or_none(target_feature_template)
    if vpn_id is None:
        logger.error(f"VPN ID not found in Cisco VPN template {target_feature_template.name}.")
        logger.error(
            "All items depended on this template will NOT be converted:"
            f"{[sub.template_id for sub in cisco_vpn_template.sub_templates]}"
        )
        return set()

    if vpn_id == 0:
        cisco_vpn_template.template_type = VPN_TRANSPORT
    elif vpn_id == 512:
        cisco_vpn_template.template_type = VPN_MANAGEMENT
    else:
        cisco_vpn_template.template_type = VPN_SERVICE

    new_vpn_id = str(uuid4())
    new_vpn_name = f"{target_feature_template.name}_{new_vpn_id[:5]}"
    vpn = target_feature_template.model_copy(deep=True)
    vpn.id = new_vpn_id
    vpn.name = new_vpn_name

    ux1_config.templates.feature_templates.append(vpn)
    cisco_vpn_template.template_id = new_vpn_id
    cisco_vpn_template.name = new_vpn_name

    used_feature_templates = {vpn.id}

    logger.debug(
        f"Resolved Cisco VPN {target_feature_template.name} "
        f"template to type {cisco_vpn_template.template_type } and changed name to new name {new_vpn_name}"
    )

    # Get templates that need casting
    general_templates_from_device_template = [
        t for t in cisco_vpn_template.sub_templates if t.template_type in VPN_ADDITIONAL_TEMPLATES
    ]

    if len(general_templates_from_device_template) == 0:
        # No additional templates on VPN, nothing to cast
        return used_feature_templates

    feature_and_general_templates = create_feature_template_and_general_template_pairs(
        general_templates_from_device_template, ux1_config.templates.feature_templates
    )

    for ft, gt in feature_and_general_templates:
        new_id = str(uuid4())
        new_name = f"{ft.name}_{new_id[:5]}{VPN_TEMPLATE_MAPPINGS[cisco_vpn_template.template_type ]['suffix']}"
        new_type = VPN_TEMPLATE_MAPPINGS[cisco_vpn_template.template_type]["mapping"][ft.template_type]  # type: ignore

        if NO_SUBSTITUTE_ERROR in new_type:
            cisco_vpn_template.sub_templates.remove(gt)
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

        gt.template_id = new_id
        gt.template_type = new_type
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
        feature_template = next((ft for ft in feature_templates if ft.id == gt.template_id), None)

        if not feature_template:
            logger.error(f"Feature template with UUID [{gt.template_id}] not found in Feature Templates list.")
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


class PolicyGroupMetadata:
    def __init__(self, transformed_policy_group: TransformedPolicyGroup, policy_group_subelements: Set[UUID]):
        self.transformed_policy_group = transformed_policy_group
        self.policy_group_subelements = frozenset(policy_group_subelements)


class PolicyGroupMetadataCreator:
    def __init__(self, ux1: UX1Config):
        self.ux1 = ux1
        self.policies: List[PolicyGroupMetadata] = list()

    def get_policies_metadata(self) -> List[PolicyGroupMetadata]:
        return self.policies

    def create(self, dt: DeviceTemplateWithInfo) -> PolicyGroupMetadata:
        policy_elements_uuids = self._get_policy_elements(dt.get_policy_uuid())
        security_elements_uuids = self._get_security_elements(dt.get_security_policy_uuid())
        sig_uuid = dt.get_sig_template_uuid()
        sig_uuid_set = set([sig_uuid]) if sig_uuid else set()
        policy_group_subelements = set().union(policy_elements_uuids, security_elements_uuids, sig_uuid_set)
        transformed_policy_group = TransformedPolicyGroup(
            header=TransformHeader(
                type="policy_group",
                origin=UUID(dt.template_id),
                origname=dt.template_name,
                subelements=policy_group_subelements,
                info=[f"Policy Group created from Device Template. Included elements: {policy_group_subelements}"],
            ),
            policy_group=PolicyGroup(
                name=dt.template_name,
                description="",  # Place for information about merged policy group
                profiles=[],
                solution="sdwan",
            ),
        )
        return PolicyGroupMetadata(transformed_policy_group, policy_group_subelements)

    def create_and_store(self, dt: DeviceTemplateWithInfo) -> None:
        self.policies.append(self.create(dt))

    def _get_policy_elements(self, policy_uuid: Optional[UUID]) -> Set[UUID]:
        """Localized policy creates application-priority profile"""
        if not policy_uuid:
            return set()

        policy_c = self.ux1.policies.get_centralized_policy_by_id(policy_uuid)
        # policy_l = self.ux1.policies.get_localized_policy_by_id(policy_uuid)
        if policy_c:
            return set()
        return {policy_uuid}

    def _get_security_elements(self, security_uuid: Optional[UUID]) -> Set[UUID]:
        if not security_uuid:
            return set()

        security = self.ux1.policies.get_security_policy_by_id(security_uuid)
        if not security:
            return set()

        # Return self and dns security policy
        # SecurityPolicy converts to PolicyParcel and creates feature profile
        # DNSSecurity converts to DNSParcel and creates feature profile
        dns_uuid = next((a for a in security.policy_definition.assembly if a.type == "DNSSecurity"), None)
        if dns_uuid is None:
            return set([security_uuid])
        return set([security_uuid, dns_uuid.definition_id])


class PolicyGroupMetadataMerger:
    def __init__(self, policies_metadata: List[PolicyGroupMetadata]):
        self.policy_groups = policies_metadata
        self.policy_map: Dict[Set[UUID], PolicyGroupMetadata] = dict()

    def remove_policies_with_no_subelements(self):
        """The policy groups with no subelements, no need to create empty groups."""
        self.policy_groups = [policy for policy in self.policy_groups if policy.policy_group_subelements]

    def merge_by_subelements(self):
        """Merge Policy Groups with the same subelements into one."""
        for policy in self.policy_groups:
            if policy.policy_group_subelements in self.policy_map:
                existing = self.policy_map[policy.policy_group_subelements]
                existing.transformed_policy_group.policy_group.description += (
                    f" {policy.transformed_policy_group.policy_group.name}"
                )
            else:
                self.policy_map[policy.policy_group_subelements] = policy

    def get_merged_transformed_policy_groups(self) -> List[TransformedPolicyGroup]:
        return [policy.transformed_policy_group for policy in self.policy_map.values()]
