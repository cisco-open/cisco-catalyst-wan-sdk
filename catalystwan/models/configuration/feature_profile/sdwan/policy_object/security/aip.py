# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal

from pydantic import AliasPath, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.sdwan.transport.bgp import RefIdItem

TlsDecryptionAction = Literal["decrypt", "neverDecrypt", "skipDecrypt"]


class AdvancedInspectionProfileParcel(_ParcelBase):
    type_: Literal["unified/advanced-inspection-profile"] = Field(
        default="unified/advanced-inspection-profile", exclude=True
    )
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )
    tls_decryption_action: Global[TlsDecryptionAction] = Field(
        default=Global[TlsDecryptionAction](value="skipDecrypt"),
        validation_alias=AliasPath("data", "tlsDecryptionAction"),
    )
    intrusion_prevention: RefIdItem = Field(default=None, validation_alias=AliasPath("data", "intrusionPrevention"))
    url_filtering: RefIdItem = Field(default=None, validation_alias=AliasPath("data", "urlFiltering"))
    advanced_malware_protection: RefIdItem = Field(
        default=None, validation_alias=AliasPath("data", "advancedMalwareProtection")
    )
    ssl_decryption_profile: RefIdItem = Field(default=None, validation_alias=AliasPath("data", "sslDecryptionProfile"))
