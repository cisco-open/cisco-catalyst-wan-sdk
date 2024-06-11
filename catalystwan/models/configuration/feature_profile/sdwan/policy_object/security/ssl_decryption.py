# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase

Action = Literal["decrypt", "drop"]
UnspportedModeAction = Literal["drop", "no-decrypt"]
CertificateRevocationStatus = Literal["ocsp", "none"]
FailureMode = Literal["close", "open"]
KeyModulus = Literal["1024", "2048", "4096"]
EckeyType = Literal["P256", "P384", "P521"]
TlsVersion = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]
CaTpLabel = Literal["PROXY-SIGNING-CA"]


class CaCertBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    default: Global[bool] = Field(default=Global[bool](value=True))
    file_name: Optional[Global[str]] = Field(default=None, validation_alias="fileName", serialization_alias="fileName")
    bundle_string: Optional[Global[str]] = Field(
        default=None, validation_alias="bundleString", serialization_alias="bundleString"
    )

    @classmethod
    def create(
        cls,
        default: bool = True,
        file_name: Optional[str] = None,
        bundle_string: Optional[str] = None,
    ) -> "CaCertBundle":
        return cls(
            default=Global[bool](value=default),
            file_name=Global[str](value=file_name) if file_name else None,
            bundle_string=Global[str](value=bundle_string) if bundle_string else None,
        )


class SslDecryptionParcel(_ParcelBase):
    type_: Literal["unified/ssl-decryption"] = Field(default="unified/ssl-decryption", exclude=True)
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    ssl_enable: Global[bool] = Field(default=Global[bool](value=True), validation_alias=AliasPath("data", "sslEnable"))
    expired_certificate: Global[Action] = Field(
        default=Global[Action](value="drop"), validation_alias=AliasPath("data", "expiredCertificate")
    )
    untrusted_certificate: Global[Action] = Field(
        default=Global[Action](value="drop"), validation_alias=AliasPath("data", "untrustedCertificate")
    )
    certificate_revocation_status: Global[CertificateRevocationStatus] = Field(
        default=Global[CertificateRevocationStatus](value="none"),
        validation_alias=AliasPath("data", "certificateRevocationStatus"),
    )
    unknown_status: Optional[Global[Action]] = Field(default=None, validation_alias=AliasPath("data", "unknownStatus"))
    unsupported_protocol_versions: Global[UnspportedModeAction] = Field(
        default=Global[Action](value="drop"), validation_alias=AliasPath("data", "unsupportedProtocolVersions")
    )
    unsupported_cipher_suites: Global[UnspportedModeAction] = Field(
        default=Global[Action](value="drop"), validation_alias=AliasPath("data", "unsupportedCipherSuites")
    )
    failure_mode: Global[FailureMode] = Field(
        default=Global[FailureMode](value="close"), validation_alias=AliasPath("data", "failureMode")
    )
    ca_cert_bundle: CaCertBundle = Field(default=CaCertBundle(), validation_alias=AliasPath("data", "caCertBundle"))
    key_modulus: Global[KeyModulus] = Field(
        default=Global[KeyModulus](value="1024"), validation_alias=AliasPath("data", "keyModulus")
    )
    eckey_type: Global[EckeyType] = Field(
        default=Global[EckeyType](value="P256"), validation_alias=AliasPath("data", "eckeyType")
    )
    certificate_lifetime: Global[str] = Field(
        default=Global[str](value="1"), validation_alias=AliasPath("data", "certificateLifetime")
    )
    min_tls_ver: Global[TlsVersion] = Field(
        default=Global[TlsVersion](value="TLSv1"), validation_alias=AliasPath("data", "minTlsVer")
    )
    ca_tp_label: Global[CaTpLabel] = Field(
        default=Global[CaTpLabel](value="PROXY-SIGNING-CA"), validation_alias=AliasPath("data", "caTpLabel")
    )

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        ssl_enable: bool = True,
        expired_certificate: Action = "drop",
        untrusted_certificate: Action = "drop",
        certificate_revocation_status: CertificateRevocationStatus = "none",
        unknown_status: Optional[Action] = None,
        unsupported_protocol_versions: UnspportedModeAction = "drop",
        unsupported_cipher_suites: UnspportedModeAction = "drop",
        failure_mode: FailureMode = "close",
        ca_cert_bundle: CaCertBundle = CaCertBundle(),
        key_modulus: KeyModulus = "1024",
        eckey_type: EckeyType = "P256",
        certificate_lifetime: str = "1",
        min_tls_ver: TlsVersion = "TLSv1",
        ca_tp_label: CaTpLabel = "PROXY-SIGNING-CA",
    ) -> "SslDecryptionParcel":
        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            ssl_enable=Global[bool](value=ssl_enable),
            expired_certificate=Global[Action](value=expired_certificate),
            untrusted_certificate=Global[Action](value=untrusted_certificate),
            certificate_revocation_status=Global[CertificateRevocationStatus](value=certificate_revocation_status),
            unknown_status=Global[Action](value=unknown_status) if unknown_status else None,
            unsupported_protocol_versions=Global[UnspportedModeAction](value=unsupported_protocol_versions),
            unsupported_cipher_suites=Global[UnspportedModeAction](value=unsupported_cipher_suites),
            failure_mode=Global[FailureMode](value=failure_mode),
            ca_cert_bundle=ca_cert_bundle,
            key_modulus=Global[KeyModulus](value=key_modulus),
            eckey_type=Global[EckeyType](value=eckey_type),
            certificate_lifetime=Global[str](value=certificate_lifetime),
            min_tls_ver=Global[TlsVersion](value=min_tls_ver),
            ca_tp_label=Global[CaTpLabel](value=ca_tp_label),
        )
