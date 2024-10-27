# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    MediaProfileRef,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    VoicePortType,
)


class SrstPhoneProfilePolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    media_profile: Optional[MediaProfileRef] = Field(
        default=None, serialization_alias="mediaProfile", validation_alias="mediaProfile"
    )


class SrstPhoneProfilePolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["srstPhoneProfile", "srstphoneprofile"] = "srstPhoneProfile"
    port_type: Optional[VoicePortType] = Field(
        default="srstPhone", serialization_alias="portType", validation_alias="portType"
    )
    definition: SrstPhoneProfilePolicyDefinition = SrstPhoneProfilePolicyDefinition()


class SrstPhoneProfilePolicyEditPayload(SrstPhoneProfilePolicy, PolicyDefinitionId):
    pass


class SrstPhoneProfilePolicyGetResponse(SrstPhoneProfilePolicy, PolicyDefinitionGetResponse):
    pass
