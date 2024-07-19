# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, SerializationInfo, SerializerFunctionWrapHandler, model_serializer

Region = Literal["nam", "eur"]


class ThreadGridApiEntires(BaseModel):
    model_config = ConfigDict(extra="forbid")
    region: Region
    apikey: Optional[str] = Field(default="")


class ThreatGridApi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entries: List[ThreadGridApiEntires] = Field(
        default_factory=lambda: [
            ThreadGridApiEntires(region="nam"),
            ThreadGridApiEntires(region="eur"),
        ]
    )

    def set_region_api_key(self, region: Region, apikey: str) -> None:
        for entry in self.entries:
            if entry.region == region:
                entry.apikey = apikey
                return
        raise ValueError(f"Region {region} not found in ThreatGridApi")

    @model_serializer(mode="wrap")
    def envelope_data(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> Dict[str, Any]:
        return {"data": [handler(self)]}
