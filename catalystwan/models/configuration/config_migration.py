# Copyright 2024 Cisco Systems, Inc. and its affiliates

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Literal, Optional, Sequence, Set, Tuple, TypeVar, Union, cast
from uuid import UUID, uuid4

from packaging.version import Version
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel

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
from catalystwan.models.common import IntStr, VpnId
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload, ProfileType
from catalystwan.models.configuration.feature_profile.parcel import AnyParcel, list_types
from catalystwan.models.configuration.feature_profile.sdwan.policy_object import AnyPolicyObjectParcel
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.network_hierarchy import NodeInfo
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy import AnyPolicyDefinitionInfo, AnyPolicyListInfo, URLAllowListInfo, URLBlockListInfo
from catalystwan.models.policy.centralized import CentralizedPolicyInfo
from catalystwan.models.policy.definition.ssl_decryption import NetworkDecryptionRuleSequence, UrlProfile
from catalystwan.models.policy.definition.zone_based_firewall import ZoneBasedFWPolicyEntry
from catalystwan.models.policy.localized import LocalizedPolicyInfo
from catalystwan.models.policy.security import (
    AnySecurityPolicyInfo,
    HighSpeedLoggingEntry,
    HighSpeedLoggingList,
    LoggingEntry,
    ZoneToNoZoneInternet,
)
from catalystwan.models.templates import FeatureTemplateInformation, TemplateInformation
from catalystwan.version import parse_api_version

T = TypeVar("T", bound=AnyParcel)
TO = TypeVar("TO")

ConvertOutputStatus = Literal["complete", "partial"]
ConvertAbortStatus = Literal["failed", "unsupported"]
ConvertStatus = Literal[ConvertOutputStatus, ConvertAbortStatus]

camel = AliasGenerator(
    serialization_alias=to_camel,
    validation_alias=to_camel,
)


class VersionInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    platform: str = "unknown"
    sdk: str = PACKAGE_VERSION

    @property
    def platform_api(self) -> Version:
        return parse_api_version(self.platform)

    def is_compatible(self, other: "VersionInfo"):
        return True if (self.sdk == other.sdk and self.platform_api == other.platform_api) else False


class DeviceTemplateWithInfo(DeviceTemplate):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    template_id: str
    devices_attached: int

    @staticmethod
    def from_merged(template: DeviceTemplate, info: TemplateInformation) -> "DeviceTemplateWithInfo":
        info_dict = template.model_dump()
        return DeviceTemplateWithInfo(
            template_id=info.id,
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
            subtemplates = template.sub_templates
            if subtemplates and template.template_type not in ["cisco_vpn", "vpn-vedge", "cellular-cedge-controller"]:
                template.sub_templates = []
                for subtemplate in subtemplates:
                    result.append(subtemplate)
            result.append(template)

        return result


class UX1Policies(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    centralized_policies: List[CentralizedPolicyInfo] = Field(default_factory=list)
    localized_policies: List[LocalizedPolicyInfo] = Field(default_factory=list)
    security_policies: List[AnySecurityPolicyInfo] = Field(default_factory=list)
    policy_definitions: List[AnyPolicyDefinitionInfo] = Field(default_factory=list)
    policy_lists: List[AnyPolicyListInfo] = Field(default_factory=list)


class UX1Templates(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    feature_templates: List[FeatureTemplateInformation] = Field(default_factory=list)
    device_templates: List[DeviceTemplateWithInfo] = Field(default_factory=list)

    def create_device_template_by_policy_id_lookup(self) -> Dict[Literal["policy", "security"], Dict[UUID, UUID]]:
        lookup: Dict[Literal["policy", "security"], Dict[UUID, UUID]] = {"policy": {}, "security": {}}
        for dt in self.device_templates:
            policy_id = dt.get_policy_uuid()
            security_policy_id = dt.get_security_policy_uuid()
            if policy_id is not None:
                lookup["policy"][policy_id] = UUID(dt.template_id)
            if security_policy_id is not None:
                lookup["security"][security_policy_id] = UUID(dt.template_id)
        return lookup


class UX1Config(BaseModel):
    # All UX1 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    version: VersionInfo = VersionInfo()
    policies: UX1Policies = UX1Policies()
    templates: UX1Templates = UX1Templates()
    network_hierarchy: List[NodeInfo] = Field(default_factory=list)


class TransformHeader(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    type: str = Field(
        description="Needed to push item to specific endpoint."
        "Type discriminator is not present in many UX2 item payloads"
    )
    origin: UUID = Field(description="Original UUID of converted item")
    origname: Optional[str] = None
    subelements: Set[UUID] = Field(default_factory=set)
    localized_policy_subelements: Optional[Set[UUID]] = Field(default=None)
    status: ConvertOutputStatus = Field(default="complete")
    info: List[str] = Field(default_factory=list)

    def add_localized_policy_subelement(self, subelement: UUID) -> None:
        if self.localized_policy_subelements is None:
            self.localized_policy_subelements = {subelement}
        else:
            self.localized_policy_subelements.add(subelement)


class TransformedTopologyGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    header: TransformHeader
    topology_group: TopologyGroup


class TransformedConfigGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    header: TransformHeader
    config_group: ConfigGroupCreationPayload


class TransformedFeatureProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    header: TransformHeader
    feature_profile: FeatureProfileCreationPayload


class TransformedParcel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    header: TransformHeader
    parcel: AnyParcel


class FailedConversionItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    feature_template: Optional[FeatureTemplateInformation] = Field(default=None)
    policy: Optional[
        Union[
            CentralizedPolicyInfo,
            LocalizedPolicyInfo,
            AnySecurityPolicyInfo,
            AnyPolicyDefinitionInfo,
            AnyPolicyListInfo,
        ]
    ] = Field(default=None)
    exception_message: str


class UnsupportedConversionItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    name: str
    uuid: UUID
    type: Optional[str] = None


class UX2Config(BaseModel):
    # All UX2 Configuration items - Mega Model
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    version: VersionInfo = VersionInfo()
    topology_groups: List[TransformedTopologyGroup] = Field(default_factory=list)
    config_groups: List[TransformedConfigGroup] = Field(default_factory=list)
    policy_groups: List[TransformedConfigGroup] = Field(default_factory=list)
    feature_profiles: List[TransformedFeatureProfile] = Field(default_factory=list)
    profile_parcels: List[TransformedParcel] = Field(default_factory=list)
    cloud_credentials: Optional[CloudCredentials] = Field(default=None)

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

    def list_transformed_parcels_with_origin(self, origin: Set[UUID]) -> List[TransformedParcel]:
        return [p for p in self.profile_parcels if p.header.origin in origin]

    def add_subelement_in_config_group(
        self, profile_types: List[ProfileType], device_template_id: UUID, subelement: UUID
    ) -> bool:
        profile_ids: Set[UUID] = set()
        added = False
        for config_group in self.config_groups:
            if config_group.header.origin == device_template_id:
                profile_ids = config_group.header.subelements
                break
        if not profile_ids:
            return added
        for feature_profile in self.feature_profiles:
            if feature_profile.header.type in profile_types and feature_profile.header.origin in profile_ids:
                head = feature_profile.header
                if head.localized_policy_subelements is None:
                    head.localized_policy_subelements = {subelement}
                else:
                    head.localized_policy_subelements.add(subelement)
                added = True
        return added


class ConfigTransformResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    uuid: UUID = Field(default_factory=uuid4)
    ux2_config: UX2Config = Field(default_factory=UX2Config)
    failed_items: List[FailedConversionItem] = Field(default_factory=list)
    unsupported_items: List[UnsupportedConversionItem] = Field(default_factory=list)

    @property
    def policy_object_parcel_maxlen(self) -> int:
        return 32

    @property
    def suffix(self) -> str:
        return f"_{str(self.uuid)[:5]}"

    def create_policy_object_parcel_name_lookup(
        self, use_suffix: bool = False
    ) -> Dict[str, List[AnyPolicyObjectParcel]]:
        namelen = (
            self.policy_object_parcel_maxlen - len(self.suffix)
            if use_suffix
            else (self.policy_object_parcel_maxlen - 2)
        )
        lookup: Dict[str, List[AnyPolicyObjectParcel]] = {}
        # parcel rename only for policy groups-of-interest which share global profile
        for profile_parcel in self.ux2_config.profile_parcels:
            profile_parcel.header.origname = profile_parcel.parcel.parcel_name
            if profile_parcel.header.type in [t._get_parcel_type() for t in list_types(AnyPolicyObjectParcel)]:
                # build lookup by parcel name to find duplicates
                # if suffix is added we need to take into consideration shortened names
                parcel = cast(AnyPolicyObjectParcel, profile_parcel.parcel)
                name = profile_parcel.header.origname[:namelen]
                if not lookup.get(name):
                    lookup[name] = [parcel]
                else:
                    lookup[name].append(parcel)
        return lookup

    def add_suffix_to_names(self) -> None:
        for config_group in self.ux2_config.config_groups:
            config_group.header.origname = config_group.config_group.name
            config_group.config_group.name += self.suffix
        for topology_group in self.ux2_config.topology_groups:
            topology_group.header.origname = topology_group.topology_group.name
            topology_group.topology_group.name += self.suffix
        for feature_profile in self.ux2_config.feature_profiles:
            feature_profile.header.origname = feature_profile.feature_profile.name
            feature_profile.feature_profile.name += self.suffix

    def resolve_conflicts_on_policy_object_parcel_names(self, use_suffix: bool = False) -> None:
        # policy object parcel names are restricted to 32 characters and needs to be unique
        # TODO: cleanup, also this works only for suffix len = 6 (eg. "_1afc9")
        assert len(self.suffix) == 6
        for name, parcels in self.create_policy_object_parcel_name_lookup().items():
            maxlen = self.policy_object_parcel_maxlen
            if use_suffix:
                # dedicated conflict resolving when suffix is used (we increment suffix digit)
                for i, parcel in enumerate(parcels):
                    if i > 0:
                        # replace last 3-digit of suffix (can handle 4096 duplicates)
                        suffix_num = int(self.suffix[1:], 16) + i
                        parcel.parcel_name = name[:-3] + hex(suffix_num)[-3:]
                        continue
                    # add suffix
                    if len(name) >= (maxlen - 6):
                        name = name[: maxlen - 7]
                    name = name + self.suffix
                    parcel.parcel_name = name
            else:
                for i, parcel in enumerate(parcels):
                    if i > 0:
                        suffix_str = f"_{hex(i)[-1]}"
                        if len(name) > (maxlen - 2):
                            parcel.parcel_name = name[:-2] + suffix_str
                        else:
                            parcel.parcel_name = name + suffix_str

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

    def add_unsupported_item(self, name: str, uuid: UUID, type: Optional[str] = None):
        item = UnsupportedConversionItem(
            name=name,
            uuid=uuid,
            type=type,
        )
        self.unsupported_items.append(item)


class GroupReportBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    name: str
    uuid: UUID
    feature_profiles: List[FeatureProfileBuildReport] = Field(default_factory=list)


class ConfigGroupReport(GroupReportBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)


class TopologyGroupReport(GroupReportBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)


class PolicyGroupReport(GroupReportBase):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)


class DefaultPolicyObjectProfileReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    present_before_migration: Optional[bool] = None
    created_by: Optional[str] = None
    creation_failed: Optional[bool] = None


class GroupsOfInterestBuildReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    default_policy_object_profile: DefaultPolicyObjectProfileReport = Field(
        default_factory=DefaultPolicyObjectProfileReport
    )
    created_parcels: List[Tuple[str, UUID]] = Field(default_factory=list)
    failed_parcels: List[FailedParcel] = Field(default_factory=list)

    def add_created(self, name: str, id: UUID):
        self.created_parcels.append((name, id))

    def add_failed(self, parcel: AnyParcel, error: ManagerHTTPError):
        failed_parcel = FailedParcel(
            parcel_name=parcel.parcel_name,
            parcel_type=parcel._get_parcel_type(),
            error_info=error.info,
            request_details=FailedRequestDetails.from_response(error.response),
        )
        self.failed_parcels.append(failed_parcel)


class UX2ConfigPushReport(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", alias_generator=camel)
    config_groups: List[ConfigGroupReport] = Field(default_factory=list)
    policy_groups: List[PolicyGroupReport] = Field(default_factory=list)
    topology_groups: List[TopologyGroupReport] = Field(default_factory=list)
    standalone_feature_profiles: List[FeatureProfileBuildReport] = Field(default_factory=list)
    groups_of_interest: GroupsOfInterestBuildReport = Field(default_factory=GroupsOfInterestBuildReport)
    security_policies: List[FeatureProfileBuildReport] = Field(default_factory=list)
    failed_push_parcels: List[FailedParcel] = Field(default_factory=list)

    @property
    def groups(self) -> Sequence[GroupReportBase]:
        groups: List[GroupReportBase] = list()
        groups.extend(self.config_groups)
        groups.extend(self.policy_groups)
        groups.extend(self.topology_groups)
        return groups

    def add_report(self, name: str, uuid: UUID, feature_profiles: List[FeatureProfileBuildReport]) -> None:
        self.config_groups.append(ConfigGroupReport(name=name, uuid=uuid, feature_profiles=feature_profiles))

    def add_standalone_feature_profiles(self, feature_profiles: List[FeatureProfileBuildReport]) -> None:
        """This happends when parent config group failes to create or profile don't have config group"""
        self.standalone_feature_profiles.extend(feature_profiles)

    def set_failed_push_parcels_flat_list(self):
        for group in self.groups:
            for feature_profile in group.feature_profiles:
                for failed_parcel in feature_profile.failed_parcels:
                    self.failed_push_parcels.append(failed_parcel)

        for s_feature_profile in self.standalone_feature_profiles:
            for failed_parcel in s_feature_profile.failed_parcels:
                self.failed_push_parcels.append(failed_parcel)

        for failed_parcel in self.groups_of_interest.failed_parcels:
            self.failed_push_parcels.append(failed_parcel)

    @property
    def get_summary(self) -> str:
        created_parcels = 0
        failed_parcels = 0

        for group in self.groups:
            for feature_profile in group.feature_profiles:
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
    profile_id: UUID
    parcels: List[Tuple[UUID, str]] = Field(default_factory=list)

    def add_parcel(self, parcel_type: str, parcel_id: UUID):
        self.parcels.append((parcel_id, parcel_type))


class UX2RollbackInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, alias_generator=camel)
    config_group_ids: List[UUID] = Field(default_factory=list)
    policy_group_ids: List[UUID] = Field(default_factory=list)
    topology_group_ids: List[UUID] = Field(default_factory=list)
    feature_profile_ids: List[Tuple[UUID, ProfileType]] = Field(default_factory=list)
    default_policy_object_profile: Optional[DefaultPolicyObjectProfile] = Field(
        default=None,
        description="Do not delete this profile! only selected parcel contents for which profile id is provided",
    )

    def add_config_group(self, config_group_id: UUID) -> None:
        self.config_group_ids.append(config_group_id)

    def add_feature_profile(self, feature_profile_id: UUID, profile_type: ProfileType) -> None:
        self.feature_profile_ids.append((feature_profile_id, profile_type))

    def add_default_policy_object_profile_id(self, profile_id: UUID) -> DefaultPolicyObjectProfile:
        # do not delete this profile! only selected parcel contents
        self.default_policy_object_profile = DefaultPolicyObjectProfile(profile_id=profile_id)
        return self.default_policy_object_profile

    def add_policy_group(self, group_id: UUID) -> None:
        self.policy_group_ids.append(group_id)

    def add_topology_group(self, topology_id: UUID) -> None:
        self.topology_group_ids.append(topology_id)


class UX2ConfigPushResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=camel)
    rollback: UX2RollbackInfo = UX2RollbackInfo()
    report: UX2ConfigPushReport = UX2ConfigPushReport()


@dataclass
class SslProfileResidues:
    filtered_url_black_list: List[URLBlockListInfo]
    filtered_url_white_list: List[URLAllowListInfo]


@dataclass
class SslDecryptioneResidues:
    sequences: List[NetworkDecryptionRuleSequence]
    profiles: List[UrlProfile]


@dataclass
class SecurityPolicyResidues:
    high_speed_logging_setting: Optional[Union[HighSpeedLoggingEntry, HighSpeedLoggingList]]
    logging_setting: Optional[List[LoggingEntry]] = None
    zone_to_no_zone_internet_setting: Optional[ZoneToNoZoneInternet] = None
    platform_match_setting: Optional[str] = None


@dataclass
class QoSMapResidues:
    buffer_percent: IntStr
    burst: Optional[IntStr] = None
    temp_key_values: Optional[str] = None


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
    amp_target_vpns_id: Dict[UUID, List[VpnId]] = field(default_factory=dict)
    dns_security_umbrella_data: Dict[UUID, UUID] = field(default_factory=dict)
    intrusion_prevention_target_vpns_id: Dict[UUID, List[VpnId]] = field(default_factory=dict)
    ssl_decryption_residues: Dict[UUID, SslDecryptioneResidues] = field(default_factory=dict)
    ssl_profile_residues: Dict[UUID, SslProfileResidues] = field(default_factory=dict)
    url_filtering_target_vpns: Dict[UUID, List[VpnId]] = field(default_factory=dict)
    zone_based_firewall_residues: Dict[UUID, List[ZoneBasedFWPolicyEntry]] = field(default_factory=dict)
    security_policy_residues: Dict[UUID, SecurityPolicyResidues] = field(default_factory=dict)
    qos_map_residues: Dict[UUID, List[QoSMapResidues]] = field(default_factory=dict)
    as_path_list_num_mapping: Dict[str, int] = field(default_factory=dict)

    def get_vpn_id_to_vpn_name_map(self) -> Dict[Union[str, int], List[str]]:
        vpn_map: Dict[Union[str, int], List[str]] = {}
        for k, v in self.lan_vpn_map.items():
            vpn_map[v] = vpn_map.get(v, [])
            vpn_map[v].append(k)
        return vpn_map

    def generate_as_path_list_num_from_name(self, name: str) -> int:
        """The UX1 and UX2 intersection in AS Path list name and ID but only for the ISR Edge router (number 1 to 500).
        If there is number we can insert the value in as_path_list_num field otherwise we will
        generate the value and keep track of it in the context."""
        number = len(self.as_path_list_num_mapping) + 1
        self.as_path_list_num_mapping[name] = number
        return number

    @staticmethod
    def from_configs(
        network_hierarchy: List[NodeInfo],
        transformed_parcels: List[TransformedParcel],
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


@dataclass
class PushContext:
    default_policy_object_profile_id: Optional[UUID] = None
    id_lookup: Dict[UUID, UUID] = field(
        default_factory=dict
    )  # universal lookup for finding pushed item id by origin id


@dataclass
class ConvertResult(Generic[TO]):
    status: ConvertStatus = "complete"
    output: Optional[TO] = None
    info: List[str] = field(default_factory=list)

    def update_status(self, status: ConvertStatus, message: str):
        self.status = status
        self.info.append(message)

    def get_info(self) -> str:
        return "\n".join(self.info)
