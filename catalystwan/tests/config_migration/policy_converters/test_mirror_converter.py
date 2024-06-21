import unittest

from catalystwan.models.configuration.feature_profile.sdwan.policy_object import MirrorParcel
from catalystwan.models.policy.list.mirror import MirrorList, MirrorListEntry
from catalystwan.utils.config_migration.converters.policy.policy_lists import mirror


class TestMirrorConverter(unittest.TestCase):
    def test_mirror_policy_list_conversion_1(self):
        mirror_v1 = MirrorList(
            name="mirror_list",
            entries=[
                MirrorListEntry(remote_dest="1.2.3.4", source="11:22:33::66"),
            ],
        )

        v2_parcel = mirror(mirror_v1, context=None).output

        assert type(v2_parcel) is MirrorParcel

    def test_mirror_policy_list_conversion_2(self):
        mirror_v1 = MirrorList(
            name="mirror_list",
            entries=[
                MirrorListEntry(remote_dest="1:2::5", source="10.20.30.40"),
            ],
        )

        v2_parcel = mirror(mirror_v1, context=None).output

        assert type(v2_parcel) is MirrorParcel
