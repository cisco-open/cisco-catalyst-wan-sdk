import unittest

from catalystwan.models.policy.list.communities import ExtendedCommunityList
from catalystwan.utils.config_migration.converters.policy.policy_lists import extended_community


class TestExtendedCommunityConverter(unittest.TestCase):
    def test_conversion_entry_without_community_prefix(self):
        community_list = ExtendedCommunityList(name="ext_community_1")
        community_list.add_route_target_community(100, 1000)
        community_list.add_site_of_origin_community("1.2.3.4", 1000)

        extended_community_parcel = extended_community(community_list, None).output
        assert extended_community_parcel is not None

        assert len(extended_community_parcel.entries) == 2
        assert extended_community_parcel.entries[0].extended_community.value == "rt 100:1000"
        assert extended_community_parcel.entries[1].extended_community.value == "soo 1.2.3.4:1000"

    def test_conversion_entry_with_community_prefix(self):
        community_list = ExtendedCommunityList(name="ext_community_1")
        community_list.add_route_target_community(123, 1234, name="dummy prefix")
        community_list.add_site_of_origin_community("1.2.3.4", 2000, name="community")

        extended_community_parcel = extended_community(community_list, None).output
        assert extended_community_parcel is not None

        assert len(extended_community_parcel.entries) == 2
        assert extended_community_parcel.entries[0].extended_community.value == "rt 123:1234"
        assert extended_community_parcel.entries[1].extended_community.value == "soo 1.2.3.4:2000"

    def test_conversion_raises_conversion_error_when_soo_with_ipv6_used(self):
        community_list = ExtendedCommunityList(name="ext_community_1")
        community_list.add_site_of_origin_community("1:2:3::5", 2000, name="community")

        result = extended_community(community_list, None)
        assert result.status == "failed"
