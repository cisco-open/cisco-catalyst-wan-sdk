# Copyright 2023 Cisco Systems, Inc. and its affiliates

from typing import Optional

from pydantic import BaseModel, Field


class FullConfig(BaseModel):
    fullconfig: str


class FullConfigParcel(BaseModel):
    name: str = Field(pattern=r'^[^&<>! "]+$', min_length=1, max_length=128)
    description: Optional[str]
    data: FullConfig
