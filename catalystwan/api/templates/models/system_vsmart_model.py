# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional, Union

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.models.common import Timezone, TLOCColor

Toology = Literal["hub-and-spoke"]


class TlocColorComparison(FeatureTemplateValidator):
    color_1: Optional[TLOCColor] = Field(
        default=None,
        description="First TLOC color in comparsion",
        json_schema_extra={"vmanage_key": "color-1"},
    )
    color_2: Optional[TLOCColor] = Field(
        default=None,
        description="Second TLOC color in comparsion",
        json_schema_extra={"vmanage_key": "color-2"},
    )
    model_config = ConfigDict(populate_by_name=True)


class SystemVsmart(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Security settings for vSmart controller"

    timezone: Optional[Timezone] = Field(
        default="UTC",
        description="The timezone setting for the vSmart controller",
        json_schema_extra={"data_path": ["clock"]},
    )
    host_name: DeviceVariable = Field(
        default=DeviceVariable(name="system_host_name"),
        json_schema_extra={"vmanage_key": "host-name"},
        description="The hostname for the vSmart controller",
    )
    dual_stack_ipv6: Union[DeviceVariable, BoolStr] = Field(
        default=DeviceVariable(name="system_ipv6-strict-control"),
        json_schema_extra={"vmanage_key": "ipv6-strict-control"},
        description="Enable Dual Stack IPv6 Default",
    )
    description: Optional[str] = Field(default=None, description="Set a text description of the device")
    location: Optional[str] = Field(
        default=None, description="A description of the physical location of the vSmart controller"
    )
    system_tunnel_mtu: Optional[int] = Field(
        default=1024, json_schema_extra={"vmanage_key": "system-tunnel-mtu"}, description="MTU size for system tunnels"
    )
    latitude: Optional[int] = Field(
        default=None,
        ge=-90,
        le=90,
        json_schema_extra={"data_path": ["gps-location"]},
        description="Geographical latitude of the vSmart controller",
    )
    longitude: Optional[int] = Field(
        default=None,
        ge=-180,
        le=180,
        json_schema_extra={"data_path": ["gps-location"]},
        description="Geographical longitude of the vSmart controller",
    )
    device_groups: List[str] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "device-groups"},
        description="Device group names for the vSmart controller",
    )
    system_ip: DeviceVariable = Field(
        default=DeviceVariable(name="system_system_ip"),
        json_schema_extra={"vmanage_key": "system-ip"},
        description="System IP address for the vSmart controller",
    )
    site_id: DeviceVariable = Field(
        default=DeviceVariable(name="system_site_id"),
        json_schema_extra={"vmanage_key": "site-id"},
        description="Site ID for the vSmart controller",
    )
    overlay_id: Optional[int] = Field(
        default=1,
        ge=1,
        le=4294967295,
        json_schema_extra={"vmanage_key": "overlay-id"},
        description="Overlay ID for the vSmart controller",
    )
    topology: Optional[List[Toology]] = Field(
        default=None,
        description="Set the topology",
    )
    port_offset: Optional[int] = Field(
        default=0,
        ge=0,
        le=20,
        json_schema_extra={"vmanage_key": "port-offset"},
        description="Port offset for port hopping",
    )
    port_hop: Optional[bool] = Field(
        default=True, json_schema_extra={"vmanage_key": "port-hop"}, description="Enable or disable port hopping"
    )
    control_session_pps: Optional[int] = Field(
        default=300,
        json_schema_extra={"vmanage_key": "control-session-pps"},
        description="Control session packets per second limit",
    )
    controller_group_id: Optional[int] = Field(
        default=0,
        ge=0,
        le=100,
        json_schema_extra={"vmanage_key": "controller-group-id"},
        description="Group ID for the vSmart controller",
    )
    track_transport: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "track-transport"},
        description="Enable or disable tracking of transport connections",
    )
    track_default_gateway: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "track-default-gateway"},
        description="Enable or disable tracking of the default gateway",
    )
    iptables_enable: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "iptables-enable"},
        description="Enable or disable iptables for security",
    )
    admin_tech_on_failure: Optional[BoolStr] = Field(
        default=True,
        json_schema_extra={"vmanage_key": "admin-tech-on-failure"},
        description="Enable automatic generation of tech-support file on failure",
    )
    idle_timeout: Optional[int] = Field(
        default=None,
        ge=0,
        le=300,
        json_schema_extra={"vmanage_key": "idle-timeout"},
        description="Idle timeout in minutes for user sessions",
    )
    dns_cache_timeout: Optional[int] = Field(
        default=2,
        ge=1,
        le=30,
        json_schema_extra={"vmanage_key": "dns-cache-timeout"},
        description="DNS cache timeout in minutes",
    )
    region_list_id: Optional[int] = Field(
        default=None,
        ge=1,
        le=64,
        json_schema_extra={"vmanage_key": "region-id-list"},
        description="Configure a list of region ID",
    )
    management_region: Optional[BoolStr] = Field(
        default=None,
        json_schema_extra={"vmanage_key": "management-region"},
        description="Management Region",
    )
    compatible: Optional[List[TlocColorComparison]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["tloc-color-compatibility"],
            "priority_order": ["color-1", "color-2"],
        },
        description="Configure compatible TLOC color",
    )
    incompatible: Optional[List[TlocColorComparison]] = Field(
        default=None,
        json_schema_extra={
            "data_path": ["tloc-color-compatibility"],
            "priority_order": ["color-1", "color-2"],
        },
        description="Configure incompatible TLOC color",
    )

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "system-vsmart"
