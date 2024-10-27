# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.policy.policy_definition import (
    MediaProfileRef,
    PolicyDefinitionBase,
    PolicyDefinitionGetResponse,
    PolicyDefinitionId,
    TranslationProfileEntry,
    TrunkGroupPreference,
    VoicePortType,
)


class DialPeerType(BaseModel):
    type: Literal["pots", "sip"]


class DialPeerPolicyDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    dial_peer_type: DialPeerType = Field(serialization_alias="dialPeerType", validation_alias="dialPeerType")
    media_profile: Optional[MediaProfileRef] = Field(
        default=None, serialization_alias="mediaProfile", validation_alias="mediaProfile"
    )
    modem_passthrough: Optional[UUID] = Field(
        default=None, serialization_alias="modemPassthrough", validation_alias="modemPassthrough"
    )
    fax_protocol: Optional[UUID] = Field(
        default=None, serialization_alias="faxProtocol", validation_alias="faxProtocol"
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


class DialPeerPolicy(PolicyDefinitionBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["dialPeer", "dialpeer"] = "dialPeer"
    port_type: Optional[VoicePortType] = Field(
        default="potsDialPeer", serialization_alias="portType", validation_alias="portType"
    )
    definition: DialPeerPolicyDefinition


class DialPeerPolicyEditPayload(DialPeerPolicy, PolicyDefinitionId):
    pass


class DialPeerPolicyGetResponse(DialPeerPolicy, PolicyDefinitionGetResponse):
    pass
