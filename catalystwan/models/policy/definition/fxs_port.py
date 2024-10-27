# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    CommonStation,
    FxsTuningParams,
    LineParams,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    TranslationProfileEntry,
    TrunkGroupPreference,
    VoicePortType,
)


class FxsPortPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    common_station: Optional[CommonStation] = Field(
        default=None, serialization_alias="commonStation", validation_alias="commonStation"
    )
    line_params: Optional[LineParams] = Field(
        default=None, serialization_alias="lineParams", validation_alias="lineParams"
    )
    tuning_params: Optional[FxsTuningParams] = Field(
        default=None, serialization_alias="tuningParams", validation_alias="tuningParams"
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


class FxsPortPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["fxsPort", "fxsport"] = "fxsPort"
    port_type: Optional[VoicePortType] = Field(
        default="voicePort", serialization_alias="portType", validation_alias="portType"
    )
    definition: FxsPortPolicyDefinition = FxsPortPolicyDefinition()


class FxsPortPolicyEditPayload(FxsPortPolicy, PolicyDefinitionId):
    pass


class FxsPortPolicyGetResponse(FxsPortPolicy, PolicyDefinitionGetResponse):
    pass
