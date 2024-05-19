from typing import List

import pytest

from catalystwan.api.configuration_groups.parcel import Default, Global
from catalystwan.exceptions import ManagerHTTPError
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.application_priority import (
    PolicySettingsParcel,
    QosMap,
    QosPolicyParcel,
    TrafficPolicyParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.qos_policy import QosPolicyTarget
from catalystwan.models.configuration.feature_profile.sdwan.application_priority.traffic_policy import (
    BaseAction,
    Direction,
    TrafficPolicyTarget,
)


class TestPolicySettingsParcel(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile("TestApplicationPriorityProfile", "Description").id

    def test_create_policy_settings_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

        assert parcel.parcel_name == "policy_settings_test_parcel"

    def test_update_policy_settings_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
            app_visibility=Default[bool](value=False),
            flow_visibility=Global[bool](value=True),
            app_visibility_ipv6=Global[bool](value=True),
            flow_visibility_ipv6=Global[bool](value=True),
        )
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload
        parcel.app_visibility = Global[bool](value=True)
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

        # Assert
        assert parcel.app_visibility == Global[bool](value=True)

    def test_delete_qos_policy_parcel(self):
        policy_settings_parcel = PolicySettingsParcel(
            name="policy_settings_test_parcel",
            app_visibility=Global[bool](value=True),
            flow_visibility=Global[bool](value=True),
            app_visibility_ipv6=Global[bool](value=True),
            flow_visibility_ipv6=Global[bool](value=True),
        )
        parcel_id = self.api.create_parcel(self.profile_id, policy_settings_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, PolicySettingsParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, PolicySettingsParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)


class TestQosPolicyParcel(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile("TestApplicationPriorityProfile", "Description").id

    def test_create_qos_policy_parcel(self):
        qos_policy_parcel = QosPolicyParcel(
            name="qos_policy_test_parcel",
            qos_map=QosMap(qos_schedulers=[]),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, qos_policy_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload

        assert parcel.parcel_name == "qos_policy_test_parcel"
        assert len(parcel.qos_map.qos_schedulers) == 0

    def test_update_qos_policy_parcel(self):
        qos_policy_parcel = QosPolicyParcel(
            name="qos_policy_test_parcel",
            qos_map=QosMap(qos_schedulers=[]),
            target=QosPolicyTarget(interfaces=Global[List[str]](value=["GigabitEthernet1"])),
        )
        parcel_id = self.api.create_parcel(self.profile_id, qos_policy_parcel).id
        parcel = self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload
        parcel.target = QosPolicyTarget(interfaces=Global[List[str]](value=["GigabitEthernet2"]))
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload

        # Assert
        assert parcel.target == QosPolicyTarget(interfaces=Global[List[str]](value=["GigabitEthernet2"]))

    def test_delete_qos_policy_parcel(self):
        qos_policy_parcel = QosPolicyParcel(
            name="qos_policy_test_parcel",
            qos_map=QosMap(qos_schedulers=[]),
        )
        parcel_id = self.api.create_parcel(self.profile_id, qos_policy_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, QosPolicyParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, QosPolicyParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)


class TestTrafficPolicyParcel(TestFeatureProfileModels):
    def setUp(self) -> None:
        self.api = self.session.api.sdwan_feature_profiles.application_priority
        self.profile_id = self.api.create_profile("TestApplicationPriorityProfile", "Description").id

    def test_create_traffic_policy_parcel(self):
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[BaseAction](value="accept"),
            target=TrafficPolicyTarget(
                direction=Global[Direction](value="all"), vpn=Global[List[str]](value=["VPN_1"])
            ),
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        # Assert
        assert parcel_id
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

        assert parcel.parcel_name == "traffic_policy_test_parcel"

    def test_update_traffic_policy_parcel(self):
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[BaseAction](value="accept"),
            target=TrafficPolicyTarget(
                direction=Global[Direction](value="all"), vpn=Global[List[str]](value=["VPN_1"])
            ),
        )
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload
        parcel.target = TrafficPolicyTarget(
            direction=Global[Direction](value="service"), vpn=Global[List[str]](value=["VPN_2"])
        )
        # Act
        self.api.update_parcel(self.profile_id, parcel, parcel_id)
        parcel = self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

        # Assert
        assert parcel.target == TrafficPolicyTarget(
            direction=Global[Direction](value="service"), vpn=Global[List[str]](value=["VPN_2"])
        )

    def test_delete_traffic_policy_parcel(self):
        traffic_policy_parcel = TrafficPolicyParcel(
            name="traffic_policy_test_parcel",
            data_default_action=Global[BaseAction](value="accept"),
            target=TrafficPolicyTarget(
                direction=Global[Direction](value="all"), vpn=Global[List[str]](value=["VPN_1"])
            ),
        )
        parcel_id = self.api.create_parcel(self.profile_id, traffic_policy_parcel).id
        # Act
        self.api.delete_parcel(self.profile_id, TrafficPolicyParcel, parcel_id)

        # Assert
        with pytest.raises(ManagerHTTPError):
            self.api.get_parcel(self.profile_id, TrafficPolicyParcel, parcel_id).payload

    def tearDown(self) -> None:
        self.api.delete_profile(self.profile_id)
