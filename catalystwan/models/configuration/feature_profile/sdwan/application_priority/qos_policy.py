# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field
from typing_extensions import Self

from catalystwan.api.configuration_groups.parcel import (
    Global,
    Variable,
    _ParcelBase,
    as_global,
    as_optional_global,
    as_variable,
)
from catalystwan.models.configuration.feature_profile.common import RefIdItem


class QosPolicyTarget(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    interfaces: Union[Global[List[str]], Variable]


class QosSchedulers(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    bandwidth_percent: Optional[Global[str]] = Field(
        default=None, validation_alias="bandwidthPercent", serialization_alias="bandwidthPercent"
    )
    class_map_ref: Optional[RefIdItem] = Field(
        default=None, validation_alias="classMapRef", serialization_alias="classMapRef"
    )
    drops: Optional[Global[str]] = Field(default=None)
    queue: Optional[Global[str]] = Field(default=None)
    scheduling: Optional[Global[str]] = Field(default=None)

    @classmethod
    def create(
        cls,
        bandwidth_percent: Optional[str] = None,
        class_map_ref: Optional[UUID] = None,
        drops: Optional[str] = None,
        queue: Optional[str] = None,
        scheduling: Optional[str] = None,
    ) -> Self:
        return cls(
            bandwidth_percent=as_optional_global(bandwidth_percent),
            class_map_ref=RefIdItem.from_uuid(class_map_ref) if class_map_ref else None,
            drops=as_optional_global(drops),
            queue=as_optional_global(queue),
            scheduling=as_optional_global(scheduling),
        )


class QosMap(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    qos_schedulers: List[QosSchedulers] = Field(validation_alias="qosSchedulers", serialization_alias="qosSchedulers")

    @classmethod
    def create(cls, schedulers: Optional[List[QosSchedulers]] = None) -> Self:
        return cls(qos_schedulers=schedulers if schedulers else [])


class QosPolicyParcel(_ParcelBase):
    type_: Literal["qos-policy"] = Field(default="qos-policy", exclude=True)
    qos_map: QosMap = Field(validation_alias=AliasPath("data", "qosMap"))
    target: Optional[QosPolicyTarget] = Field(default=None, validation_alias=AliasPath("data", "target"))
    parcel_description: str = Field(
        default="",
        serialization_alias="description",
        validation_alias="description",
        description="Set the parcel description",
    )

    @classmethod
    def create(
        cls, parcel_name: str, parcel_description: str, schedulers: Optional[List[QosSchedulers]] = None
    ) -> Self:
        return cls(parcel_name=parcel_name, parcel_description=parcel_description, qos_map=QosMap.create(schedulers))

    def add_scheduler(
        self,
        bandwidth_percent: Optional[str] = None,
        class_map_ref: Optional[UUID] = None,
        drops: Optional[str] = None,
        queue: Optional[str] = None,
        scheduling: Optional[str] = None,
    ) -> None:
        self.qos_map.qos_schedulers.append(
            QosSchedulers.create(
                bandwidth_percent=bandwidth_percent,
                class_map_ref=class_map_ref,
                drops=drops,
                queue=queue,
                scheduling=scheduling,
            )
        )

    def set_variable_target(self, variable: str) -> None:
        self.target = QosPolicyTarget(interfaces=as_variable(value=variable))

    def set_list_target(self, interfaces: List[str]) -> None:
        self.target = QosPolicyTarget(interfaces=as_global(value=interfaces))
