# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase

SlotId = Literal[
    "0/1",
    "0/2",
    "0/3",
    "0/4",
    "1/0",
    "1/1",
    "2/0",
    "2/1",
    "3/0",
    "4/0",
]


class MediaResource(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    slot_id: Optional[Union[Variable, Global[SlotId]]] = Field(
        default=None, validation_alias="slotId", serialization_alias="slotId"
    )


class ServerList(BaseModel):
    ip: Union[Variable, Global[str]] = Field()
    identifier: Optional[Global[int]] = Field(default=None)


class CucmServerListPriority(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    cucm_server_identifier: Union[Variable, Global[str]] = Field(
        validation_alias="cucmServerIdentifier", serialization_alias="cucmServerIdentifier"
    )
    cucm_server_priority: Optional[Global[int]] = Field(
        default=None, validation_alias="cucmServerPriority", serialization_alias="cucmServerPriority"
    )


class CucmMediaResourceGroupList(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    media_resource_group_name: Union[Variable, Global[str]] = Field(
        validation_alias="mediaResourceGroupName", serialization_alias="mediaResourceGroupName"
    )
    profile_name: Union[Variable, Global[str]] = Field(
        validation_alias="profileName", serialization_alias="profileName"
    )


CucmSwitchover = Literal[
    "graceful",
    "immediate",
]


CucmSwitchback = Literal[
    "graceful",
    "guard",
    "immediate",
]


class CucmGroup(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    bind_interface: Union[Variable, Global[str]] = Field(
        validation_alias="bindInterface", serialization_alias="bindInterface"
    )
    cucm_media_resource_group_list: List[CucmMediaResourceGroupList] = Field(
        validation_alias="cucmMediaResourceGroupList",
        serialization_alias="cucmMediaResourceGroupList",
        description="CUCM Media Resource Group List",
    )
    cucm_server_list_priority: List[CucmServerListPriority] = Field(
        validation_alias="cucmServerListPriority",
        serialization_alias="cucmServerListPriority",
        description="CUCM Server List Priority",
    )
    cucm_switchback: Union[Variable, Default[Literal["guard"]], Global[CucmSwitchback]] = Field(
        validation_alias="cucmSwitchback", serialization_alias="cucmSwitchback"
    )
    cucm_switchover: Union[Variable, Default[Literal["graceful"]], Global[CucmSwitchover]] = Field(
        validation_alias="cucmSwitchover", serialization_alias="cucmSwitchover"
    )
    keep_alive_retries: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="keepAliveRetries", serialization_alias="keepAliveRetries"
    )
    keep_alive_time_out: Union[Variable, Default[int], Global[int]] = Field(
        validation_alias="keepAliveTimeOut", serialization_alias="keepAliveTimeOut"
    )
    cucm_group_id: Optional[Global[int]] = Field(
        default=None, validation_alias="cucmGroupId", serialization_alias="cucmGroupId"
    )


ProfileType = Literal[
    "conference",
    "mtp",
    "transcode",
]

DspVoiceCodec = Literal[
    "g711alaw",
    "g711ulaw",
    "g722-64",
    "g729abr8",
    "g729ar8",
    "g729br8",
    "g729r8",
    "ilbc",
    "isac",
    "opus",
    "pass-through",
]

DspVoiceFeature = Literal[
    "acoustic-shock-protection",
    "call-progress-analysis",
    "cng-fax-detect",
    "dtmf suppress",
    "noise-reduction",
]

Application = Literal[
    "cube",
    "sccp",
]

ConferenceMaxParticipants = Literal[
    "16",
    "32",
    "8",
]


class Profile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    codec_list: Union[Variable, Default[List[DspVoiceCodec]], Global[List[DspVoiceCodec]]] = Field(
        validation_alias="codecList", serialization_alias="codecList"
    )
    profile_name: Union[Variable, Global[str]] = Field(
        validation_alias="profileName", serialization_alias="profileName"
    )
    application: Optional[Global[Application]] = Field(default=None)
    conference_max_participants: Union[
        Variable, Default[Literal["8"]], Global[ConferenceMaxParticipants], None
    ] = Field(
        default=None, validation_alias="conferenceMaxParticipants", serialization_alias="conferenceMaxParticipants"
    )
    feature: Union[Variable, Default[None], Global[List[DspVoiceFeature]]] = Field(default=Default[None](value=None))
    max_session: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="maxSession", serialization_alias="maxSession"
    )
    mtp_hardware: Optional[Global[bool]] = Field(
        default=None, validation_alias="mtpHardware", serialization_alias="mtpHardware"
    )
    mtp_max_sessions_hardware: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="mtpMaxSessionsHardware", serialization_alias="mtpMaxSessionsHardware"
    )
    mtp_max_sessions_software: Optional[Union[Variable, Global[int]]] = Field(
        default=None, validation_alias="mtpMaxSessionsSoftware", serialization_alias="mtpMaxSessionsSoftware"
    )
    mtp_software: Optional[Global[bool]] = Field(
        default=None, validation_alias="mtpSoftware", serialization_alias="mtpSoftware"
    )
    profile_id: Global[int] = Field(validation_alias="profileId", serialization_alias="profileId")
    profile_type: Global[ProfileType] = Field(validation_alias="profileType", serialization_alias="profileType")
    shutdown: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)
    universal: Optional[Union[Variable, Global[bool], Default[bool]]] = Field(default=None)


class DspFarmParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["dsp-farm"] = Field(default="dsp-farm", exclude=True)
    profile: List[Profile] = Field(validation_alias=AliasPath("data", "profile"), description="Configure Profile")
    cucm_group: Optional[List[CucmGroup]] = Field(
        default=None, validation_alias=AliasPath("data", "cucmGroup"), description="Configure CUCM Group"
    )
    ip_precedence: Optional[Union[Variable, Default[int], Global[int]]] = Field(
        default=None, validation_alias=AliasPath("data", "ipPrecedence")
    )
    local_interface: Optional[Union[Variable, Global[str]]] = Field(
        default=None, validation_alias=AliasPath("data", "localInterface")
    )
    media_resource: Optional[List[MediaResource]] = Field(
        default=None, validation_alias=AliasPath("data", "mediaResource"), description="Configure Media Resource"
    )
    server_list: Optional[List[ServerList]] = Field(
        default=None, validation_alias=AliasPath("data", "serverList"), description="Configure Server List"
    )
