from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


# Common Enums
class HealthEnum(str, Enum):
    fair = "fair"
    good = "good"
    na = "n/a"
    poor = "poor"


class ReachabilityEnum(str, Enum):
    reachable = "reachable"
    unreachable = "unreachable"


class StateEnum(str, Enum):
    down = "Down"
    up = "Up"


# Models for tunnelhealth/history
class DeviceHealthEntryItem(BaseModel):
    cpu_load: Optional[float] = None
    data: Dict = Field(default_factory=dict)  # Empty dictionary by default
    entry_time: int
    health: HealthEnum
    health_score: float
    memory_utilization: Optional[float] = None


class TunnelHealthData(BaseModel):
    jitter: float
    latency: float
    loss_percentage: float
    rx_octets: int
    state: StateEnum
    tx_octets: int
    vqoe_score: float


class TunnelHealthHistoryItem(BaseModel):
    health: HealthEnum
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
    health: HealthEnum
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
    state: StateEnum
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
