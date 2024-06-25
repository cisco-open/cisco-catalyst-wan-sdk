# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from uuid import uuid4

from catalystwan.api.configuration_groups.parcel import as_global
from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption_profile import (
    SslDecryptionProfileParcel,
)
from catalystwan.models.policy.definition.ssl_decryption_utd_profile import (
    SslDecryptionUtdProfileDefinition,
    SslDecryptionUtdProfilePolicy,
)
from catalystwan.models.policy.policy_definition import Reference
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestSslDecryptionConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_ssl_decryption_conversion(self):
        # Arrange
        url_white_list_ref = uuid4()
        url_black_list_ref = uuid4()
        ssl_decryption_profile = SslDecryptionUtdProfilePolicy(
            name="ssl_decryption",
            description="test_description",
            mode="security",
            optimized="false",
            definition=SslDecryptionUtdProfileDefinition(
                decrypt_categories=["auctions", "computer-and-internet-security"],
                never_decrypt_categories=["dynamic-content"],
                skip_decrypt_categories=["hacking"],
                reputation=True,
                fail_decrypt=True,
                decrypt_threshold="high-risk",
                filtered_url_white_list=[],
                filtered_url_black_list=[],
                url_white_list=Reference(ref=url_white_list_ref),
                url_black_list=Reference(ref=url_black_list_ref),
            ),
        )
        uuid = uuid4()
        # Act
        parcel = convert(ssl_decryption_profile, uuid, context=self.context).output
        # Assert
        assert isinstance(parcel, SslDecryptionProfileParcel)
        assert parcel.parcel_name == "ssl_decryption"
        assert parcel.parcel_description == "test_description"
        assert parcel.decrypt_categories.value == ["auctions", "computer-and-internet-security"]
        assert parcel.never_decrypt_categories.value == ["dynamic-content"]
        assert parcel.skip_decrypt_categories.value == ["hacking"]
        assert parcel.reputation.value is True
        assert parcel.fail_decrypt.value is True
        assert parcel.decrypt_threshold.value == "high-risk"
        assert parcel.url_allowed_list.ref_id == as_global(str(url_white_list_ref))
        assert parcel.url_blocked_list.ref_id == as_global(str(url_black_list_ref))

        assert len(self.context.ssl_profile_residues) == 0

    def test_ssl_decryption_conversion_woth_residues(self):
        filtered_lists_sets = (
            (["dummy"], []),
            ([], ["dummy"]),
            (["dummy"], ["dummy"]),
        )

        url_white_list_ref = uuid4()
        url_black_list_ref = uuid4()

        for filtered_url_black_list, filtered_url_white_list in enumerate(filtered_lists_sets):
            with self.subTest():
                ssl_decryption_profile = SslDecryptionUtdProfilePolicy(
                    name="ssl_decryption",
                    description="test_description",
                    mode="security",
                    optimized="false",
                    definition=SslDecryptionUtdProfileDefinition.model_construct(
                        decrypt_categories=["auctions", "computer-and-internet-security"],
                        never_decrypt_categories=["dynamic-content"],
                        skip_decrypt_categories=["hacking"],
                        reputation=True,
                        fail_decrypt=True,
                        decrypt_threshold="high-risk",
                        filtered_url_white_list=filtered_url_white_list,
                        filtered_url_black_list=filtered_url_black_list,
                        url_white_list=Reference(ref=url_white_list_ref),
                        url_black_list=Reference(ref=url_black_list_ref),
                    ),
                )
                uuid = uuid4()
                convert(ssl_decryption_profile, uuid, context=self.context)

        assert len(self.context.ssl_profile_residues) == 3
