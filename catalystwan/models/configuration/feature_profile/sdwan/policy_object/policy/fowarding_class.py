# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List, Literal

from pydantic import AliasPath, ConfigDict, Field, field_validator

from catalystwan.api.configuration_groups.parcel import Global, _ParcelBase, _ParcelEntry, as_global


class FowardingClassQueueEntry(_ParcelEntry):
    queue: Global[str]

    @field_validator("queue")
    @classmethod
    def check_burst(cls, queue: Global):
        assert 0 <= int(queue.value) <= 7
        return queue


class FowardingClassParcel(_ParcelBase):
    model_config = ConfigDict(populate_by_name=True)
    type_: Literal["class"] = Field(default="class", exclude=True)
    entries: List[FowardingClassQueueEntry] = Field(default_factory=list, validation_alias=AliasPath("data", "entries"))

    def add_queue(self, queue: int):
        self.entries.append(FowardingClassQueueEntry(queue=as_global(str(queue))))
