# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Literal, Optional, Union

from pydantic import AliasPath, BaseModel, ConfigDict, Field

from catalystwan.api.configuration_groups.parcel import Default, Global, Variable, _ParcelBase, as_default

ConfigTypeValue = Literal["non-eSim"]


class ControllerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    id: Union[Variable, Global[str]] = Field(description="Cellular ID", examples=["0/2/0"])
    slot: Optional[Union[Variable, Global[int], Default[int]]] = Field(
        default=None, description="Set primary SIM slot. 0 or 1"
    )
    max_retry: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None,
        description="Set SIM failover retries",
        serialization_alias="maxRetry",
        validation_alias="maxRetry",
    )
    failover_timer: Optional[Union[Variable, Global[int], Default[None]]] = Field(
        default=None,
        description="Set SIM failover timeout in minutes",
        serialization_alias="failovertimer",
        validation_alias="failovertimer",
    )
    auto_sim: Optional[Union[Variable, Global[bool], Default[None]]] = Field(
        default=None,
        description="Enable/Disable Firmware Auto Sim",
        serialization_alias="autoSim",
        validation_alias="autoSim",
    )


class CellularControllerParcel(_ParcelBase):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
    type_: Literal["cellular-controller"] = Field(default="cellular-controller", exclude=True, frozen=True)
    config_type: Default[ConfigTypeValue] = Field(
        default=as_default("non-eSim", ConfigTypeValue), validation_alias=AliasPath("data", "configType")
    )
    controller_config: ControllerConfig = Field(validation_alias=AliasPath("data", "controllerConfig"))

    def set_controller_config(
        self,
        id: Union[Global[str]],
        max_retry: Optional[Union[Global[int]]] = None,
        failover_timer: Optional[Union[Global[int]]] = None,
        auto_sim: Optional[Union[Global[bool]]] = None,
    ):
        self.controller_config = ControllerConfig(
            id=id, max_retry=max_retry, failover_timer=failover_timer, auto_sim=auto_sim
        )
