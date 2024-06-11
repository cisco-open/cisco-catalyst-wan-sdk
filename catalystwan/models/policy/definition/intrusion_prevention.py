# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from catalystwan.models.common import PolicyModeType, VpnId
from catalystwan.models.policy.policy_definition import (
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    Reference,
)

SignatureSetType = Literal["balanced", "connectivity", "security"]
InspectionModeType = Literal["protection", "detection"]
LogLevel = Literal["emergency", "alert", "critical", "error", "warning", "notice", "info", "debug"]


class IntrusionPreventionDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    signature_set: SignatureSetType = Field(validation_alias="signatureSet", serialization_alias="signatureSet")
    inspection_mode: InspectionModeType = Field(validation_alias="inspectionMode", serialization_alias="inspectionMode")
    signature_white_list: Optional[Reference] = Field(
        default=None, validation_alias="signatureWhiteList", serialization_alias="signatureWhiteList"
    )
    log_level: Optional[LogLevel] = Field(default="error", validation_alias="logLevel", serialization_alias="logLevel")
    logging: List[str] = Field(default=[])
    target_vpns: List[VpnId] = Field(default=[], validation_alias="targetVpns", serialization_alias="targetVpns")
    custom_signature: bool = Field(
        default=False, validation_alias="customSignature", serialization_alias="customSignature"
    )

    @field_validator("signature_white_list", mode="before")
    @classmethod
    def convert_empty_dict_to_none(cls, value):
        if not value:
            return None
        return value


class IntrusionPreventionPolicy(PolicyDefinitionBase):
    type: Literal["intrusionPrevention"] = "intrusionPrevention"
    mode: PolicyModeType = "security"
    definition: IntrusionPreventionDefinition


class IntrusionPreventionPolicyEditPayload(IntrusionPreventionPolicy, PolicyDefinitionId):
    pass


class IntrusionPreventionPolicyGetResponse(IntrusionPreventionPolicy, PolicyDefinitionGetResponse):
    pass
