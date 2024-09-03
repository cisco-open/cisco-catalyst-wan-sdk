# Copyright 2022 Cisco Systems, Inc. and its affiliates

from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from catalystwan.models.common import IntStr, SLAClassCriteria
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class FallbackBestTunnel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    criteria: Optional[SLAClassCriteria] = None
    jitter_variance: Optional[IntStr] = Field(
        default=None,
        serialization_alias="jitterVariance",
        validation_alias="jitterVariance",
        description="jitter variance in ms",
        ge=1,
        le=1000,
    )
    latency_variance: Optional[IntStr] = Field(
        default=None,
        serialization_alias="latencyVariance",
        validation_alias="latencyVariance",
        description="latency variance in ms",
        ge=1,
        le=1000,
    )
    loss_variance: Optional[IntStr] = Field(
        default=None,
        serialization_alias="lossVariance",
        validation_alias="lossVariance",
        description="loss variance as percentage",
        ge=0,
        le=100,
    )


class SLAClassListEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    latency: Optional[IntStr] = Field(default=None, ge=1, le=1000)
    loss: Optional[IntStr] = Field(default=None, ge=0, le=100)
    jitter: Optional[IntStr] = Field(default=None, ge=1, le=1000)
    app_probe_class: Optional[UUID] = Field(
        default=None, serialization_alias="appProbeClass", validation_alias="appProbeClass"
    )
    fallback_best_tunnel: Optional[FallbackBestTunnel] = Field(
        default=None, serialization_alias="fallbackBestTunnel", validation_alias="fallbackBestTunnel"
    )


class SLAClassList(PolicyListBase):
    type: Literal["sla"] = "sla"
    entries: List[SLAClassListEntry] = []

    def assign_app_probe_class(
        self,
        app_probe_class_id: UUID,
        latency: Optional[int] = None,
        loss: Optional[int] = None,
        jitter: Optional[int] = None,
    ) -> SLAClassListEntry:
        entry = SLAClassListEntry(latency=latency, loss=loss, jitter=jitter, app_probe_class=app_probe_class_id)
        self._add_entry(entry, single=True)
        return entry


class SLAClassListEditPayload(SLAClassList, PolicyListId):
    pass


class SLAClassListInfo(SLAClassList, PolicyListInfo):
    pass
