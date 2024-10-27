# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import HuntSchemeChannel as HuntSchemeMethodPrecedence
from catalystwan.models.common import HuntSchemeMethod
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class TrunkGroupListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    hunt_scheme_method: HuntSchemeMethod = Field(
        validation_alias="huntSchemeMethod", serialization_alias="huntSchemeMethod"
    )
    hunt_scheme_precedence: Optional[HuntSchemeMethodPrecedence] = Field(
        default=None, validation_alias="huntSchemePrecedence", serialization_alias="huntSchemePrecedence"
    )
    max_calls_in: Optional[int] = Field(
        default=None, validation_alias="maxCallsIn", serialization_alias="maxCallsIn", ge=0, le=1000
    )
    max_calls_out: Optional[int] = Field(
        default=None, validation_alias="maxCallsOut", serialization_alias="maxCallsOut", ge=0, le=1000
    )
    max_retries: int = Field(validation_alias="maxRetries", serialization_alias="maxRetries", ge=1, le=5)


class TrunkGroupList(PolicyListBase):
    type: Literal["trunkGroup"] = "trunkGroup"
    entries: List[TrunkGroupListEntry] = []

    def add_entry(
        self,
        hunt_scheme_method: HuntSchemeMethod,
        hunt_scheme_precedence: Optional[HuntSchemeMethodPrecedence],
        max_retries: int,
        max_calls_in: Optional[int] = None,
        max_calls_out: Optional[int] = None,
    ) -> None:
        entry = TrunkGroupListEntry(
            hunt_scheme_method=hunt_scheme_method,
            hunt_scheme_precedence=hunt_scheme_precedence,
            max_retries=max_retries,
            max_calls_in=max_calls_in,
            max_calls_out=max_calls_out,
        )
        self.entries.append(entry)


class TrunkGroupListEditPayload(TrunkGroupList, PolicyListId):
    pass


class TrunkGroupListInfo(TrunkGroupList, PolicyListInfo):
    pass
