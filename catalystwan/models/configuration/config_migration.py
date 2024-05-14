# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Any, Dict, List, Optional, Set, Tuple, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from catalystwan.api.builders.feature_profiles.report import FailedParcel, FeatureProfileBuildReport
from catalystwan.api.templates.device_template.device_template import DeviceTemplate, GeneralTemplate
from catalystwan.endpoints.configuration_group import ConfigGroupCreationPayload
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy import AnyPolicyDefinitionInfo, AnyPolicyListInfo
from catalystwan.models.policy.centralized import CentralizedPolicyInfo
from catalystwan.models.policy.localized import LocalizedPolicyInfo
from catalystwan.models.policy.security import AnySecurityPolicyInfo
from catalystwan.models.templates import FeatureTemplateInformation, TemplateInformation


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
        Flatten the representation but leave cisco vpn templates as they are.

        Returns:
            A list of GeneralTemplate objects representing the flattened templates list.
        """
        result = []
        for template in self.general_templates:
            subtemplates = template.subTemplates
            if subtemplates and template.templateType != "cisco_vpn":
                template.subTemplates = []
                for subtemplate in subtemplates:
                    result.append(subtemplate)
            result.append(template)

        return result


class UX1Policies(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
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
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()


class TransformHeader(BaseModel):
    type: str = Field(
        description="Needed to push item to specific endpoint."
        "Type discriminator is not present in many UX2 item payloads"
    )
    origin: UUID = Field(description="Original UUID of converted item")
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
    model_config = ConfigDict(populate_by_name=True)
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

    @model_validator(mode="before")
    @classmethod
    def insert_parcel_type_from_headers(cls, values: Dict[str, Any]):
        profile_parcels = values.get("profileParcels", [])
        if not profile_parcels:
            profile_parcels = values.get("profile_parcels", [])
        for profile_parcel in profile_parcels:
            if not isinstance(profile_parcel, dict):
                break
            profile_parcel["parcel"]["type_"] = profile_parcel["header"]["type"]
        return values


class ConfigTransformResult(BaseModel):
    ux2_config: UX2Config = Field(
        default_factory=lambda: UX2Config(), serialization_alias="ux2Config", validation_alias="ux2Config"
    )
    failed_items: List[FailedConversionItem] = Field(
        default_factory=list, serialization_alias="failedConversionItems", validation_alias="failedConversionItems"
    )

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


class UX2ConfigPushReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    config_groups: List[ConfigGroupReport] = Field(
        default_factory=list, serialization_alias="ConfigGroups", validation_alias="ConfigGroups"
    )
    failed_push_parcels: List[FailedParcel] = Field(
        default_factory=list, serialization_alias="FailedPushParcels", validation_alias="FailedPushParcels"
    )

    def add_report(self, name: str, uuid: UUID, feature_profiles: List[FeatureProfileBuildReport]) -> None:
        self.config_groups.append(ConfigGroupReport(name=name, uuid=uuid, feature_profiles=feature_profiles))

    def set_failed_push_parcels_flat_list(self):
        failed_parcels = []
        for config_group in self.config_groups:
            for feature_profile in config_group.feature_profiles:
                for failed_parcel in feature_profile.failed_parcels:
                    failed_parcels.append(failed_parcel)
        self.failed_push_parcels = failed_parcels

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


class UX2ConfigRollback(BaseModel):
    config_group_ids: List[UUID] = Field(
        default_factory=list,
        serialization_alias="ConfigGroupIds",
        validation_alias="ConfigGroupIds",
    )
    feature_profile_ids: List[Tuple[UUID, ProfileType]] = Field(
        default_factory=list,
        serialization_alias="FeatureProfileIds",
        validation_alias="FeatureProfileIds",
    )

    report: UX2ConfigPushReport = Field(
        default=UX2ConfigPushReport(),
        serialization_alias="ConfigPushReport",
        validation_alias="ConfigPushReport",
    )

    def add_config_group(self, config_group_id: UUID) -> None:
        self.config_group_ids.append(config_group_id)

    def add_feature_profile(self, feature_profile_id: UUID, profile_type: ProfileType) -> None:
        self.feature_profile_ids.append((feature_profile_id, profile_type))
