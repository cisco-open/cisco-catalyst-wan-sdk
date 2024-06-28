# Copyright 2023 Cisco Systems, Inc. and its affiliates

from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.models.system_vsmart_model import SystemVsmart, TlocColorComparison

system_vsmart_complex = SystemVsmart(
    template_name="system_vsmart_complex",
    template_description="Apply System settings for vSmart controller",
    device_models=["vsmart"],
    timezone="UTC",
    host_name=DeviceVariable(name="system_host_name"),
    location="Location",
    dual_stack_ipv6=True,
    description="Example description",
    latitude=37,
    longitude=-122,
    system_tunnel_mtu=1000,
    device_groups=["example1", "example2"],
    system_ip=DeviceVariable(name="system_system_ip"),
    site_id=DeviceVariable(name="system_site_id"),
    overlay_id=44,
    topology=["hub-and-spoke"],
    port_offset=5,
    port_hop=True,
    control_session_pps=999,
    controller_group_id=44,
    track_transport=True,
    track_default_gateway=True,
    iptables_enable=True,
    admin_tech_on_failure=True,
    idle_timeout=100,
    dns_cache_timeout=10,
    region_list_id=12,
    management_region=True,
    compatible=[TlocColorComparison(color_1="mpls", color_2="metro-ethernet")],
    incompatible=[TlocColorComparison(color_1="biz-internet", color_2="public-internet")],
)
