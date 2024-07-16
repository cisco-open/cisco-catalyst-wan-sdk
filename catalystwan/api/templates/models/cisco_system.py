# Copyright 2023 Cisco Systems, Inc. and its affiliates

from pathlib import Path
from typing import ClassVar, List, Literal, Optional

from pydantic import ConfigDict, Field

from catalystwan.api.templates.bool_str import BoolStr
from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.feature_template import FeatureTemplate, FeatureTemplateValidator
from catalystwan.models.common import Protocol, Timezone

SiteType = Literal["type-1", "type-2", "type-3", "cloud", "branch", "br", "spoke"]
ConsoleBaudRate = Literal["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
Boolean = Literal["or", "and"]
Type = Literal["interface", "static-route"]
Role = Literal["edge-router", "border-router"]
EnableMrfMigration = Literal["enabled", "enabled-from-bgp-core"]
Epfr = Literal["disabled", "aggressive", "moderate", "conservative"]


class MobileNumber(FeatureTemplateValidator):
    number: str = Field(description="The mobile phone number used for notification or security purposes.")


class Tracker(FeatureTemplateValidator):
    name: str = Field(description="Name for the Tracker")
    endpoint_ip: Optional[str] = Field(
        default=None,
        description="The IP address of the endpoint to track.",
        json_schema_extra={"vmanage_key": "endpoint-ip"},
    )
    endpoint_ip_transport_port: Optional[str] = Field(
        default=None,
        description="The transport port of the endpoint IP address.",
        json_schema_extra={"vmanage_key": "endpoint-ip", "data_path": ["endpoint-ip-transport-port"]},
    )
    protocol: Optional[Protocol] = Field(
        default=None,
        description="The protocol used for the tracker (TCP or UDP).",
        json_schema_extra={"data_path": ["endpoint-ip-transport-port"]},
    )
    port: Optional[int] = Field(
        default=None,
        description="The port number used for the tracker.",
        json_schema_extra={"data_path": ["endpoint-ip-transport-port"]},
    )
    endpoint_dns_name: Optional[str] = Field(
        default=None,
        description="The DNS name of the endpoint to track.",
        json_schema_extra={"vmanage_key": "endpoint-dns-name"},
    )
    endpoint_api_url: Optional[str] = Field(
        default=None,
        description="The API URL of the endpoint to track.",
        json_schema_extra={"vmanage_key": "endpoint-api-url"},
    )
    elements: Optional[List[str]] = Field(default=None, description="A list of elements to track.")
    boolean: Optional[Boolean] = Field(
        default="or", description="The boolean condition to use when evaluating multiple elements."
    )
    threshold: Optional[int] = Field(default=300, description="The threshold for triggering the tracker.")
    interval: Optional[int] = Field(default=60, description="The interval at which the tracker checks the elements.")
    multiplier: Optional[int] = Field(default=3, description="The multiplier used for determining the loss threshold.")
    type: Optional[Type] = Field(default="interface", description="The type of tracker (interface or static route).")

    model_config = ConfigDict(populate_by_name=True)


class Object(FeatureTemplateValidator):
    number: int = Field(description="The unique identifier for the object.")


class ObjectTrack(FeatureTemplateValidator):
    object_number: int = Field(
        description="The tracking object number.", json_schema_extra={"vmanage_key": "object-number"}
    )
    interface: str = Field(description="The name of the interface to track.")
    sig: str = Field(description="The signature associated with the tracking object.")
    ip: str = Field(description="The IP address used for tracking.")
    mask: Optional[str] = Field(
        default="0.0.0.0", description="The subnet mask associated with the IP address for tracking."
    )
    vpn: int = Field(description="The VPN instance associated with the tracking object.")
    object: List[Object] = Field(description="A list of objects related to the tracking.")
    boolean: Boolean = Field(description="The boolean condition to use when evaluating multiple objects.")
    model_config = ConfigDict(populate_by_name=True)


class AffinityPerVrf(FeatureTemplateValidator):
    affinity_group_number: Optional[int] = Field(
        default=None,
        description="The affinity group number for VRF binding.",
        json_schema_extra={"vmanage_key": "affinity-group-number"},
    )
    vrf_range: Optional[str] = Field(
        default=None,
        description="The range of VRFs associated with the affinity group.",
        json_schema_extra={"vmanage_key": "vrf-range"},
    )
    model_config = ConfigDict(populate_by_name=True)


class Vrf(FeatureTemplateValidator):
    vrf_id: int = Field(
        description="The VRF (VPN Routing and Forwarding) instance ID.", json_schema_extra={"vmanage_key": "vrf-id"}
    )
    gateway_preference: Optional[List[int]] = Field(
        default=None,
        description="List of affinity group preferences for VRF",
        json_schema_extra={"vmanage_key": "gateway-preference"},
    )
    model_config = ConfigDict(populate_by_name=True)


class CiscoSystemModel(FeatureTemplate):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    _docs_description: str = "Cisco System configuration settings for SD-WAN devices."

    timezone: Optional[Timezone] = Field(
        default=None, description="The timezone setting for the system.", json_schema_extra={"data_path": ["clock"]}
    )
    description: Optional[str] = Field(default=None, description="Set a text description of the device")
    hostname: DeviceVariable = Field(
        default=DeviceVariable(name="system_host_name"),
        validate_default=True,
        description="The hostname for the device.",
        json_schema_extra={"vmanage_key": "host-name"},
    )
    location: Optional[str] = Field(default=None, description="The physical location of the device.")
    latitude: Optional[float] = Field(
        default=None,
        description="The latitude coordinate for the device's location.",
        json_schema_extra={"data_path": ["gps-location"]},
    )
    longitude: Optional[float] = Field(
        default=None,
        description="The longitude coordinate for the device's location.",
        json_schema_extra={"data_path": ["gps-location"]},
    )
    range: Optional[int] = Field(
        default=100,
        description="The range for geo-fencing feature.",
        json_schema_extra={"data_path": ["gps-location", "geo-fencing"]},
    )
    enable_fencing: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable geo-fencing.",
        json_schema_extra={"data_path": ["gps-location", "geo-fencing"], "vmanage_key": "enable"},
    )
    mobile_number: Optional[List[MobileNumber]] = Field(
        default=None,
        description="List of mobile numbers for SMS notifications.",
        json_schema_extra={"vmanage_key": "mobile-number", "data_path": ["gps-location", "geo-fencing", "sms"]},
    )
    enable_sms: Optional[BoolStr] = Field(
        default=False,
        description="Enable or disable SMS notifications.",
        json_schema_extra={"data_path": ["gps-location", "geo-fencing", "sms"], "vmanage_key": "enable"},
    )
    device_groups: Optional[List[str]] = Field(
        default=None,
        description="List of device groups the device belongs to.",
        json_schema_extra={"vmanage_key": "device-groups"},
    )
    controller_group_list: Optional[List[int]] = Field(
        default=None,
        description="List of controller groups the device is associated with.",
        json_schema_extra={"vmanage_key": "controller-group-list"},
    )
    system_ip: DeviceVariable = Field(
        default=DeviceVariable(name="system_system_ip"),
        description="The system IP address of the device.",
        json_schema_extra={"vmanage_key": "system-ip"},
    )
    overlay_id: Optional[int] = Field(
        default=None, description="The overlay ID of the device.", json_schema_extra={"vmanage_key": "overlay-id"}
    )
    site_id: int = Field(
        default=DeviceVariable(name="system_site_id"),
        description="The site ID of the device.",
        json_schema_extra={"vmanage_key": "site-id"},
    )
    site_type: Optional[List[SiteType]] = Field(
        default=None,
        description="The site type classification for the device.",
        json_schema_extra={"vmanage_key": "site-type"},
    )
    port_offset: Optional[int] = Field(
        default=None, description="The port offset for the device.", json_schema_extra={"vmanage_key": "port-offset"}
    )
    port_hop: Optional[BoolStr] = Field(
        default=None, description="Enable or disable port hopping.", json_schema_extra={"vmanage_key": "port-hop"}
    )
    control_session_pps: Optional[int] = Field(
        default=None,
        description="Control session packets per second setting.",
        json_schema_extra={"vmanage_key": "control-session-pps"},
    )
    track_transport: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable transport tracking.",
        json_schema_extra={"vmanage_key": "track-transport"},
    )
    track_interface_tag: Optional[int] = Field(
        default=None,
        description="The tag of the interface to be tracked.",
        json_schema_extra={"vmanage_key": "track-interface-tag"},
    )

    console_baud_rate: Optional[ConsoleBaudRate] = Field(
        default=None,
        description="The console baud rate setting for the device.",
        json_schema_extra={"vmanage_key": "console-baud-rate"},
    )
    max_omp_sessions: Optional[int] = Field(
        default=None,
        description="The maximum number of OMP (Overlay Management Protocol) sessions.",
        json_schema_extra={"vmanage_key": "max-omp-sessions"},
    )
    multi_tenant: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable multi-tenant support.",
        json_schema_extra={"vmanage_key": "multi-tenant"},
    )
    track_default_gateway: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable default gateway tracking.",
        json_schema_extra={"vmanage_key": "track-default-gateway"},
    )
    admin_tech_on_failure: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable automatic generation of admin technical details on failure.",
        json_schema_extra={"vmanage_key": "admin-tech-on-failure"},
    )
    enable_tunnel: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable tunnel functionality.",
        json_schema_extra={"vmanage_key": "enable", "data_path": ["on-demand"]},
    )
    idle_timeout: Optional[int] = Field(
        default=None,
        description="The idle timeout setting for tunnels.",
        json_schema_extra={"vmanage_key": "idle-timeout"},
    )
    on_demand_idle_timeout_min: Optional[int] = Field(
        default=None,
        description="The minimum idle timeout for on-demand tunnels.",
        json_schema_extra={"vmanage_key": "idle-timeout", "data_path": ["on-demand"]},
    )
    tracker: Optional[List[Tracker]] = Field(default=None, description="List of tracker configurations.")
    object_track: Optional[List[ObjectTrack]] = Field(
        default=None,
        description="List of object tracking configurations.",
        json_schema_extra={"vmanage_key": "object-track"},
    )
    region_id: Optional[int] = Field(
        default=None, description="The region ID of the device.", json_schema_extra={"vmanage_key": "region-id"}
    )
    secondary_region: Optional[int] = Field(
        default=None,
        description="The secondary region ID of the device.",
        json_schema_extra={"vmanage_key": "secondary-region"},
    )
    role: Optional[Role] = Field(
        default=None,
        description="The role of the device in the network.",
    )
    affinity_group_number: Optional[int] = Field(
        default=None,
        description="The affinity group number for VRF binding.",
        json_schema_extra={"vmanage_key": "affinity-group-number", "data_path": ["affinity-group"]},
    )
    preference: Optional[List[int]] = Field(
        default=None,
        description="List of affinity group preferences.",
        json_schema_extra={"data_path": ["affinity-group"]},
    )
    preference_auto: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable automatic preference setting for affinity groups.",
        json_schema_extra={"vmanage_key": "preference-auto", "data_path": ["affinity-group"]},
    )
    affinity_per_vrf: Optional[List[AffinityPerVrf]] = Field(
        default=None,
        description="List of affinity configurations per VRF.",
        json_schema_extra={"vmanage_key": "affinity-per-vrf", "data_path": ["affinity-group"]},
    )
    transport_gateway: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable the transport gateway feature.",
        json_schema_extra={"vmanage_key": "transport-gateway"},
    )
    enable_mrf_migration: Optional[EnableMrfMigration] = Field(
        default=None,
        description="Enable Multicast Routing Framework (MRF) migration settings.",
        json_schema_extra={"vmanage_key": "enable-mrf-migration"},
    )
    migration_bgp_community: Optional[int] = Field(
        default=None,
        description="BGP community value for MRF migration.",
        json_schema_extra={"vmanage_key": "migration-bgp-community"},
    )
    enable_management_region: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable management region configuration.",
        json_schema_extra={"vmanage_key": "enable-management-region"},
    )
    vrf: Optional[List[Vrf]] = Field(default=None, description="List of VRF configurations.")
    management_gateway: Optional[BoolStr] = Field(
        default=None,
        description="Enable or disable the management gateway feature.",
        json_schema_extra={"vmanage_key": "management-gateway"},
    )
    epfr: Optional[Epfr] = Field(default=None, description="Edge Policy-based Framework Routing (EPFR) setting.")

    payload_path: ClassVar[Path] = Path(__file__).parent / "DEPRECATED"
    type: ClassVar[str] = "cisco_system"
