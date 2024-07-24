import unittest

from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.policy.as_path import AsPathParcel
from catalystwan.models.policy.list.as_path import ASPathList, ASPathListEntry
from catalystwan.utils.config_migration.converters.policy.policy_lists import convert


class TestAsPathConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_aspath_with_name_conversion(self):
        # Arrange
        name = "aspath"
        description = "aspath description"
        entry_1 = "600008"
        entry_2 = "600009"
        entry_3 = "600010"
        aspath = ASPathList(
            name=name,
            description=description,
        )
        for entry in [entry_1, entry_2, entry_3]:
            aspath._add_entry(ASPathListEntry(as_path=entry))
        # Act
        parcel = convert(aspath, self.context).output
        # Assert
        assert isinstance(parcel, AsPathParcel)
        assert parcel.parcel_name == name
        assert parcel.parcel_description == description
        assert len(parcel.entries) == 3
        assert parcel.entries[0].as_path.value == entry_1
        assert parcel.entries[1].as_path.value == entry_2
        assert parcel.entries[2].as_path.value == entry_3
        assert parcel.as_path_list_num.value == self.context.as_path_list_num_mapping[name]

    def test_aspath_with_number_conversion(self):
        # Arrange
        name = "490"
        description = "aspath description"
        aspath = ASPathList(
            name=name,
            description=description,
        )
        # Act
        parcel = convert(aspath, self.context).output
        # Assert
        assert isinstance(parcel, AsPathParcel)
        assert parcel.parcel_name == name
        assert parcel.parcel_description == description
        assert len(parcel.entries) == 0
        assert parcel.as_path_list_num.value == 490
