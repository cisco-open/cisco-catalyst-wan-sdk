# Copyright 2024 Cisco Systems, Inc. and its affiliates

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, TypeVar, Union, cast
from uuid import UUID, uuid4

from packaging.version import Version
from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan import PACKAGE_VERSION
from catalystwan.api.builders.feature_profiles.report import (
    FailedParcel,
    FailedRequestDetails,
    FeatureProfileBuildReport,
)
from catalystwan.api.templates.device_template.device_template import DeviceTemplate, GeneralTemplate
from catalystwan.endpoints.configuration_group import ConfigGroupCreationPayload
from catalystwan.endpoints.configuration_settings import CloudCredentials
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.network_hierarchy import NodeInfo
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy import AnyPolicyDefinitionInfo, AnyPolicyListInfo
from catalystwan.models.policy.centralized import CentralizedPolicyInfo
from catalystwan.models.policy.localized import LocalizedPolicyInfo
from catalystwan.models.policy.security import AnySecurityPolicyInfo
from catalystwan.models.templates import FeatureTemplateInformation, TemplateInformation
from catalystwan.version import parse_api_version

T = TypeVar("T", bound=AnyParcel)


class VersionInfo(BaseModel):
    platform: str = "unknown"
    sdk: str = PACKAGE_VERSION

    @property
    def platform_api(self) -> Version:
        return parse_api_version(self.platform)

    def is_compatible(self, other: "VersionInfo"):
        return True if (self.sdk == other.sdk and self.platform_api == other.platform_api) else False


class DeviceTemplateWithInfo(DeviceTemplate):
    model_config = ConfigDict(populate_by_name=True)
    template_id: str = Field(serialization_alias="templateId", validation_alias="templateId")
    factory_default: bool = Field(serialization_alias="factoryDefault", validation_alias="factoryDefault")
    devices_attached: int = Field(serialization_alias="devicesAttached", validation_alias="devicesAttached")

    @staticmethod
    def from_merged(template: DeviceTemplate, info: TemplateInformation) -> "DeviceTemplateWithInfo":
        info_dict = template.model_dump()
        return DeviceTemplateWithInfo(
            template_id=info.id,
            factory_default=info.factory_default,
            devices_attached=info.devices_attached,
            **info_dict,
        )

    def get_flattened_general_templates(self) -> List[GeneralTemplate]:
        """
        Flatten the representation but leave cisco vpn templates and
        cellular cedge controller as they are, because they have subtemplates
        that need to have the same parent template in UX2.0. For example cisco_system
        also have subtemplates but they have flat structure in UX2.0.

        Returns:
            A list of GeneralTemplate objects representing the flattened templates list.
        """
        result = []
        for template in self.general_templates:
            subtemplates = template.subTemplates
            if subtemplates and template.templateType not in ["cisco_vpn", "cellular-cedge-controller"]:
                template.subTemplates = []
                for subtemplate in subtemplates:
                    result.append(subtemplate)
            result.append(template)

        return result


class UX1Policies(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    centralized_policies: List[CentralizedPolicyInfo] = Field(
        default=[],
        serialization_alias="centralizedPolicies",
        validation_alias="centralizedPolicies",
    )
    localized_policies: List[LocalizedPolicyInfo] = Field(
        default=[],
        serialization_alias="localizedPolicies",
        validation_alias="localizedPolicies",
    )
    security_policies: List[AnySecurityPolicyInfo] = Field(
        default=[],
        serialization_alias="securityPolicies",
        validation_alias="securityPolicies",
    )
    policy_definitions: List[AnyPolicyDefinitionInfo] = Field(
        default=[],
        serialization_alias="policyDefinitions",
        validation_alias="policyDefinitions",
    )
    policy_lists: List[AnyPolicyListInfo] = Field(
        default=[], serialization_alias="policyLists", validation_alias="policyLists"
    )


class UX1Templates(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    feature_templates: List[FeatureTemplateInformation] = Field(
        default=[],
        serialization_alias="featureTemplates",
        validation_alias="featureTemplates",
    )
    device_templates: List[DeviceTemplateWithInfo] = Field(
        default=[],
        serialization_alias="deviceTemplates",
        validation_alias="deviceTemplates",
    )


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True)
    version: VersionInfo = VersionInfo()
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()
    network_hierarchy: List[NodeInfo] = Field(
        default_factory=list, validation_alias="networkHierarchy", serialization_alias="networkHierarchy"
    )


class TransformHeader(BaseModel):
    type: str = Field(
        description="Needed to push item to specific endpoint."
        "Type discriminator is not present in many UX2 item payloads"
    )
    origin: UUID = Field(description="Original UUID of converted item")
    origname: Optional[str] = None
    subelements: Set[UUID] = Field(default_factory=set)


class TransformedTopologyGroup(BaseModel):
    header: TransformHeader
    topology_group: TopologyGroup


class TransformedConfigGroup(BaseModel):
    header: TransformHeader
    config_group: ConfigGroupCreationPayload


class TransformedFeatureProfile(BaseModel):
    header: TransformHeader
    feature_profile: FeatureProfileCreationPayload


class TransformedParcel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    header: TransformHeader
    parcel: AnyParcel


class FailedConversionItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    feature_template: Optional[FeatureTemplateInformation] = Field(
        default=None, serialization_alias="featureTemplate", validation_alias="featureTemplate"
    )
    policy: Optional[
        Union[
            CentralizedPolicyInfo,
            LocalizedPolicyInfo,
            AnySecurityPolicyInfo,
            AnyPolicyDefinitionInfo,
            AnyPolicyListInfo,
        ]
    ] = Field(default=None)
    exception_message: str = Field(serialization_alias="exceptionMessage", validation_alias="exceptionMessage")


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    version: VersionInfo = VersionInfo()
    topology_groups: List[TransformedTopologyGroup] = Field(
        default=[],
        serialization_alias="topologyGroups",
        validation_alias="topologyGroups",
    )
    config_groups: List[TransformedConfigGroup] = Field(
        default=[],
        serialization_alias="configurationGroups",
        validation_alias="configurationGroups",
    )
    policy_groups: List[TransformedConfigGroup] = Field(
        default=[], serialization_alias="policyGroups", validation_alias="policyGroups"
    )
    feature_profiles: List[TransformedFeatureProfile] = Field(
        default=[],
        serialization_alias="featureProfiles",
        validation_alias="featureProfiles",
    )
    profile_parcels: List[TransformedParcel] = Field(
        default=[],
        serialization_alias="profileParcels",
        validation_alias="profileParcels",
    )
    cloud_credentials: Optional[CloudCredentials] = Field(
        default=None, serialization_alias="cloudCredentials", validation_alias="cloudCredentials"
    )

    @model_validator(mode="before")
    @classmethod
    def insert_parcel_type_from_headers(cls, values: Dict[str, Any]):
        if not isinstance(values, dict):
            return values
        profile_parcels = values.get("profileParcels", [])
        if not profile_parcels:
            profile_parcels = values.get("profile_parcels", [])
        for profile_parcel in profile_parcels:
            if not isinstance(profile_parcel, dict):
                break
            profile_parcel["parcel"]["type_"] = profile_parcel["header"]["type"]
        return values

    def parcels_with_origin(self, origin: Set[UUID]) -> List[AnyParcel]:
        return [p.parcel for p in self.profile_parcels if p.header.origin in origin]


class ConfigTransformResult(BaseModel):
    # https://docs.pydantic.dev/2.0/usage/models/#fields-with-dynamic-default-values
    uuid: UUID = Field(default_factory=uuid4)
    ux2_config: UX2Config = Field(
        default_factory=lambda: UX2Config(), serialization_alias="ux2Config", validation_alias="ux2Config"
    )
    failed_items: List[FailedConversionItem] = Field(
        default_factory=list, serialization_alias="failedConversionItems", validation_alias="failedConversionItems"
    )

    def add_suffix_to_names(self) -> None:
        suffix = f"_{str(self.uuid)[:5]}"
        parcel_name_lookup: Dict[str, List[AnyPolicyObjectParcel]] = {}
        for config_group in self.ux2_config.config_groups:
            config_group.header.origname = config_group.config_group.name
            config_group.config_group.name += suffix
        for topology_group in self.ux2_config.topology_groups:
            topology_group.header.origname = topology_group.topology_group.name
            topology_group.topology_group.name += suffix
        for feature_profile in self.ux2_config.feature_profiles:
            feature_profile.header.origname = feature_profile.feature_profile.name
            feature_profile.feature_profile.name += suffix
        # parcel rename only for policy groups-of-interest which share global profile
        for profile_parcel in self.ux2_config.profile_parcels:
            profile_parcel.header.origname = profile_parcel.parcel.parcel_name
            if profile_parcel.header.type in [t._get_parcel_type() for t in list_types(AnyPolicyObjectParcel)]:
                # build lookup by parcel name to find duplicates
                parcel = cast(AnyPolicyObjectParcel, profile_parcel.parcel)
                name = profile_parcel.header.origname
                if not parcel_name_lookup.get(name):
                    parcel_name_lookup[name] = [parcel]
                else:
                    parcel_name_lookup[name].append(parcel)

        for name, parcels in parcel_name_lookup.items():
            # policy object parcel names are restricted to 32 characters and needs to be unique
            maxlen = 32
            for i, parcel in enumerate(parcels):
                if i > 0:
                    # replace last 3-digit of suffix (can handle 4096 duplicates)
                    suffix_num = int(suffix[1:], 16) + i
                    parcel.parcel_name = name[:-3] + hex(suffix_num)[-3:]
                    continue
                # add suffix
                if len(name) >= (maxlen - 6):
                    name = name[maxlen - 7 :]
                name = name + suffix
                parcel.parcel_name = name

    def add_failed_conversion_parcel(
        self,
        exception_message: str,
        feature_template: Optional[FeatureTemplateInformation] = None,
        policy: Optional[
            Union[
                CentralizedPolicyInfo,
                LocalizedPolicyInfo,
                AnySecurityPolicyInfo,
                AnyPolicyDefinitionInfo,
                AnyPolicyListInfo,
            ]
        ] = None,
    ):
        self.failed_items.append(
            FailedConversionItem(
                feature_template=feature_template,
                policy=policy,
                exception_message=exception_message,
            )
        )


class ConfigGroupReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    name: str = Field(
        serialization_alias="ConfigGroupName",
        validation_alias="ConfigGroupName",
        description="Name of the Config Group created from Device Template",
    )
    uuid: UUID = Field(
        serialization_alias="ConfigGroupUuid",
        validation_alias="ConfigGroupUuid",
        description="UUID of the Config Group created from Device Template",
    )
    feature_profiles: List[FeatureProfileBuildReport] = Field(
        default=[],
        serialization_alias="FeatureProfiles",
        validation_alias="FeatureProfiles",
        description="List of Feature Profiles created from Device Template and attached to the Config Group",
    )


class GroupsOfInterestBuildReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    created_parcels: List[Tuple[str, UUID]] = Field(
        default_factory=list, serialization_alias="createdParcels", validation_alias="createdParcels"
    )
    failed_parcels: List[FailedParcel] = Field(
        default_factory=list, serialization_alias="failedParcels", validation_alias="failedParcels"
    )

    def add_created(self, name: str, id_: UUID):
        self.created_parcels.append((name, id_))

    def add_failed(self, parcel: AnyParcel, error: ManagerHTTPError):
        failed_parcel = FailedParcel(
            parcel_name=parcel.parcel_name,
            parcel_type=parcel._get_parcel_type(),
            error_info=error.info,
            request_details=FailedRequestDetails.from_response(ManagerHTTPError.response),
        )
        self.failed_parcels.append(failed_parcel)


class UX2ConfigPushReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    config_groups: List[ConfigGroupReport] = Field(
        default_factory=list, serialization_alias="ConfigGroups", validation_alias="ConfigGroups"
    )
    standalone_feature_profiles: List[FeatureProfileBuildReport] = Field(
        default_factory=list,
        serialization_alias="StandaloneFeatureProfiles",
        validation_alias="StandaloneFeatureProfiles",
    )
    groups_of_interest: GroupsOfInterestBuildReport = Field(
        default=GroupsOfInterestBuildReport(), serialization_alias="groupsOfIterest", validation_alias="groupsOfIterest"
    )
    failed_push_parcels: List[FailedParcel] = Field(
        default_factory=list, serialization_alias="FailedPushParcels", validation_alias="FailedPushParcels"
    )

    def add_report(self, name: str, uuid: UUID, feature_profiles: List[FeatureProfileBuildReport]) -> None:
        self.config_groups.append(ConfigGroupReport(name=name, uuid=uuid, feature_profiles=feature_profiles))

    def add_feature_profiles_not_assosiated_with_config_group(
        self, feature_profiles: List[FeatureProfileBuildReport]
    ) -> None:
        """This happends when config group failes to create but we have to store created feature profiles in report"""
        self.standalone_feature_profiles.extend(feature_profiles)

    def set_failed_push_parcels_flat_list(self):
        for config_group in self.config_groups:
            for feature_profile in config_group.feature_profiles:
                for failed_parcel in feature_profile.failed_parcels:
                    self.failed_push_parcels.append(failed_parcel)

        for s_feature_profile in self.standalone_feature_profiles:
            for failed_parcel in s_feature_profile.failed_parcels:
                self.failed_push_parcels.append(failed_parcel)

    @property
    def get_summary(self) -> str:
        created_parcels = 0
        failed_parcels = 0
        for config_group in self.config_groups:
            for feature_profile in config_group.feature_profiles:
                created_parcels += len(feature_profile.created_parcels)
                failed_parcels += len(feature_profile.failed_parcels)
        all_parcels = created_parcels + failed_parcels
        success_rate_message = (
            f"{created_parcels}/{all_parcels} "
            f"({int((created_parcels / all_parcels) * 100)}%)"
            " parcels created successfully."
        )
        return success_rate_message


class DefaultPolicyObjectProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    profile_id: UUID = Field(
        serialization_alias="defaultPolicyObjectProfileId", validation_alias="defaultPolicyObjectProfileId"
    )
    parcels: List[Tuple[UUID, str]] = Field(default_factory=list)

    def add_parcel(self, parcel_type: str, parcel_id: UUID):
        self.parcels.append((parcel_id, parcel_type))


class UX2RollbackInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True)
    config_group_ids: List[UUID] = Field(
        default_factory=list,
        serialization_alias="ConfigGroupIds",
        validation_alias="ConfigGroupIds",
    )
    policy_group_ids: List[UUID] = Field(
        default_factory=list,
        serialization_alias="PolicyGroupIds",
        validation_alias="PolicyGroupIds",
    )
    topology_group_ids: List[UUID] = Field(
        default_factory=list,
        serialization_alias="TopologyGroupIds",
        validation_alias="TopologyGroupIds",
    )
    feature_profile_ids: List[Tuple[UUID, ProfileType]] = Field(
        default_factory=list,
        serialization_alias="FeatureProfileIds",
        validation_alias="FeatureProfileIds",
    )
    default_policy_object_profile: Optional[DefaultPolicyObjectProfile] = Field(
        default=None,
        serialization_alias="defaultPolicyObjectProfile",
        validation_alias="defaultPolicyObjectProfile",
    )

    def add_config_group(self, config_group_id: UUID) -> None:
        self.config_group_ids.append(config_group_id)

    def add_feature_profile(self, feature_profile_id: UUID, profile_type: ProfileType) -> None:
        self.feature_profile_ids.append((feature_profile_id, profile_type))

    def add_default_policy_object_profile(self, profile_id: UUID) -> DefaultPolicyObjectProfile:
        self.default_policy_object_profile = DefaultPolicyObjectProfile(profile_id=profile_id)
        return self.default_policy_object_profile

    def add_policy_group(self, group_id: UUID) -> None:
        self.policy_group_ids.append(group_id)

    def add_topology_group(self, topology_id: UUID) -> None:
        self.topology_group_ids.append(topology_id)


class UX2ConfigPushResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    rollback: UX2RollbackInfo = UX2RollbackInfo()
    report: UX2ConfigPushReport = UX2ConfigPushReport()


@dataclass
class PolicyConvertContext:
    # conversion input
    region_map: Dict[str, int] = field(default_factory=dict)
    site_map: Dict[str, int] = field(default_factory=dict)
    lan_vpn_map: Dict[str, Union[int, str]] = field(default_factory=dict)
    # emited during conversion
    regions_by_list_id: Dict[UUID, List[str]] = field(default_factory=dict)
    sites_by_list_id: Dict[UUID, List[str]] = field(default_factory=dict)
    lan_vpns_by_list_id: Dict[UUID, List[str]] = field(default_factory=dict)

    @staticmethod
    def from_configs(
        network_hierarchy: List[NodeInfo],
        transformed_parcels: List[TransformedParcel],
        policy_list_infos: List[AnyPolicyListInfo],
    ) -> "PolicyConvertContext":
        context = PolicyConvertContext()
        for node in network_hierarchy:
            if node.data.hierarchy_id is not None:
                if node.data.label == "SITE" and node.data.hierarchy_id.site_id is not None:
                    context.site_map[node.name] = node.data.hierarchy_id.site_id
                if node.data.label == "REGION" and node.data.hierarchy_id.region_id is not None:
                    context.region_map[node.name] = node.data.hierarchy_id.region_id
        for parcel in [p.parcel for p in transformed_parcels]:
            if isinstance(parcel, LanVpnParcel):
                if parcel.vpn_id.value is not None:
                    context.lan_vpn_map[parcel.parcel_name] = parcel.vpn_id.value
        return context
