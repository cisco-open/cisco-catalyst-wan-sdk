# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from catalystwan.models.common import IntStr
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class DualToneModeEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    mode: Literal["dualtone_mode"] = "dualtone_mode"
    cadence_variable: IntStr = Field(
        ge=0, le=200, serialization_alias="cadenceVariable", validation_alias="cadenceVariable"
    )
    frequency_max_delay: IntStr = Field(
        ge=10, le=100, serialization_alias="frequencyMaxDelay", validation_alias="frequencyMaxDelay"
    )
    frequency_max_deviation: IntStr = Field(
        ge=10, le=125, serialization_alias="frequencyMaxDeviation", validation_alias="frequencyMaxDeviation"
    )
    frequency_max_power: IntStr = Field(
        ge=0, le=20, serialization_alias="frequencyMaxPower", validation_alias="frequencyMaxPower"
    )
    frequency_min_power: IntStr = Field(
        ge=10, le=35, serialization_alias="frequencyMinPower", validation_alias="frequencyMinPower"
    )
    frequency_min_power_twist: IntStr = Field(
        ge=0, le=15, serialization_alias="frequencyMinPowerTwist", validation_alias="frequencyMinPowerTwist"
    )


class CustomModeEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    mode: Literal["custom_mode"] = "custom_mode"
    dualtone_type: str = Field(validation_alias="dualtoneType", serialization_alias="dualtoneType")
    cadence: IntStr = Field(ge=0, le=10_000)
    dualtone_frequency1: IntStr = Field(
        ge=300, le=3600, validation_alias="dualtoneFrequency1", serialization_alias="dualtoneFrequency1"
    )
    dualtone_frequency2: IntStr = Field(
        ge=300, le=3600, validation_alias="dualtoneFrequency2", serialization_alias="dualtoneFrequency2"
    )


SupervisoryDisconnectListEntry = Annotated[Union[DualToneModeEntry, CustomModeEntry], Field(discriminator="mode")]


class SupervisoryDisconnectList(PolicyListBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["supervisoryDisc", "supervisorydisc"] = "supervisoryDisc"
    entries: List[SupervisoryDisconnectListEntry] = Field(default_factory=list)


class SupervisoryDisconnectListEditPayload(SupervisoryDisconnectList, PolicyListId):
    pass


class SupervisoryDisconnectListInfo(SupervisoryDisconnectList, PolicyListInfo):
    pass
