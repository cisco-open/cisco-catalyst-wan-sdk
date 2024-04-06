import os
import unittest
from typing import cast
from uuid import UUID

from catalystwan.api.feature_profile_api import TopologyFeatureProfileAPI
from catalystwan.models.configuration.feature_profile.sdwan.topology.hubspoke import HubSpokeParcel
from catalystwan.models.configuration.feature_profile.sdwan.topology.mesh import MeshParcel
from catalystwan.session import ManagerSession, create_manager_session


class TestTopologyFeatureProfileModels(unittest.TestCase):
    session: ManagerSession
    api: TopologyFeatureProfileAPI
    profile_id: UUID

    @classmethod
    def setUpClass(cls) -> None:
        cls.session = create_manager_session(
            url=cast(str, os.environ.get("TEST_VMANAGE_URL")),
            port=cast(int, int(os.environ.get("TEST_VMANAGE_PORT"))),  # type: ignore
            username=cast(str, os.environ.get("TEST_VMANAGE_USERNAME")),
            password=cast(str, os.environ.get("TEST_VMANAGE_PASSWORD")),
        )
        cls.api = cls.session.api.sdwan_feature_profiles.topology
        cls.profile_id = cls.api.create_profile("TestProfile", "Description").id

    # TODO: need service parcel vpn api implemented to create referenced VPN-1 as precondition
    def test_mesh(self):
        mesh = MeshParcel(parcel_name="MeshParcel-1")
        mesh.add_target_vpn("VPN-1")
        mesh.add_site("SITE-1")
        mesh_id = self.api.create_parcel(self.profile_id, mesh)
        self.api.delete_parcel(self.profile_id, MeshParcel, mesh_id)

    # TODO: need service parcel vpn api implemented to create referenced VPN-1 as precondition
    def test_hubspoke(self):
        hubspoke = HubSpokeParcel(parcel_name="HubSpokeParcel-1")
        spoke = hubspoke.add_spoke(name="Spoke-1", spoke_sites=["SITE-1"])
        spoke.add_spoke_site("SITE-2")
        spoke.add_hub_site(["SITE-3"], preference=100891)
        hubspoke.add_target_vpn("VPN-1")
        hubspoke.add_selected_hub("HUB-1")
        hubspoke_id = self.api.create_parcel(self.profile_id, hubspoke)
        self.api.delete_parcel(self.profile_id, HubSpokeParcel, hubspoke_id)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_id)
        cls.session.close()
