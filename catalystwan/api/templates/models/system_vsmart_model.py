# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.feature_template import FeatureTemplate
from catalystwan.utils.timezone import Timezone


class SystemVsmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    timezone: Optional[Timezone] = Field(default=None, description="The timezone setting for the vSmart controller")
    idle_timeout: Optional[int] = Field(
        default=None,
        ge=0,
        le=300,
        json_schema_extra={"vmanage_key": "idle-timeout"},
        description="Idle timeout in minutes for user sessions",
    )
    admin_tech_on_failure: Optional[bool] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "admin-tech-on-failure"},
        description="Enable automatic generation of tech-support file on failure",
    )
    iptables_enable: Optional[bool] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "iptables-enable"},
        description="Enable or disable iptables for security",
    )
    track_default_gateway: Optional[bool] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "track-default-gateway"},
        description="Enable or disable tracking of the default gateway",
    )
    dns_cache_timeout: Optional[int] = Field(
        default=2,
        ge=1,
        le=30,
        json_schema_extra={"vmanage_key": "dns-cache-timeout"},
        description="DNS cache timeout in minutes",
    )
    track_transport: Optional[bool] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "track-transport"},
        description="Enable or disable tracking of transport connections",
    )
    controller_group_id: Optional[int] = Field(
        default=0,
        ge=0,
        le=100,
        json_schema_extra={"vmanage_key": "controller-group-id"},
        description="Group ID for the vSmart controller",
    )
    control_session_pps: Optional[int] = Field(
        default=300,
        json_schema_extra={"vmanage_key": "control-session-pps"},
        description="Control session packets per second limit",
    )
    port_hop: Optional[bool] = Field(
        default=True, json_schema_extra={"vmanage_key": "port-hop"}, description="Enable or disable port hopping"
    )
    port_offset: Optional[int] = Field(
        default=0,
        ge=0,
        le=20,
        json_schema_extra={"vmanage_key": "port-offset"},
        description="Port offset for port hopping",
    )
    overlay_id: Optional[int] = Field(
        default=1,
        ge=1,
        le=4294967295,
        json_schema_extra={"vmanage_key": "overlay-id"},
        description="Overlay ID for the vSmart controller",
    )
    site_id: Optional[int] = Field(
        default=1,
        ge=1,
        le=4294967295,
        json_schema_extra={"vmanage_key": "site-id"},
        description="Site ID for the vSmart controller",
    )
    system_ip: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "system-ip"},
        description="System IP address for the vSmart controller",
    )
    device_groups: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "device-groups"},
        description="Device group names for the vSmart controller",
    )
    longitude: Optional[int] = Field(
        default=None, ge=-180, le=180, description="Geographical longitude of the vSmart controller"
    )
    latitude: Optional[int] = Field(
        default=None, ge=-90, le=90, description="Geographical latitude of the vSmart controller"
    )
    system_tunnel_mtu: Optional[str] = Field(
        default=1024, json_schema_extra={"vmanage_key": "system-tunnel-mtu"}, description="MTU size for system tunnels"
    )
    location: Optional[str] = Field(
        default=None, description="A description of the physical location of the vSmart controller"
    )
    host_name: Optional[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "host-name"},
        description="The hostname for the vSmart controller",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "system-vsmart"
