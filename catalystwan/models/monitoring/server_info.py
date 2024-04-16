# Copyright 2024 Cisco Systems, Inc. and its affiliates

from pydantic import BaseModel, Field


class ServerInfoResponse(BaseModel):
    """The response may contain an incorrect spelling "Achitecture"."""

    Architecture: str = Field(..., alias="Achitecture")
    Available_processors: int
