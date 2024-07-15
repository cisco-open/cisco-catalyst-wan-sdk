# Copyright 2024 Cisco Systems, Inc. and its affiliates
# Copyright 2023 Cisco Systems, Inc. and its affiliates
import logging
from collections import defaultdict
from typing import Callable, Optional, Set, TypeVar, cast
from uuid import UUID, uuid4

from pydantic import ValidationError

from catalystwan import PACKAGE_VERSION
from catalystwan.api.policy_api import POLICY_LIST_ENDPOINTS_MAP
from catalystwan.endpoints.configuration_group import ConfigGroupCreationPayload
from catalystwan.models.configuration.config_migration import (
    ConfigTransformResult,
    DeviceTemplateWithInfo,
    PolicyConvertContext,
    TransformedConfigGroup,
    TransformedFeatureProfile,
    TransformedParcel,
    TransformedTopologyGroup,
    TransformHeader,
    UX1Config,
    UX2Config,
    UX2RollbackInfo,
    VersionInfo,
)
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy import AnyPolicyDefinitionInfo
from catalystwan.session import ManagerSession
from catalystwan.utils.config_migration.converters.feature_template.cloud_credentials import (
    create_cloud_credentials_from_templates,
)
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert as convert_policy_definition
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert as convert_policy_list
from catalystwan.utils.config_migration.converters.policy.security_policy import convert_security_policy
from catalystwan.utils.config_migration.creators.config_pusher import UX2ConfigPusher, UX2ConfigPushResult
from catalystwan.utils.config_migration.reverters.config_reverter import UX2ConfigReverter
from catalystwan.utils.config_migration.steps.constants import (
    LAN_BGP,
    LAN_OSPF,
    LAN_OSPFV3,
    LAN_VPN_ETHERNET,
    LAN_VPN_GRE,
    LAN_VPN_IPSEC,
    LAN_VPN_MULTILINK,
    MANAGEMENT_VPN_ETHERNET,
    MULTI_PARCEL_FEATURE_TEMPLATES,
    VPN_MANAGEMENT,
    VPN_SERVICE,
    VPN_TRANSPORT,
    WAN_BGP,
    WAN_OSPF,
    WAN_OSPFV3,
    WAN_VPN_ETHERNET,
    WAN_VPN_GRE,
    WAN_VPN_MULTILINK,
)
from catalystwan.utils.config_migration.steps.transform import (
    convert_multi_parcel_feature_template,
    convert_single_parcel_feature_template,
    merge_parcels,
    remove_unused_feature_templates,
    resolve_vpn_and_subtemplates_type,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")

SUPPORTED_TEMPLATE_TYPES = [
    "cisco_aaa",
    "cedge_aaa",
    "aaa",
    "cisco_banner",
    "cisco_security",
    "security",
    "security-vsmart",
    "security-vedge",
    "cisco_system",
    "system-vsmart",
    "system-vedge",
    "cisco_bfd",
    "bfd-vedge",
    "cedge_global",
    "cisco_logging",
    "logging",
    "cisco_omp",
    "omp-vedge",
    "omp-vsmart",
    "cisco_ntp",
    "ntp",
    "bgp",
    "cisco_bgp",
    "cisco_thousandeyes",
    "ucse",
    "dhcp",
    "cisco_dhcp_server",
    "cisco_vpn",
    "vpn-vedge",
    "cisco_ospf",
    "switchport",
    "cisco_wireless_lan",
    "cisco_multicast",
    "cisco_pim",
    "cisco_igmp",
    "cisco_IGMP",
    "igmp",
    "pim",
    "multicast",
    "cedge_igmp",
    "cedge_multicast",
    "cedge_pim",
    "vpn-interface-t1-e1",
    "vpn-interface-ethpppoe",
    "vpn-interface-pppoe",
    "vpn-interface-pppoa",
    "vpn-interface-ipoe",
    WAN_VPN_MULTILINK,
    LAN_VPN_MULTILINK,
    WAN_VPN_GRE,
    WAN_VPN_ETHERNET,
    LAN_VPN_GRE,
    LAN_VPN_ETHERNET,
    LAN_VPN_IPSEC,
    MANAGEMENT_VPN_ETHERNET,
    WAN_BGP,
    LAN_BGP,
    "cli-template",
    "cisco_secure_internet_gateway",
    "cisco_ospfv3",
    "dhcp",
    "cisco_dhcp_server",
    "dhcp-server",
    "cellular-cedge-profile",
    "cellular-cedge-controller",
    "cellular-cedge-gps-controller",
    LAN_OSPF,
    WAN_OSPF,
    LAN_OSPFV3,
    WAN_OSPFV3,
]


CLOUD_CREDENTIALS_FEATURE_TEMPLATES = ["cisco_sig_credentials"]


FEATURE_PROFILE_SYSTEM = [
    "cisco_aaa",
    "cedge_aaa",
    "aaa",
    "cisco_banner",
    "cisco_security",
    "security",
    "security-vsmart",
    "security-vedge",
    "cisco_system",
    "system-vsmart",
    "system-vedge",
    "cisco_bfd",
    "bfd-vedge",
    "cedge_global",
    "cisco_logging",
    "logging",
    "cisco_omp",
    "omp-vedge",
    "omp-vsmart",
    "cisco_ntp",
    "ntp",
    "cisco_snmp",
]

FEATURE_PROFILE_TRANSPORT = [
    "dhcp",
    "cisco_dhcp_server",
    "dhcp-server",
    "vpn-interface-t1-e1",
    "vpn-interface-ethpppoe",
    "vpn-interface-pppoe",
    "vpn-interface-pppoa",
    "vpn-interface-ipoe",
    VPN_TRANSPORT,
    VPN_MANAGEMENT,
    WAN_BGP,
    "cisco_ospfv3",
    "cellular-cedge-profile",
    "cellular-cedge-controller",
    "cellular-cedge-gps-controller",
]

FEATURE_PROFILE_OTHER = [
    "cisco_thousandeyes",
    "ucse",
]

FEATURE_PROFILE_SERVICE = [
    "cisco_ospf",
    "switchport",
    "cisco_wireless_lan",
    "cisco_multicast",
    "cisco_pim",
    "cisco_igmp",
    "cisco_IGMP",
    "igmp",
    "pim",
    "multicast",
    "cedge_igmp",
    "cedge_multicast",
    "cedge_pim",
    VPN_SERVICE,
    LAN_BGP,
]

FEATURE_PROFILE_CLI = [
    "cli-template",
]

DEVICE_TYPE_BLOCKLIST = ["vsmart", "vbond", "vmanage"]

VPN_TEMPLATE_TYPES = [
    "cisco_vpn",
    "vpn-vedge",
]

TOPOLOGY_POLICIES = ["control", "hubAndSpoke", "mesh"]


def log_progress(task: str, completed: int, total: int) -> None:
    logger.info(f"{task} {completed}/{total}")


def get_version_info(session: ManagerSession) -> VersionInfo:
    return VersionInfo(platform=session._platform_version, sdk=PACKAGE_VERSION)


def transform(ux1: UX1Config, add_suffix: bool = False) -> ConfigTransformResult:
    transform_result = ConfigTransformResult()
    ux2 = UX2Config(version=ux1.version)
    subtemplates_mapping = defaultdict(set)
    used_feature_templates: Set[str] = set()
    # Create Feature Profiles and Config Group
    for dt in ux1.templates.device_templates:
        templates = dt.get_flattened_general_templates()
        # Create Feature Profiles
        fp_system_uuid = uuid4()
        transformed_fp_system = TransformedFeatureProfile(
            header=TransformHeader(
                type="system",
                origin=fp_system_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_system",
                description="system",
            ),
        )
        fp_other_uuid = uuid4()
        transformed_fp_other = TransformedFeatureProfile(
            header=TransformHeader(
                type="other",
                origin=fp_other_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_other",
                description="other",
            ),
        )
        fp_service_uuid = uuid4()
        transformed_fp_service = TransformedFeatureProfile(
            header=TransformHeader(
                type="service",
                origin=fp_service_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_service",
                description="service",
            ),
        )
        fp_transport_and_management_uuid = uuid4()
        transformed_fp_transport_and_management = TransformedFeatureProfile(
            header=TransformHeader(
                type="transport",
                origin=fp_transport_and_management_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_transport_and_management",
                description="transport_and_management",
            ),
        )
        fp_cli_uuid = uuid4()
        transformed_fp_cli = TransformedFeatureProfile(
            header=TransformHeader(
                type="cli",
                origin=fp_cli_uuid,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=f"{dt.template_name}_cli",
                description="cli",
            ),
        )

        for template in templates:
            # Those feature templates IDs are real UUIDs and are used to map to the feature profiles
            if template.templateType in VPN_TEMPLATE_TYPES:
                copied_feature_templates = resolve_vpn_and_subtemplates_type(template, ux1)
                used_feature_templates.update(copied_feature_templates)
            else:
                used_feature_templates.add(template.templateId)
            template_uuid = UUID(template.templateId)
            if template.templateType in FEATURE_PROFILE_SYSTEM:
                transformed_fp_system.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_OTHER:
                transformed_fp_other.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_SERVICE:
                transformed_fp_service.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_TRANSPORT:
                transformed_fp_transport_and_management.header.subelements.add(template_uuid)
            elif template.templateType in FEATURE_PROFILE_CLI:
                transformed_fp_cli.header.subelements.add(template_uuid)
            # Map subtemplates
            if len(template.subTemplates) > 0:
                # Interfaces, BGP, OSPF, etc
                for subtemplate_level_1 in template.subTemplates:
                    used_feature_templates.add(subtemplate_level_1.templateId)
                    subtemplates_mapping[template_uuid].add(UUID(subtemplate_level_1.templateId))
                    if len(subtemplate_level_1.subTemplates) > 0:
                        # DHCPs, Trackers
                        for subtemplate_level_2 in subtemplate_level_1.subTemplates:
                            used_feature_templates.add(subtemplate_level_2.templateId)
                            subtemplates_mapping[UUID(subtemplate_level_1.templateId)].add(
                                UUID(subtemplate_level_2.templateId)
                            )
        policy_id = dt.get_policy_uuid()
        transformed_cg = TransformedConfigGroup(
            header=TransformHeader(
                type="config_group",
                origin=UUID(dt.template_id),
                subelements=set(
                    [fp_system_uuid, fp_other_uuid, fp_service_uuid, fp_transport_and_management_uuid, fp_cli_uuid]
                ),
                localized_policy_subelements=set([policy_id]) if policy_id else None,
            ),
            config_group=ConfigGroupCreationPayload(
                name=dt.template_name,
                description=dt.template_description,
                solution="sdwan",
                profiles=[],
            ),
        )
        # Add to UX2
        ux2.feature_profiles.append(transformed_fp_system)
        ux2.feature_profiles.append(transformed_fp_other)
        ux2.feature_profiles.append(transformed_fp_service)
        ux2.feature_profiles.append(transformed_fp_transport_and_management)
        ux2.feature_profiles.append(transformed_fp_cli)
        ux2.config_groups.append(transformed_cg)

    # Sort by vpn feature templates to avoid any confilics with subtemplates
    ux1.templates.feature_templates.sort(key=lambda ft: ft.template_type in VPN_TEMPLATE_TYPES, reverse=True)
    remove_unused_feature_templates(ux1, used_feature_templates)

    cloud_credential_templates = []
    for ft in ux1.templates.feature_templates:
        if ft.template_type in CLOUD_CREDENTIALS_FEATURE_TEMPLATES:
            cloud_credential_templates.append(ft)
        elif ft.template_type in MULTI_PARCEL_FEATURE_TEMPLATES:
            convert_multi_parcel_feature_template(ux2, transform_result, ft, subtemplates_mapping)
        else:
            convert_single_parcel_feature_template(ux2, transform_result, ft, subtemplates_mapping)

    # Add Cloud Credentials to UX2
    if cloud_credential_templates:
        ux2.cloud_credentials = create_cloud_credentials_from_templates(cloud_credential_templates)

    # Prepare Context for Policy Conversion (VPN Parcels must be already transformed)
    policy_context = PolicyConvertContext.from_configs(ux1.network_hierarchy, ux2.profile_parcels)

    # Policy Lists
    for policy_list in ux1.policies.policy_lists:
        pl_result = convert_policy_list(policy_list, policy_context)
        pl_parcel = pl_result.output
        pl_status = pl_result.status
        if pl_status == "unsupported":
            transform_result.add_unsupported_item(
                name=policy_list.name, uuid=policy_list.list_id, type=policy_list.type
            )
        elif pl_status == "failed":
            transform_result.add_failed_conversion_parcel(
                exception_message="\n".join(pl_result.info),
                policy=policy_list,
            )
        elif pl_parcel is not None:
            header = TransformHeader(
                type=pl_parcel._get_parcel_type(),
                origin=policy_list.list_id,
                origname=policy_list.name,
                status=pl_status,
                info=pl_result.info,
            )
            ux2.profile_parcels.append(TransformedParcel(header=header, parcel=pl_parcel))

    # Policy Definitions
    for policy_definition in ux1.policies.policy_definitions:
        pd_result = convert_policy_definition(policy_definition, policy_definition.definition_id, policy_context)
        pd_parcel = pd_result.output
        pd_status = pd_result.status
        if pd_status == "unsupported":
            transform_result.add_unsupported_item(
                name=policy_definition.name, uuid=policy_definition.definition_id, type=policy_definition.type
            )
        elif pd_status == "failed":
            transform_result.add_failed_conversion_parcel(
                exception_message="\n".join(pd_result.info),
                policy=policy_definition,
            )
        elif pd_parcel is not None:
            header = TransformHeader(
                type=pd_parcel._get_parcel_type(),
                origin=policy_definition.definition_id,
                origname=policy_definition.name,
                status=pd_status,
                info=pd_result.info,
            )
            ux2.profile_parcels.append(TransformedParcel(header=header, parcel=pd_parcel))

    # Localized Policies
    _lookup = ux1.templates.create_device_template_by_policy_id_lookup()
    dt_by_policy_id = _lookup["policy"]
    for localized_policy in ux1.policies.localized_policies:
        if not isinstance(localized_policy.policy_definition, str):
            if dt_id := dt_by_policy_id.get(localized_policy.policy_id):
                for item in localized_policy.policy_definition.assembly:
                    if item.type == "deviceaccesspolicy" or item.type == "deviceaccesspolicyv6":
                        ux2.add_subelement_in_config_group(
                            profile_types=["system"], device_template_id=dt_id, subelement=item.definition_id
                        )
                    elif item.type == "acl" or item.type == "aclv6":
                        ux2.add_subelement_in_config_group(
                            profile_types=["transport", "service"],
                            device_template_id=dt_id,
                            subelement=item.definition_id,
                        )
                    elif item.type == "vedgeRoute":
                        ux2.add_subelement_in_config_group(
                            profile_types=["transport", "service"],
                            device_template_id=dt_id,
                            subelement=item.definition_id,
                        )

    # Security policies
    for security_policy in ux1.policies.security_policies:
        sp_result = convert_security_policy(security_policy, security_policy.policy_id, policy_context)
        sp_parcel = sp_result.output
        sp_status = sp_result.status

        if sp_status == "unsupported":  # move to common
            transform_result.add_unsupported_item(
                name=security_policy.policy_name, uuid=security_policy.policy_id, type=security_policy.policy_type
            )
        elif sp_status == "failed":
            transform_result.add_failed_conversion_parcel(
                exception_message="\n".join(sp_result.info),
                policy=security_policy,
            )
        elif sp_parcel is not None:
            header = TransformHeader(
                type=sp_parcel._get_parcel_type(),
                origin=security_policy.policy_id,
                origname=security_policy.policy_name,
                status=sp_status,
                info=sp_result.info,
            )
            ux2.profile_parcels.append(TransformedParcel(header=header, parcel=sp_parcel))

    # Topology Group and Profile
    topology_sources = [p.definition_id for p in ux1.policies.policy_definitions if p.type in TOPOLOGY_POLICIES]
    topology_name = "Migrated-from-policy-config"
    topology_description = "Created by config migration tool"
    ux2.feature_profiles.append(
        TransformedFeatureProfile(
            header=TransformHeader(
                type="topology",
                origin=UUID(int=0),
                subelements=set(topology_sources),
                origname=topology_name,
            ),
            feature_profile=FeatureProfileCreationPayload(
                name=topology_name,
                description=topology_description,
            ),
        )
    )
    ux2.topology_groups.append(
        TransformedTopologyGroup(
            header=TransformHeader(type="", origin=UUID(int=0), origname=topology_name, subelements=set()),
            topology_group=TopologyGroup(name=topology_name, description=topology_description, solution="sdwan"),
        )
    )

    ux2 = merge_parcels(ux2)
    transform_result.ux2_config = ux2
    if add_suffix:
        transform_result.add_suffix_to_names()
    transform_result.resolve_conflicts_on_policy_object_parcel_names(add_suffix)
    transform_result.ux2_config = UX2Config.model_validate(transform_result.ux2_config)
    return transform_result


def collect_ux1_config(session: ManagerSession, progress: Callable[[str, int, int], None] = log_progress) -> UX1Config:
    ux1 = UX1Config(version=get_version_info(session))

    """Get Network Hierarchy"""
    ux1.network_hierarchy = session.endpoints.network_hierarchy.list_nodes().data

    """Collect Policies"""
    policy_api = session.api.policy

    def guard(func: Callable[..., T], *args, **kwargs) -> Optional[T]:
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            logger.warning(f"{args} {kwargs}\n{e}")
        return None

    progress("Collecting Policy Info", 0, 1)
    policy_definition_types_and_ids = [
        (policy_type, info.definition_id) for policy_type, info in policy_api.definitions.get_all()
    ]
    progress("Collecting Policy Info", 1, 1)

    policy_list_types = POLICY_LIST_ENDPOINTS_MAP.keys()
    for i, policy_list_type in enumerate(policy_list_types):
        if policy_list := guard(policy_api.lists.get, policy_list_type):
            ux1.policies.policy_lists.extend(policy_list)
        progress("Collecting Policy Lists", i + 1, len(policy_list_types))

    for i, type_and_id in enumerate(policy_definition_types_and_ids):
        if _policy_definition := guard(policy_api.definitions.get, *type_and_id):
            # type checker cannot infer correct signature not knowing arguments (it is overloaded method)
            policy_definition = cast(AnyPolicyDefinitionInfo, _policy_definition)
            ux1.policies.policy_definitions.append(policy_definition)
        progress("Collecting Policy Definitions", i + 1, len(policy_definition_types_and_ids))

    progress("Collecting Centralized Policies", 0, 1)
    ux1.policies.centralized_policies = policy_api.centralized.get().data
    progress("Collecting Centralized Policies", 1, 1)

    progress("Collecting Localized Policies", 0, 1)
    ux1.policies.localized_policies = policy_api.localized.get().data
    progress("Collecting Localized Policies", 1, 1)

    progress("Collecting Security Policies", 0, 1)
    ux1.policies.security_policies = policy_api.security.get().root
    progress("Collecting Security Policies", 1, 1)

    """Collect Templates"""
    template_api = session.api.templates

    progress("Collecting Feature Templates", 0, 1)
    ux1.templates.feature_templates = [t for t in template_api.get_feature_templates()]
    progress("Collecting Feature Templates", 1, 1)

    device_templates_information = template_api.get_device_templates()
    for i, device_template_information in enumerate(device_templates_information):
        device_template = template_api.get_device_template(device_template_information.id)
        device_template_with_info = DeviceTemplateWithInfo.from_merged(device_template, device_template_information)
        if device_template_with_info.device_type not in DEVICE_TYPE_BLOCKLIST:
            ux1.templates.device_templates.append(device_template_with_info)
        progress("Collecting Device Templates", i + 1, len(device_templates_information))

    return ux1


def push_ux2_config(
    session: ManagerSession, ux2_config: UX2Config, progress: Callable[[str, int, int], None] = log_progress
) -> UX2ConfigPushResult:
    current_versions = get_version_info(session)
    if not ux2_config.version.is_compatible(current_versions):
        logger.warning(
            f"Pushing UX2 config with versions mismatch\nsource: {ux2_config.version}\ntarget: {current_versions}"
        )
    config_pusher = UX2ConfigPusher(session, ux2_config, progress)
    result = config_pusher.push()
    return result


def rollback_ux2_config(
    session: ManagerSession,
    rollback_config: UX2RollbackInfo,
    progress: Callable[[str, int, int], None] = log_progress,
) -> bool:
    config_reverter = UX2ConfigReverter(session)
    status = config_reverter.rollback(rollback_config, progress)
    return status
