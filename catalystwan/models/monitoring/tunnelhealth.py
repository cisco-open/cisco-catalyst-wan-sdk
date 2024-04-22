from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

HealthValues = Literal["fair", "good", "n/a", "poor"]
StateValues = Literal["Down", "Up"]


# Optional Params for both endpoints.
class TunnelHealthRequest(BaseModel):
    last_n_hours: int = Field(default=12, description="Time range for the data in hours.")
    site: Optional[str] = Field(default=None, description="Specific site to filter the data.")
    limit: int = Field(default=30, description="Limit for the number of records returned.")


# Models for tunnelhealth/history
class DeviceHealthEntryItem(BaseModel):
    cpu_load: Optional[float] = None
    data: Dict = Field(default_factory=dict)  # Empty dictionary by default
    entry_time: int
    health: HealthValues
    health_score: float
    memory_utilization: Optional[float] = None


class TunnelHealthData(BaseModel):
    jitter: float
    latency: float
    loss_percentage: float
    rx_octets: int
    state: StateValues
    tx_octets: int
    vqoe_score: float


class TunnelHealthHistoryItem(BaseModel):
    health: HealthValues
    health_score: float
    history: List[DeviceHealthEntryItem]
    local_color: str
    local_system_ip: str
    name: str
    remote_color: str
    remote_system_ip: str
    summary: TunnelHealthData


# Models for tunnelhealth/overview/<type>
class TunnelHealthOverviewEntry(BaseModel):
    health: HealthValues
    health_score: float
    jitter: float
    latency: float
    local_color: str
    local_system_ip: str
    loss_percentage: float
    name: str
    remote_color: str
    remote_system_ip: str
    rx_octets: int
    state: StateValues
    tx_octets: int
    vqoe_score: float


class TunnelHealthOverviewDetail(BaseModel):
    fair: List[TunnelHealthOverviewEntry]
    good: List[TunnelHealthOverviewEntry]
    poor: List[TunnelHealthOverviewEntry]


class TunnelHealthOverviewTotal(BaseModel):
    fair: int
    good: int
    poor: int


class TunnelHealthOverview(BaseModel):
    detail: TunnelHealthOverviewDetail
    total: TunnelHealthOverviewTotal
