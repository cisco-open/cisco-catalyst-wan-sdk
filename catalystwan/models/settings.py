# Copyright 2024 Cisco Systems, Inc. and its affiliates
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Region = Literal["nam", "eur"]


class ThreatGridApiEntires(BaseModel):
    model_config = ConfigDict(extra="forbid")
    region: Region
    apikey: Optional[str] = Field(default="")


class ThreatGridApiData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entries: List[ThreatGridApiEntires] = Field(
        default_factory=lambda: [
            ThreatGridApiEntires(region="nam"),
            ThreatGridApiEntires(region="eur"),
        ],
    )


class ThreatGridApi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    data: List[ThreatGridApiData] = Field(default_factory=lambda: [ThreatGridApiData()])

    def set_region_api_key(self, region: Region, apikey: str) -> None:
        for entry in self.data[0].entries:
            if entry.region == region:
                entry.apikey = apikey
                return
        raise ValueError(f"Region {region} not found in ThreatGridApi")

    def get_region_api_key(self, region: Region) -> str:
        for entry in self.data[0].entries:
            if entry.region == region:
                apikey = entry.apikey
                return "" if apikey is None else apikey
        raise ValueError(f"Region {region} not found in ThreatGridApi")
