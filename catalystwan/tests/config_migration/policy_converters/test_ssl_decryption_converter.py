# Copyright 2024 Cisco Systems, Inc. and its affiliates
import unittest
from uuid import uuid4

from catalystwan.models.common import VpnId
from catalystwan.models.configuration.config_migration import PolicyConvertContext
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption import (
    SslDecryptionParcel,
)
from catalystwan.models.policy.definition.ssl_decryption import (
    CaCertBundle,
    ControlPolicyBaseAction,
    NetworkDecryptionRuleSequence,
    SslDecryptionDefinition,
    SslDecryptionPolicy,
    SslDecryptionSettings,
    UrlProfile,
)
from catalystwan.utils.config_migration.converters.policy.policy_definitions import convert


class TestSslDecryptionConverter(unittest.TestCase):
    def setUp(self) -> None:
        self.context = PolicyConvertContext()

    def test_ssl_decryption_conversion(self):
        # Arrange
        ssl_decryption_v1_entry = SslDecryptionPolicy(
            name="ssl_decryption",
            description="test_description",
            mode="security",
            definition=SslDecryptionDefinition(
                default_action=ControlPolicyBaseAction(type="doNotDecrypt"),
                sequences=[
                    NetworkDecryptionRuleSequence(
                        sequence_name="test_sequence",
                    )
                ],
                profiles=[UrlProfile(name="test_profile", order_no=2, vpn=[VpnId(3)], ref=uuid4())],
                settings=SslDecryptionSettings(
                    ssl_enable="true",
                    expired_certificate="drop",
                    untrusted_certificate="drop",
                    certificate_revocation_status="none",
                    unknown_status="drop",
                    unsupported_protocol_versions="drop",
                    unsupported_cipher_suites="drop",
                    failure_mode="close",
                    ca_cert_bundle=CaCertBundle(default=True, file_name="test_file", bundle_string="test_string"),
                ),
            ),
        )
        uuid = uuid4()

        # Act
        parcel = convert(ssl_decryption_v1_entry, uuid, context=self.context).output
        # Assert
        assert isinstance(parcel, SslDecryptionParcel)
        assert parcel.parcel_name == "ssl_decryption"
        assert parcel.parcel_description == "test_description"
        assert parcel.ssl_enable.value is True
        assert parcel.expired_certificate.value == "drop"
        assert parcel.untrusted_certificate.value == "drop"
        assert parcel.certificate_revocation_status.value == "none"
        assert parcel.unknown_status is None  # because certificate_revocation_status == "none"
        assert parcel.unsupported_protocol_versions.value == "drop"
        assert parcel.unsupported_cipher_suites.value == "drop"
        assert parcel.failure_mode.value == "close"
        assert parcel.ca_cert_bundle.default.value is True
        assert parcel.ca_cert_bundle.file_name.value == "test_file"
        assert parcel.ca_cert_bundle.bundle_string.value == "test_string"
        assert self.context.ssl_decryption_residues[uuid].profiles == ssl_decryption_v1_entry.definition.profiles
        assert self.context.ssl_decryption_residues[uuid].sequences == ssl_decryption_v1_entry.definition.sequences

    def test_ssl_decryption_conversion_with_custom_certificate(self):
        ssl_decryption_v1_entry = SslDecryptionPolicy(
            name="ssl_decryption",
            description="test_description",
            mode="security",
            definition=SslDecryptionDefinition(
                default_action=ControlPolicyBaseAction(type="doNotDecrypt"),
                sequences=[
                    NetworkDecryptionRuleSequence(
                        sequence_name="test_sequence",
                    )
                ],
                profiles=[UrlProfile(name="test_profile", order_no=2, vpn=[VpnId(3)], ref=uuid4())],
                settings=SslDecryptionSettings(
                    ssl_enable="true",
                    expired_certificate="drop",
                    untrusted_certificate="drop",
                    certificate_revocation_status="none",
                    unknown_status="drop",
                    unsupported_protocol_versions="drop",
                    unsupported_cipher_suites="drop",
                    failure_mode="close",
                    ca_cert_bundle=CaCertBundle(
                        default=False, file_name="certificate.ca-bundle", bundle_string="fdsfsdfsdfsd\nfsfs\n\n"
                    ),
                ),
            ),
        )
        uuid = uuid4()

        # Act
        parcel = convert(ssl_decryption_v1_entry, uuid, context=self.context).output
        # # Assert
        assert isinstance(parcel, SslDecryptionParcel)
        assert parcel.ca_cert_bundle.default.value is False
        assert parcel.ca_cert_bundle.file_name.value == "certificate.ca-bundle"
        assert parcel.ca_cert_bundle.bundle_string.value == "fdsfsdfsdfsd\nfsfs\n\n"
