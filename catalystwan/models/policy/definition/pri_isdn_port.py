# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    LineParams,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    TranslationProfileEntry,
    TrunkGroupPreference,
    VoicePortType,
)


class PriIsdnPortPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    line_params: Optional[LineParams] = Field(
        default=None, serialization_alias="lineParams", validation_alias="lineParams"
    )
    trunk_group: Optional[List[TrunkGroupPreference]] = Field(
        default=None, serialization_alias="trunkGroup", validation_alias="trunkGroup"
    )
    incoming_translation_profile: Optional[TranslationProfileEntry] = Field(
        default=None, serialization_alias="incomingTranslationProfile", validation_alias="incomingTranslationProfile"
    )
    outgoing_translation_profile: Optional[TranslationProfileEntry] = Field(
        default=None, serialization_alias="outgoingTranslationProfile", validation_alias="outgoingTranslationProfile"
    )


class PriIsdnPortPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["priIsdnPort", "priisdnport"] = "priIsdnPort"
    port_type: Optional[VoicePortType] = Field(
        default="voicePort", serialization_alias="portType", validation_alias="portType"
    )
    definition: PriIsdnPortPolicyDefinition = PriIsdnPortPolicyDefinition()


class PriIsdnPortPolicyEditPayload(PriIsdnPortPolicy, PolicyDefinitionId):
    pass


class PriIsdnPortPolicyGetResponse(PriIsdnPortPolicy, PolicyDefinitionGetResponse):
    pass
