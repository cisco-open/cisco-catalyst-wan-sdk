# Copyright 2024 Cisco Systems, Inc. and its affiliates

from pydantic import BaseModel, Field


class ServerInfoResponse(BaseModel):
    """The response may contain an incorrect spelling "Achitecture"."""

    architecture: str = Field(..., alias="Achitecture")
    available_processors: int = Field(
        ..., serialization_alias="Available processors", validation_alias="Available processors"
    )
