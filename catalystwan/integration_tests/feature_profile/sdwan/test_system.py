from catalystwan.integration_tests.feature_profile.sdwan.base import TestFeatureProfileModels
from catalystwan.models.configuration.feature_profile.sdwan.system import (
    BannerParcel,
    BasicParcel,
    BFDParcel,
    GlobalParcel,
    LoggingParcel,
    MRFParcel,
    NTPParcel,
    OMPParcel,
    SecurityParcel,
    SNMPParcel,
)


class TestSystemFeatureProfileModels(TestFeatureProfileModels):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.api = cls.session.api.sdwan_feature_profiles.system
        cls.profile_uuid = cls.api.create_profile("TestProfileService", "Description").id

    def test_when_default_values_banner_parcel_expect_successful_post(self):
        # Arrange
        banner_parcel = BannerParcel(
            parcel_name="BannerDefault",
            parcel_description="Banner Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, banner_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_banner_parcel_expect_successful_post(self):
        # Arrange
        banner_parcel = BannerParcel(
            parcel_name="BannerFullySpecified",
            parcel_description="Banner Parcel",
        )
        banner_parcel.add_login("Login")
        banner_parcel.add_motd("Hello! Welcome to the network!")
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, banner_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_logging_parcel_expect_successful_post(self):
        # Arrange
        logging_parcel = LoggingParcel(
            parcel_name="LoggingDefault",
            parcel_description="Logging Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, logging_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_logging_parcel_expect_successful_post(self):
        # Arrange
        logging_parcel = LoggingParcel(
            parcel_name="LoggingFullySpecified",
            parcel_description="Logging Parcel",
        )
        logging_parcel.set_disk(
            enable=True,
            disk_file_rotate=10,
            disk_file_size=10,
        )
        logging_parcel.add_tls_profile(
            profile="TLSProfile",
            version="TLSv1.2",
            ciphersuite_list=[
                "aes-256-cbc-sha",
                "aes-128-cbc-sha",
                "ecdhe-ecdsa-aes-gcm-sha2",
                "ecdhe-rsa-aes-cbc-sha2",
            ],
        )
        logging_parcel.add_ipv4_server(
            name="Server1",
            vpn=0,
            source_interface="fastethernet1/0",
            priority="debugging",
            enable_tls=True,
            custom_profile=True,
            profile_properties="TLSProfile",
        )
        logging_parcel.add_ipv6_server(
            name="Server2",
            vpn=0,
            source_interface="fastethernet1/1",
            priority="debugging",
            enable_tls=True,
            custom_profile=True,
            profile_properties="TLSProfile",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, logging_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_bfd_parcel_expect_successful_post(self):
        # Arrange
        bfd_parcel = BFDParcel(
            parcel_name="BFDDefault",
            parcel_description="BFD Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, bfd_parcel).id
        # Assert
        assert parcel_id

    def test_when_fully_specified_bfd_parcel_expect_successful_post(self):
        # Arrange
        bfd_parcel = BFDParcel(
            parcel_name="BFDFullySpecified",
            parcel_description="BFD Parcel",
        )
        bfd_parcel.set_muliplier(1)
        bfd_parcel.set_poll_interval(700000)
        bfd_parcel.set_default_dscp(51)
        bfd_parcel.add_color(color="lte", hello_interval=300000, multiplier=7, pmtu_discovery=False)
        bfd_parcel.add_color(color="mpls", pmtu_discovery=False)
        bfd_parcel.add_color(color="biz-internet")
        bfd_parcel.add_color(color="public-internet")
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, bfd_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_basic_parcel_expect_successful_post(self):
        # Arrange
        basic_parcel = BasicParcel(
            parcel_name="BasicDefault",
            parcel_description="Basic Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, basic_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_security_parcel_expect_successful_post(self):
        # Arrange
        security_parcel = SecurityParcel(
            parcel_name="SecurityDefault",
            parcel_description="Security Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, security_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_ntp_parcel_expect_successful_post(self):
        # Arrange
        ntp_parcel = NTPParcel(
            parcel_name="NTPDefault",
            parcel_description="NTP Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, ntp_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_global_parcel_expect_successful_post(self):
        # Arrange
        global_parcel = GlobalParcel(
            parcel_name="GlobalDefault",
            parcel_description="Global Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, global_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_mrf_parcel_expect_successful_post(self):
        # Arrange
        mrf_parcel = MRFParcel(
            parcel_name="MRFDefault",
            parcel_description="MRF Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, mrf_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_snmp_parcel_expect_successful_post(self):
        # Arrange
        snmp_parcel = SNMPParcel(
            parcel_name="SNMPDefault",
            parcel_description="SNMP Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, snmp_parcel).id
        # Assert
        assert parcel_id

    def test_when_default_values_omp_parcel_expect_successful_post(self):
        # Arrange
        omp_parcel = OMPParcel(
            parcel_name="OMPDefault",
            parcel_description="OMP Parcel",
        )
        # Act
        parcel_id = self.api.create_parcel(self.profile_uuid, omp_parcel).id
        # Assert
        assert parcel_id

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.delete_profile(cls.profile_uuid)
        super().tearDownClass()
