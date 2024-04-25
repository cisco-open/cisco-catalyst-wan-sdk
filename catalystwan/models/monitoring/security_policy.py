# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from pydantic import BaseModel, Field


class SecurityPolicyDeviceList(BaseModel):
    amp_down: List[str] = Field(..., alias="amp_down")
    amp_up: List[str] = Field(..., alias="amp_up")
    ips_down: List[str] = Field(..., alias="ips_down")
    ips_up: List[str] = Field(..., alias="ips_up")
    urlf_down: List[str] = Field(..., alias="urlf_down")
    urlf_up: List[str] = Field(..., alias="urlf_up")
    zbfw_down: List[str] = Field(..., serialization_alias="zbfw_down", validation_alias="zbfw_down")
    zbfw_up: List[str] = Field(..., serialization_alias="zbfw_up", validation_alias="zbfw_up")
