from catalystwan.api.feature_profile_api import PolicyObjectFeatureProfileAPI
from catalystwan.endpoints.configuration_feature_profile import ConfigurationFeatureProfile
from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.policy_object.security.ssl_decryption import (
    CaCertBundle,
    SslDecryptionParcel,
)
from catalystwan.typed_list import DataSequence

PROFILE_NAME = "Default_Policy_Object_Profile"


class TestSslDecryptionParcel(TestFeatureProfileModels):
    policy_api: PolicyObjectFeatureProfileAPI

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.policy_api = cls.session.api.sdwan_feature_profiles.policy_object
        cls.profile_uuid = (
            ConfigurationFeatureProfile(cls.session.api.sdwan_feature_profiles.policy_object.session)
            .get_sdwan_feature_profiles()
            .filter(profile_name=PROFILE_NAME)
            .single_or_default()
        ).profile_id

    def setUp(self) -> None:
        self.created_id = None
        return super().setUp()

    def tearDown(self) -> None:
        if self.created_id:
            self.policy_api.delete(self.profile_uuid, SslDecryptionParcel, self.created_id)

        return super().tearDown()

    def test_create_ssl_decryption_parcel(self):
        cert_bundle = CaCertBundle.create(
            default=False, bundle_string="cert_content", file_name="certificate.ca-bundle"
        )

        ssl_decryption_parcel = SslDecryptionParcel.create(
            parcel_name="test_ssl_profile",
            parcel_description="description",
            ssl_enable=True,
            expired_certificate="drop",
            untrusted_certificate="drop",
            certificate_revocation_status="none",
            unknown_status=None,
            unsupported_protocol_versions="drop",
            unsupported_cipher_suites="drop",
            failure_mode="open",
            ca_cert_bundle=cert_bundle,
            key_modulus="4096",
            eckey_type="P384",
            certificate_lifetime="1",
            min_tls_ver="TLSv1.1",
        )

        self.created_id = self.policy_api.create_parcel(self.profile_uuid, ssl_decryption_parcel).id
        read_parcel = self.policy_api.get(self.profile_uuid, SslDecryptionParcel, parcel_id=self.created_id)

        assert read_parcel.payload.parcel_name == "test_ssl_profile"
        assert read_parcel.payload.parcel_description == "description"
        assert read_parcel.payload.ssl_enable.value is True
        assert read_parcel.payload.expired_certificate.value == "drop"
        assert read_parcel.payload.untrusted_certificate.value == "drop"
        assert read_parcel.payload.certificate_revocation_status.value == "none"
        assert read_parcel.payload.unknown_status is None
        assert read_parcel.payload.unsupported_protocol_versions.value == "drop"
        assert read_parcel.payload.unsupported_cipher_suites.value == "drop"
        assert read_parcel.payload.failure_mode.value == "open"
        assert read_parcel.payload.key_modulus.value == "4096"
        assert read_parcel.payload.eckey_type.value == "P384"
        assert read_parcel.payload.certificate_lifetime.value == "1"
        assert read_parcel.payload.min_tls_ver.value == "TLSv1.1"
        assert read_parcel.payload.ca_cert_bundle.default.value is False
        assert read_parcel.payload.ca_cert_bundle.file_name.value == "certificate.ca-bundle"
        assert read_parcel.payload.ca_cert_bundle.bundle_string.value == "cert_content"

    def test_get_all_ssl_decryption_parcels(self):
        parcels = self.policy_api.get(self.profile_uuid, SslDecryptionParcel)
        assert type(parcels) is DataSequence
