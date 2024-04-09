import os
import unittest
from typing import cast
from uuid import UUID

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.api.feature_profile_api import ServiceFeatureProfileAPI, TopologyFeatureProfileAPI
from catalystwan.models.configuration.feature_profile.sdwan.service.lan.vpn import LanVpnParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.session import ManagerSession, create_manager_session


class TestTopologyFeatureProfile(unittest.TestCase):
    session: ManagerSession
    topology_api: TopologyFeatureProfileAPI
    topology_profile_id: UUID
    service_api: ServiceFeatureProfileAPI
    service_profile_id: UUID
    lanvpn_parcel_name: str
    lanvpn_parcel_id: UUID

    @classmethod
    def setUpClass(cls) -> None:
        cls.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )
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

    # TODO: need service parcel vpn api implemented to create referenced VPN-1 as precondition
    def test_mesh(self):
        mesh = MeshParcel(parcel_name="MeshParcel-1")
        mesh.add_target_vpn(self.lanvpn_parcel_name)
        mesh.add_site("SITE-1")
        mesh_id = self.topology_api.create_parcel(self.topology_profile_id, mesh).id
        self.topology_api.delete_parcel(self.topology_profile_id, MeshParcel, mesh_id)

    # TODO: need service parcel vpn api implemented to create referenced VPN-1 as precondition
    def test_hubspoke(self):
        hubspoke = HubSpokeParcel(parcel_name="HubSpokeParcel-1")
        spoke = hubspoke.add_spoke(name="Spoke-1", spoke_sites=["SITE-1"])
        spoke.add_spoke_site("SITE-2")
        spoke.add_hub_site(["SITE-3"], preference=100891)
        hubspoke.add_target_vpn(self.lanvpn_parcel_name)
        hubspoke.add_selected_hub("HUB-1")
        hubspoke_id = self.topology_api.create_parcel(self.topology_profile_id, hubspoke).id
        self.topology_api.delete_parcel(self.topology_profile_id, HubSpokeParcel, hubspoke_id)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.topology_api.delete_profile(cls.topology_profile_id)
        cls.service_api.delete_profile(cls.service_profile_id)
        cls.session.close()
