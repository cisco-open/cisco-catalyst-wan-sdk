# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Self

from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
)

TlsDecryptionAction = Literal["decrypt", "neverDecrypt", "skipDecrypt"]


class AdvancedInspectionProfileDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    tls_decryption_action: TlsDecryptionAction = Field(
        validation_alias="tlsDecryptionAction", serialization_alias="tlsDecryptionAction"
    )

    advanced_malware_protection: Optional[Reference] = Field(
        default=None, validation_alias="advancedMalwareProtection", serialization_alias="advancedMalwareProtection"
    )

    intrusion_prevention: Optional[Reference] = Field(
        default=None, validation_alias="intrusionPrevention", serialization_alias="intrusionPrevention"
    )
    url_filtering: Optional[Reference] = Field(
        default=None, validation_alias="urlFiltering", serialization_alias="urlFiltering"
    )

    ssl_utd_decrypt_profile: Optional[Reference] = Field(
        default=None, validation_alias="sslUtdDecryptProfile", serialization_alias="sslUtdDecryptProfile"
    )

    @model_validator(mode="after")
    def check_at_least_one_optional_filled(self) -> Self:
        if not any([self.advanced_malware_protection, self.intrusion_prevention, self.url_filtering]):
            raise ValueError(
                "At least one of Intrusion Prevention, URL Filtering, Advanced Malware Protection shall be filled."
            )
        return self


class AdvancedInspectionProfilePolicy(PolicyDefinitionBase):
    type: Literal["advancedInspectionProfile"] = "advancedInspectionProfile"
    mode: Literal["unified"] = "unified"
    definition: AdvancedInspectionProfileDefinition


class AdvancedInspectionProfilePolicyEditPayload(AdvancedInspectionProfilePolicy, PolicyDefinitionId):
    pass


class AdvancedInspectionProfilePolicyGetResponse(AdvancedInspectionProfilePolicy, PolicyDefinitionGetResponse):
    pass
