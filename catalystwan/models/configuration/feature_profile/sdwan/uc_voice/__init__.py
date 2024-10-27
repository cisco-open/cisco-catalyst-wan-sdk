# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.media_profile import MediaProfileParcel
from catalystwan.models.configuration.feature_profile.sdwan.uc_voice.trunk_group import TrunkGroupParcel

from .dsp_farm import DspFarmParcel

AnyUcVoiceParcel = Annotated[
    Union[
        DspFarmParcel,
        MediaProfileParcel,
        TrunkGroupParcel,
    ],
    Field(discriminator="type_"),
]

__all__ = ("AnyUcVoiceParcel", "DspFarmParcel", "MediaProfileParcel", "TrunkGroupParcel")


def __dir__() -> "List[str]":
    return list(__all__)
