# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Global, Variable, _ParcelBase
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


class QosMap(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    qos_schedulers: List[QosSchedulers] = Field(validation_alias="qosSchedulers", serialization_alias="qosSchedulers")


class QosPolicyParcel(_ParcelBase):
    type_: Literal["qos-policy"] = Field(default="qos-policy", exclude=True)
    qos_map: QosMap = Field(validation_alias=AliasPath("data", "qosMap"))
    target: Optional[QosPolicyTarget] = Field(default=None, validation_alias=AliasPath("data", "target"))
