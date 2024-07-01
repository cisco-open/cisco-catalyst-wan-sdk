# Copyright 2023 Cisco Systems, Inc. and its affiliates

#  type: ignore
from catalystwan.api.templates.device_variable import DeviceVariable
from catalystwan.api.templates.models.omp_vsmart_model import OMPvSmart

omp_vsmart_1 = OMPvSmart(
    template_name="omp_vsmart_1",
    template_description="default",
    device_models=["vedge-C8000V"],
)


omp_vsmart_2 = OMPvSmart(
    template_name="omp_vsmart_2",
    template_description="some changes",
    device_models=["vedge-C8000V"],
    graceful_restart=False,
    send_backup_paths=False,
    shutdown=True,
    holdtime=30,
)

omp_vsmart_3 = OMPvSmart(
    template_name="omp_vsmart_3",
    template_description="advanced",
    device_models=["vedge-C8000V"],
    graceful_restart=False,
    graceful_restart_timer=DeviceVariable(name="omp_graceful_restart_timer"),
    send_path_limit=DeviceVariable(name="omp_send_path_limit"),
    discard_rejected=DeviceVariable(name="omp_discard_rejected_custom"),
    send_backup_paths=True,
    shutdown=False,
    advertisement_interval=3,
    holdtime=30,
)

omp_vsmart_complex = OMPvSmart(
    template_name="omp_vsmart_complex",
    template_description="Apply OMP settings for vSmart controller",
    device_models=["vsmart"],
    graceful_restart=True,
    send_path_limit=100,
    send_backup_paths=True,
    discard_rejected=False,
    shutdown=False,
    graceful_restart_timer=120,
    eor_timer=50,
    holdtime=300,
    affinity_group_preference=True,
    advertisement_interval=30,
    tloc_color=True,
)
