import unittest
from uuid import uuid4

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.application_list import (
    ApplicationListParcel,
)
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.application_list import (
    SecurityApplicationListParcel,
)
from catalystwan.models.policy.list.app import AppList
from catalystwan.models.policy.list.local_app import LocalAppList
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert


class TestAppListConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_app_list_conversion(self):
        policy = AppList(
            name="app_list",
            description="app list description",
        )
        policy.add_app_family("TestFamily")
        policy.add_app_family("TestFamily2")
        # Act
        parcel = convert(policy, uuid4(), self.context).output
        # Assert
        assert isinstance(parcel, ApplicationListParcel)
        assert parcel.parcel_name == "app_list"
        assert parcel.parcel_description == "app list description"
        assert len(parcel.entries) == 2
        assert parcel.entries[0].app_list_family.value == "TestFamily"
        assert parcel.entries[1].app_list_family.value == "TestFamily2"


class TestLocalAppListConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_local_app_list_conversion(self):
        policy = LocalAppList(
            name="local_app_list",
            description="app list description",
        )
        policy.add_app_family("TestFamily")
        policy.add_app_family("TestFamily2")
        # Act
        parcel = convert(policy, uuid4(), self.context).output
        # Assert
        assert isinstance(parcel, SecurityApplicationListParcel)
        assert parcel.parcel_name == "local_app_list"
        assert parcel.parcel_description == "app list description"
        assert len(parcel.entries) == 2
        assert parcel.entries[0].app_list_family.value == "TestFamily"
        assert parcel.entries[1].app_list_family.value == "TestFamily2"
