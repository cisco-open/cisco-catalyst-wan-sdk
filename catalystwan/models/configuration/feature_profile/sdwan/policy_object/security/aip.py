# Copyright 2023 Cisco Systems, Inc. and its affiliates
# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional
from uuid import UUID

from pydantic import AliasPath, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase
from catalystwan.models.configuration.feature_profile.common import RefIdItem

TlsDecryptionAction = Literal["decrypt", "neverDecrypt", "skipDecrypt"]


class AdvancedInspectionProfileParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
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
    intrusion_prevention: Optional[RefIdItem] = Field(
        default=None, validation_alias=AliasPath("data", "intrusionPrevention")
    )
    url_filtering: Optional[RefIdItem] = Field(default=None, validation_alias=AliasPath("data", "urlFiltering"))
    advanced_malware_protection: Optional[RefIdItem] = Field(
        default=None, validation_alias=AliasPath("data", "advancedMalwareProtection")
    )
    ssl_decryption_profile: Optional[RefIdItem] = Field(
        default=None, validation_alias=AliasPath("data", "sslDecryptionProfile")
    )

    @classmethod
    def create(
        cls,
        parcel_name: str,
        parcel_description: str,
        tls_decryption_action: TlsDecryptionAction = "skipDecrypt",
        intrusion_prevention: Optional[UUID] = None,
        url_filtering: Optional[UUID] = None,
        advanced_malware_protection: Optional[UUID] = None,
        ssl_decryption_profile: Optional[UUID] = None,
    ) -> "AdvancedInspectionProfileParcel":
        ip = RefIdItem.from_uuid(intrusion_prevention) if intrusion_prevention else None
        uf = RefIdItem.from_uuid(url_filtering) if url_filtering else None
        amp = RefIdItem.from_uuid(advanced_malware_protection) if advanced_malware_protection else None
        sdp = RefIdItem.from_uuid(ssl_decryption_profile) if ssl_decryption_profile else None
        return cls(
            parcel_name=parcel_name,
            parcel_description=parcel_description,
            tls_decryption_action=Global[TlsDecryptionAction](value=tls_decryption_action),
            intrusion_prevention=ip,
            url_filtering=uf,
            advanced_malware_protection=amp,
            ssl_decryption_profile=sdp,
        )
