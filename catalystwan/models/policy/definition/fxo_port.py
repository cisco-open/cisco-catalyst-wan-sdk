# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    CommonStation,
    FxoTuningParams,
    LineParams,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    SupervisoryDisconnectEntry,
    TranslationProfileEntry,
    TrunkGroupPreference,
    VoicePortType,
)


class FxoPortPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    common_station: Optional[CommonStation] = Field(
        default=None, serialization_alias="commonStation", validation_alias="commonStation"
    )
    line_params: Optional[LineParams] = Field(
        default=None, serialization_alias="lineParams", validation_alias="lineParams"
    )
    tuning_params: Optional[FxoTuningParams] = Field(
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
    supervisory_disc_custom: Optional[SupervisoryDisconnectEntry] = Field(
        default=None, serialization_alias="supervisoryDiscCustom", validation_alias="supervisoryDiscCustom"
    )
    supervisory_disc_dualtone: Optional[SupervisoryDisconnectEntry] = Field(
        default=None, serialization_alias="supervisoryDiscDualtone", validation_alias="supervisoryDiscDualtone"
    )


class FxoPortPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["fxoPort", "fxoport"] = "fxoPort"
    port_type: Optional[VoicePortType] = Field(
        default="voicePort", serialization_alias="portType", validation_alias="portType"
    )
    definition: FxoPortPolicyDefinition = FxoPortPolicyDefinition()


class FxoPortPolicyEditPayload(FxoPortPolicy, PolicyDefinitionId):
    pass


class FxoPortPolicyGetResponse(FxoPortPolicy, PolicyDefinitionGetResponse):
    pass
