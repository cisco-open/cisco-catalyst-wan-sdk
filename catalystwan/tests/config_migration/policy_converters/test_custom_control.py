import unittest
from ipaddress import IPv4Address
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.policy.definition.control import ControlPolicy
from catalystwan.models.policy.policy_definition import PolicyAcceptRejectAction
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestCustomControlConverter(unittest.TestCase):
    def test_custom_control_with_route_sequence_conversion(self):
        # Arrange
        default_action = "accept"
        name = "custom_control"
        description = "Custom control policy"
        # Arrange policy
        policy = ControlPolicy(
            default_action=PolicyAcceptRejectAction(type=default_action),
            name=name,
            description=description,
        )
        # Arrange Route Sequence
        color_list = uuid4()
        community_list = uuid4()
        expanded_community_list = uuid4()
        omp_tag = 2
        origin = "eigrp-summary"
        originator = IPv4Address("20.30.3.1")
        path_type = "direct-path"
        preference = 100
        prefix_list = uuid4()
        region_id = 200
        region_role = "border-router"
        site_id = 1
        tloc_ip = IPv4Address("30.1.2.3")
        tloc_color = "private5"
        tloc_encap = "ipsec"
        vpn_list_id = uuid4()
        vpn_list_entries = ["30", "31", "32"]
        seq_name = "route_sequence"
        base_action = "accept"
        ip_type = "ipv4"
        action_affinity = 3
        action_community = "1000:10000"
        action_community_additive = True
        action_export_vpn_list_id = uuid4()
        # action_export_vpn_list_entries = ["50", "51"]
        action_omp_tag = 5
        action_preference = 109
        action_service_type = "netsvc1"
        action_service_tloc_list_id = uuid4()
        action_service_vpn = 70

        route = policy.add_route_sequence(
            name=seq_name,
            base_action=base_action,
            ip_type=ip_type,
        )
        route.match_color_list(color_list)
        route.match_community_list(community_list)
        route.match_expanded_community_list(expanded_community_list)
        route.match_omp_tag(omp_tag)
        route.match_origin(origin)
        route.match_originator(originator)
        route.match_path_type(path_type)
        route.match_preference(preference)
        route.match_prefix_list(prefix_list)
        route.match_region(region_id, region_role)
        route.match_site(site_id)
        route.match_tloc(ip=tloc_ip, color=tloc_color, encap=tloc_encap)
        route.match_vpn_list(vpn_list_id)
        route.associate_affinity_action(action_affinity)
        route.associate_community_action(action_community, action_community_additive)
        route.associate_export_to_action(action_export_vpn_list_id)
        route.associate_omp_tag_action(action_omp_tag)
        route.associate_preference_action(action_preference)
        route.associate_service_action(
            action_service_type, action_service_vpn, tloc_list_id=action_service_tloc_list_id
        )
        # Arrange context
        context = PolicyConvertContext(lan_vpns_by_list_id=dict.fromkeys([vpn_list_id], vpn_list_entries))
        # Act
        parcel = convert(policy, uuid4(), context).output
        # Assert parcel
        assert isinstance(parcel, CustomControlParcel)
        assert parcel.parcel_name == name
        assert parcel.parcel_description == description
        assert parcel.default_action.value == default_action
        # Assert route sequence
        assert len(parcel.sequences) == 1
        seq = parcel.sequences[0]
        assert seq.sequence_type.value == "route"
        assert seq.sequence_ip_type.value == ip_type
        assert seq.sequence_name.value == seq_name
        assert seq.base_action.value == base_action
        entries = seq.match.entries
        assert entries[0].color_list.ref_id.value == str(color_list)
        assert entries[1].community.ref_id.value == str(community_list)
        assert entries[2].expanded_community.ref_id.value == str(expanded_community_list)
        assert entries[3].omp_tag.value == omp_tag
        assert entries[4].origin.value == origin
        assert entries[5].originator.value == str(originator)
        assert entries[6].path_type.value == path_type
        assert entries[7].preference.value == preference
        assert entries[8].prefix_list.ref_id.value == str(prefix_list)
        assert entries[9].regions[0].region.value == str(region_id)
        assert entries[10].role.value == region_role
        assert entries[11].site.value == [str(site_id)]
        assert entries[12].tloc.ip.value == str(tloc_ip)
        assert entries[12].tloc.color.value == tloc_color
        assert entries[12].tloc.encap.value == tloc_encap
        assert entries[13].vpn.value == vpn_list_entries
        action_set = seq.actions[0].set[0]
        assert action_set.affinity.value == action_affinity
        assert action_set.community.value == str(action_community)
        assert action_set.community_additive.value == action_community_additive

    def test_custom_control_with_tloc_sequence_conversion(self):
        # Arrange
        default_action = "accept"
        name = "custom_control"
        description = "Custom control policy"
        # Arrange policy
        policy = ControlPolicy(
            default_action=PolicyAcceptRejectAction(type=default_action),
            name=name,
            description=description,
        )
        # Arrange Tloc Sequence
        carrier = "carrier1"
        color_list = uuid4()
        domain_id = 100
        group_id = 200
        omp_tag = 2
        originator = IPv4Address("20.30.3.1")
        preference = 100
        region_list_id = uuid4()
        region_list_entries = ["Region-9", "Region-10"]
        region_role = "edge-router"
        site_list_id = uuid4()
        site_list_entries = ["SITE_100", "SITE_200"]
        tloc_list_id = uuid4()
        seq_name = "tloc_sequence"
        base_action = "accept"
        ip_type = "ipv4"
        action_affinity = 3
        action_omp_tag = 9
        action_preference = 11
        tloc = policy.add_tloc_sequence(
            name=seq_name,
            base_action=base_action,
            ip_type=ip_type,
        )
        tloc.match_carrier(carrier)
        tloc.match_color_list(color_list)
        tloc.match_domain_id(domain_id)
        tloc.match_group_id(group_id)
        tloc.match_omp_tag(omp_tag)
        tloc.match_originator(originator)
        tloc.match_preference(preference)
        tloc.match_region_list(region_list_id, region_role)
        tloc.match_site_list(site_list_id)
        tloc.match_tloc_list(tloc_list_id)
        tloc.associate_affinity_action(action_affinity)
        tloc.associate_omp_tag_action(action_omp_tag)
        tloc.associate_preference_action(action_preference)
        # Arrange context
        context = PolicyConvertContext(
            sites_by_list_id=dict.fromkeys([site_list_id], site_list_entries),
            regions_by_list_id=dict.fromkeys([region_list_id], region_list_entries),
        )
        # Act
        parcel = convert(policy, uuid4(), context).output
        # Assert parcel
        assert isinstance(parcel, CustomControlParcel)
        assert parcel.parcel_name == name
        assert parcel.parcel_description == description
        assert parcel.default_action.value == default_action
        # Assert tloc sequence
        assert len(parcel.sequences) == 1
        seq = parcel.sequences[0]
        assert seq.sequence_type.value == "tloc"
        assert seq.sequence_ip_type.value == ip_type
        assert seq.sequence_name.value == seq_name
        assert seq.base_action.value == base_action
        entries = seq.match.entries
        assert entries[0].carrier.value == carrier
        assert entries[1].color_list.ref_id.value == str(color_list)
        assert entries[2].domain_id.value == domain_id
        assert entries[3].group_id.value == group_id
        assert entries[4].omp_tag.value == omp_tag
        assert entries[5].originator.value == str(originator)
        assert entries[6].preference.value == preference
        assert entries[7].regions[0].region.value == region_list_entries[0]
        assert entries[7].regions[1].region.value == region_list_entries[1]
        assert entries[8].role.value == region_role
        assert entries[9].site.value == site_list_entries
        assert entries[10].tloc_list.ref_id.value == str(tloc_list_id)
