# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import PolicyModeType, VpnId
from catalystwan.models.policy.policy_definition import (
    AppListEntry,
    DefinitionWithSequencesCommonBase,
    DestinationDataPrefixListEntry,
    DestinationIPEntry,
    DestinationPortEntry,
    DestinationVpnEntry,
    Match,
    MatchEntry,
    PolicyActionBase,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    PolicyDefinitionSequenceBase,
    SourceDataPrefixListEntry,
    SourceIPEntry,
    SourcePortEntry,
    SourceVpnEntry,
)

CertificateCheckAction = Literal["drop", "decrypt"]
UnspportedModeAction = Literal["drop", "no-decrypt"]
CertificateRevocation = Literal["none", "ocsp"]
FailureMode = Literal["close", "open"]
KeyModulus = Literal["1024", "2048", "4096"]
EcKeyType = Literal["P256", "P384", "P521"]
TlsVersion = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]
CaTpLabel = Literal["PROXY-SIGNING-CA"]
StrBool = Literal["false", "true"]


SslSecurityPolicyBaseActionType = Literal["decrypt", "doNotDecrypt", "noIntent"]


class ControlPolicyBaseAction(PolicyActionBase):
    type: SslSecurityPolicyBaseActionType


class CaCertBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    default: bool = True
    file_name: Optional[str] = Field(default=None, validation_alias="fileName", serialization_alias="fileName")
    bundle_string: Optional[str] = Field(
        default=None, validation_alias="bundleString", serialization_alias="bundleString"
    )


class UrlProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    order_no: int = Field(validation_alias="orderNo", serialization_alias="orderNo")
    vpn: List[VpnId]
    ref: UUID


class NetworkDecryptionRuleSequenceMatch(Match):
    entries: List[MatchEntry] = []


class NetworkDecryptionRuleSequence(PolicyDefinitionSequenceBase):
    model_config = ConfigDict(populate_by_name=True)
    sequence_type: Literal["sslDecryption"] = Field(
        default="sslDecryption", serialization_alias="sequenceType", validation_alias="sequenceType"
    )
    base_action: SslSecurityPolicyBaseActionType = Field(
        default="doNotDecrypt", serialization_alias="baseAction", validation_alias="baseAction"
    )
    match: NetworkDecryptionRuleSequenceMatch = NetworkDecryptionRuleSequenceMatch()

    def match_source_vpns(self, source_vpns: SourceVpnEntry):
        self._insert_match(source_vpns)

    def match_destination_vpns(self, destination_vpns: DestinationVpnEntry):
        self._insert_match(destination_vpns)

    def match_source_ports(self, source_ports: SourcePortEntry):
        self._insert_match(source_ports)

    def match_destinations_ports(self, destination_ports: DestinationPortEntry):
        self._insert_match(destination_ports)

    def match_source_networks_by_ref(self, source_network_ref: UUID):
        self._insert_match(SourceDataPrefixListEntry(ref=[source_network_ref]))

    def match_destination_networks_by_ref(self, destination_network_ref: UUID):
        self._insert_match(DestinationDataPrefixListEntry(ref=[destination_network_ref]))

    def match_source_networks_by_ip_prefix(self, source_ip_entry: str):
        self._insert_match(SourceIPEntry(value=source_ip_entry))

    def match_destination_networks_by_ip_prefix(self, destination_ip_entry: str):
        self._insert_match(DestinationIPEntry(value=destination_ip_entry))

    def match_source_networks_by_variable(self, variable_name: str):
        self._insert_match(SourceIPEntry(vip_variable_name=variable_name))

    def match_destination_networks_by_variable(self, variable_name: str):
        self._insert_match(DestinationIPEntry(vip_variable_name=variable_name))

    def match_applications(self, application_ref: UUID):
        self._insert_match(AppListEntry(ref=[application_ref]))


class SslDecryptionSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ssl_enable: StrBool = Field(default="true", validation_alias="sslEnable", serialization_alias="sslEnable")

    expired_certificate: CertificateCheckAction = Field(
        default="drop", validation_alias="expiredCertificate", serialization_alias="expiredCertificate"
    )
    untrusted_certificate: CertificateCheckAction = Field(
        default="drop", validation_alias="untrustedCertificate", serialization_alias="untrustedCertificate"
    )
    certificate_revocation_status: CertificateRevocation = Field(
        default="none",
        validation_alias="certificateRevocationStatus",
        serialization_alias="certificateRevocationStatus",
    )
    unknown_status: CertificateCheckAction = Field(
        default="drop", validation_alias="unknownStatus", serialization_alias="unknownStatus"
    )
    unsupported_protocol_versions: UnspportedModeAction = Field(
        default="drop",
        validation_alias="unsupportedProtocolVersions",
        serialization_alias="unsupportedProtocolVersions",
    )
    unsupported_cipher_suites: UnspportedModeAction = Field(
        default="drop", validation_alias="unsupportedCipherSuites", serialization_alias="unsupportedCipherSuites"
    )
    failure_mode: FailureMode = Field(
        default="close", validation_alias="failureMode", serialization_alias="failureMode"
    )
    ca_cert_bundle: CaCertBundle = Field(
        default=CaCertBundle(), validation_alias="caCertBundle", serialization_alias="caCertBundle"
    )
    key_modulus: KeyModulus = Field(default="2048", validation_alias="keyModulus", serialization_alias="keyModulus")
    eckey_type: EcKeyType = Field(default="P256", validation_alias="eckeyType", serialization_alias="eckeyType")
    certificate_lifetime: int = Field(
        default=1, validation_alias="certificateLifetime", serialization_alias="certificateLifetime"
    )
    min_tls_ver: TlsVersion = Field(default="TLSv1", validation_alias="minTlsVer", serialization_alias="minTlsVer")
    ca_tp_label: CaTpLabel = Field(
        default="PROXY-SIGNING-CA", validation_alias="caTpLabel", serialization_alias="caTpLabel"
    )


class SslDecryptionDefinition(DefinitionWithSequencesCommonBase):
    default_action: Optional[ControlPolicyBaseAction] = Field(
        default=ControlPolicyBaseAction(type="doNotDecrypt"),
        serialization_alias="defaultAction",
        validation_alias="defaultAction",
    )

    sequences: List[NetworkDecryptionRuleSequence] = []
    profiles: List[UrlProfile] = []
    settings: SslDecryptionSettings


class SslDecryptionPolicy(PolicyDefinitionBase):
    type: Literal["sslDecryption"] = "sslDecryption"
    mode: PolicyModeType = "security"
    definition: SslDecryptionDefinition

    @classmethod
    def create_unified_policy(
        cls, name: str, settings: SslDecryptionSettings, description: str = "default description"
    ):
        return cls(
            name=name, mode="unified", description=description, definition=SslDecryptionDefinition(settings=settings)
        )

    @classmethod
    def create_security_policy(
        cls,
        name: str,
        settings: SslDecryptionSettings,
        default_action=ControlPolicyBaseAction(type="doNotDecrypt"),
        sequences: List[NetworkDecryptionRuleSequence] = [],
        profiles: List[UrlProfile] = [],
        description: str = "default description",
    ):
        return cls(
            name=name,
            mode="security",
            description=description,
            definition=SslDecryptionDefinition(
                profiles=profiles, sequences=sequences, default_action=default_action, settings=settings
            ),
        )

    sequences: List[NetworkDecryptionRuleSequence] = []


class SslDecryptionPolicyEditPayload(SslDecryptionPolicy, PolicyDefinitionId):
    pass


class SslDecryptionPolicyGetResponse(SslDecryptionPolicy, PolicyDefinitionGetResponse):
    pass
