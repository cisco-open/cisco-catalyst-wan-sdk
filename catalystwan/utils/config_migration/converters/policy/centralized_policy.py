# Copyright 2024 Cisco Systems, Inc. and its affiliates

from dataclasses import dataclass, field
from typing import Dict, List, Set
from uuid import UUID, uuid4

from pydantic import ValidationError

from catalystwan.models.configuration.config_migration import (
    FailedConversionItem,
    PolicyConvertContext,
    TransformedFeatureProfile,
    TransformedParcel,
    TransformedTopologyGroup,
    TransformHeader,
    UX1Config,
    UX2Config,
)
from catalystwan.models.configuration.feature_profile.common import FeatureProfileCreationPayload
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.models.configuration.topology_group import TopologyGroup
from catalystwan.models.policy.centralized import CentralizedPolicy, CentralizedPolicyDefinition, ControlPolicyItem
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.definition.hub_and_spoke import HubAndSpokePolicy
from catalystwan.models.policy.definition.mesh import MeshPolicy

TOPOLOGY_POLICIES = ["control", "hubAndSpoke", "mesh"]


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
        self.unreferenced_topologies: List[TransformedParcel] = list()
        self.topology_lookup: Dict[UUID, List[TransformedParcel]] = dict()
        self._create_topology_by_policy_id_lookup()
        self.failed_items: List[FailedConversionItem] = list()

    def _create_topology_by_policy_id_lookup(self) -> None:
        for policy_definition in self.ux1.policies.policy_definitions:
            if policy_definition.type in TOPOLOGY_POLICIES:
                assert isinstance(policy_definition, (ControlPolicy, HubAndSpokePolicy, MeshPolicy))
                transformed_topology_parcels = self.ux2.list_transformed_parcels_with_origin(
                    {policy_definition.definition_id}
                )
                if policy_definition.reference_count == 0:
                    self.unreferenced_topologies.extend(transformed_topology_parcels)
                for ref_id in set([ref.id for ref in policy_definition.references]):
                    if self.topology_lookup.get(ref_id) is not None:
                        self.topology_lookup[ref_id].extend(transformed_topology_parcels)
                    else:
                        self.topology_lookup[ref_id] = list(transformed_topology_parcels)

    def update_topology_groups_and_profiles(self) -> None:
        parcel_remove_ids: Set[UUID] = set()
        for centralized_policy in self.ux1.policies.centralized_policies:
            problems: List[str] = list()
            if centralized_policy.policy_type == "feature":
                dst_transformed_parcels: List[TransformedParcel] = list()
                if src_transformed_parcels := self.topology_lookup.get(centralized_policy.policy_id):
                    for src_transformed_parcel in src_transformed_parcels:
                        try:
                            assert isinstance(
                                src_transformed_parcel.parcel, (MeshParcel, HubSpokeParcel, CustomControlParcel)
                            )
                            parcel_remove_ids.add(src_transformed_parcel.header.origin)
                            parcel = src_transformed_parcel.parcel.model_copy(deep=True)
                            header = src_transformed_parcel.header.model_copy(deep=True)
                            if parcel.type_ == "custom-control":
                                assembly = find_control_assembly(centralized_policy, header.origin)
                                application = convert_control_policy_application(
                                    assembly=assembly, context=self.context
                                )
                                parcel.assign_target_sites(
                                    inbound_sites=application.inbound_sites,
                                    outbound_sites=application.outbound_sites,
                                )
                            header.origin = uuid4()
                            dst_transformed_parcel = TransformedParcel(header=header, parcel=parcel)
                            dst_transformed_parcels.append(dst_transformed_parcel)
                            self.ux2.profile_parcels.append(dst_transformed_parcel)
                        except (ValidationError, AssertionError) as e:
                            problems.append(str(e))
                if dst_transformed_parcels:
                    self.ux2.feature_profiles.append(
                        TransformedFeatureProfile(
                            header=TransformHeader(
                                type="topology",
                                origin=centralized_policy.policy_id,
                                subelements=set([p.header.origin for p in dst_transformed_parcels]),
                                origname=centralized_policy.policy_name,
                            ),
                            feature_profile=FeatureProfileCreationPayload(
                                name=centralized_policy.policy_name,
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
            if problems:
                self.failed_items.append(
                    FailedConversionItem(policy=centralized_policy, exception_message="\n".join(problems))
                )
        self.export_standalone_topology_parcels()
        self.ux2.remove_transformed_parcels_with_origin(parcel_remove_ids)

    def export_standalone_topology_parcels(self):
        # Topology Group and Profile
        if self.unreferenced_topologies:
            topology_name = "Unreferenced-Topologies"
            topology_description = (
                "Created by config migration tool, "
                "contains topologies which were not attached to any Centralized Policy"
            )
            self.ux2.feature_profiles.append(
                TransformedFeatureProfile(
                    header=TransformHeader(
                        type="topology",
                        origin=UUID(int=0),
                        subelements=set([p.header.origin for p in self.unreferenced_topologies]),
                        origname=topology_name,
                    ),
                    feature_profile=FeatureProfileCreationPayload(
                        name=topology_name,
                        description=topology_description,
                    ),
                )
            )
            self.ux2.topology_groups.append(
                TransformedTopologyGroup(
                    header=TransformHeader(type="", origin=UUID(int=0), origname=topology_name, subelements=set()),
                    topology_group=TopologyGroup(
                        name=topology_name, description=topology_description, solution="sdwan"
                    ),
                )
            )
