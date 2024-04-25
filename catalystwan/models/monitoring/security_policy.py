# Copyright 2024 Cisco Systems, Inc. and its affiliates

from typing import List

from pydantic import BaseModel


class SecurityPolicyDeviceList(BaseModel):
    amp_down: List[str]
    amp_up: List[str]
    ips_down: List[str]
    ips_up: List[str]
    urlf_down: List[str]
    urlf_up: List[str]
    zbfw_down: List[str]
    zbfw_up: List[str]
