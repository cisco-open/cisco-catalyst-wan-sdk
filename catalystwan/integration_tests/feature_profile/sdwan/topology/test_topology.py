from ipaddress import IPv4Address
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI, TopologyFeatureProfileAPI
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.custom_control import CustomControlParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel


class TestTopologyFeatureProfile(TestFeatureProfileModels):
    topology_api: TopologyFeatureProfileAPI
    topology_profile_id: UUID
    service_api: ServiceFeatureProfileAPI
    service_profile_id: UUID
    lanvpn_parcel_name: str
    lanvpn_parcel_id: UUID

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.topology_api = cls.session.api.sdwan_feature_profiles.topology
        cls.topology_profile_id = cls.topology_api.create_profile("TestProfile", "Description").id
        # preconditions
        cls.lanvpn_parcel_name = "VPN-1"
        cls.service_api = cls.session.api.sdwan_feature_profiles.service
        cls.service_profile_id = cls.service_api.create_profile("PreconditionServiceProfile", "Description").id
        lanvpn_parcel = LanVpnParcel(
            parcel_name=cls.lanvpn_parcel_name,
            parcel_description="Test Vpn Parcel",
            vpn_id=as_global(2),
        )
        cls.lanvpn_parcel_id = cls.service_api.create_parcel(cls.service_profile_id, lanvpn_parcel).id

    def test_mesh(self):
        mesh = MeshParcel(parcel_name="MeshParcel-1")
        mesh.add_target_vpn(self.lanvpn_parcel_name)
        mesh.add_site("SITE-1")
        # create
        mesh_id = self.topology_api.create_parcel(self.topology_profile_id, mesh).id
        # get
        self.topology_api.get_parcel(self.topology_profile_id, MeshParcel, mesh_id)
        # delete
        self.topology_api.delete_parcel(self.topology_profile_id, MeshParcel, mesh_id)

    def test_hubspoke(self):
        hubspoke = HubSpokeParcel(parcel_name="HubSpokeParcel-1")
        spoke = hubspoke.add_spoke(name="Spoke-1", spoke_sites=["SITE-1"])
        spoke.add_spoke_site("SITE-2")
        spoke.add_hub_site(["SITE-3"], preference=100891)
        hubspoke.add_target_vpn(self.lanvpn_parcel_name)
        hubspoke.add_selected_hub("HUB-1")
        # create
        hubspoke_id = self.topology_api.create_parcel(self.topology_profile_id, hubspoke).id
        # get
        self.topology_api.get_parcel(self.topology_profile_id, HubSpokeParcel, hubspoke_id)
        # delete
        self.topology_api.delete_parcel(self.topology_profile_id, HubSpokeParcel, hubspoke_id)

    def test_custom_control(self):
        cc = CustomControlParcel(parcel_name="CustomControlParcel-1")
        cc.set_default_action("accept")
        cc.assign_target([self.lanvpn_parcel_name])
        s = cc.add_sequence("my_sequence", 1, "route", "ipv4", "reject")
        s.match_carrier("carrier4")
        s.match_domain_id(555)
        s.match_group_id(80)
        s.match_omp_tag(999)
        s.match_origin("eigrp-summary")
        s.match_originator(IPv4Address("10.0.0.1"))
        s.match_path_type("hierarchical-path")
        s.match_preference(1000)
        s.match_tloc(IPv4Address("10.0.0.1"), "biz-internet", "ipsec")
        s.match_vpns(["VPN-1"])
        # create
        cc_id = self.topology_api.create_parcel(self.topology_profile_id, cc).id
        # get
        self.topology_api.get_parcel(self.topology_profile_id, CustomControlParcel, cc_id)
        # delete
        self.topology_api.delete_parcel(self.topology_profile_id, CustomControlParcel, cc_id)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.topology_api.delete_profile(cls.topology_profile_id)
        cls.service_api.delete_profile(cls.service_profile_id)
        cls.session.close()
