# Copyright 2024 Cisco Systems, Inc. and its affiliates

from dataclasses import dataclass, field
from typing import Dict, List, Set
from uuid import UUID, uuid4

from packaging.version import Version
from pydantic import ValidationError

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.configuration.config_migration import (
    FailedConversionItem,
    PolicyConvertContext,
    TransformedFeatureProfile,
    TransformedParcel,
    TransformedTopologyGroup,
    TransformHeader,
    UnsupportedConversionItem,
    UX1Config,
    UX2Config,
)
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.traffic_policy import (
    TrafficPolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy.centralized import (
    CentralizedPolicy,
    CentralizedPolicyDefinition,
    CentralizedPolicyInfo,
    ControlPolicyItem,
    TrafficDataDirection,
    TrafficDataPolicyItem,
)
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy
from catalystwan.models.policy.definition.traffic_data import TrafficDataPolicy

POLICY_TYPES = ["control", "hubAndSpoke", "mesh", "data"]


@dataclass
class ControlPolicyApplication:
    inbound_sites: List[str] = field(default_factory=list)
    outbound_sites: List[str] = field(default_factory=list)


def find_control_assembly(policy: CentralizedPolicy, control_definition_id: UUID) -> ControlPolicyItem:
    definition = policy.policy_definition
    assert isinstance(definition, CentralizedPolicyDefinition)
    assembly = definition.find_assembly_item_by_definition_id(control_definition_id)
    assert isinstance(assembly, ControlPolicyItem)
    return assembly


def find_traffic_data_assembly(policy: CentralizedPolicy, traffic_data_definition_id: UUID) -> TrafficDataPolicyItem:
    definition = policy.policy_definition
    assert isinstance(definition, CentralizedPolicyDefinition)
    assembly = definition.find_assembly_item_by_definition_id(traffic_data_definition_id)
    assert isinstance(assembly, TrafficDataPolicyItem)
    return assembly


def convert_control_policy_application(
    assembly: ControlPolicyItem, context: PolicyConvertContext
) -> ControlPolicyApplication:
    application = ControlPolicyApplication()
    for entry in assembly.entries:
        if entry.site_lists:
            for site_list_id in entry.site_lists:
                sites = context.sites_by_list_id.get(site_list_id, [])
                if entry.direction == "in":
                    application.inbound_sites.extend(sites)
                elif entry.direction == "out":
                    application.outbound_sites.extend(sites)
    application.inbound_sites = list(set(application.inbound_sites))
    application.outbound_sites = list(set(application.outbound_sites))
    return application


class CentralizedPolicyConverter:
    def __init__(self, ux1: UX1Config, context: PolicyConvertContext, ux2: UX2Config):
        self.ux1 = ux1
        self.context = context
        self.ux2 = ux2
        self.parcel_lookup: Dict[UUID, List[TransformedParcel]] = dict()
        self._create_parcel_by_policy_id_lookup()
        self.failed_items: List[FailedConversionItem] = list()
        self.unsupported_items: List[UnsupportedConversionItem] = list()

    def _create_parcel_by_policy_id_lookup(self) -> None:
        for policy_definition in self.ux1.policies.policy_definitions:
            if policy_definition.type in POLICY_TYPES:
                assert isinstance(policy_definition, (ControlPolicy, HubAndSpokePolicy, MeshPolicy, TrafficDataPolicy))
                transformed_parcels = self.ux2.list_transformed_parcels_with_origin({policy_definition.definition_id})
                for ref_id in set([ref.id for ref in policy_definition.references]):
                    if self.parcel_lookup.get(ref_id) is not None:
                        self.parcel_lookup[ref_id].extend(transformed_parcels)
                    else:
                        self.parcel_lookup[ref_id] = list(transformed_parcels)

    def update_topology_groups_and_profiles(
        self, centralized_policy: CentralizedPolicyInfo, transformed_topology_parcels: List[TransformedParcel]
    ) -> None:
        self.ux2.feature_profiles.append(
            TransformedFeatureProfile(
                header=TransformHeader(
                    type="topology",
                    origin=centralized_policy.policy_id,
                    subelements=set([p.header.origin for p in transformed_topology_parcels]),
                    origname=centralized_policy.policy_name,
                ),
                feature_profile=FeatureProfileCreationPayload(
                    name=f"{centralized_policy.policy_name}_TOPOLOGY",
                    description=centralized_policy.policy_description,
                ),
            )
        )
        self.ux2.topology_groups.append(
            TransformedTopologyGroup(
                header=TransformHeader(
                    type="",
                    origin=centralized_policy.policy_id,
                    origname=centralized_policy.policy_name,
                    subelements={centralized_policy.policy_id},
                ),
                topology_group=TopologyGroup(
                    name=centralized_policy.policy_name,
                    description=centralized_policy.policy_description,
                    solution="sdwan",
                ),
            )
        )

    def update_app_prio_profiles(
        self,
        centralized_policy: CentralizedPolicyInfo,
        transformed_app_prio_parcels: List[TransformedParcel],
    ) -> None:
        self.ux2.feature_profiles.append(
            TransformedFeatureProfile(
                header=TransformHeader(
                    type="application-priority",
                    origin=centralized_policy.policy_id,
                    subelements=set([p.header.origin for p in transformed_app_prio_parcels]),
                    origname=centralized_policy.policy_name,
                ),
                feature_profile=FeatureProfileCreationPayload(
                    name=centralized_policy.policy_name,
                    description=centralized_policy.policy_description,
                ),
            )
        )

    def update_groups_and_profiles(self) -> None:
        parcel_remove_ids: Set[UUID] = set()
        for centralized_policy in self.ux1.policies.centralized_policies:
            problems: List[str] = list()
            if centralized_policy.policy_type == "feature":
                dst_transformed_topology_parcels: List[TransformedParcel] = list()
                dst_transformed_app_prio_parcels: List[TransformedParcel] = list()
                if src_transformed_parcels := self.parcel_lookup.get(centralized_policy.policy_id):
                    for src_transformed_parcel in src_transformed_parcels:
                        try:
                            assert isinstance(
                                src_transformed_parcel.parcel,
                                (MeshParcel, HubSpokeParcel, CustomControlParcel, TrafficPolicyParcel),
                            )
                            parcel_remove_ids.add(src_transformed_parcel.header.origin)
                            parcel = src_transformed_parcel.parcel.model_copy(deep=True)
                            header = src_transformed_parcel.header.model_copy(deep=True)
                            if parcel.type_ == "custom-control":
                                if self.context.platform_version < Version("20.15"):
                                    _dummy_vpns = self.context.find_any_service_vpn()
                                else:
                                    _dummy_vpns = [";dummy-vpn"]
                                ctrl_assembly = find_control_assembly(centralized_policy, header.origin)
                                ctrl_application = convert_control_policy_application(
                                    assembly=ctrl_assembly, context=self.context
                                )
                                parcel.assign_target_sites(
                                    inbound_sites=ctrl_application.inbound_sites,
                                    outbound_sites=ctrl_application.outbound_sites,
                                    _dummy_vpns=_dummy_vpns,
                                )
                            elif parcel.type_ == "traffic-policy":
                                data_assembly = find_traffic_data_assembly(centralized_policy, header.origin)
                                for i, data_application in enumerate(data_assembly.entries):
                                    _parcel = parcel.model_copy(deep=True)
                                    _header = header.model_copy(deep=True)
                                    _suffix = f"_{i+1}" if i > 0 else ""
                                    _parcel.parcel_name += _suffix
                                    _header.origin = uuid4()
                                    _parcel.target.direction = as_global(
                                        data_application.direction, TrafficDataDirection
                                    )
                                    _parcel.target.vpn.value = []
                                    for vpn_list_id in data_application.vpn_lists:
                                        _parcel.target.vpn.value.extend(
                                            self.context.lan_vpns_by_list_id.get(vpn_list_id, [])
                                        )
                                    if not _parcel.target.vpn.value:
                                        continue
                                    dst_transformed_app_prio_parcel = TransformedParcel(header=_header, parcel=_parcel)
                                    dst_transformed_app_prio_parcels.append(dst_transformed_app_prio_parcel)
                                    self.ux2.profile_parcels.append(dst_transformed_app_prio_parcel)
                                continue
                            header.origin = uuid4()
                            dst_transformed_topology_parcel = TransformedParcel(header=header, parcel=parcel)
                            dst_transformed_topology_parcels.append(dst_transformed_topology_parcel)
                            self.ux2.profile_parcels.append(dst_transformed_topology_parcel)
                        except (ValidationError, AssertionError) as e:
                            problems.append(str(e))
                if dst_transformed_topology_parcels:
                    self.update_topology_groups_and_profiles(centralized_policy, dst_transformed_topology_parcels)
                if dst_transformed_app_prio_parcels:
                    self.update_app_prio_profiles(centralized_policy, dst_transformed_app_prio_parcels)
            else:
                self.unsupported_items.append(
                    UnsupportedConversionItem(
                        name=centralized_policy.policy_name,
                        uuid=centralized_policy.policy_id,
                        type=centralized_policy.policy_type,
                    )
                )
            if problems:
                self.failed_items.append(
                    FailedConversionItem(policy=centralized_policy, exception_message="\n".join(problems))
                )
        self.ux2.remove_transformed_parcels_with_origin(parcel_remove_ids)
