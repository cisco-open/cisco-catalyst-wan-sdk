# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import FaxFallBackProtocols, FaxPrimaryProtocols
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class T38Options(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    version: int = Field(ge=0)
    rate: str
    nse: str
    lowSpeed: int = Field(ge=0, validation_alias="lowSpeed", serialization_alias="lowSpeed")
    highSpeed: int = Field(ge=0, validation_alias="highSpeed", serialization_alias="highSpeed")
    fallbackProtocol: FaxFallBackProtocols = Field(
        validation_alias="fallbackProtocol", serialization_alias="fallbackProtocol"
    )


class FaxProtocolListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    primary_protocol: FaxPrimaryProtocols = Field(
        validation_alias="primaryProtocol", serialization_alias="primaryProtocol"
    )
    ecm: bool = Field(default=False)
    t38_options: Optional[T38Options] = Field(
        default=None, serialization_alias="t38Options", validation_alias="t38Options"
    )


class FaxProtocolList(PolicyListBase):
    model_config = ConfigDict(populate_by_name=True)
    type: Literal["faxProtocol", "faxprotocol"] = "faxProtocol"
    entries: List[FaxProtocolListEntry] = Field(default_factory=list)


class FaxProtocolListEditPayload(FaxProtocolList, PolicyListId):
    pass


class FaxProtocolListInfo(FaxProtocolList, PolicyListInfo):
    pass
