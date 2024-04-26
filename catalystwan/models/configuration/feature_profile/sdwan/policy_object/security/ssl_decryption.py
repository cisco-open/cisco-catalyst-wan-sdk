# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase

Action = Literal["decrypt", "drop"]
CertificateRevocationStatus = Literal["oscp", "none"]
FailureMode = Literal["close", "open"]
KeyModulus = Literal["1024", "2048", "4096"]
EckeyType = Literal["P256", "P384", "P521"]
TlsVersion = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]
CaTpLabel = Literal["PROXY-SIGNING-CA"]


class CaCertBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    default: Global[bool] = Field(default=Global[bool](value=True), validation_alias="default")
    file_name: Global[str] = Field(default=None, validation_alias="fileName")
    bundle_string: Global[str] = Field(default=None, validation_alias="bundle_string")


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
    unknown_status: Global[Action] = Field(default=None, validation_alias=AliasPath("data", "unknownStatus"))
    unsupported_protocol_versions: Global[Action] = Field(
        default=Global[Action](value="drop"), validation_alias=AliasPath("data", "unsupportedProtocolVersions")
    )
    unsupported_cipher_suites: Global[Action] = Field(
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
